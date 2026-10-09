#!/usr/bin/env python3
"""Refresh light and dark profile star counters from GitHub."""

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

OWNER = "TahaHydra"
PROJECTS = {
    "Brave-Free-Origin": "brave",
    "CompDesk": "compdesk",
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
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/{OWNER}/{repository}", headers=headers)
    with urlopen(request, timeout=20) as response:
        return int(json.load(response)["stargazers_count"])


def render_svg(stars: int, light: bool) -> str:
    if stars < 10:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>\n'
    width = 32 + max(2, len(str(stars))) * 9
    star_color = "#b8860b" if light else "#e3b341"
    text_color = "#1f2328" if light else "#ffffff"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" '
        f'viewBox="0 0 {width} 20" role="img" aria-label="{stars} GitHub stars">'
        f'<path d="{STAR_PATH}" fill="{star_color}"/>'
        f'<text x="23" y="14.5" fill="{text_color}" '
        'font-family="Arial, Helvetica, sans-serif" font-size="13" '
        f'font-weight="700">{stars}</text></svg>\n'
    )


def main() -> None:
    for repository, name in PROJECTS.items():
        stars = github_stars(repository)
        for theme, light in (("white", False), ("light", True)):
            path = Path(f"assets/profile-stars-{name}-{theme}.svg")
            content = render_svg(stars, light)
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                print(f"Updated {path}: {stars} stars")
            else:
                print(f"Unchanged {path}: {stars} stars")


if __name__ == "__main__":
    main()
