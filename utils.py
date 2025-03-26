import re


def upper_to_snake(upper_str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', upper_str)

    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
