import random
import re
import logging
import os


def setup_logger(name, log_folder, log_file, level=logging.INFO):
    """Function to setup a logger with the specified name, log folder, and log file."""
    # Ensure the folder exists
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Full path for the log file
    log_path = os.path.join(log_folder, log_file)

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # Create a file handler for writing logs to a file (in append mode)
    handler = logging.FileHandler(log_path, mode="a")  # 'a' is for append
    handler.setLevel(level)

    # Create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger


class PhoneNumber:
    def __init__(self, number):
        if not self.is_valid(number):
            raise ValueError("Invalid French phone number")
        self.number = number

    def is_valid(self, number):
        # Regex for validating a French phone number
        regex = r"^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$"
        return re.match(regex, number) is not None

    def __str__(self):
        return self.number


def generate_french_phone_number():
    # Generates a random French phone number
    # French numbers are in the format "0X XX XX XX XX", where X is a digit from 0-9
    # For simplicity, we'll exclude the international format here
    number = "0" + str(random.randint(1, 9))  # First digit after 0 should be 1-9
    for _ in range(4):
        part = str(random.randint(0, 99)).zfill(2)  # Two-digit sections of the number
        number += " " + part
    return number


def generate_and_validate_french_numbers(n):
    valid_numbers = []
    for _ in range(n):
        try:
            number = generate_french_phone_number()
            valid_number = PhoneNumber(number)
            valid_numbers.append(str(valid_number))
        except ValueError:
            pass  # If the number is invalid, we simply skip it
    return valid_numbers


# Lists of first names and last names for username generation
first_names = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Ethan",
    "Fiona",
    "George",
    "Hannah",
    "Ivan",
    "Julia",
    "Kevin",
    "Luna",
    "Mike",
    "Nora",
    "Oscar",
    "Penny",
    "Quinn",
    "Ryan",
    "Sara",
    "Tom",
]

last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
]


def generate_usernames(num_usernames):
    usernames = []
    for _ in range(num_usernames):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        number = random.randint(10, 99)
        username = f"{first_name}{last_name}{number}"
        usernames.append(username.lower())
    return usernames


def generate_random_email(usernames):
    domain = random.choice(["gmail", "yahoo", "example", "mail"])
    extension = random.choice(["com", "net", "org", "io"])
    username = random.choice(usernames)
    email_address = f"{username}@{domain}.{extension}"
    return email_address


def generate_emails(n):
    emails = []
    # Generate a list of 20 usernames
    usernames_list = generate_usernames(200)
    for i in range(n):
        emails.append(generate_random_email(usernames_list))
    return emails
