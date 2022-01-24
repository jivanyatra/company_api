# API Client example

### Purpose

This was used as a client to automate fixing devices when in the field.

Devices could be accessed via IMEI (a 15 digit number hardcoded to the device) or by a phone number (which was hardcoded to the SIM).

Commands were referenced from manuals, and parameters were carefully crafted on a per-use basis. These were built into a command for use in bulk-updates. This library is what enabled both automated and manual updates of devices in this way. The default command was the most used and enabled the device to report to a centralized server from the manufacturer.

This client and the other files were organized to be used by me for daily/weekly ongoing tasks, as well as for custom automation deployment (AWS Lambda or VPS) on an as-needed basis.

### __init__.py, .env, Pipfile

Boilerplate for reusability.

### session.py, client.py, exceptions.py

These are the main classes for the API client itself. Written to load credentials from .env (see example).

### refurb_check.py
Refurbishment

### parse_timestamps.py

Pendulum was a key library to use while parsing the logs that came out of AWS Cloudwatch. The goal was to clearly see the differences between the device's GPS lock time, the message send time, and the receipt time on AWS's end. This was super helpful in identifying issues related to reception and also issues receiving them over the cellular network itself.

The conversion functions weren't needed, but were planned for future business-to-business deployments that were upcoming.

### format_imeis.py

This is a command-line tool to input a list of IMEIs from a different department who had the physical inventory

### tools.py

tools.py contains some often used code for scripts that utilized this client and were automated by an external system. It was also used in parsing slack commands (in progress, not completed).