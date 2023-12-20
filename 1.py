import requests

def check_rate_limit(token):
    url = "https://api.github.com/rate_limit"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # The request was successful
        rate_limit_info = response.json()["resources"]["core"]
        remaining_requests = rate_limit_info["remaining"]
        limit = rate_limit_info["limit"]
        reset_time = rate_limit_info["reset"]

        print(f"Remaining requests: {remaining_requests}/{limit}")
        print(f"Reset time: {reset_time} (UTC)")

        if remaining_requests == 0:
            print("You have reached the rate limit.")
    else:
        print(f"Failed to check rate limit. Status code: {response.status_code}")
        print(response.text)

# Replace "your_token_here" with your actual GitHub token
check_rate_limit("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")
