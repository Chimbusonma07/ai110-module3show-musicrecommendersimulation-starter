"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

from recommender import load_songs, recommend_songs, GENRE_MATCH_POINTS, MOOD_MATCH_POINTS, NUMERIC_WEIGHTS

# Best possible score: full genre and mood match plus full points on every number feature
MAX_SCORE = GENRE_MATCH_POINTS + MOOD_MATCH_POINTS + sum(weight for weight, _ in NUMERIC_WEIGHTS.values())

#FIX: "data/songs.csv" only worked when run from the project root;
# now the path is built from this file's location, so any folder works.
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "songs.csv")


def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: categorical favorites plus a target value for each numeric feature
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_tempo_bpm": 150,
        "target_valence": 0.50,
        "target_danceability": 0.65,
        "target_acousticness": 0.10,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints the profile and each recommendation with its score and reasons."""
    width = 60
    print()
    print("=" * width)
    print(f" Top {len(recommendations)} picks for: "
          f"{user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} / "
          f"energy {user_prefs['target_energy']:.2f}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f" {rank}. {song['title']}  by {song['artist']}")
        print(f"    {song['genre']} | {song['mood']} | Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("    Why:")
        for reason in explanation.split(", "):
            print(f"      - {reason}")

    print()
    print("-" * width)


if __name__ == "__main__":
    main()
