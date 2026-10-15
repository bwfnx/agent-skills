"""Check a README's local files and guide links before shipping.

Usage (from the target repo root):
    python3 check_readme.py README.md [--pages-base https://bwfnx.github.io/sbdc-toolkit/]

Fails if a local src/href/srcset path doesn't exist, or a link under --pages-base
has no matching docs/<page>.html. Run with --self-test to check this script.
"""
import argparse, pathlib, re, sys, tempfile

LINK = re.compile(r'(?:src|href|srcset)="([^"#]+)|\]\(([^)#\s]+)\)')


def problems(readme: pathlib.Path, pages_base: str | None) -> list[str]:
    root, out = readme.parent, []
    for m in LINK.finditer(readme.read_text()):
        target = m.group(1) or m.group(2)
        if pages_base and target.startswith(pages_base):
            page = target[len(pages_base):] or "index.html"
            if not (root / "docs" / page).is_file():
                out.append(f"guide page missing: docs/{page}  ({target})")
        elif not re.match(r"[a-z]+:", target) and not (root / target).exists():
            out.append(f"missing file: {target}")
    return out


def self_test():
    with tempfile.TemporaryDirectory() as d:
        r = pathlib.Path(d)
        (r / "docs").mkdir(); (r / "docs" / "a.html").write_text("x"); (r / "img.png").write_text("x")
        md = r / "README.md"
        md.write_text('<img src="img.png"> [ok](https://x.io/s/a.html) [bad](https://x.io/s/b.html) '
                      '<img src="gone.png"> [web](https://example.com) [anchor](#install)')
        found = problems(md, "https://x.io/s/")
        assert found == ["guide page missing: docs/b.html  (https://x.io/s/b.html)", "missing file: gone.png"], found
    print("self-test ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("readme", nargs="?", default="README.md")
    ap.add_argument("--pages-base")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test(); sys.exit(0)
    found = problems(pathlib.Path(a.readme), a.pages_base)
    print("\n".join(found) or "all links and files resolve")
    sys.exit(1 if found else 0)
