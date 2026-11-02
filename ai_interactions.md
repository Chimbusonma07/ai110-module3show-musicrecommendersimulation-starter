# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code to add at least 5 new song attributes to the dataset and make the scoring use them.

**Prompts used:**

> Add Advanced Song Features. Introduce 5 or more complex attributes to your dataset that are not currently present in the baseline data, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags (e.g., "nostalgic," "aggressive," "euphoric"). Update both `data/songs.csv` and the scoring logic in `src/recommender.py` so scoring accounts for the new attributes.

**What did the agent generate or change?**

- **`data/songs.csv`:** added 5 columns to all 20 songs:
  - `popularity` (0–100)
  - `release_decade` (1960–2020)
  - `mood_tags` (2–3 detailed tags, like `nostalgic;warm;carefree`)
  - `instrumentalness` (0–1)
  - `explicit` (true/false)
- **`src/recommender.py`:**
  - `load_songs` now converts the new columns: numbers, a list of tags, and a true/false flag.
  - Popularity, decade and instrumentalness use the same "closer to target = more points" rule as energy, worth up to 0.5 each.
  - Mood tags earn 0.25 points per shared tag, capped at 0.75 so tags can't outweigh genre.
  - Explicit songs lose points, but only if the user sets `allow_explicit: False`.
  - `Song` got the new fields with default values, so the existing tests still build songs the old way.
- **`src/main.py`:** added 3 profiles that use the new features (Clean Workout Pop, Nostalgic Deep Cuts, Instrumental Focus). The max score now includes tag points (6.75 → 9.00).
- **Commands run:** `python src/main.py` and `python -m pytest`.

**What did you verify or fix manually?**

- **Caught a weak penalty.** In the first version, the explicit penalty was only −1.0. Running "Clean Workout Pop" showed the explicit song Gym Hero still at #1, because its genre and mood labels earn 3 points. The penalty was raised to −3.0, and Gym Hero dropped to #4.
- **Checked the old results didn't change.** Old profiles don't set the new targets, so their scores stayed the same (High-Energy Pop is still 6.61). Only the max shown went from 6.75 to 9.00.
- **Checked the new features do something.** Nostalgic Deep Cuts pulled up older, less popular songs (the 1980s synthwave song moved to #2). Instrumental Focus ranked the most wordless lofi track (Focus Flow) first.
- **Tests:** both tests in `tests/test_recommender.py` still pass.
- **Still to do:** the tag values in the CSV are made up by hand, so they reflect one person's opinion of each song.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
