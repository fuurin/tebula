from .line.line_sender import LINESender
from .slack.slack_sender import SlackSender

def get_sender_for(platform, *args, **kwargs):
    if platform == 'LINE':
        return LINESender(*args, **kwargs)
    elif platform == 'Slack':
        return SlackSender(*args, **kwargs)

    raise ValueError(f'Unknown platform: {platform}')