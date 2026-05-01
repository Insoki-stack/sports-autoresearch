# Sports Autoresearch - Autonomous Betting Research

This is an autonomous sports betting research system where Cascade (Windsurf AI) experiments with ML models to find betting edges for MLB, NBA, Golf, and Tennis.

## Setup

To set up a new experiment, work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date (e.g. `may1`). The branch `autoresearch/<tag>` must not already exist.
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from current master.
3. **Read the in-scope files**: Read these files for full context:
   - `README.md` — repository context.
   - `prepare.py` — fixed constants, data prep, evaluation. **DO NOT MODIFY**.
   - `train.py` — the file you modify. ML models, features, hyperparameters.
4. **Verify data exists**: Check that `~/.cache/sports-autoresearch/` contains historical data and odds for your target sports. If not, tell the human to download and place data there.
5. **Initialize results.tsv**: Create `results.tsv` with header row. Baseline will be recorded after first run.
6. **Confirm and go**: Confirm setup looks good.

Once confirmed, kick off experimentation.

## Experimentation

Each experiment runs for a **fixed time budget of 5 minutes** per sport (configurable in `prepare.py`). You launch it as: `python train.py`.

**What you CAN do:**
- Modify `train.py` — this is the only file you edit. Everything is fair game: model architecture (XGBoost parameters, try other models), features, hyperparameters, training logic.

**What you CANNOT do:**
- Modify `prepare.py`. It is read-only. Contains evaluation harness, data loading, and fixed constants.
- Install new packages beyond what's in `pyproject.toml`.
- Modify the evaluation functions in `prepare.py`.

**The goal is simple: maximize the edge vs Vegas.** Higher positive edge means the model finds betting opportunities the market is mispricing.

**Simplicity criterion**: All else being equal, simpler is better. A complex feature engineering pipeline for a 0.1% edge improvement? Probably not worth it. Removing features and getting equal or better results? Definitely keep.

**The first run**: Always run the training script as-is to establish baseline.

## Output Format

The script prints metrics like:

```
---
sport:              mlb
accuracy:           0.550000
avg_edge_vs_vegas:  0.023400
positive_edge_rate: 0.450000
---
```

Key metrics:
- **accuracy**: Prediction accuracy on validation set
- **avg_edge_vs_vegas**: Average difference between model probability and implied Vegas probability (higher is better)
- **positive_edge_rate**: Percentage of predictions where model has positive edge

## Logging Results

When an experiment is done, log it to `results.tsv` (tab-separated).

The TSV has a header row and 5 columns:

```
commit	sport	accuracy	avg_edge	status	description
```

1. git commit hash (short, 7 chars)
2. sport (mlb, nba, golf, tennis)
3. accuracy achieved (e.g. 0.550000)
4. avg edge vs Vegas (e.g. 0.023400)
5. status: `keep`, `discard`, or `crash`
6. short description of what this experiment tried

Example:

```
commit	sport	accuracy	avg_edge	status	description
a1b2c3d	mlb	0.550000	0.023400	keep	baseline
b2c3d4e	mlb	0.555000	0.028000	keep	increase n_estimators to 200
c3d4e5f	nba	0.540000	0.015000	discard	switch to deeper max_depth
d4e5f6g	mlb	0.000000	0.000000	crash	invalid feature column
```

## The Experiment Loop

LOOP FOREVER:

1. Look at git state: current branch/commit
2. Tune `train.py` with an experimental idea by hacking the code
3. git commit
4. Run the experiment: `python train.py > run.log 2>&1`
5. Read out the results from the log
6. If run crashed, read the error and attempt fix. If can't fix after a few attempts, skip and log "crash"
7. Record results in `results.tsv` (do not commit results.tsv)
8. If avg_edge_vs_vegas improved (higher), advance the branch (keep commit)
9. If edge is equal or worse, git reset back to where you started

The idea: you're an autonomous researcher trying things. If they work, keep. If not, discard. Advance the branch to iterate.

**Timeout**: Each sport experiment should take ~5 minutes. If a run exceeds 10 minutes, kill and treat as failure.

**Crashes**: If crash due to dumb bug (typo, missing import), fix and re-run. If idea is fundamentally broken, skip, log "crash", move on.

**NEVER STOP**: Once the loop begins, do NOT pause to ask human if you should continue. Do NOT ask "should I keep going?". The human might be asleep. You are autonomous. If you run out of ideas, think harder — read sports betting research, re-read files for new angles, try combining previous near-misses, try radical architectural changes. Loop until human interrupts.

Example use case: user leaves you running while they sleep. Each experiment ~5 minutes × 4 sports = 20 minutes per full cycle. In 8 hours, you can run ~24 cycles of experiments.

## Sports-Specific Notes

**MLB**: Focus on pitcher stats (ERA, WHIP, K rate), team hitting trends, home/away splits, recent performance (last 5-10 games).

**NBA**: Focus on player matchups, rest days, injury reports, home/away performance, recent form, pace of play.

**Golf**: Focus on course fit (strokes gained categories), recent form, weather conditions, player history on specific course types.

**Tennis**: Focus on surface preferences (clay/grass/hard), head-to-head records, recent form, injury status, playing style matchups.

Remember: The goal is to find edges where the model disagrees with Vegas odds, not just maximize accuracy.
