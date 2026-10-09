#!/usr/bin/env python3
"""Update profile star SVGs from public GitHub repository counts."""

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

OWNER = "TahaHydra"
PROJECTS = {
    "Brave-Free-Origin": Path("assets/profile-stars-brave.svg"),
    "CompDesk": Path("assets/profile-stars-compdesk.svg"),
}

STAR_PATH = (
    "M10 1.5l2.58 5.22 5.76.84-4.17 4.06.98 5.74L10 14.65"
    "l-5.15 2.71.98-5.74L1.66 7.56l5.76-.84Z"
)


def github_stars(repository: str) -> int:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "TahaHydra-profile-star-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/{OWNER}/{repository}", headers=headers)
    with urlopen(request, timeout=20) as response:
        payload = json.load(response)
    return int(payload["stargazers_count"])


def render_svg(stars: int) -> str:
    if stars < 10:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>\n'
    width = 32 + max(2, len(str(stars))) * 9
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" '
        f'viewBox="0 0 {width} 20" role="img" aria-label="{stars} GitHub stars">'
        f'<path d="{STAR_PATH}" fill="#e3b341"/>'
        '<text x="23" y="14.5" fill="#ffffff" '
        'font-family="Arial, Helvetica, sans-serif" font-size="13" '
        f'font-weight="600">{stars}</text></svg>\n'
    )


def main() -> None:
    for repository, path in PROJECTS.items():
        stars = github_stars(repository)
        svg = render_svg(stars)
        if not path.exists() or path.read_text(encoding="utf-8") != svg:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(svg, encoding="utf-8")
            print(f"Updated {repository}: {stars} stars")
        else:
            print(f"Unchanged {repository}: {stars} stars")


if __name__ == "__main__":
    main()
