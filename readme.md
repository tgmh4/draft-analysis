# Dota Draft Dashboard

An interactive Streamlit dashboard and supporting Jupyter notebooks for analyzing Dota 2 drafts and match data. The dashboard provides draft-phase visualizations, player stats tables, advantage graphs, and role coverage heatmaps. The `/exploration` folder includes notebooks for data discovery and feature engineering.

---

## Features
- **Pick/Ban Visualization**  
  • Chronological Radiant/Dire rows with hero portraits.  
  • Grayscale bans and numbered order labels.  
  • Draft timing annotations.  

- **Player Stats Table**  
  • Hero portrait with level overlay.  
  • Lane + player fields with KDA, GPM, XPM, and net worth.  
  • Radiant and Dire tables with team totals.  

- **Team Advantage Graph**  
  • XP and Gold advantage vs time.  
  • Radiant/Dire advantage clearly highlighted.  

- **Role Coverage Heatmap**  
  • Radiant and Dire role distribution with overlap toggle.  
  • Dark theme with team-colored highlights.  

- **Exploration Support**  
  • `/exploration/json_preview.ipynb` for `df.head()`-style JSON previews.  

---

## Dataset
Data is pulled from the [OpenDota API](https://docs.opendota.com/).  
Example endpoints:  
- `https://api.opendota.com/api/matches/{match_id}`  
- `https://api.opendota.com/api/heroes`  
- `https://api.opendota.com/api/heroStats`  

---

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
- Populate single match view with metadata

- ML sequence models for draft prediction.

- Tournament-level scraping (league ID → all matches).  

