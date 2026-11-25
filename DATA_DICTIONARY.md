# Data dictionary

One player's first 100 levels of Color Block Jam (iPhone, Türkiye App Store, 20 to 23 November 2026, no money spent). Every level was screen-recorded, and the recordings were read at one frame per second with on-device text recognition, so `t` and the `*_t` columns are seconds from the start of a recording. Blank cells mean "not read", never zero.

The tables are the output of `analysis/parse_cbj.py` with three changes for publication: recording file names, which are timestamps, became R01 to R09; the recognised text of ad screens was removed; and `analysis/derive_cbj.py` added the columns marked "derived".

## How each value was obtained

| Label | Meaning |
|---|---|
| parsed | Found by `parse_cbj.py` from the game's fixed English screen text. Unmarked columns are parsed |
| derived | Computed by `derive_cbj.py` from the same frames |
| checked | Parsed, then checked by eye on the video frame. Every time-out and offer screen was checked |

## `data/attempts.csv`: one row per attempt (102)

| Column | Meaning |
|---|---|
| `recording` | R01 to R09, in time order |
| `level` | Level number |
| `start_t`, `end_t` | The attempt's first gameplay frame, and the frame that ended it: a win screen, a fail screen without a continue, the home screen, or the end of the recording |
| `start_timer` | Level clock at the first gameplay frame, in seconds (300 is 5:00) |
| `coins_start` | Coin balance at the first gameplay frame. Above 1,000 the game shows it as, for example, 2.28k, so it is exact to 10 coins |
| `offers`, `continues` | Time-outs in the attempt, and continues bought at 900 coins each. Checked |
| `gameplay_frames` | Frames recognised as gameplay between `start_t` and `end_t`. Derived |
| `banner_frames` | Those of them with a banner ad at the bottom of the screen. Derived |
| `x2_offered` | `True` if the win screen showed the rewarded "X2 Coins" button. `False` on levels 1-14: there was no button. `False` on levels 29 and 73: the button could not be read. Blank for attempts that did not end in a win |
| `coins_at_complete` | Balance on the win screen |
| `result` | `win`, `fail` (ended without a win) or `cut` (the recording ended during the attempt) |

## `data/offers.csv`: one row per time-out (6)

| Column | Meaning |
|---|---|
| `recording`, `level` | As above |
| `t` | First frame of the "Out of Time!" screen |
| `steps` | The screens shown, in order. `fail_offer`: +20 seconds for 900 coins. `fail_warn`: a second screen at the same price that lists the event progress you will lose. `fail_lucky`: a second screen at the same price that offers +65 seconds in total (it shows +20 and +45) and 3 rockets, with a 30-second countdown. Checked |
| `cards` | Real-money packs on the fail screens: Fail Offer, Golden Ticket, Coin Madness. Checked |
| `price` | Coin price of the continue, read on the screen: 900 at every time-out. Checked |
| `balance` | Coin balance on the fail screen |
| `decision` | `bought` (play resumed with time on the clock) or `declined` (the level was failed). Checked |
| `decide_seconds` | Seconds from the first fail screen to the last one, both frames included: the whole time-out flow, which can span two screens. Royal Kingdom's figure is per offer screen. Derived |
| `resume_timer` | Level clock on the first gameplay frame read after a continue. The clock may still be counting up there (38 at level 71, where the game showed +65 and the clock reached 1:04 a second later), so it is not the time granted |
| `balance_after` | Balance after the continue, where it could be read |

## `data/ads.csv`: one row per full-screen ad episode the parser found (67)

| Column | Meaning |
|---|---|
| `recording` | As above |
| `t`, `seconds` | First frame of the episode, and its length. An episode is a run of frames without game screens that carries an ad badge or a call to action, 2 seconds or longer; every episode found lasted 6 seconds or more. A frame with a badge or call to action counts as an ad frame even when the ad also shows game-like words |
| `after_screen` | The last game screen before it: `complete` (the win screen) or `menu` (another game screen). Blank if none was read |
| `level` | The level just played. For the episode that opens R03, 27: R02 ends on the level 27 win screen, and R03 opens with the iOS Control Center (read as `menu`), then this ad, then the same win screen, then level 28 |

An interstitial is a full-screen ad seen between a win and the next attempt that I did not choose. That covers every episode after a win except after levels 17 and 38, where I tapped X2 Coins and the ad was the rewarded video I chose; the balances show which, because after an X2 win the next level starts 80 coins higher, not 40. `seconds` is the observed length of the episode, which can include an end card or the App Store page. The note and the scorecard count episodes of 3 seconds or more.

## `data/levels.csv`: one row per level (100)

| Column | Meaning |
|---|---|
| `level` | 1 to 100 |
| `label` | Difficulty label the game showed for the level, on the home screen or before the level: `HARD`, `VERY HARD`, or blank. Derived |

## `data/recordings.csv`: one row per recording (9)

| Column | Meaning |
|---|---|
| `recording` | R01 to R09 |
| `day` | Day of the recording, local time |
| `minutes` | Length, from the number of frames read at one per second |
| `first_level`, `last_level` | Levels played in it. Blank for R04, a 49-second check of the home screen and the shop before level 50 |
