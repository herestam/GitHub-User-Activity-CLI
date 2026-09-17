# GitHub Activity CLI

A simple command-line tool that fetches the recent public activity of a GitHub user from the GitHub API and displays it in the terminal.

**Project URL:** <https://roadmap.sh/projects/github-user-activity>

**Repository:** <https://github.com/herestam/GitHub-User-Activity-CLI>

## Requirements

- Python 3.6+
- Internet connection (no third-party packages needed — uses only the standard library)

## Getting started

Clone or download the project, then make the script executable (macOS/Linux):

```bash
chmod +x github_activity.py
```

## Usage

### One-shot mode

Pass the GitHub username as an argument:

```bash
python3 github_activity.py <username>
```

Example:

```bash
python3 github_activity.py torvalds
```

Output:

```
- Pushed to torvalds/GuitarPedal
- Pushed to torvalds/linux
- Pushed 3 commits to torvalds/test
- Starred kamranahmedse/developer-roadmap
- ...
```

### Interactive mode

Run without arguments to start an interactive prompt:

```bash
python3 github_activity.py
```

Then type a username to see their recent activity:

```
github-activity> torvalds
- Pushed to torvalds/GuitarPedal
- Pushed to torvalds/linux

github-activity> quit
```

Available interactive commands:

| Command          | Description                                    |
| ---------------- | ---------------------------------------------- |
| `<username>`     | Fetch and display the user's recent activity   |
| `limit <number>` | Change how many events are displayed (default: 10) |
| `quit` / `exit`  | Leave the interactive prompt                   |

### Options

| Option      | Description                                     |
| ----------- | ----------------------------------------------- |
| `--limit N` | Maximum number of events to show (default: 10)  |

## How it works

The tool queries the GitHub Events API:

```
GET https://api.github.com/users/<username>/events
```

and translates each raw event into a human-readable line based on its event type (push, issue, star, pull request, fork, release, etc.).

## Error handling

- Unknown user → `Error: user '<username>' not found.`
- Rate limit exceeded / forbidden → error message suggesting to retry later
- No network → error message explaining the connection failed
- No recent activity → prints a friendly notice

## Project structure

```
cli_pyhton/
└── github_activity.py   # the CLI application
```