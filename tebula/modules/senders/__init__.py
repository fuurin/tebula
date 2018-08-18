from .line.line_sender import LINESender
from .slack.slack_sender import SlackSender
from .dummy.dummy_sender import DummySender

def get_sender_for(platform, *args, **kwargs):
    if platform == 'LINE':
        return LINESender(*args, **kwargs)
    elif platform == 'Slack':
        return SlackSender(*args, **kwargs)
    elif platform == 'Dummy':
        return DummySender(*args, **kwargs)

    raise ValueError(f'Unknown platform: {platform}')
