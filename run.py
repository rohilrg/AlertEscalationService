from src.pager_service import PagerService
import pprint
import sys
import asyncio
import threading

print(
    "Hello Aircall Engineer, let's simulate a real life work scenario for incident alerts and on-call shifts."
)

number_of_services = input(
    "To simulate, please tell us the number of services(int)(max 6): "
)
pager_service = PagerService(number_of_services=int(number_of_services))
pager_service._create_n_services_json()
ep_policy = pager_service._read_ep_or_create_ep()
print(f"The escalation policy for {number_of_services} services is:\n")
pprint.pprint(ep_policy)

edit_input = input("Do you want to edit the policy?(0 or 1): ")

if edit_input == "1":
    print("Please edit the escalation policy in folder 'src/storage/ep.json'")
    print(
        "Restart the program after editing, make sure to update number_of_services.json file also. Killing!!"
    )
    sys.exit()


class SharedData:
    stop_thread = False
    input_queue = asyncio.Queue()


def read_input(loop):
    while not SharedData.stop_thread:
        user_input = input(
            "Report HEALTHY/UNHEALTHY state for specific service, please make sure to follow the format "
            "(For example: Service 1/UNHEALTHY or Service 1/HEALTHY): "
        )
        asyncio.run_coroutine_threadsafe(SharedData.input_queue.put(user_input), loop)


async def handle_input():
    while True:
        user_input = await SharedData.input_queue.get()
        try:
            service_name, state = user_input.split("/")
            await pager_service.run(
                service_name=service_name.strip(), state=state.strip()
            )
        except ValueError:
            print("Invalid input format. Please follow 'Service Name/STATE' format.")
        except Exception as e:
            print(f"Error processing input: {e}")


async def main():
    loop = asyncio.get_running_loop()
    threading.Thread(target=read_input, args=(loop,), daemon=True).start()
    await handle_input()


asyncio.run(main())
