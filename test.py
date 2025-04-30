from github import Github
import os
from dotenv import load_dotenv

load_dotenv()  # Ensure environment variables from .env are loaded

# Initialize GitHub with token
g = Github(os.getenv("GITHUB_TOKEN"))

# Get the authenticated user
user = g.get_user()
print("✅ Authenticated as:", user.login)
