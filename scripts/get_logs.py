import requests
import json

url = "https://api.github.com/repos/ks1324679-lab/ai-news-site/actions/runs/22492856635/jobs"
response = requests.get(url)
jobs = response.json().get("jobs", [])
for job in jobs:
    if job["name"] == "update-news":
        log_url = f"https://api.github.com/repos/ks1324679-lab/ai-news-site/actions/jobs/{job['id']}/logs"
        log_response = requests.get(log_url)
        print(log_response.text)
