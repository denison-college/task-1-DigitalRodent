import json
import os
from datetime import datetime

SCORE_FILE = os.path.join(os.path.dirname(__file__), "scores.json")
MAX_HIGHSCORES = 10


def load_scores():
    """Load saved high scores from disk."""
    if not os.path.exists(SCORE_FILE):
        return []

    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, OSError):
        return []

    return []


def save_scores(scores):
    """Save scores to disk."""
    with open(SCORE_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


def _score_key(entry):
    """
    Sort key for highscores.
    Won games come first, then faster times.
    """
    result = str(entry.get("result", "")).strip().lower()
    result_rank = 0 if result == "won" else 1
    time_taken = float(entry.get("time", 999999))
    return (result_rank, time_taken)


def add_score(name, result, time_taken, difficulty):
    """
    Add a completed game to the highscore list.

    Only the best results are kept.
    """
    scores = load_scores()

    new_entry = {
        "name": str(name).strip() if name else "Unknown",
        "result": str(result).strip().title(),
        "difficulty": str(difficulty).strip(),
        "time": round(float(time_taken), 2),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    scores.append(new_entry)
    scores = sorted(scores, key=_score_key)[:MAX_HIGHSCORES]
    save_scores(scores)


def show_scoreboard():
    """Display the saved highscores."""
    scores = load_scores()

    print()
    print("=" * 78)
    print("FINAL HIGHSCORES".center(78))
    print("=" * 78)

    if not scores:
        print("No highscores have been recorded yet.")
        print("=" * 78)
        return

    print(f"{'#':<4}{'Name':<18}{'Result':<10}{'Difficulty':<24}{'Time':<10}{'Date'}")
    print("-" * 78)

    for index, entry in enumerate(sorted(scores, key=_score_key), start=1):
        name = entry.get("name", "Unknown")
        result = entry.get("result", "Unknown")
        difficulty = entry.get("difficulty", "Unknown")
        time_taken = entry.get("time", 0.0)
        date = entry.get("date", "")

        print(
            f"{index:<4}"
            f"{name:<18}"
            f"{result:<10}"
            f"{difficulty:<24}"
            f"{time_taken:<10}"
            f"{date}"
        )

    print("=" * 78)


def clear_scores():
    """Remove all stored highscores."""
    save_scores([])