#!/usr/bin/env python3
"""Turn the 1-fps OCR of Color Block Jam recordings into attempt, offer and ad tables.

Usage: python3 -I analysis/parse_cbj.py            (reads data/ocr/*.jsonl, writes data/*.csv)

Screens are recognised by their fixed English UI text, checked on video frames on 23 Nov 2026:
  gameplay      "Level" label top-left, level number under it, timer top-centre, coins top-right
  complete      "LEVEL COMPLETE", "X2 Coins 80" (rewarded video) and "Continue 40"
  fail_offer    "Out of Time!", "+20 Get 20 seconds to keep playing!", "Continue 900"
  fail_warn     "Out of Time!", "You will lose ..." (event progress at stake), "Continue 900"
  fail_lucky    "Out of Time!", "Lucky you! Grab +45s and 3 bonus rockets", 30 s timer, "Continue 900"
  failed        "Level Failed!", "Retry"
  prelevel      "Select Boosters:" before a level starts
  home          "Level N" button, "Daily", "FREE"
Anything without game UI is an ad or another app. Ad creatives are never parsed for meaning.

A frame with an ad badge or call to action above the banner strip ("Play Now", "Open Store", "GET",
"Install", ...) is an ad frame even when the creative also shows game-like words. "GET" counts only in
capitals or as a "Get" / "Get App" button, because the game's own text says "Get consecutive wins".
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = ROOT / "data" / "ocr"
UI_WORDS = ("Out of Time", "COMPLETE", "Failed!", "Select Boosters", "SETTINGS", "Shop", "Daily", "DAILY",
            "BOOSTER", "UNLOCKED", "WELL", "Captain Stu", "CLOUD", "Cloud Rise", "Collection", "BLOCK", "PASS",
            "Stage", "Are you sure", "Retry", "Legal Terms", "Support", "Funfair", "HEIST", "Star Dash", "Gem Rush",
            "Bundles", "Coins", "Continue", "Start", "Play", "CLAIM", "Claim", "Open", "Home", "Lv.")
AD_MARK = re.compile(r"^(AD|Ad)$|Ads served by|Sponsored|\bINSTALL\b|Install|Learn More|Open Store|Play Now|"
                     r"Play now|(?-i:\bGET\b)|^Get( [AaАа]pp)?$|Shop Now|Kurmak|Şimdi yükle|Hemen [İI]ndirin|App Store|#reklam", re.I)


def num_coins(s):
    s = s.replace(",", ".").replace(" ", "").rstrip("+")
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([kK]?)", s)
    if not m:
        return None
    v = float(m.group(1)) * (1000 if m.group(2) else 1)
    return int(round(v))


def x2(text):
    """Rewarded-video button on the complete screen: "X2 Coins 80" (OCR sometimes reads "Coin3" or only "80")."""
    return bool(re.search(r"X2 Coin|(^|\| )80( G)? \| \w?ontin", text))


def frame_info(r):
    ls = [l for l in r["lines"] if l["c"] > 0.35]
    up = [l for l in ls if l["y"] < 0.86]
    text = " | ".join(l["s"] for l in up)
    info = {"t": r["t"], "text": text}
    info["hud"] = any(l["s"].startswith(("Level", "Leve")) and l["x"] < 0.32 and l["y"] < 0.17 for l in ls)
    lv = [l["s"] for l in ls if re.fullmatch(r"\d{1,3}", l["s"]) and l["x"] < 0.32 and 0.09 < l["y"] < 0.18]
    info["level"] = int(lv[0]) if lv and info["hud"] else None
    tm = [l["s"].replace("O", "0") for l in ls if re.fullmatch(r"[0O]\d:\d\d", l["s"]) and 0.35 < l["x"] < 0.7
          and l["y"] < 0.18]
    info["timer"] = int(tm[0][:2]) * 60 + int(tm[0][3:]) if tm else None
    coins = [num_coins(l["s"]) for l in ls if l["x"] > 0.65 and l["y"] < 0.26]
    info["coins"] = next((c for c in coins if c is not None and c < 100000), None)
    # Banner ads sit at the very bottom (title y~0.93, "AD" badge y~0.95); booster labels "Lv.N" sit at y~0.89.
    info["banner"] = any(l["y"] > 0.905 and not re.fullmatch(r"(Lv\.\d+|LV\.\d+|Home|Shop|Hold to see the board)",
                                                             l["s"].strip()) for l in ls)
    # Interstitials carry their badge or call to action above the banner strip; a banner alone does not count.
    info["ad_mark"] = any(AD_MARK.search(l["s"].strip()) for l in ls if l["y"] < 0.88)
    has = lambda s: s in text
    if has("Out of Time"):
        info["screen"] = ("fail_lucky" if ("Lucky" in text or "extra time" in text or "+45" in text)
                          else "fail_warn" if "You will lose" in text else "fail_offer")
        info["cards"] = sorted({c for c in ("Fail Offer", "Golden Ticket", "Coin Madness") if c in text})
    elif has("Failed!"):
        info["screen"] = "failed"
    elif re.search(r"COMP[A-ZĘ]{2,4}E\b", text) or has("X2 Coins"):
        info["screen"] = "complete"
    elif has("Are you sure"):
        info["screen"] = "quit"
    elif has("Select Boosters"):
        info["screen"] = "prelevel"
    elif info["hud"] and (info["timer"] is not None or info["level"] is not None):
        info["screen"] = "gameplay"
    elif re.search(r"(^|\| )Level \d{1,3}( \||$)", text) and ("Daily" in text or "FREE" in text or "Home" in text):
        info["screen"] = "home"
    elif info["ad_mark"]:
        # an ad's badge or call to action outranks game-like words in its creative ("Play", "Coins", "Open")
        info["screen"] = "ad_or_other"
    elif any(w in text for w in UI_WORDS):
        info["screen"] = "menu"
    elif any(AD_MARK.search(l["s"].strip()) for l in ls) or len(up) >= 2:
        info["screen"] = "ad_or_other"
    else:
        info["screen"] = "blank"
    return info


def parse(path):
    frames = [frame_info(json.loads(l)) for l in open(path)]
    rec = path.stem
    attempts, offers, ads = [], [], []
    att = None
    i = 0
    n = len(frames)

    def level_now():
        if att and att["reads"]:
            return max(set(att["reads"]), key=att["reads"].count)
        return attempts[-1]["level"] if attempts else None

    def close(result, t):
        nonlocal att
        if att and att["frames"] < 3 and att["offers"] == 0:
            att = None  # a stray HUD frame between screens, not an attempt
            return
        if att:
            reads = att.pop("reads")
            if reads:  # the most frequent HUD reading wins; single misreads do not split an attempt
                att["level"] = max(set(reads), key=reads.count)
            elif attempts and attempts[-1]["level"]:
                att["level"] = attempts[-1]["level"] + (1 if attempts[-1]["result"] == "win" else 0)
            att.update(result=result, end_t=t)
            attempts.append(att)
            att = None

    while i < n:
        f = frames[i]
        s = f["screen"]
        if s == "gameplay":
            if att is None:
                att = {"recording": rec, "level": None, "start_t": f["t"], "start_timer": None,
                       "coins_start": f["coins"], "offers": 0, "continues": 0, "reads": [], "frames": 0}
            att["frames"] += 1
            if f["level"]:
                att["reads"].append(f["level"])
            if att["start_timer"] is None and f["timer"] is not None:
                att["start_timer"] = f["timer"]
            if att["coins_start"] is None:
                att["coins_start"] = f["coins"]
        elif s in ("home", "prelevel") and att:
            close("left", f["t"])
        elif s.startswith("fail_"):
            # one fail episode = consecutive fail screens (gaps of up to 3 frames allowed)
            j, steps, cards, last = i, [], set(), i
            while j < n and j - last <= 3:
                if frames[j]["screen"].startswith("fail_"):
                    st = frames[j]["screen"]
                    if not steps or steps[-1] != st:
                        steps.append(st)
                    cards |= set(frames[j].get("cards", []))
                    last = j
                j += 1
            # bought = play resumes with time on the clock (or the level is won) before any failed/home screen
            bought, resume, after = False, None, None
            for k in range(last + 1, min(n, last + 12)):
                sk = frames[k]["screen"]
                if sk in ("failed", "home", "prelevel"):
                    break
                if sk == "complete" or (sk == "gameplay" and (frames[k]["timer"] or 0) > 0):
                    bought, resume = True, frames[k]["timer"]
                    after = next((frames[x]["coins"] for x in range(k, min(n, k + 8)) if frames[x]["coins"]), None)
                    break
            bal = next((frames[x]["coins"] for x in range(i, last + 1) if frames[x]["coins"]), None)
            offers.append({"recording": rec, "level": level_now(), "t": f["t"], "steps": ">".join(steps),
                           "cards": "+".join(sorted(cards)), "price": 900, "balance": bal,
                           "decision": "bought" if bought else "declined", "resume_timer": resume,
                           "balance_after": after})
            if att:
                att["offers"] += 1
                att["continues"] += int(bought)
                if not bought:
                    close("fail", f["t"])
            i = last + 1
            continue
        elif s == "failed":
            close("fail", f["t"])
        elif s == "quit":
            pass
        elif s == "complete":
            if att:
                att["x2_offered"] = x2(f["text"])
                att["coins_at_complete"] = f["coins"] or att.get("coins_start")
                close("win", f["t"])
            # skip the rest of the complete screen; the X2 button can animate in a second after "LEVEL COMPLETE"
            while i + 1 < n and frames[i + 1]["screen"] == "complete":
                i += 1
                if attempts and attempts[-1]["result"] == "win" and x2(frames[i]["text"]):
                    attempts[-1]["x2_offered"] = True
        elif s == "ad_or_other":
            j = i
            while j < n and frames[j]["screen"] in ("ad_or_other", "blank"):
                j += 1
            dur = frames[j - 1]["t"] - f["t"] + 1
            prev = next((frames[x]["screen"] for x in range(i - 1, max(-1, i - 6), -1)
                         if frames[x]["screen"] != "blank"), None)
            marked = any(frames[x]["ad_mark"] for x in range(i, j))
            lv = level_now()
            if lv is None:
                # before a recording's first attempt: the level of the win screen the game returns to after the ad
                # (R03 opens on level 27's win screen, the screen R02 ended on)
                lv = next((frames[x]["level"] for x in range(j, min(n, j + 4))
                           if frames[x]["screen"] == "complete" and frames[x]["level"]), None)
            if dur >= 2 and marked:
                ads.append({"recording": rec, "t": f["t"], "seconds": dur, "after_screen": prev,
                            "level": lv, "first_text": next((frames[x]["text"][:60] for x in range(i, j)
                                                                      if frames[x]["text"]), "")})
            i = j
            continue
        i += 1
    close("cut", frames[-1]["t"] if frames else 0)
    # an attempt whose level was never read takes it from the next attempt (one less if it was won)
    for a, b in zip(attempts[::-1][1:], attempts[::-1]):
        if a["level"] is None and b["level"] is not None:
            a["level"] = b["level"] - 1 if a["result"] == "win" else b["level"]
    gameplay = [f for f in frames if f["screen"] == "gameplay"]
    banner_share = (sum(f["banner"] for f in gameplay) / len(gameplay)) if gameplay else None
    return frames, attempts, offers, ads, banner_share


def main():
    all_att, all_off, all_ads = [], [], []
    print(f"{'recording':40} {'levels':>9} {'att':>4} {'win':>4} {'fail':>4} {'offers':>6} {'bought':>6} "
          f"{'ads>=3s':>7} {'banner%':>7}")
    for p in sorted(OCR.glob("*.jsonl")):
        frames, att, off, ads, bshare = parse(p)
        lv = [a["level"] for a in att if a["level"]]
        print(f"{p.stem:40} {(f'{min(lv)}-{max(lv)}' if lv else '-'):>9} {len(att):4} "
              f"{sum(a['result'] == 'win' for a in att):4} {sum(a['result'] == 'fail' for a in att):4} "
              f"{len(off):6} {sum(o['decision'] == 'bought' for o in off):6} {len(ads):7} "
              f"{(f'{100 * bshare:.0f}' if bshare is not None else '-'):>7}")
        all_att += att
        all_off += off
        all_ads += ads
    for name, rows in (("attempts", all_att), ("offers", all_off), ("ads", all_ads)):
        if rows:
            keys = list(dict.fromkeys(k for r in rows for k in r))
            with open(ROOT / "data" / f"{name}.csv", "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=keys)
                w.writeheader()
                w.writerows(rows)
    return all_att, all_off, all_ads


if __name__ == "__main__":
    main()
