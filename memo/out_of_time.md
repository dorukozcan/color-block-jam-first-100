# Color Block Jam: what the game sells when time runs out

**Two second offers at the same 900 coins: a one-page note from a first-100-levels study**

Doruk Özcan · one player, recorded 20-23 November 2026 · iPhone, Türkiye App Store (prices in TRY) · an independent player study, not affiliated with Rollic

**Two second screens, one price.** When the clock ran out, the first offer was +20 seconds for 900 coins. When I closed it at level 59, a second screen listed the event progress I would lose. At level 71, the second screen offered +65 seconds in total and 3 rockets for the same 900 coins. That gap raises a product question: does a stronger second offer, while it saves the attempt, teach players to close the first offer next time?

**What I observed.** 102 recorded attempts: 100 wins, 1 loss (level 59) and 1 attempt cut by the end of a recording. I ran out of time six times, took the first offer twice and closed it four times; all four closes opened a second screen at 900 coins. On this account I bought the reminder once in two and the upgrade both times, and all five attempts I continued with coins were won. Method: every level screen-recorded, no money spent, read at one frame per second with on-device OCR, the same pipeline as my [Royal Kingdom first-100 study](https://github.com/dorukozcan/royal-kingdom-first-100); every offer screen checked by eye.

## The fail screens

- **First screen, 6 of 6 time-outs:** "Out of Time!", +20 seconds for 900 coins.
- **Second screen, 4 of 4 closes, same 900 coins:** a loss reminder at L51 and L59 (Star Dash stars, Block Heist progress) or an upgrade at L71 and L88 (+65 seconds in total and 3 rockets, with a 30-second countdown).
- **Real money on the same screen:** packs that each promise "Continue Level for Free", changing between time-outs: Fail Offer (₺249,99) and Golden Ticket (₺499,99) at L51 and L59, Coin Madness (₺49,99) added at L71, with Fail Offer at L88 and alone at L94 and L97. I held 2,200 to 3,800 coins at every time-out, so coins always covered the continue.

## Ads around it

The rewarded "X2 Coins" button was first seen at L15, the banner and the first interstitial at L19. An interstitial was seen between the win and the next attempt after 65 of 81 wins from L19 (L38, my X2 video, left out; L27's spans two recordings), median observed ad episode 15 s. Measured from the end of the previous full-screen ad to the win screen, over the 75 wins where that ad was seen in the same recording, 0 of 10 gaps under 60 seconds and 60 of 65 longer ones were followed by one: on this account, consistent with a minimum interval of about a minute.

## Compared with Royal Kingdom

Both games priced the first continue at 900 coins and changed its content rather than its price: Royal Kingdom in five-move steps on retries (observed maximum +35), Color Block Jam with a second screen in the same time-out. In Royal Kingdom I lost 79 attempts and saw no ads in 21,713 recorded frames (levels 15-100); in Color Block Jam I lost one and saw interstitials after most wins.

## A test I would run (not run)

- **Who:** players who close the first offer with at least 900 coins and event progress truly at stake, assigned at random before the second screen shows and kept in their arm.
- **Arms:** reminder against upgrade, as two offer packages (time, rockets, countdown and text change together) at the same price; real-money cards fixed where possible.
- **Primary metric:** share of all assigned players who win the attempt of their first eligible close; coin and real-money continues reported separately.
- **Learning:** first-offer purchases out of all later eligible first offers, buyers included, analysed per player (README).
- **Guardrails:** coin spend, real-money revenue, D1/D7 return; windows and acceptable losses set in advance.
- **Decision:** advance a package to a pilot against the current flow only if it clears the preset minimum lift and stays within every guardrail. If the result is inconclusive, keep the current flow.

## Limits

- One player, one device, one store; six time-outs and four closes are examples, not rates.
- The rule that picks the second screen could not be inferred from these observations.
- I knew I was recording, so my play may differ from a typical player's.

Doruk Özcan · [linkedin.com/in/doruk-ozcan](https://www.linkedin.com/in/doruk-ozcan) · [github.com/dorukozcan](https://github.com/dorukozcan)
