import re

imei_prefixes = {
    "Model01": "001001",
    "Model02": "001002",
    "Model06": "001010",
    "Model03_OLD": "001003",
    "Model03_NEW": "001303",
    "Model04_OLD": "001004",
    "Model04_NEW": "001204",
    "Model05_OLD": "006002",
    "Model05_NEW": "006003",
    "Model07": "004010"
}

device_ids = {
    "Model01": "A8",
    "Model02": "58",
    "Model03": "DB",
    "Model04": "43",
    "Model05": "EA",
    "Model06": "EB",
    "Model07": "A2"
}

# TO DO
# compile list of major/minor versions of protocols
# e.g. "A8021A" => "Model 01: 2.10"
# version numbers are two hex digits (02 and 1A in example)


def imei_gen(text_block):
    """uses regex to spit out any imeis from a text block
    this is a generator, meant to be used with file handlers
    """
    pattern = r"[0-9]{15}"
    results = re.findall(pattern, text_block)
    if not results:
        return None
    for match in results:
        yield(match)

def validate_mfg_imei(imei):
    """Returns True if imei (as str) is in a format that manufacturer uses
    otherwise returns False
    """
    # to do: add some logic to verify after more info from mfg
    if len(imei) == 15 and imei.isdecimal():
        return True
    else:
        return False

def parse_id_from_code(code):
    """Takes device id (6 char hex) and returns a 3 tuple,
    of device name, major version, and minor version
    """
    
    device_type_code = code[0:2]
    major_version_num = int(code[2:4], 16)
    minor_version_num = int(code[4:6], 16)
    device_name = "Unknown"
    for k, v in device_ids.items():
        if device_type_code == v:
            device_name = k
    return (device_name, major_version_num, minor_version_num)

def parse_imei(imei):
    """Parses IMEI to find device name.
    WARNING: NOT guaranteed to work!! IMEIs do not always equate to a device
    and multiple device types may be returned.
    Returns a list of potential device types.
    Use raw data and one of the parse_id functions if possible.
    """
    
    possible_devices = []
    
    imei = imei.strip()
    
    if not validate_mfg_imei(imei):
        possible_devices.append("Unknown")
        return possible_devices

    for k, v in imei_prefixes.items():
        if imei.startswith(v):
            possible_devices.append(k)
    if not possible_devices:
        possible_devices.append("Unknown")
    return possible_devices

def parse_id_from_msg(msg):
    """Takes device +RESP msg of any type and returns a 3 tuple,
    of device name, major version, and minor version
    """
    
    try:
        parts = msg.split(",")
        code = parts[1]
    except IndexError:
        print("No code found in the expected location!")
        return ("Unknown", "Unknown", "Unknown")
    if len(code) != 6:
        print("Another error")
    return parse_id_from_code(code)