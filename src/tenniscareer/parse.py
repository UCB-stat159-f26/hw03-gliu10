"""Read values out of tennisabstract.com JavaScript files."""

import json
import re


def extract_js_array(js_text, var_name="morematchmx"):
    """Return the list assigned to `var <var_name> = [...]` in a JS file.

    The match arrays are plain lists of strings, so once we find where
    the array starts, Python's JSON decoder can read it directly.
    """
    found = re.search(r"var\s+" + re.escape(var_name) + r"\s*=\s*", js_text)
    if found is None:
        raise ValueError(f"Could not find 'var {var_name}' in the JS file")
    array, _ = json.JSONDecoder().raw_decode(js_text, found.end())
    return array


def extract_birth_date(js_text):
    """Return the player's date of birth (yyyymmdd string) from `var dob=...`."""
    found = re.search(r"var\s+dob\s*=\s*['\"]?(\d{8})", js_text)
    return found.group(1) if found else None


def extract_full_name(js_text):
    """Return the player's display name from `var fullname = '...'`."""
    found = re.search(r"var\s+fullname\s*=\s*['\"]([^'\"]+)['\"]", js_text)
    return found.group(1) if found else None