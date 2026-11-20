import os

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
API_URL = f"{BASE_URL}/api"
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "20"))

# The demo site loads ad and consent scripts that randomly cover the page.
# Blocking them is the main thing that keeps the UI tests stable.
BLOCKED_HOSTS = (
    "googlesyndication.com",
    "doubleclick.net",
    "googleadservices.com",
    "google-analytics.com",
    "googletagmanager.com",
    "fundingchoicesmessages.google.com",
    "adservice.google.com",
    "googletagservices.com",
    "adtrafficquality.google",
)
