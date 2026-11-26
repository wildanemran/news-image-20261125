#!/usr/bin/env python3
"""Render news-image-20261125 entry.png (1024x1024) from the agreed GLM layout
spec plus mandatory verification fixes. All text English. Deterministic PIL
render, no invented text.

Corrections applied vs the planning spec:
- Lead/ticker market numbers are the VERIFIED closes for Wed 25 Nov 2026
  (sedaily + AP/Barchart + Edge wrap): TAIEX -4.8% (38,195.43),
  KOSPI -6.2% (4,697.51), Nikkei -2.8% (57,011.62). The planning figure
  TAIEX -7.9% was the intraday fall, not the close.
- GLM mandatory fixes: ticker rows start y=840 (no 4px overflow); card 6
  title shortened; article "the" added in card 3 and card 6 bodies; card
  bodies at y+112 (padding at card bottom).
- Card 6 title reworded to a detonation PLAN (per coordinator verification):
  "Iowa Ammo Plant Detonation Plan Probed".
- Card 4 body uses "NATO Secretary General" (GLM minor).
- Ticker CYBER reworded so "unclassified systems" does not dangle (GLM minor).
- Masthead date at y=82 (GLM minor, avoids 6px overlap with title box).
"""
import hashlib
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

BG = (14, 23, 38)        # 0E1726
MASTHEAD = (16, 26, 46)   # 101A2E
LEAD = (27, 42, 68)       # 1B2A44
LEAD_BAR = (229, 72, 77)  # E5484D
CARD = (20, 33, 56)       # 142138
TICKER_BG = (11, 18, 32)  # 0B1220
GOLD = (240, 180, 41)     # F0B429
WHITE = (255, 255, 255)
CAT = (127, 178, 229)     # 7FB2E5
BODY = (199, 211, 224)    # C7D3E0
MUTED = (143, 163, 191)   # 8FA3BF
DARK = (14, 23, 38)       # 0E1726 (badge number text)

SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


def wrap(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---- Masthead (0,0,1024,108) ----
d.rectangle([0, 0, 1024, 108], fill=MASTHEAD)
f_title = font(SANS_B, 60)
t = "THE WORLD IN A DAY"
d.text(((W - d.textlength(t, font=f_title)) / 2, 24), t, font=f_title, fill=WHITE)
f_date = font(SANS_B, 24)
t2 = "WEDNESDAY, 25 NOVEMBER 2026"
d.text(((W - d.textlength(t2, font=f_date)) / 2, 82), t2, font=f_date, fill=MUTED)

# ---- Lead (48,132,928,150) ----
d.rectangle([48, 132, 976, 282], fill=LEAD)
d.rectangle([48, 132, 58, 282], fill=LEAD_BAR)
f_kicker = font(SANS_B, 22)
d.text((74, 150), "ASIA MARKETS", font=f_kicker, fill=GOLD)
f_lead = font(SANS_B, 34)
lead_l1 = "AI Selloff Hits Asian Shares"
lead_l2 = "TAIEX -4.8%, KOSPI -6.2%, Nikkei -2.8%"
d.text((74, 186), lead_l1, font=f_lead, fill=WHITE)
d.text((74, 228), lead_l2, font=f_lead, fill=WHITE)
check(d.textlength(lead_l1, font=f_lead) <= 902, "lead line 1 too wide")
check(d.textlength(lead_l2, font=f_lead) <= 902, "lead line 2 too wide")

# ---- Grid 2x3, cards 452x164 ----
CARDS = [
    ("WORLD", "Australia Passes Digital Duty of Care Bill",
     "Fines can reach five percent of global revenue."),
    ("EUROPE", "Russia Cuts Zaporizhzhia External Power",
     "Attack severed the nuclear plant's electricity supply."),
    ("GULF", "Saudi Coalition Intercepts Four Houthi Drones",
     "The drones were intercepted near the Ras Tanura terminal."),
    ("US", "NATO Chief Rutte Meets Trump in Florida",
     "NATO Secretary General Mark Rutte holds talks with Trump."),
    ("CYBER", "Hackers Breach CIA and ODNI Unclassified Systems",
     "The investigation is under way into the breach."),
    ("SAFETY", "Iowa Ammo Plant Detonation Plan Probed",
     "The plan was reported by the Iowa health department."),
]
COLS = [48, 524]
ROWS = [300, 478, 656]
f_badge = font(SANS_B, 20)
f_cat = font(SANS, 20)
f_ctitle = font(SANS_B, 26)
f_cbody = font(SANS, 20)

for i, (cat, title, body) in enumerate(CARDS):
    x = COLS[i % 2]
    y = ROWS[i // 2]
    d.rectangle([x, y, x + 452, y + 164], fill=CARD)
    # badge
    d.rectangle([x + 16, y + 12, x + 44, y + 40], fill=GOLD)
    num = str(i + 1)
    d.text((x + 16 + (28 - d.textlength(num, font=f_badge)) / 2, y + 14),
           num, font=f_badge, fill=DARK)
    d.text((x + 54, y + 16), cat, font=f_cat, fill=CAT)
    # title, max 2 lines of 420px
    tlines = wrap(d, title, f_ctitle, 420)
    check(len(tlines) <= 2, "card %d title needs >2 lines: %r" % (i + 1, tlines))
    for j, line in enumerate(tlines[:2]):
        check(d.textlength(line, font=f_ctitle) <= 420,
              "card %d title line too wide: %r" % (i + 1, line))
        d.text((x + 16, y + 52 + j * 30), line, font=f_ctitle, fill=WHITE)
    # body, max 2 lines of 420px, at y+112 (GLM fix 4)
    blines = wrap(d, body, f_cbody, 420)
    check(len(blines) <= 2, "card %d body needs >2 lines: %r" % (i + 1, blines))
    for j, line in enumerate(blines[:2]):
        check(d.textlength(line, font=f_cbody) <= 420,
              "card %d body line too wide: %r" % (i + 1, line))
        d.text((x + 16, y + 112 + j * 24), line, font=f_cbody, fill=BODY)

# ---- Ticker (48,836,928,116), rows start y=840 (GLM fix 1) ----
d.rectangle([48, 836, 976, 952], fill=TICKER_BG)
f_tick = font(SANS, 22)
TICKER = [
    "MARKETS: TAIEX -4.8%, KOSPI -6.2%, Nikkei -2.8%",
    "TRADE: Section 301 tariff plan covers 16 partners, release unverified",
    "CYBER: CIA and ODNI breach probe of unclassified systems continues",
    "SAFETY: Iowa plant plan reported, no detonation confirmed",
]
for j, line in enumerate(TICKER):
    y = 840 + j * 30
    check(d.textlength(line, font=f_tick) <= 912, "ticker line too wide: %r" % line)
    d.text((64, y), line, font=f_tick, fill=BODY)

# ---- Footer ----
f_foot = font(SANS, 20)
foot = "As of 22:00 WIB, Wednesday 25 November 2026. Next update 02:00 WIB."
d.text((48, 972), foot, font=f_foot, fill=MUTED)
check(d.textlength(foot, font=f_foot) <= 976, "footer too wide")

if failures:
    print("BUILD FAILED:")
    for f in failures:
        print(" - " + f)
    sys.exit(1)

out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
img.save(out, "PNG")
print("saved " + out)
# determinism is verified by the caller running this script twice in
# separate processes and comparing sha256.
print("sha256:", hashlib.sha256(open(out, "rb").read()).hexdigest())
print("size bytes:", len(open(out, "rb").read()))
