"""Applies the portfolio branding (icon + splash) to the generated Android project.
Run after `npx cap add android`. Uses only www/icon-512.png (a copy; the original is never touched)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
RES = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "android/app/src/main/res"
SRC = Image.open(ROOT / "www/icon-512.png").convert("RGBA")
BG = (10, 20, 40, 255)  # #0A1428

LAUNCHER = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

def resized(img, size):
    return img.resize((size, size), Image.LANCZOS)

for dens, px in LAUNCHER.items():
    d = RES / f"mipmap-{dens}"
    d.mkdir(parents=True, exist_ok=True)
    resized(SRC, px).save(d / "ic_launcher.png")
    # round icon
    sq = resized(SRC, px)
    mask = Image.new("L", (px * 4, px * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, px * 4 - 1, px * 4 - 1), fill=255)
    mask = mask.resize((px, px), Image.LANCZOS)
    rd = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    rd.paste(sq, (0, 0), mask)
    rd.save(d / "ic_launcher_round.png")
    # adaptive foreground (108dp canvas, icon kept inside the safe zone)
    fg_px = round(px * 108 / 48)
    fg = Image.new("RGBA", (fg_px, fg_px), (0, 0, 0, 0))
    inner = round(fg_px * 0.60)
    fg.paste(resized(SRC, inner), ((fg_px - inner) // 2, (fg_px - inner) // 2))
    fg.save(d / "ic_launcher_foreground.png")

vals = RES / "values"
vals.mkdir(parents=True, exist_ok=True)
(vals / "ic_launcher_background.xml").write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
    '    <color name="ic_launcher_background">#0A1428</color>\n</resources>\n')

# splash: same size as each existing splash.png, navy background + centered icon
count = 0
for f in RES.glob("drawable*/splash.png"):
    w, h = Image.open(f).size
    canvas = Image.new("RGBA", (w, h), BG)
    side = round(min(w, h) * 0.30)
    canvas.paste(resized(SRC, side), ((w - side) // 2, (h - side) // 2))
    canvas.convert("RGB").save(f)
    count += 1
print(f"Branding applied: launcher icons for {len(LAUNCHER)} densities, {count} splash images.")
