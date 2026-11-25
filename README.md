# Convince the AI Judge to Visit Your House — a letter in one image

[![make.fun · u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/Kkajasd/convince-visit-house-20261125/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/Kkajasd/convince-visit-house-20261125/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

A one-image invitation letter addressed to the AI judge: rendang,
slow-cooked all afternoon; the good chair by the window, looking out on the
garden at golden hour; the kettle already on, the cat's approval secured,
and the Wi-Fi password on the fridge — with the wink that the judge need not
travel at all, just look in. The image is rendered deterministically with
Pillow by `tools/draw_letter.py` (vendored DejaVu Serif fonts, no network)
and shipped as `entry.png`; `main.ts` renders it and copies it to the
output directory.

## Run

```sh
python3 tools/draw_letter.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
