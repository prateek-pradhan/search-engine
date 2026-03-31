import re

def normalize_token(token_string):

    normalize_token = token_string.lower()

    normalize_token = re.sub(r'[^\w\s]', '', normalize_token)

    return normalize_token


def clean_content(raw_content):
    
    while re.search(r'\{\{[^{}]*\}\}', raw_content):
        raw_content = re.sub(r'\{\{[^{}]*\}\}', '', raw_content)

    raw_content = re.sub(r'\[\[(?:[^\[\]|]*\|)?([^\[\]]*)\]\]', r'\1', raw_content)

    raw_content = re.sub(r'<ref[^>]*>.*?</ref>', '', raw_content, flags=re.DOTALL)

    raw_content = re.sub(r'<ref[^>]*/>', '', raw_content)

    raw_content = re.sub(r'<[^>]+>', '', raw_content)

    raw_content = re.sub(r'={2,}(.*?)={2,}', r'\1', raw_content)

    raw_content = re.sub(r"'{2,}", '', raw_content)

    raw_content = re.sub(r'\[https?://\S+\s+([^\]]+)\]', r'\1', raw_content)

    raw_content = re.sub(r'\[https?://\S+\]', '', raw_content)

    raw_content = re.sub(r'\n{3,}', '\n\n', raw_content)
    raw_content = re.sub(r' {2,}', ' ', raw_content)
    
    return raw_content.strip()