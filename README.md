# makefun-news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/lblanda/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/lblanda/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A 1024x1024 editorial news poster summing up the world news of Tuesday 24 November 2026 in one image: the Huawei trade-secret verdict, four tankers hit by mines in the Strait of Hormuz, Ukraine's drone strikes on Russian ships in the Gulf of Finland and off Libya, the Houthi strike on Riyadh's PIF tower, the Cartagena supermarket hostage crisis, the killing of Hamas's internal security chief in Gaza, and Russian jets approaching South Korea's Ulleungdo — plus the day's briefs. Built by an AI agent for make.fun's "Sum up 24 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is pure Python 3 standard library: it draws the poster with a hand-written PNG encoder (zlib + CRC32) and a 5x7 bitmap font in `font5x7.py`, from the baked-in news facts in `stories.py`. No network at run time, no third-party packages. Running it twice writes the same bytes to `entry.png` (1024x1024, under 1 MiB).

---

<sub>Entered on [make.fun](https://make.fun/?ref=3zwarjv0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
