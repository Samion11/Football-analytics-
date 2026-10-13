"""
generate_data.py
----------------
Synthetic football player dataset generator.
All data is synthetically generated for demonstration purposes only.
It does not represent any real player or club.

Run:  python generate_data.py
Output: football_players.csv (~300 rows, 21 columns)
"""

import numpy as np
import pandas as pd

SEED = 42
NUM_PLAYERS = 100

TEAMS = [
    "Northgate FC", "Southbank United", "Eastfield City", "Westpark Rangers",
    "Riverton Athletic", "Hillside Rovers", "Bayview Wanderers", "Lakeside Town",
    "Midvale Dynamo", "Coastal Stars",
]

POSITIONS = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

FIRST_NAMES = [
    "James", "Luca", "Matteo", "Carlos", "Diego", "Marco", "Andre", "Kai",
    "Noel", "Emil", "Pablo", "Sergio", "Ivan", "Pierre", "Leandro", "Tiago",
    "Rafael", "Yusuf", "Omar", "Ryo", "Hiroshi", "Jin", "Felix", "Hugo",
    "Bastian", "Lukas", "Tobias", "Stefan", "Mikel", "Ander", "Xabi",
    "Roberto", "Alvaro", "Filippo", "Lorenzo", "Giovanni", "Daniele",
    "Cristiano", "Neymar", "Karim", "Antoine", "Kylian", "Erling", "Vinícius",
    "Pedri", "Gavi", "Jude", "Phil", "Mason", "Harry",
]

LAST_NAMES = [
    "Silva", "Müller", "García", "Rossi", "Fernandez", "Okafor", "Takahashi",
    "Hernandez", "Becker", "Schmidt", "Diaz", "Moreira", "Pereira", "Santos",
    "Gomez", "Vargas", "Reyes", "Kim", "Nakamura", "Chen", "Lopez", "Martinez",
    "Sanchez", "Torres", "Ramírez", "Flores", "Mendoza", "Castillo", "Morales",
    "Ortega", "Ramos", "Delgado", "Castro", "Gutiérrez", "Ruiz", "Álvarez",
    "Hoffmann", "Weber", "Wagner", "Fischer", "Schneider", "Meyer", "Braun",
    "Hartmann", "Lehmann", "Koch", "Wolf", "Richter", "Klein", "Schröder",
]

SEASONS = ["2021-22", "2022-23", "2023-24"]


def _pos_goals(pos: str, rng: np.random.Generator) -> int:
    ranges = {"Forward": (5, 30), "Midfielder": (1, 12), "Defender": (0, 5), "Goalkeeper": (0, 1)}
    lo, hi = ranges[pos]
    return int(rng.integers(lo, hi + 1))


def _pos_assists(pos: str, rng: np.random.Generator) -> int:
    ranges = {"Forward": (2, 15), "Midfielder": (3, 18), "Defender": (0, 7), "Goalkeeper": (0, 2)}
    lo, hi = ranges[pos]
    return int(rng.integers(lo, hi + 1))


def _pos_passes(pos: str, rng: np.random.Generator) -> int:
    ranges = {"Forward": (400, 1200), "Midfielder": (900, 2500), "Defender": (700, 2000), "Goalkeeper": (300, 1000)}
    lo, hi = ranges[pos]
    return int(rng.integers(lo, hi + 1))


def _pos_tackles(pos: str, rng: np.random.Generator) -> int:
    ranges = {"Forward": (5, 30), "Midfielder": (20, 80), "Defender": (40, 120), "Goalkeeper": (0, 5)}
    lo, hi = ranges[pos]
    return int(rng.integers(lo, hi + 1))


def _pos_interceptions(pos: str, rng: np.random.Generator) -> int:
    ranges = {"Forward": (2, 20), "Midfielder": (15, 60), "Defender": (30, 100), "Goalkeeper": (0, 3)}
    lo, hi = ranges[pos]
    return int(rng.integers(lo, hi + 1))


def generate(output_path: str = "football_players.csv") -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    player_ids = list(range(1, NUM_PLAYERS + 1))
    used_names: set = set()
    names = []
    for _ in range(NUM_PLAYERS):
        while True:
            fn = FIRST_NAMES[rng.integers(0, len(FIRST_NAMES))]
            ln = LAST_NAMES[rng.integers(0, len(LAST_NAMES))]
            full = f"{fn} {ln}"
            if full not in used_names:
                used_names.add(full)
                names.append(full)
                break

    teams_assigned = [TEAMS[i % len(TEAMS)] for i in range(NUM_PLAYERS)]
    rng.shuffle(teams_assigned)

    pos_weights = [0.10, 0.30, 0.35, 0.25]  # GK, DEF, MID, FWD
    positions_assigned = rng.choice(POSITIONS, size=NUM_PLAYERS, p=pos_weights)

    rows = []
    for pid, name, team, pos in zip(player_ids, names, teams_assigned, positions_assigned):
        n_seasons = int(rng.choice([1, 2, 3], p=[0.20, 0.40, 0.40]))
        player_seasons = list(rng.choice(SEASONS, size=n_seasons, replace=False))
        age_start = int(rng.integers(18, 34))

        for s_idx, season in enumerate(player_seasons):
            age = min(age_start + s_idx, 36)
            appearances = int(rng.integers(5, 39))
            goals = _pos_goals(pos, rng)
            assists = _pos_assists(pos, rng)
            shots = max(goals, int(rng.integers(goals, goals + max(1, goals * 3) + 10)))
            shots_on_target = int(rng.integers(goals, shots + 1))
            passes = _pos_passes(pos, rng)
            key_passes = int(rng.integers(0, max(1, passes // 20) + 1))
            tackles = _pos_tackles(pos, rng)
            interceptions = _pos_interceptions(pos, rng)
            saves = int(rng.integers(30, 130)) if pos == "Goalkeeper" else 0
            clean_sheets = int(rng.integers(2, 16)) if pos in ("Goalkeeper", "Defender") else int(rng.integers(0, 5))
            yellow_cards = int(rng.integers(0, 11))
            red_cards = int(rng.integers(0, 4))
            minutes_played = int(appearances * (75 + rng.integers(-10, 16)))
            raw_rating = 5.0 + 0.1 * goals + 0.07 * assists + 0.03 * key_passes - 0.02 * yellow_cards
            raw_rating += float(rng.uniform(-0.3, 0.3))
            player_rating = round(float(np.clip(raw_rating, 5.0, 9.5)), 2)

            rows.append({
                "player_id": pid,
                "player_name": name,
                "team": team,
                "position": pos,
                "season": season,
                "age": age,
                "appearances": appearances,
                "goals": goals,
                "assists": assists,
                "shots": shots,
                "shots_on_target": shots_on_target,
                "passes": passes,
                "key_passes": key_passes,
                "tackles": tackles,
                "interceptions": interceptions,
                "saves": saves,
                "clean_sheets": clean_sheets,
                "yellow_cards": yellow_cards,
                "red_cards": red_cards,
                "minutes_played": minutes_played,
                "player_rating": player_rating,
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows -> {output_path}")
    return df


if __name__ == "__main__":
    generate()
