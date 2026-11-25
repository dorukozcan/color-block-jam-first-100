#!/usr/bin/env python3
"""Data checks for the Color Block Jam first-100 study.

Run:  python3 -I analysis/check_note_numbers.py

Computes values from the tables in data/ and compares each with a fixed expected value written
below. It does not read the note, the scorecard or the PDF, so it shows that the tables still give
the reported numbers, not that the documents quote them correctly. Exits with status 1 if any check
fails. Python 3.8 or later, standard library only.
"""
import csv
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def rows(name):
    with open(DATA / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def n(x):
    return int(x) if x not in ("", None) else None


att, off, ads, lev, rec = (rows(f) for f in ("attempts.csv", "offers.csv", "ads.csv", "levels.csv", "recordings.csv"))
checks = []


def check(name, got, expected):
    checks.append((name, got, expected))


# Recordings and attempts (scorecard A3-A5, B1-B5)
by = defaultdict(list)                       # recording -> attempts in time order
for a in att:
    by[a["recording"]].append(a)
for r in by:
    by[r].sort(key=lambda a: n(a["start_t"]))
per = defaultdict(list)                      # level -> results in play order (recording ids R01.. sort by time)
for r in sorted(by):
    for a in by[r]:
        per[n(a["level"])].append(a["result"])

check("recordings / days", (len(rec), sorted({r["day"] for r in rec})), (9, ["2026-11-20", "2026-11-22", "2026-11-23"]))
check("levels on video", sorted(per), list(range(1, 101)))
played = [x for rs in per.values() for x in rs if x != "cut"]
check("attempts / lost / cut by the end of a recording",
      (len(played), played.count("fail"), sum(rs.count("cut") for rs in per.values())), (101, 1, 1))
check("recorded attempts / wins", (len(att), sum(a["result"] == "win" for a in att)), (102, 100))
check("level of the lost attempt / of the cut attempt",
      ([lv for lv, rs in per.items() if "fail" in rs], [lv for lv, rs in per.items() if "cut" in rs]), ([59], [79]))
check("first-try wins in levels 1-25, 26-50, 51-75, 76-100",
      [sum(1 for x in range(lo, lo + 25) if per[x][0] == "win") for lo in (1, 26, 51, 76)], [25, 25, 24, 24])
check("most attempts on one level / levels with 5 or more",
      (max(len([x for x in rs if x != "cut"]) for rs in per.values()), sum(1 for rs in per.values() if len(rs) >= 5)), (2, 0))

# Time-outs and the continue offer (C1-C12)
off.sort(key=lambda o: n(o["level"]))
check("time-out levels", [n(o["level"]) for o in off], [51, 59, 71, 88, 94, 97])
check("time-outs that opened on the first screen (+20 seconds for 900 coins)", sum(o["steps"].split(">")[0] == "fail_offer" for o in off), 6)
check("time-outs where the first screen was closed and a second one opened", sum(">" in o["steps"] for o in off), 4)
for label, steps, levels, bought in (("loss reminder", "fail_offer>fail_warn", [51, 59], [51]),
                                     ("upgraded offer", "fail_offer>fail_lucky", [71, 88], [71, 88]),
                                     ("first screen only", "fail_offer", [94, 97], [94, 97])):
    o2 = [o for o in off if o["steps"] == steps]
    check(f"{label}: levels / bought", ([n(o["level"]) for o in o2], [n(o["level"]) for o in o2 if o["decision"] == "bought"]),
          (levels, bought))
check("continues bought / prices", (sum(o["decision"] == "bought" for o in off), sorted({n(o["price"]) for o in off})), (5, [900]))
check("continues in attempts.csv", sum(n(a["continues"]) or 0 for a in att), 5)
held = [next(a for a in by[o["recording"]] if n(a["start_t"]) <= n(o["t"]) <= n(a["end_t"])) for o in off if o["decision"] == "bought"]
check("attempts continued with coins / of them won", (len(held), sum(a["result"] == "win" for a in held)), (5, 5))
check("offer screens shown / continues bought (C9, C10 in offer screens)", (sum(len(o["steps"].split(">")) for o in off),
                                                                             sum(o["decision"] == "bought" for o in off)), (10, 5))
check("real-money cards on the fail screens, by time-out", [(n(o["level"]), o["cards"]) for o in off],
      [(51, "Fail Offer+Golden Ticket"), (59, "Fail Offer+Golden Ticket"), (71, "Coin Madness+Fail Offer+Golden Ticket"),
       (88, "Coin Madness+Fail Offer"), (94, "Coin Madness"), (97, "Coin Madness")])
check("time-outs where the balance covered 900 coins", sum(n(o["balance"]) >= 900 for o in off), 6)
check("coin balance on the fail screen: lowest / highest", (min(n(o["balance"]) for o in off), max(n(o["balance"]) for o in off)), (2200, 3800))
check("time-outs with a real-money card on the fail screen", sum(bool(o["cards"]) for o in off), 6)
dec = {d: [n(o["decide_seconds"]) for o in off if o["decision"] == d] for d in ("bought", "declined")}
check("seconds to decide, bought in level order / declined", (dec["bought"], dec["declined"]), ([13, 9, 8, 4, 2], [18]))
check("median seconds to decide, bought / declined", (st.median(dec["bought"]), st.median(dec["declined"])), (8, 18))

# Ads
wins = [a for a in att if a["result"] == "win"]
x2 = [a for a in wins if a["x2_offered"] == "True"]
check("win screens with X2 Coins in levels 1-14", sum(1 for a in x2 if n(a["level"]) <= 14), 0)
check("first level with X2 Coins", min(n(a["level"]) for a in x2), 15)
check("X2 Coins on win screens of levels 15-100", (sum(1 for a in x2 if n(a["level"]) >= 15),
                                                   sum(1 for a in wins if n(a["level"]) >= 15)), (84, 86))


def banner(lo, hi):
    a2 = [a for a in att if lo <= n(a["level"]) <= hi]
    return sum(n(a["banner_frames"]) for a in a2), sum(n(a["gameplay_frames"]) for a in a2)


b, g = banner(1, 18)
check("gameplay frames with a banner in levels 1-18", (b, g), (0, 726))
b, g = banner(19, 19)
check("banner share of gameplay frames on level 19 (%)", round(100 * b / g), 51)
b, g = banner(20, 100)
check("banner share of gameplay frames in levels 20-100 (%, frames)", (round(100 * b / g, 1), g), (98.3, 8773))

ads_by = defaultdict(list)
for x in ads:
    ads_by[x["recording"]].append(x)


def ad_level(x):
    """The level just played (for the episode that opens R03, the level 27 win screen the game returned to)."""
    if x["level"]:
        return n(x["level"])
    return next(n(a["level"]) for a in by[x["recording"]] if n(a["start_t"]) > n(x["t"]))


# X2 Coins taken: the rewarded video doubles the level's 40 coins, so the next level starts 80 coins higher, not 40
x2_taken = sorted(n(a["level"]) for r in by for a, b in zip(by[r], by[r][1:])
                  if a["result"] == "win" and a["coins_start"] and b["coins_start"] and not n(a["continues"])
                  and n(b["coins_start"]) - n(a["coins_start"]) == 80)
check("X2 Coins taken (rewarded video I chose): levels", x2_taken, [17, 38])
ads3 = [x for x in ads if n(x["seconds"]) >= 3]
check("full-screen ad episodes of 3 s or more around levels 1-18: levels", [ad_level(x) for x in ads3 if ad_level(x) <= 18], [17])
# An interstitial here is a full-screen ad seen between a win and the next attempt, and not chosen by me.
# When a recording ends on a win screen, an ad before the next recording's first attempt that the parser tied to the
# same level (the game came back to that win screen after the ad) belongs to that win. This happens once: level 27.
order = [x["recording"] for x in rec]        # R01..R09, in time order
after, across = {}, []                       # (recording, level won) -> ad episodes of 3 s or more before the next attempt
for r, a2 in by.items():
    for i, a in enumerate(a2):
        if a["result"] == "win":
            nxt = n(a2[i + 1]["start_t"]) if i + 1 < len(a2) else float("inf")
            eps = [x for x in ads_by[r] if n(a["end_t"]) <= n(x["t"]) < nxt]
            k = order.index(r)
            if i + 1 == len(a2) and k + 1 < len(order):
                nr = order[k + 1]
                first = n(by[nr][0]["start_t"]) if by.get(nr) else float("inf")
                more = [x for x in ads_by[nr] if n(x["t"]) < first and n(x["level"]) == n(a["level"])]
                across += [n(a["level"])] * bool(more)
                eps += more
            after[(r, n(a["level"]))] = [n(x["seconds"]) for x in eps if n(x["seconds"]) >= 3]
check("interstitials seen across a recording boundary: levels", across, [27])
w19 = {k: v for k, v in after.items() if k[1] >= 19}
inter = {k: v for k, v in w19.items() if k[1] not in x2_taken}   # a full-screen ad I did not choose: an interstitial
check("wins in levels 19-100 / with X2 Coins taken / the others followed by an interstitial",
      (len(w19), sorted(k[1] for k in w19 if k[1] in x2_taken), (sum(1 for v in inter.values() if v), len(inter))),
      (82, [38], (65, 81)))
check("median observed length of the first ad episode after a win (s)", st.median(v[0] for v in inter.values() if v), 15)
gaps = []                                    # (seconds from the end of the previous full-screen ad to the win, interstitial?)
for r, a2 in by.items():
    ends = sorted(n(x["t"]) + n(x["seconds"]) for x in ads_by[r] if n(x["seconds"]) >= 3)
    for a in a2:
        k = (r, n(a["level"]))
        prev = [e for e in ends if e <= n(a["end_t"])]
        if a["result"] == "win" and k in inter and prev:
            gaps.append((n(a["end_t"]) - prev[-1], bool(inter[k])))
check("wins with the previous full-screen ad seen in the same recording", len(gaps), 75)
check("interstitial after the win, by time from the end of the previous full-screen ad to the win screen: under 60 s / 60 s or more",
      ([sum(ad for g, ad in gaps if g < 60), sum(1 for g, ad in gaps if g < 60)],
       [sum(ad for g, ad in gaps if g >= 60), sum(1 for g, ad in gaps if g >= 60)]), ([0, 10], [60, 65]))
check("shortest gap followed by an interstitial / longest gap under 60 s (s)",
      (min(g for g, ad in gaps if ad), max(g for g, ad in gaps if g < 60)), (60, 56))

# Coins (D1-D4): each level-start balance against the previous one, +40 per win and -900 per continue
steps, carry, prev_end = [], [], None
for r in sorted(by):
    exp = None
    for a in by[r]:
        if a["coins_start"]:
            got = n(a["coins_start"])
            if exp is None and prev_end is not None:
                carry.append(got - prev_end)
            elif exp is not None and abs(got - exp) >= 10:
                steps.append(got - exp)
            exp = got
        if exp is not None:
            exp += (40 if a["result"] == "win" else 0) - 900 * (n(a["continues"]) or 0)
    prev_end = exp
level_rewards, spent = 40 * len(wins), 900 * sum(n(a["continues"]) or 0 for a in att)
income = level_rewards + sum(steps)
check("starting balance", n(by[sorted(by)[0]][0]["coins_start"]), 400)
check("largest balance gap between two recordings (coins)", max(abs(c) for c in carry), 0)
check("other coin steps: count / sum / X2 Coins bonuses of +40 among them", (len(steps), sum(steps), steps.count(40)), (11, 2380, 2))
check("balance after level 100: 400 + level rewards + other steps - continues", 400 + income - spent, 2280)
check("computed balance after level 100 (the screen shows 2.28k)", prev_end, 2280)
check("D1 coins per level: level rewards / other steps", (level_rewards / 100, round(sum(steps) / 100, 1)), (40.0, 23.8))
check("D2 share of coin income from other steps (%)", round(100 * sum(steps) / income), 37)
check("D3 first continue price in average level rewards", round(900 / (level_rewards / len(wins)), 1), 22.5)
check("D4 coins spent on continues as a share of coin income (%)", round(100 * spent / income), 71)

# Difficulty labels (F1)
lab = {n(x["level"]): x["label"] for x in lev if x["label"]}
check("levels with a difficulty label", len(lab), 17)
check("VERY HARD / HARD levels", (sorted(lv for lv, x in lab.items() if x == "VERY HARD"),
                                  sorted(lv for lv, x in lab.items() if x == "HARD")),
      (list(range(19, 100, 10)), list(range(24, 100, 10))))
check("time-outs on labeled levels", [(n(o["level"]), lab[n(o["level"])]) for o in off if n(o["level"]) in lab],
      [(59, "VERY HARD"), (94, "HARD")])

bad = 0
for name, got, expected in checks:
    ok = got == expected
    bad += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {got}" + ("" if ok else f"   expected {expected}"))
if bad:
    print(f"{bad} of {len(checks)} data checks failed")
    sys.exit(1)
print(f"{len(checks)} data checks passed")
