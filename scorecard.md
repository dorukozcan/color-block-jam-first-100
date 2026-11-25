# First-100-levels scorecard: Royal Kingdom and Color Block Jam (24 November 2026)

Same metric ids and definitions as the Royal Kingdom study's [PROTOCOL.md](https://github.com/dorukozcan/royal-kingdom-first-100/blob/main/PROTOCOL.md); the Royal Kingdom column is summarised from its [scorecard.md](https://github.com/dorukozcan/royal-kingdom-first-100/blob/main/scorecard.md).
Color Block Jam sources: "table" = computed from the tables in `data/` and checked by `analysis/check_note_numbers.py`; "observed" = read on the video frame, with its scope.
Color Block Jam levels are timed: a "time-out" is the moment the clock hits zero; an attempt is lost only when it ends without a win.

| Id | Metric | Royal Kingdom | Color Block Jam | CBJ source |
|---|---|---|---|---|
| A1 | Game | Royal Kingdom | Color Block Jam | observed |
| A2 | Platform and store | iOS, Türkiye store | iOS, Türkiye store | observed |
| A3 | Played | 2026-11-04 to 2026-11-11 | 2026-11-20 to 2026-11-23 (9 recordings) | observed |
| A4 | Levels covered | 1-100 | 1-100, every level on recording | table |
| A5 | Attempts / failed attempts | 179 / 79 | 101 / 1, plus 1 attempt cut by the end of a recording (L79) | table |
| A6 | Real money spent | 0 | 0 | observed (no purchase made) |
| B1 | First level with a fail | 9 | 59; first time-out at 51, rescued with a coin continue | table |
| B2 | First level with 3 or more fails | 12 | none | table |
| B3_1 | Levels 1-25: fails per level / first-try wins | 0.56 / 15 of 25 | 0.00 / 25 of 25 | table |
| B3_26 | Levels 26-50: fails per level / first-try wins | 0.16 / 23 of 25 | 0.00 / 25 of 25 | table |
| B3_51 | Levels 51-75: fails per level / first-try wins | 1.24 / 17 of 25 | 0.04 / 24 of 25 | table |
| B3_76 | Levels 76-100: fails per level / first-try wins | 1.20 / 13 of 25 | 0.00 / 24 of 25 (L79 unknown: first attempt cut) | table |
| B4 | Most attempts on one level | 11 (level 57) | 2 (level 59) | table |
| B5 | Levels that took 5 or more attempts | 7 | 0 | table |
| B6 | Levels on which lives ran out | 8 | none seen; an infinite-lives timer was running at L71, L88, L94 and L97 (source not identified) | observed |
| C1 | First continue offer | +5 moves for 900 coins | +20 seconds for 900 coins (the first screen at all 6 time-outs) | observed |
| C2 | How the offer changes | first offer of each attempt grew in five-move steps on retries, reaching an observed maximum of +35; price 900 | within a time-out: closing the first screen opens a second one at the same 900 coins, either a loss reminder (L51, L59) or an upgrade to +65 s in total (+20 and +45 shown) and 3 rockets with a 30-second countdown (L71, L88). No time-out on a retry, so growth across attempts is unknown | observed |
| C3 | Extras | 2 Electro Balls from the second step | 3 rockets on the upgraded second screen (2 of 2) | observed |
| C4 | Second continue in the same attempt | 1,900 coins for +5 moves and 1 Rocket, seen once | none seen (no attempt timed out twice) | observed |
| C5 | What the offer reacts to | no change seen with distance to goal, balance or streak | first screen identical at all 6 time-outs; rule for which second screen appears not established (reminders at L51 and L59, upgrades at L71 and L88) | observed |
| C6 | When the balance is short | the button opens the shop; cheapest pack 1,000 coins for TRY 99.99 | not seen (balance 2,200 to 3,800 at every time-out) | observed |
| C7 | Friction on declining | with a streak or event at stake, a loss screen before the second tap (23 of 23) | closing the first screen opened a second screen 4 of 4 times; declining the second ended the attempt (L59: Level Failed, Retry) | observed |
| C8 | Ad-funded continue | none seen in 82 logged offers | none at 6 time-outs; rewarded video sits on the win screen instead (X2 Coins) | observed |
| C9 | Logged offer screens / continues bought | 82 / 9 | 10 screens at 6 time-outs (6 first, 4 second) / 5 | table |
| C10 | Offers the balance covered: bought | 7 of 19 offer screens | 5 of 10 offer screens (5 of 6 time-outs) | table |
| C11 | Offers the balance did not cover: bought | 0 of 59 | none (0 of 0) | table |
| C12 | Median seconds to decide: bought / declined | 2 / 3, per offer screen | 8 / 18 per time-out flow, from the first to the last offer frame read by OCR, which can span two screens (n = 5 / 1; bought in 13, 9, 8, 4, 2 s, in level order) | table |
| C13 | Near-miss offers | 9 of 73 | not measured: remaining blocks at time-out were not logged | n/a |
| D1 | Coin income per level: level rewards / non-level coin rewards | 36.2 / 38.4 (levels 15-100) | 40.0 / 23.8 (levels 1-100; the 23.8 is 2,380 coins from 11 balance steps: 80 from the X2 Coins bonus at L17 and L38, 2,300 not yet matched to rewards on the frames) | table |
| D2 | Share of coin income from non-level coin rewards | 51% | 37% (derived estimate from balance changes: 2,380 coins, 80 of them the X2 Coins bonus, 2,300 not yet matched to rewards on the frames) | table |
| D3 | First continue price in average level rewards | 24.8 | 22.5 | table |
| D4 | Coins spent on continues as a share of coin income | 98% (levels 15-100) | 71% (levels 1-100), a derived estimate: income includes the 2,380 coins read from balance steps | table |
| D5 | First real-money offer | level 13: starter pack, TRY 49.99 | Block Pass with a paid Golden Ticket track, introduced at L36; first priced offer shown unprompted at the first time-out (L51): Fail Offer TRY 249.99, Golden Ticket TRY 499.99; Coin Madness TRY 49.99 (90% off) at an app launch before L67 | observed |
| D6 | Lives | 5 lives, 30 minutes each; refill 900 coins | 5 lives on the home screen at the L50 checkpoint; refill price not seen; Golden Ticket raises the limit to 8 | observed |
| E1 | Win-streak feature | Magic Pots from level 32, 5 stages | Cloud Rise from L66: "Beat levels without failing", 3 stages, up to 3,000 coins | observed |
| E2-E5 | Streak metrics | derived | not computed yet (needs Cloud Rise stage reads per level) | n/a |
| F1 | Special levels | every 5th level Kingdom or Dark Kingdom; x4 hard, x9 super hard | from L19, levels ending in 9 are VERY HARD and levels ending in 4 are HARD (17 labeled levels); 2 of the 6 time-outs were on labeled levels (L59, L94) | table |
| F2 | Levels that introduce a new item | 1, 4, 7, 11, 16, 21, 31, 41, 51, 61, 71, 81, 91 | Ice Door after L5, Ice Block after L9; later introductions not yet itemized | observed (partial) |
| F3 | In-level boosters first usable on levels | 8, 12, 17, 23, 28 | 6 (Freeze Timer), 8 (Rocket), 12 (Hammer), 16 (Color Vacuum) | observed |

## Checks behind the Color Block Jam column

- **Coin ledger closes:** start 400 + level rewards 4,000 (100 wins x 40) + 11 other steps 2,380 (80 from the X2 Coins bonus at L17 and L38, 2,300 not yet matched to rewards on the frames) - 5 continues 4,500 = 2,280, the balance on screen after level 100. No step falls between two recordings.
- **Purchases match balance drops:** every continue is a 900-coin drop at the time-out (L51, L71, L88, L94, L97).
- **Ads:** the banner starts during L19 and shows on 98.3% of the L20-L100 frames read as gameplay. An interstitial, a full-screen ad seen between a win and the next attempt that I did not choose, follows 65 of 81 wins from L19 (L38 left out, where I took X2 Coins; L27's spans R02 and R03). Median observed ad episode: 15 s, episodes of 3 s or more. From the end of the previous full-screen ad to the win screen, over the 75 wins where that ad was seen in the same recording: 0 of 10 gaps under 60 s and 60 of 65 longer ones were followed by an interstitial. X2 Coins appears from the L15 win screen, on 84 of 86 win screens (2 unreadable); I took it at L17 and L38.
- **Open items:** itemize the 9 other coin steps by frame; Cloud Rise stage reads (E2-E5); new-item introductions after L9 (F2); the statistics screen was not recorded. Game version 13.1.5 and tracking (App Tracking Transparency) on, both read in the iPhone's settings on 25 Nov, two days after the last recording.
