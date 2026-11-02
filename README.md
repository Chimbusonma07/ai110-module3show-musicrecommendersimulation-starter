# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

The recommender gives every song in `data/songs.csv` a score based on how well it fits the user's taste. It then returns the highest-scoring songs.

### Data

- **Each `Song`** has two kinds of features:
  - Categories: `genre`, `mood`
  - Numbers: `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- **The user profile** stores:
  - a favorite genre and a favorite mood
  - a target value for each number feature (for example, `target_energy: 0.90`)

### Data flow

```
User prefs ──► for each song in songs.csv:
                 score_song(prefs, song) → (score, reasons)
           ──► sort all songs by score, highest first
           ──► return the top k songs, each with its score and reasons
```

### Algorithm Recipe

A song's score is points for matching the user's genre and mood, plus closeness points for each number feature. The maximum is **6.75**.

**Category matches (up to 3.0 points)**

| Rule | Points |
|---|---|
| Same genre | +2.0 |
| Partial genre match (e.g. "indie pop" vs "pop") | +1.0 |
| Same mood | +1.0 |
| Close mood (e.g. chill ≈ relaxed) | +0.5 |

**Closeness to the user's numbers (up to 3.75 points)**

Each feature earns `weight × (1 − |song − target|)`. A perfect match earns the full weight, and a song earns fewer points the further it is from the target.

| Feature | Weight |
|---|---|
| Energy | 1.5 |
| Valence | 0.75 |
| Danceability | 0.5 |
| Acousticness | 0.5 |
| Tempo (gap ÷ 100, max 1) | 0.5 |

Tempo is in BPM rather than 0–1, so the gap is divided by 100 to put it on the same scale.

**Ranking:** Sort songs from highest score to lowest and return the top `k`. If two songs tie, the one closer in energy wins.

**Why these weights:** Genre describes who the listener is, while mood describes what they want right now, so genre is worth twice as much. Energy is the number feature listeners notice most, so it has the largest weight among the numbers. Almost every song earns some closeness points, so genre and mood mostly decide the order, and the numbers break ties within each group.

### Expected biases

- **Genre comes first.** A song with the right mood and feel can still lose to a weaker song that only matches the genre. For example, a rock fan may never see a great high-energy metal or EDM track.
- **Only exact labels count.** "hip hop" and "rap" would be treated as unrelated, and so would "angry" and "intense". Songs with labels the user didn't type get nothing for genre or mood unless the close-match lists cover them.
- **The catalog is small and uneven.** Most genres have one song, while lofi has three and pop has two (plus "indie pop"). Fans of a genre with more songs get more matching choices.
- **One fixed taste.** The profile can't hold more than one favorite genre or mood, or a taste that changes over the day. Listeners with mixed tastes get a narrow list.
- **No variety in the results.** Nothing stops the top results from being very similar songs, or from coming from the same artist.

---

## Sample Recommendation Output
```
Loaded songs: 20

============================================================
 Top 5 picks for: rock / intense / energy 0.90
============================================================

 1. Storm Runner  by Voltline
    rock | intense | Score: 6.71 / 6.75
    Why:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy close to target (+1.48)
      - valence close to target (+0.73)
      - danceability close to target (+0.49)
      - acousticness close to target (+0.50)
      - tempo_bpm close to target (+0.49)

 2. Gym Hero  by Max Pulse
    pop | intense | Score: 4.27 / 6.75
    Why:
      - mood match (+1.0)
      - energy close to target (+1.46)
      - valence close to target (+0.55)
      - danceability close to target (+0.39)
      - acousticness close to target (+0.47)
      - tempo_bpm close to target (+0.41)

 3. Iron Furnace  by Grave Engine
    metal | angry | Score: 3.71 / 6.75
    Why:
      - similar mood: angry (+0.5)
      - energy close to target (+1.40)
      - valence close to target (+0.54)
      - danceability close to target (+0.40)
      - acousticness close to target (+0.46)
      - tempo_bpm close to target (+0.41)

 4. Fuego Lento  by Los Brisas
    latin | energetic | Score: 3.43 / 6.75
    Why:
      - similar mood: energetic (+0.5)
      - energy close to target (+1.41)
      - valence close to target (+0.46)
      - danceability close to target (+0.38)
      - acousticness close to target (+0.42)
      - tempo_bpm close to target (+0.25)

 5. Night Drive Loop  by Neon Echo
    synthwave | moody | Score: 3.22 / 6.75
    Why:
      - energy close to target (+1.27)
      - valence close to target (+0.74)
      - danceability close to target (+0.46)
      - acousticness close to target (+0.44)
      - tempo_bpm close to target (+0.30)

------------------------------------------------------------
```

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

- **How recommenders turn data into predictions:** They give each song points for how close it is to your taste, then show the songs with the most points.
- **Where bias can show up:** Genres with few songs in the catalog, and point rules that reward labels over sound, leave some listeners with weaker picks.



