# API Client example

### Purpose

This was used as a client to automate fixing devices when in the field.

Devices could be accessed via IMEI (a 15 digit number hardcoded to the device) or by a phone number (which was hardcoded to the SIM).

Commands were referenced from manuals, and parameters were carefully crafted on a per-use basis. These were built into a command for use in bulk-updates. This library is what enabled both automated and manual updates of devices in this way. The default command was the most used and enabled the device to report to a centralized server from the manufacturer.

### Misc

tools.py contains some often used code for scripts that utilized this client and were automated by an external system. It was also used in parsing slack commands (in progress, not completed).