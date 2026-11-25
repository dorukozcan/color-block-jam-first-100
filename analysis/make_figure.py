#!/usr/bin/env python3
"""Draw the README figure from the tables: what appeared at each of levels 1 to 100.

Run:  python3 analysis/make_figure.py     (needs matplotlib; writes figures/first_100_levels.png)
"""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.transforms import blended_transform_factory  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SURFACE, INK, INK2, MUTED, GRID, AXIS, WASH = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#f0efec"
ADS, TIMEOUT = "#2a78d6", "#eb6834"          # categorical slots 1 and 2, validated together on the light surface
plt.rcParams.update({"font.family": ["Arial", "DejaVu Sans"], "font.size": 9.5})


def rows(name):
    with open(ROOT / "data" / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def n(x):
    return int(x) if x not in ("", None) else None


att, off, ads, lev, rec = (rows(f) for f in ("attempts.csv", "offers.csv", "ads.csv", "levels.csv", "recordings.csv"))

wins = {n(a["level"]): a for a in att if a["result"] == "win"}
x2_yes = sorted(lv for lv, a in wins.items() if a["x2_offered"] == "True")
x2_unread = sorted(lv for lv, a in wins.items() if lv >= 15 and a["x2_offered"] != "True")
gp, bn = defaultdict(int), defaultdict(int)
for a in att:
    gp[n(a["level"])] += n(a["gameplay_frames"])
    bn[n(a["level"])] += n(a["banner_frames"])
banner = {lv: bn[lv] / gp[lv] for lv in gp if gp[lv] and bn[lv]}
by = defaultdict(list)
for a in att:
    by[a["recording"]].append(a)
for a2 in by.values():
    a2.sort(key=lambda a: n(a["start_t"]))
# X2 Coins taken: the rewarded video doubles the level's 40 coins, so the next level starts 80 coins higher
x2_taken = {n(a["level"]) for a2 in by.values() for a, b in zip(a2, a2[1:]) if a["result"] == "win" and a["coins_start"]
            and b["coins_start"] and not n(a["continues"]) and n(b["coins_start"]) - n(a["coins_start"]) == 80}
# interstitials: a full-screen ad of 3 s or more seen between a win and the next attempt, X2 not taken. A recording that
# ends on a win screen hands over to the next one: an ad before its first attempt tied to the same level counts (level 27)
order = [x["recording"] for x in rec]
ad_after = set()
for r, a2 in by.items():
    for i, a in enumerate(a2):
        if a["result"] == "win" and n(a["level"]) not in x2_taken:
            nxt = n(a2[i + 1]["start_t"]) if i + 1 < len(a2) else float("inf")
            seen = any(x["recording"] == r and n(a["end_t"]) <= n(x["t"]) < nxt and n(x["seconds"]) >= 3 for x in ads)
            k = order.index(r)
            if i + 1 == len(a2) and k + 1 < len(order):
                nr = order[k + 1]
                first = min((n(b["start_t"]) for b in by.get(nr, [])), default=float("inf"))
                seen |= any(x["recording"] == nr and n(x["t"]) < first and n(x["level"]) == n(a["level"])
                            and n(x["seconds"]) >= 3 for x in ads)
            if seen:
                ad_after.add(n(a["level"]))
label = {n(x["level"]): x["label"] for x in lev if x["label"]}

LANES = [  # y, name, key figure
    (4, "Rewarded X2 Coins on the win screen", f"{len(x2_yes)} of {len(x2_yes) + len(x2_unread)} wins from level 15; "
                                               f"taken at {' and '.join(map(str, sorted(x2_taken)))}"),
    (3, "Banner during play", "bar height = share of frames read as play"),
    (2, "Interstitial after the win", f"{len(ad_after)} of {sum(1 for lv in wins if lv >= 19 and lv not in x2_taken)} wins "
                                      "from level 19"),
    (1, "Time-out: the clock hit zero", f"{len(off)} time-outs: {sum(o['decision'] == 'bought' for o in off)} continued, "
                                        f"{sum(o['decision'] == 'declined' for o in off)} lost"),
    (0, "Difficulty label", "tall: VERY HARD, short: HARD"),
]
H = 0.56                                       # mark height inside a lane

fig = plt.figure(figsize=(10, 4.2), dpi=200, facecolor=SURFACE)
ax = fig.add_axes([0.285, 0.235, 0.695, 0.585], facecolor=SURFACE)
ax.axvspan(0.5, 14.5, color=WASH, zorder=0, lw=0)
ax.text(7.5, 2, "No ads in\nlevels 1-14", ha="center", va="center", fontsize=9, color=INK2, zorder=1)
for x in range(10, 101, 10):
    ax.axvline(x, color=GRID, lw=0.6, zorder=0)


def bars(y, levels, color, height=lambda lv: 1.0):
    for lv in levels:
        ax.add_patch(Rectangle((lv - 0.36, y - H / 2), 0.72, H * height(lv), facecolor=color, edgecolor="none", zorder=2))


bars(4, x2_yes, ADS)
bars(4, x2_unread, AXIS)
bars(3, sorted(banner), ADS, height=lambda lv: banner[lv])
bars(2, sorted(ad_after), ADS)
bars(0, sorted(label), MUTED, height=lambda lv: 1.0 if label[lv] == "VERY HARD" else 0.5)

SHAPE = {"fail_offer": ("o", 62), "fail_offer>fail_warn": ("s", 50), "fail_offer>fail_lucky": ("D", 44)}
for o in off:
    lv, (marker, size) = n(o["level"]), SHAPE[o["steps"]]
    bought = o["decision"] == "bought"
    ax.scatter([lv], [1], s=size, marker=marker, facecolor=TIMEOUT if bought else SURFACE,
               edgecolor=SURFACE if bought else TIMEOUT, linewidth=1.2 if bought else 1.6, zorder=3)
    ax.text(lv, 1 - 0.36, str(lv), ha="center", va="top", fontsize=8, color=INK2, zorder=3)

tr = blended_transform_factory(ax.transAxes, ax.transData)
for y, name, stat in LANES:
    ax.text(-0.025, y + 0.04, name, transform=tr, ha="right", va="bottom", fontsize=10, color=INK)
    ax.text(-0.025, y - 0.02, stat, transform=tr, ha="right", va="top", fontsize=8.6, color=INK2)

ax.set_xlim(0.5, 100.5)
ax.set_ylim(-0.55, 4.5)
ax.set_xticks([1] + list(range(10, 101, 10)))
ax.tick_params(axis="x", colors=MUTED, labelsize=8.6, length=0, pad=4)
ax.set_yticks([])
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(AXIS)
ax.spines["bottom"].set_linewidth(0.8)
ax.set_xlabel("Level", color=INK2, fontsize=9, labelpad=4)

fig.text(0.02, 0.955, "Color Block Jam, levels 1 to 100: where ads and continue offers appeared",
         fontsize=13, color=INK, weight="bold", va="top")
fig.text(0.02, 0.895, "One new player, iPhone, Türkiye App Store, 20-23 November 2026, no money spent. "
         "Every level on screen recording, read at one frame per second.", fontsize=9.2, color=INK2, va="top")

handles = [Line2D([], [], ls="none", marker="o", ms=6.5, mfc=TIMEOUT, mec=SURFACE, label="first screen only (+20 s)"),
           Line2D([], [], ls="none", marker="s", ms=5.8, mfc=TIMEOUT, mec=SURFACE, label="then a loss reminder"),
           Line2D([], [], ls="none", marker="D", ms=5.2, mfc=TIMEOUT, mec=SURFACE, label="then an upgrade (+65 s, 3 rockets)"),
           Line2D([], [], ls="none", marker="s", ms=5.8, mfc=SURFACE, mec=TIMEOUT, mew=1.4, label="hollow: declined, attempt lost"),
           Line2D([], [], ls="none", marker="s", ms=5.8, mfc=AXIS, mec=AXIS, label="gray: win screen not readable")]
fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.02, 0.068), ncol=5, frameon=False, fontsize=8.4,
           labelcolor=INK2, handletextpad=0.3, columnspacing=1.2, borderaxespad=0)
fig.text(0.02, 0.022, "100 levels won in 101 attempts; 1 more cut by a recording's end. Interstitial: a 3 s+ ad between a "
         "win and the next attempt. Level 38 left out (my X2 video).", fontsize=7.8, color=MUTED, va="bottom")

out = ROOT / "figures" / "first_100_levels.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, facecolor=SURFACE)
print(f"wrote {out.relative_to(ROOT)}")
