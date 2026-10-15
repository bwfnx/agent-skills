"""Render README images: python3 docs/img/src/render.py  (needs: pip install weasyprint; pdftoppm from poppler)

Each source HTML sets its own @page size. Pages with a light/dark pair get both,
written as <name>-light.png and <name>-dark.png; the banner is one image.
"""
import pathlib, subprocess, tempfile
from weasyprint import HTML

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent
PAIRS = ["hero", "highlights"]          # rendered light + dark
SINGLE = ["banner"]                      # navy already, same in both themes


def render(name, dark=None):
    html = (SRC / f"{name}.html").read_text()
    if dark is not None:
        html = html.replace("<html>", '<html class="dark">' if dark else "<html>", 1)
    suffix = "" if dark is None else ("-dark" if dark else "-light")
    with tempfile.TemporaryDirectory() as tmp:
        pdf = pathlib.Path(tmp) / "out.pdf"
        HTML(string=html, base_url=str(SRC)).write_pdf(pdf)
        # 192 dpi = 2x the 96 dpi CSS pixel, so images are retina-sharp at their CSS size
        subprocess.run(["pdftoppm", "-png", "-r", "192", "-singlefile", str(pdf),
                        str(OUT / f"{name}{suffix}")], check=True)
    print("wrote", f"{name}{suffix}.png")


for n in SINGLE:
    render(n)
for n in PAIRS:
    render(n, dark=False)
    render(n, dark=True)
