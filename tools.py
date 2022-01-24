import re

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


