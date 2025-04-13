import re

def sanitize(name):
    """
    Convert a string into a valid Python variable name:
    - Lowercase
    - Replace spaces and dashes with underscores
    - Remove invalid characters
    - Add prefix if name starts with a digit
    """
    name = name.lower().strip()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub(r"\W", "", name)  # Remove all non-alphanumeric/underscore characters
    if re.match(r"^\d", name):
        name = f"df_{name}"  # Prefix if starts with a number
    return name

def strip_code_block(content):
    return content.strip().strip("`").replace("python", "").strip()