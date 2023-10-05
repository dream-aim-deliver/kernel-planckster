import os

RUNNING_IN_CI = os.getenv("GITHUB_ACTIONS", False) == "true"
