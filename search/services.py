import re

def normalize_token(token_string):

    normalize_token = token_string.lower()

    normalize_token = re.sub(r'[^\w\s]', '', normalize_token)

    return normalize_token

