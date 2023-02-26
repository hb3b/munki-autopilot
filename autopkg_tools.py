import os

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_TOKEN", None)

print(SLACK_WEBHOOK)
