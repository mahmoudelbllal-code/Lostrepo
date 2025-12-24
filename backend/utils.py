import re

def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[إأآا]", "ا", name)
    name = re.sub(r"[يى]", "ي", name)
    name = re.sub(r"[^ء-يa-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name
