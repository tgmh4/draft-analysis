# Dota Draft Dashboard

This repository contains a Streamlit dashboard and supporting exploration notebooks for analyzing Dota 2 drafts and match data. The dashboard visualizes the pick/ban phase, player stats, team advantage graphs, and role coverage heatmaps. The `/exploration` folder includes Jupyter notebooks for feature engineering and data discovery.

## Features
- **Pick/Ban Visualization**:
  - Chronological Radiant/Dire pick/ban rows.
  - Hero portraits with grayscale bans and order numbering.
  - Draft timing labels for each action.
- **Player Stats Table**:
  - Hero portrait with level overlay.
  - Lane + player fields with KDA, GPM, XPM, and net worth.
  - Radiant and Dire tables with team total rows.
- **Team Advantage Graph**:
  - XP and Gold advantage plotted over time.
  - Radiant/Dire advantage labeled clearly.
- **Role Coverage Heatmap**:
  - Radiant and Dire role distributions with toggle for overlap.
  - Dark theme with team-colored highlights.
- **Exploration Support**:
  - `/exploration/json_preview.ipynb` for df.head()-style JSON previews.

## Dataset
The dashboard uses match JSONs from the [OpenDota API](https://docs.opendota.com/).  
Example endpoints:
- `https://api.opendota.com/api/matches/{match_id}`
- `https://api.opendota.com/api/heroes`
- `https://api.opendota.com/api/heroStats`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/tgmh4/draft-analysis.git
   cd draft-analysis
   ```

2. Create environment:
```
conda env create -f environment.yml
conda activate dota-dashboard
```

3. Install dependencies (if not using conda):
```
pip install -r requirements.txt
```

**Usage**
1. Run the dashboard:
```
streamlit run app.py
```

2. Enter match ID into the search field.
3.	Explore the draft phase, player stats, advantage graphs, and heatmaps.
4.	Open /exploration notebooks in VS Code or Jupyter to dive deeper into JSON fields and feature engineering.

**Future Enhancements**
	•	Group draft into Ban/Pick phases (Dotabuff-style).
	•	Add attribute and attack-type breakdowns (STR/AGI/INT, melee/ranged).
	•	Compare match-level stats vs global benchmarks.
	•	Tournament-level scraping (league ID → all matches).
	•	ML models for draft prediction (sequence modeling).
	•	Downloadable match CSVs for external analysis.
