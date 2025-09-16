# Dota 2 Match Dashboard

A Python + [Streamlit](https://streamlit.io/) dashboard for analyzing Dota 2 matches.  
It visualizes draft phases, team composition balance, and game progress.

---

## Features

- **Pick/Ban Phase**
  - Visual timeline of picks and bans (Radiant and Dire).
  - Hero portraits with numbered order (picks in color, bans grayed out).
  - Draft timings (seconds taken) displayed below each portrait.

- **Team Advantage Graph**
  - Line chart of Radiant XP and Gold advantage over time.
  - Minute markers every 3 minutes.
  - Highlighted zero-line to show lead changes.

- **Role Coverage Heatmap**
  - Counts of role categories (e.g., Carry, Disabler, Nuker) per team.
  - Toggle between:
    - Separate Radiant/Dire heatmaps.
    - Overlap comparison in one chart.

---

## Dataset

The dashboard fetches live match data from the [OpenDota API](https://docs.opendota.com/).

Endpoints used:
- [`/api/matches/{match_id}`](https://docs.opendota.com/#tag/matches/GET/api-matches-match_id) – match details, picks/bans, and gold/xp advantage.  
- [`/api/heroes`](https://docs.opendota.com/#tag/heroes/GET/api-heroes) – hero metadata including roles and attributes.

---

## Installation

1. **Create environment**
```bash
   conda create -n dota-dashboard python=3.11
   conda activate dota-dashboard
```
or
```
python -m venv venv
source venv/bin/activate
```

2. **Install dependencies**
```
pip install -r requirements.txt
```

## Usage

1. Run the dashboard:
```
streamlit run app.py
```

2.	Enter a match ID in the input field (e.g., 8448961923).
3.	Explore:
	•	Pick/Ban phase visualization.
	•	XP/Gold advantage over time.
	•	Role coverage heatmaps.

## Future Enhancements
- Group draft into Ban/Pick phases (like Dotabuff).
- Add attribute and attack-type breakdowns (STR/AGI/INT, melee/ranged).
- Place advantage graph and heatmap side by side under the draft.
- Modularize code into components (`hero_tile.py`, `charts/advantage.py`, etc.).
- Add hide/show toggles for each section (draft, graphs, heatmaps).
- Introduce synergy and counter heatmaps between Radiant and Dire heroes.