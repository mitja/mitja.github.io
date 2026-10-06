#!/usr/bin/env python3
"""Check that every URL of an older build still resolves in a newer build.

Usage: scripts/check-legacy-urls.py OLD_BUILD_DIR NEW_BUILD_DIR

Collects every <loc> of the old build's sitemaps (the sitemap index and the
per-language sitemaps) and every alias page of the old build (an index.html
with a meta refresh), then checks each path in the new build: it must exist as
a page or as a redirect stub, and a stub's target must exist too.

Exit status 1 if anything is missing. Intended use:

    git worktree add /tmp/old main && hugo -s /tmp/old -d /tmp/old-public
    hugo -d /tmp/new-public
    scripts/check-legacy-urls.py /tmp/old-public /tmp/new-public
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

REFRESH = re.compile(r'http-equiv="?refresh"?[^>]*url=([^"\'> ]+)', re.I)
LOC = re.compile(r"<loc>([^<]+)</loc>")


def sitemap_paths(build: Path) -> set[str]:
    paths: set[str] = set()
    for sm in build.rglob("sitemap.xml"):
        for url in LOC.findall(sm.read_text()):
            if url.endswith("sitemap.xml"):
                continue
            paths.add(unquote(urlparse(url).path))
    return paths


def alias_paths(build: Path) -> set[str]:
    paths: set[str] = set()
    for page in build.rglob("index.html"):
        text = page.read_text(errors="replace")
        if REFRESH.search(text):
            paths.add("/" + page.parent.relative_to(build).as_posix().strip(".") + "/")
    return {p.replace("//", "/") for p in paths}


def resolve(build: Path, path: str, depth: int = 0) -> str | None:
    """Return the final path a request to `path` ends at, or None."""
    if depth > 3:
        return None
    page = build / path.lstrip("/") / "index.html"
    if not page.is_file():
        return None
    m = REFRESH.search(page.read_text(errors="replace"))
    if not m:
        return path
    target = unquote(urlparse(m.group(1)).path)
    return resolve(build, target, depth + 1)


def main() -> int:
    old, new = Path(sys.argv[1]), Path(sys.argv[2])
    from_sitemap = sitemap_paths(old)
    from_aliases = alias_paths(old)
    missing = []
    for path in sorted(from_sitemap | from_aliases):
        # Hugo writes a "/page/1/" alias for every paginated list; nothing links to it.
        if path.endswith("/page/1/"):
            continue
        if resolve(new, path) is None:
            missing.append(path)
    print(f"old sitemap URLs: {len(from_sitemap)}, old alias URLs: {len(from_aliases - from_sitemap)}, "
          f"checked: {len(from_sitemap | from_aliases)}, missing: {len(missing)}")
    for path in missing:
        print("MISSING", path)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
