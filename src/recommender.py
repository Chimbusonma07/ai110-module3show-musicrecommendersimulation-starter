import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Algorithm Recipe weights (see README "How The System Works")
GENRE_MATCH_POINTS = 2.0
GENRE_PARTIAL_POINTS = 1.0
MOOD_MATCH_POINTS = 1.0
MOOD_CLOSE_POINTS = 0.5

# feature -> (max points, scale used to turn the gap into 0-1)
NUMERIC_WEIGHTS = {
    "energy": (1.5, 1.0),
    "valence": (0.75, 1.0),
    "danceability": (0.5, 1.0),
    "acousticness": (0.5, 1.0),
    "tempo_bpm": (0.5, 100.0),
}

# Moods in the same group earn partial credit for each other
MOOD_GROUPS = [
    {"chill", "relaxed", "peaceful", "laid-back"},
    {"intense", "angry", "energetic"},
    {"happy", "euphoric", "confident"},
    {"sad", "melancholic", "nostalgic", "moody"},
]

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # csv returns every value as a string; convert numbers so they can be used in math
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # Genre: exact match, or partial when one name contains the other ("indie pop" vs "pop")
    user_genre = user_prefs["favorite_genre"].lower()
    song_genre = song["genre"].lower()
    if song_genre == user_genre:
        score += GENRE_MATCH_POINTS
        reasons.append(f"genre match (+{GENRE_MATCH_POINTS:.1f})")
    elif user_genre in song_genre or song_genre in user_genre:
        score += GENRE_PARTIAL_POINTS
        reasons.append(f"related genre: {song['genre']} (+{GENRE_PARTIAL_POINTS:.1f})")

    # Mood: exact match, or half credit when both moods are in the same group
    user_mood = user_prefs["favorite_mood"].lower()
    song_mood = song["mood"].lower()
    if song_mood == user_mood:
        score += MOOD_MATCH_POINTS
        reasons.append(f"mood match (+{MOOD_MATCH_POINTS:.1f})")
    elif any(user_mood in group and song_mood in group for group in MOOD_GROUPS):
        score += MOOD_CLOSE_POINTS
        reasons.append(f"similar mood: {song['mood']} (+{MOOD_CLOSE_POINTS:.1f})")

    # Numeric features: weight * (1 - gap), so closer to the target earns more
    for feature, (weight, scale) in NUMERIC_WEIGHTS.items():
        target = user_prefs.get(f"target_{feature}")
        if target is None:
            continue
        gap = min(abs(song[feature] - target) / scale, 1.0)
        points = weight * (1 - gap)
        score += points
        reasons.append(f"{feature} close to target (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Judge every song once: (song, score, reasons)
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # Highest score first; ties go to the song closer to the target energy
    target_energy = user_prefs.get("target_energy", 0.5)
    ranked = sorted(
        scored,
        key=lambda item: (-item[1], abs(item[0]["energy"] - target_energy)),
    )

    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]
