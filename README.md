# API Client example

### Purpose

This was used as a client to automate fixing devices when in the field.

Devices could be accessed via IMEI (a 15 digit number hardcoded to the device) or by a phone number (which was hardcoded to the SIM).

Commands were referenced from manuals, and parameters were carefully crafted on a per-use basis. These were built into a command for use in bulk-updates. This library is what enabled both automated and manual updates of devices in this way. The default command was the most used and enabled the device to report to a centralized server from the manufacturer.

This client and the other files were organized to be used by me for daily/weekly ongoing tasks, as well as for custom automation deployment (AWS Lambda or VPS) on an as-needed basis.

### __init__.py, .env, Pipfile

Boilerplate for reusability.

### session.py, client.py, exceptions.py

These are the main classes for the API client itself. Written to load credentials from .env (see example). There are default values for the message to be sent (which had the device report to us) and there is a method for proper authentication.

Re-auth after an expired session needs some work.

### refurb_check.py
Refurbishment was a manual process that required coordination between three departments:

1. Refurb dept would gather returned units, scan the devices, and report them to an engineering liaison. We expected an IMEI (15 digit number) followed by an ICCID (19 digit number) on each line.
1. Engineering would use this tool to query the device info api and delineate devices into categories, with their IMEI and ICCIDs being collated for each department's follow up tasks.
  1. Devices that gave us a specific error code were successfully shut off and coud be refurbished.
  1. Devices that had any other REST code were generally in use in some way, so they had to go to Customer Service and the customer had to be contacted before further action could be taken.
  1. Devices that failed the request usually had some other aspect that needed looking into. These devices also could not be refurbished right away and required some further lookup using different systems.
1. The output gave us three lists:
  1. "Successful": The IMEIs went back to Refurbishment and they went on to physically refurbish the device and move on to testing.
  1. "Taken": These devices' IMEIs went to CS for followup, and if no contact was made, the ICCIDs were suspended automatically using a different API endpoint.
  1. "Failed": These IMEIs and ICCIDs were tested manually by the engineering liaison on a different system.
  1. The results of "Taken" and "Failed" followups generally led to the devices being refurbished in a later batch or discarded/destroyed.

This is far and away the oldest script/tool/workflow in this module, and was scheduled for refactoring to both utilize newer, more efficient code (API client, tools.py functions) and to reflect a newer, more streamlined refurbishment and testing process.

### parse_timestamps.py

Pendulum was a key library to use while parsing the logs that came out of AWS Cloudwatch. The goal was to clearly see the differences between the device's GPS lock time, the message send time, and the receipt time on AWS's end. This was super helpful in identifying issues related to reception and also issues receiving them over the cellular network itself.

The conversion functions weren't needed, but were planned for future business-to-business deployments that were upcoming.

### format_imeis.py

This is a command-line tool utilizing the Click library meant to ease batch device processing.

Departments would collate lists of devices that were problematic for whatever reason. As you can imagine, they can come in a wide variety of formats. This program parsed lines and provided output specially formatted for specific tools (python scripts, postman JSON payloads, etc) for further processing.

This is a stupid little program that saved tens of minutes per day formatting lists and was used by both Technical Support agents and Engineering for troubleshooting and updating devices in bulk. Moreover, it made life a _lot_ less tedious for a lot of people.

### tools.py

tools.py contains some often used code for scripts that utilized this client and were automated by an external system. It was also used in parsing slack commands (in progress, but never completed) and generally provided some basic necessary functionality:

1. A generator to return IMEIs one line at a time.
1. A function to pull a device code string from a device message.
1. A function to lookup device model name and another to return major/minor firmware versions.
1. A function to lookup device model based on known IMEI patterns as shared by the manufacturer.