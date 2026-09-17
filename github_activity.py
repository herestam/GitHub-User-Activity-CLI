#!/usr/bin/env python3
"""Fetch and display the recent activity of a GitHub user from the terminal."""

import argparse
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_ENDPOINT = "https://api.github.com/users/{username}/events"
USER_AGENT = "github-activity-cli"


def fetch_events(username):
    url = API_ENDPOINT.format(username=username)
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    try:
        with urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        if error.code == 404:
            sys.exit(f"Error: user '{username}' not found.")
        if error.code in (403, 429):
            sys.exit("Error: rate limit exceeded or access forbidden. Try again later.")
        sys.exit(f"Error: GitHub API request failed with status {error.code}.")
    except URLError as error:
        sys.exit(f"Error: could not reach GitHub API ({error.reason}).")


def format_event(event):
    repo = event["repo"]["name"]
    event_type = event["type"]
    payload = event.get("payload", {})

    if event_type == "PushEvent":
        count = len(payload.get("commits", []))
        if count:
            noun = "commit" if count == 1 else "commits"
            return f"Pushed {count} {noun} to {repo}"
        return f"Pushed to {repo}"

    if event_type == "IssueCommentEvent":
        number = payload.get("issue", {}).get("number")
        return f"Commented on issue #{number} in {repo}"

    if event_type == "WatchEvent":
        return f"Starred {repo}"

    if event_type == "PullRequestEvent":
        action = payload.get("action", "")
        if action == "closed" and payload.get("pull_request", {}).get("merged"):
            return f"Merged a pull request in {repo}"
        return f"{action.capitalize()} a pull request in {repo}"

    if event_type == "IssuesEvent":
        action = payload.get("action", "")
        return f"{action.capitalize()} an issue in {repo}"

    if event_type == "CreateEvent":
        ref = payload.get("ref")
        ref_type = payload.get("ref_type", "")
        if ref_type == "repository":
            return f"Created a repository {repo}"
        return f"Created {ref_type} {ref} in {repo}"

    if event_type == "DeleteEvent":
        ref = payload.get("ref")
        ref_type = payload.get("ref_type", "")
        return f"Deleted {ref_type} {ref} in {repo}"

    if event_type == "ForkEvent":
        return f"Forked {repo}"

    if event_type == "CommitCommentEvent":
        return f"Commented on a commit in {repo}"

    if event_type == "PullRequestReviewEvent":
        return f"Reviewed a pull request in {repo}"

    if event_type == "PullRequestReviewCommentEvent":
        return f"Commented on a pull request in {repo}"

    if event_type == "ReleaseEvent":
        name = payload.get("release", {}).get("name")
        label = f" '{name}'" if name else ""
        return f"Released {label} in {repo}"

    if event_type == "PublicEvent":
        return f"Made {repo} public"

    if event_type == "MemberEvent":
        return f"Added a collaborator to {repo}"

    if event_type == "GollumEvent":
        return f"Updated the wiki in {repo}"

    return f"{event_type} in {repo}"


def show_activity(username, limit):
    events = fetch_events(username)
    if not events:
        print(f"No recent activity found for '{username}'.")
        return
    for event in events[:limit]:
        print(f"- {format_event(event)}")


def interactive():
    print("GitHub Activity — type a username to see their recent activity.")
    print("Commands: 'quit' or 'exit' to leave. 'limit N' sets the event count.")
    limit = 10
    while True:
        try:
            command = input("github-activity> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not command:
            continue
        if command.lower() in ("quit", "exit"):
            break
        if command.lower().startswith("limit "):
            try:
                new_limit = int(command.split()[1])
                if new_limit < 1:
                    print("Error: limit must be a positive integer.")
                else:
                    limit = new_limit
                    print(f"Now showing up to {limit} events.")
            except (IndexError, ValueError):
                print("Usage: limit <number>")
            continue
        try:
            show_activity(command, limit)
        except SystemExit as error:
            print(error)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display the recent activity of a GitHub user."
    )
    parser.add_argument(
        "username",
        nargs="?",
        help="GitHub username to inspect (omit to start interactive mode)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="maximum number of events to display (default: 10)",
    )
    args = parser.parse_args()

    if args.limit < 1:
        sys.exit("Error: --limit must be a positive integer.")

    if not args.username:
        interactive()
        return

    show_activity(args.username, args.limit)


if __name__ == "__main__":
    main()