import os

SLACK_WEBHOOK = os.environ.get("TEST_SECRET", None)

print(SLACK_WEBHOOK + "12345")
