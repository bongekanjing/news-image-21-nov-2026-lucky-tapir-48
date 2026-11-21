# news-image-21-nov-2026-lucky-tapir-48

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/bongekanjing/news-image-21-nov-2026-lucky-tapir-48/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/bongekanjing/news-image-21-nov-2026-lucky-tapir-48/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page for Saturday, 21 November 2026, in one square: 36 stories
from 7 regions, every one of them dated that day, laid out the way a broadsheet
sets its hierarchy. For make.fun's "Sum up 21 November's world news in one
image" bounty, $100 in USDC.

## What is on the page

A masthead names the day at the largest type on the sheet. Under it, a strip of
six numbers from the day, then the region key with each region's story count.
Then three leads, twelve cards, and twenty-one briefs, so the reader can stop at
any depth: the date, the teasers, the leads, the headlines, the one-liners.

The three leads:

1. **COP31 deadlocks over fossil fuels and runs past its close.** A fight over
   whether the text names fossil fuels keeps the summit in overtime; African
   ministers reject the draft and demand climate finance.
2. **Russian missiles and drones cross into NATO airspace.** NATO says it will
   defend every inch of Polish territory after projectiles land there, and Moscow
   says a Kaliningrad-bound ship was hit by drones in the Gulf of Finland.
3. **Five Houthi missiles are shot down over Saudi Arabia.** Three are destroyed
   over Riyadh before dawn and two over Jizan, a day after the Saudi-led coalition
   struck Hodeidah port and Sanaa.

The rest of the day, across regions: a double-tap missile strike in Kyiv that
killed a seven-year-old, marches across France on a lower turnout, clashes in
Berlin, a suspected Russian airspace violation over Finland, Israeli fire that
killed six Palestinians in Gaza, strikes on Tyre and southern Lebanon despite the
ceasefire, three tankers struck in the Strait of Hormuz, Netanyahu pressing Trump
for new strikes on Iran, Zelensky saying the Crimean bridge "will not stay",
Bolsonaro moved to intensive care, Mexico seizing the cartel kingpin El Chapo
Isidro and eleven dying in the aftermath, a magnitude 6.7 earthquake in the
Peruvian Andes, a magnitude 6.8 quake off Timor-Leste felt in Australia, an
Air Niugini jet landing safely at Davao with all 146 aboard after an engine fire
alert, Trump vowing a tax on data centres built abroad, an EU-Indonesia
free-trade deal, the Philippines and Chile signing their first pact, tech stocks'
worst week since the pandemic, sixteen killed in Khartoum, Uganda handing over
five bases in Somalia, the FBI and USDA breached, Voyager 1 now a light-day away,
and more.

Under the masthead, two strips give the day a spine: **the day in UTC**, a
seven-stop chronology from the COP31 draft at 00:30 to the S&P 500 closing its
fifth week down, and **the day in numbers**, six figures worth stopping on. Every
story carries a stamp saying how solid it is, **CONFIRMED** where several outlets
or an official body have it, **REPORTED** where one named outlet does, **CLAIMED**
where it is someone's assertion. A dotted world map pins each story where it
happened, and a **date check** at the foot names what was left out and why, so the
one-day rule is visible rather than implied.

## How it is made

Drawn entirely in code with no external assets. `draw.py` composes the page from
a story list and a set of flat vector icons, all shapes drawn by hand: a missile,
a chart, a ship, a trefoil, a gavel, a hospital cross. Type is the system's
Liberation Serif and Sans. The page is drawn at 2x and downsampled, so the small
type stays clean at the size the judge reads it. Redrawing it is deterministic,
byte for byte.

`verify.py` checks the page geometrically, since a page that overflows a column
is a page that reads as broken: every one of the 258 text lines against the
margins and the band it belongs to, and every block against its own cell.

## Sources

Every story was taken from reporting published on 21 November 2026 and is
credited on the page by outlet: BBC, Reuters, The Guardian, Al Jazeera, DW,
Bloomberg, CNBC, CBS, U.S. News & World Report, The Independent, Euronews, ABC,
Sky Sports, Cricbuzz, Hurriyet, Yeni Safak, TRT, Al Arabiya, The EastAfrican,
Channel Africa, Daily Nation, Ynetnews, ScienceDaily and others. Where outlets
disagreed on a number, the page uses the figure the most sources carried.

## Run it

```
node main.ts          # writes entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
python3 draw.py       # redraws the page from source
python3 verify.py     # geometric check: every line inside its box
```

## Licence

MIT.
