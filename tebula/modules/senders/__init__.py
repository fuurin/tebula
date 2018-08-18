from .line.line_sender import LINESender


def get_sender_for(platform, *args, **kwargs):
    if (platform == 'LINE'):
        return LINESender(*args, **kwargs)
    raise ValueError(f'Unknown platform: {platform}')