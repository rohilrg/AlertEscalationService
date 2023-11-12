# AlertEscalationService

## Overview
This project is designed to simulate real-life work scenarios for incident alerts and on-call shifts.
The challenge is described here: https://github.com/aircall/technical-test-pager

## Project Structure
````bash
./AlertEscalationService/
├── src
│   ├── logs
│   │   ├── info_Service 1.log
│   │   ├── info_Service 2.log
│   │   └── info_Service 3.log
│   ├── storage
│   │   ├── ep.json
│   │   └── number_of_services.json
│   ├── tests
│   │   └── test_pager_service.py
│   ├── __init__.py
│   ├── pager_service.py
│   └── utils.py
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── run.py
└── tmp.txt

4 directories, 15 files
````
## Description of Files

### run.py
- **Purpose**: Main entry file for the application.
- **Functionality**: Initiates the simulation of incident alerts and on-call shifts. Interacts with the user to set up the simulation parameters.

### pager_service.py
- **Purpose**: Defines the `PagerService` class.
- **Functionality**: Manages the number of services, their states, and handles escalation policies. Also includes functionality for alert acknowledgment and log management.

### utils.py
- **Purpose**: Provides utility functions.
- **Functionality**: Includes functions for setting up loggers, generating emails, and validating French phone numbers.

## Pre-installation steps:
- Make sure you have python 3+ installed on your computer.
- Make sure you have pip3 package installed on your computer.
- Make sure you clone this package to your computer.

## Install requirements: 
In your terminal/command-line go to the project folder and execute the command below:
```bash
pip install -r requirements.txt
```
## Checking before building
Please run these make commands to make sure the formatting, linting are working.
````commandline
make format
make lint
````

## Running 
To run the app just run the following command in bash in the root directory of the folder:
````bash
python run.py
````

## Dependencies

- Tested on Python (Version 3.10.12 recommended) 
- No external libraries are required as per the current code files.

## Notes

- The simulation handles a maximum of 6 services, but can be configured.
- Logging and alert management are integral components of the simulation.
- The codebase is likely intended for educational or demonstration purposes.

Refer to the comments in the respective files for detailed documentation on each class and function.
