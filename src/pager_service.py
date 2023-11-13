import os
import json
import sys
import random
import time
import asyncio
import threading
from src.utils import (
    generate_emails,
    generate_and_validate_french_numbers,
    setup_logger,
)


class PagerService:
    def __init__(self, number_of_services: int):
        """
        Initialize the PagerService with a specific number of services.

        Args:
            number_of_services (int): Number of services to be monitored.
        """
        self.number_of_services = number_of_services  # Total number of services
        self.number_of_services_dict = (
            {}
        )  # Dictionary to track the status of each service
        self.ep_path = "src/storage/ep.json"  # Path to the escalation policy JSON file
        self.log_folder = "src/logs/"  # Directory to store log files
        self.ep_json = {}  # Dictionary to store escalation policies
        self.alert_received = []  # List to track services that have received alerts
        self.alert_acknowledgment = {}  # Dictionary to track alert acknowledgments
        self.current_escalation_level = (
            {}
        )  # Track current escalation level for each service
        self.make_healthy_the_services_later = []  # Services to be marked healthy later

    def _create_n_services_json(self):
        """
        Create a JSON file with the initial status of each service as 'HEALTHY'.
        """
        for i in range(self.number_of_services):
            # Set each service's status as 'HEALTHY'
            self.number_of_services_dict[f"Service {i + 1}"] = "HEALTHY"
        # Write this information to a JSON file
        json.dump(
            self.number_of_services_dict,
            open("src/storage/number_of_services.json", "w"),
        )

    def _read_ep_or_create_ep(self):
        """
        Read the escalation policy from a file or create a new one if it doesn't exist.

        Returns:
            dict: Escalation policy for each service.
        """
        if os.path.exists(self.ep_path):
            # Read the existing escalation policy
            ep_json = json.load(open(self.ep_path, "r"))
            if len(ep_json) == self.number_of_services:
                self.ep_json = ep_json
            else:
                print(
                    f"Stored escalation policy had {len(ep_json)} services. Killing!!"
                )
                sys.exit()
        else:
            # Create an escalation policy for each service
            max_number_of_levels = 7
            for i in range(self.number_of_services):
                self.ep_json[f"Service {i + 1}"] = {}
                number_levels = random.randint(1, max_number_of_levels - 1)
                emails = generate_emails(number_levels)
                phone_numbers = generate_and_validate_french_numbers(number_levels)
                emails_and_numbers = emails + phone_numbers
                emails_and_numbers_n_levels = random.sample(
                    emails_and_numbers, number_levels
                )

                # Populate the escalation policy dictionary
                for j in range(number_levels):
                    self.ep_json[f"Service {i + 1}"][
                        str(j + 1)
                    ] = emails_and_numbers_n_levels[j]

            # Store the escalation policy
            json.dump(self.ep_json, open(self.ep_path, "w"))
        return self.ep_json

    def _send_alerts(self, service_name):
        """
        Send alerts for a specific service and escalate if not acknowledged.

        Args:
            service_name (str): The name of the service to send alerts for.
        """
        escalate = True
        while escalate:
            current_level = self.current_escalation_level.get(service_name, str(1))
            contact_info = self.ep_json[service_name][current_level]
            info_logger = setup_logger(
                service_name, self.log_folder, f"info_{service_name}.log"
            )
            info_logger.info(
                f"Escalating alert for {service_name} to level {current_level}: {contact_info}"
            )
            # Wait for 15 minutes for acknowledgment
            time.sleep(15)  # 900 seconds = 15 minutes
            # Check for acknowledgment after 15 minutes
            if service_name not in self.alert_acknowledgment:
                info_logger.info(
                    f"No acknowledgment received for {service_name} within 15 minutes"
                )
                escalate = self._escalate_alert(service_name)

            else:
                escalate = False

    def _escalate_alert(self, service_name):
        """
        Escalate the alert for a service to the next level.

        Args:
            service_name (str): The name of the service for which to escalate the alert.
        """
        current_level = self.current_escalation_level.get(service_name, str(1))
        next_level = int(current_level) + 1
        # Escalate alert to the next level if possible
        if str(next_level) in self.ep_json[service_name]:
            self.current_escalation_level[service_name] = str(next_level)
            return True
        else:
            # No further escalation level available
            info_logger = setup_logger(
                service_name, self.log_folder, f"info_{service_name}.log"
            )
            info_logger.info(f"No further escalation levels for {service_name}")
            return False

    def _acknowledgment_listener(self, service_name):
        """
        Continuously listen for and process alert acknowledgments.

        Args:
            service_name (str): The name of the service to listen for acknowledgments.
        """
        while True:
            # Randomly wait for a time less than 30 mins
            time.sleep(random.randint(10, 90))  # Random time up to 30 mins

            # Process acknowledgment for a randomly selected service
            if self.alert_received:
                acknowledged_service = random.choice(self.alert_received)
                self.alert_acknowledgment[acknowledged_service] = True
                self.alert_received.remove(acknowledged_service)
                info_logger = setup_logger(
                    acknowledged_service, self.log_folder, f"info_{service_name}.log"
                )
                info_logger.info(f"Acknowledgment received for {acknowledged_service}")
                break

    async def run(self, service_name: str, state: str):
        """
        Run the alert simulation for a given service based on its state.

        Args:
            service_name (str): The name of the service.
            state (str): The current state of the service ('UNHEALTHY' or 'HEALTHY').
        """
        if state == "UNHEALTHY":
            # Process UNHEALTHY state
            if (
                service_name not in self.alert_received
                and service_name not in self.make_healthy_the_services_later
            ):
                self.number_of_services_dict[service_name] = state
                self.alert_received.append(service_name)
                self.make_healthy_the_services_later.append(service_name)
                self.current_escalation_level[service_name] = str(
                    1
                )  # Reset escalation level
                info_logger = setup_logger(
                    service_name, self.log_folder, f"info_{service_name}.log"
                )
                info_logger.info(f"UNHEALTHY state detected for {service_name}")

                # Start threads for sending alerts and listening for acknowledgments
                threading.Thread(
                    target=self._acknowledgment_listener, args=(service_name,)
                ).start()
                threading.Thread(target=self._send_alerts, args=(service_name,)).start()
            else:
                # Log if UNHEALTHY state is already processed
                info_logger = setup_logger(
                    service_name, self.log_folder, f"info_{service_name}.log"
                )
                info_logger.info(
                    f"Already received UNHEALTHY state before for {service_name}!! Doing nothing."
                )
        else:
            # Process HEALTHY state
            if service_name in self.make_healthy_the_services_later:
                info_logger = setup_logger(
                    service_name, self.log_folder, f"info_{service_name}.log"
                )
                info_logger.info(
                    f"Received HEALTHY state for {service_name}, waiting for acknowledgment timer to timeout."
                )
                time.sleep(15)
                info_logger.info(
                    f"Received HEALTHY state for {service_name}, stopping alert state for the service."
                )
                info_logger.info(
                    "-------------------------------------------------------------------"
                )
                self.number_of_services_dict[service_name] = "HEALTHY"
                self.make_healthy_the_services_later.remove(service_name)
                if service_name in self.alert_acknowledgment:
                    del self.alert_acknowledgment[service_name]
