import os
import json
import requests
import time

owner = "divineaurora1"
github_token = "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"

repositories = ["random"]  # Replace with your repository names

def get_issues(repo):
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues", headers=headers)

    # Check if the response is successful
    response.raise_for_status()

    return response.json()

def claim_issue(repo, issue_number):
    comment = "claim"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments",
        json={"body": comment},
        headers=headers,
    )
    return response.status_code

def main():
    try:
        # Initialize the previous_issues dictionary with the initial existing issues for each repository
        previous_issues = {}
        for repo in repositories:
            try:
                issues = get_issues(repo)
                issue_numbers = [issue["number"] for issue in issues]
                previous_issues[repo] = set(issue_numbers)
            except requests.exceptions.HTTPError as e:
                # Handle HTTPError, e.g., when there are no issues in the repository
                print(f"Error fetching issues for {owner}/{repo}: {e}")
                previous_issues[repo] = set()

        print("Initial previous_issues:", previous_issues)

        while True:
            for repo in repositories:
                issues = get_issues(repo)
                current_issues = set(issue["number"] for issue in issues)

                new_issues = current_issues - previous_issues[repo]

                if len(new_issues) > 0:
                    newest_issue_number = max(new_issues)
                    status_code = claim_issue(repo, newest_issue_number)

                    if status_code == 201:
                        print(f"Successfully claimed issue {newest_issue_number} in {owner}/{repo}.")
                    else:
                        print(f"Failed to claim issue {newest_issue_number} in {owner}/{repo}. Status code: {status_code}")

                previous_issues[repo] = current_issues

            time.sleep(15)  # Sleep for 5 seconds before checking again
    except KeyboardInterrupt:
        print("Script terminated.")

if __name__ == "__main__":
    main()
