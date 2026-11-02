"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

from recommender import (load_songs, recommend_songs, GENRE_MATCH_POINTS, MOOD_MATCH_POINTS,
                         MAX_TAG_POINTS, NUMERIC_WEIGHTS)

# Best possible score: full genre, mood and tag match plus full points on every number feature
MAX_SCORE = (GENRE_MATCH_POINTS + MOOD_MATCH_POINTS + MAX_TAG_POINTS
             + sum(weight for weight, _ in NUMERIC_WEIGHTS.values()))

#FIX: "data/songs.csv" only worked when run from the project root;
# now the path is built from this file's location, so any folder works.
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "songs.csv")

# Taste profiles: categorical favorites plus a target value for each numeric feature
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_tempo_bpm": 122,
        "target_valence": 0.85,
        "target_danceability": 0.85,
        "target_acousticness": 0.10,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.38,
        "target_tempo_bpm": 76,
        "target_valence": 0.58,
        "target_danceability": 0.60,
        "target_acousticness": 0.80,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_tempo_bpm": 150,
        "target_valence": 0.50,
        "target_danceability": 0.65,
        "target_acousticness": 0.10,
    },
}

# Edge cases meant to "trick" the scoring logic
ADVERSARIAL_PROFILES = {
    # Conflict: sad mood but party-level energy; no song is both
    "Sad Banger": {
        "favorite_genre": "blues",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "target_tempo_bpm": 140,
        "target_valence": 0.20,
        "target_danceability": 0.80,
        "target_acousticness": 0.10,
    },
    # Empty genre: "" is a substring of every genre, so every song gets partial genre credit
    "Empty Genre": {
        "favorite_genre": "",
        "favorite_mood": "chill",
        "target_energy": 0.40,
    },
    # Genre not in catalog, but "pop" is a substring of "k-pop" -> unearned partial credit
    "K-Pop Fan": {
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
    },
    # Stray whitespace/case: lower() runs but strip() does not, so exact "rock" drops to partial credit
    "Sloppy Input": {
        "favorite_genre": "  Rock ",
        "favorite_mood": "INTENSE",
        "target_energy": 0.90,
    },
    # Impossible targets: gaps are capped at 1.0, so out-of-range values silently score 0
    "Out of Range": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 1.80,
        "target_tempo_bpm": 400,
        "target_valence": -0.5,
    },
    # Mood outside every group: only an exact "romantic" match earns mood points
    "Romantic Only": {
        "favorite_genre": "jazz",
        "favorite_mood": "romantic",
        "target_energy": 0.50,
    },
    # No label matches and every target mid-range: ranking rests on tiny numeric gaps
    "Fence Sitter": {
        "favorite_genre": "polka",
        "favorite_mood": "curious",
        "target_energy": 0.50,
        "target_tempo_bpm": 100,
        "target_valence": 0.50,
        "target_danceability": 0.50,
        "target_acousticness": 0.50,
    },
}

# Profiles that use the advanced features (popularity, decade, tags, instrumentalness, explicit)
ADVANCED_PROFILES = {
    # Same taste as High-Energy Pop, but clean lyrics only: explicit Gym Hero should drop
    "Clean Workout Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_danceability": 0.85,
        "favorite_tags": ["motivational", "driving"],
        "allow_explicit": False,
    },
    # Older, less mainstream, warm-sounding songs
    "Nostalgic Deep Cuts": {
        "favorite_genre": "country",
        "favorite_mood": "nostalgic",
        "target_energy": 0.50,
        "target_popularity": 35,
        "target_release_decade": 1980,
        "favorite_tags": ["nostalgic", "warm", "dreamy"],
    },
    # Wordless background music for studying
    "Instrumental Focus": {
        "favorite_genre": "lofi",
        "favorite_mood": "focused",
        "target_energy": 0.35,
        "target_instrumentalness": 0.95,
        "favorite_tags": ["focused", "calm", "cozy"],
        "allow_explicit": False,
    },
}


def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in {**PROFILES, **ADVERSARIAL_PROFILES, **ADVANCED_PROFILES}.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Prints the profile and each recommendation with its score and reasons."""
    width = 60
    print()
    print("=" * width)
    print(f" {name}: top {len(recommendations)} picks for "
          f"{user_prefs['favorite_genre']!r} / {user_prefs['favorite_mood']} / "
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
