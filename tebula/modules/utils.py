import emoji

def remove_emoji(s):
    return "".join(c for c in s if c not in emoji.UNICODE_EMOJI)
