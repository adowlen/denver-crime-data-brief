"""Composite the headline figure onto the hero illustration.
Figure text is the verified vehicle share from stats.json (48.3% in the
2022 window, 24.8% in the 2026 window) - typed once here and checked
against stats.json by assertion before compositing.
"""
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17"
SRC = f"{PKG}/hero_source/media-generation-hero-illustration-0-c8985da6-dc83-47d7-ba0a-3eac8ed716c5.png"
S = json.load(open(f"{PKG}/stats.json"))
share22 = S["vehicle_complex"]["share_of_window_pct"]["2022"]
share26 = S["vehicle_complex"]["share_of_window_pct"]["2026"]
assert share22 == 48.3 and share26 == 24.8, (share22, share26)

img = Image.open(SRC).convert("RGB")
W, H = img.size
# soft dark gradient scrim across the top for text legibility
scrim = Image.new("L", (1, H))
for y in range(H):
    scrim.putpixel((0, y), int(200 * max(0.0, 1 - y / (H * 0.52))))
scrim = scrim.resize((W, H))
black = Image.new("RGB", (W, H), (5, 6, 7))
img = Image.composite(black, img, scrim.point(lambda v: v // 3))

d = ImageDraw.Draw(img)
FD = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17/.venv/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf"
f_kick = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 44)
f_big = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 168)
f_sub = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 47)
AMBER, FG, MUT = (245, 168, 0), (232, 230, 225), (190, 196, 201)

x = 96
d.text((x, 84), "DENVER REPORTED OFFENSES, 2021-2026", font=f_kick, fill=AMBER)
d.text((x, 150), f"{share22}% \u2192 {share26}%", font=f_big, fill=FG)
d.text((x, 368), "Share of reported offenses involving a motor vehicle,", font=f_sub, fill=MUT)
d.text((x, 428), "matched Jan 1-Oct 13 windows, 2022 vs 2026", font=f_sub, fill=MUT)
img.save(f"{PKG}/hero.png")
print("hero.png written", img.size)
