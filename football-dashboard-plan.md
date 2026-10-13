# Football Player Performance Analytics Dashboard — Implementation Plan

## Top-Level Overview

**Goal:** Build a portfolio-quality, interactive football (soccer) analytics dashboard using Python and Streamlit. The app will let users explore, filter, and compare synthetic football player data across multiple seasons, teams, and positions.

**Scope:**
- Four deliverables: `app.py`, `football_players.csv`, `requirements.txt`, `README.md`
- Synthetic dataset (≥100 players, clearly labelled as synthetic)
- Five dashboard pages/sections: Overview, Player Analysis, Team Analysis, Position Analysis, Data Table
- Sidebar filters: season, team, position, player
- Dark green football-inspired UI via Plotly theming and Streamlit CSS overrides
- No external APIs or heavyweight dependencies

**Approach:** Each sub-task is independent and produces a concrete, testable artefact. Sub-tasks are ordered so that the data layer is built first, then the app skeleton, then each page, then styling and finishing touches.

**Non-goals:** Real-world data ingestion, authentication, database connectivity, deployment automation scripts beyond README instructions.

---

## Sub-Tasks

---

### Sub-Task 1 — Synthetic Dataset Generation (`football_players.csv`)

**Status:** [ ] pending

**Intent:**
Generate a reproducible, realistic-looking synthetic dataset that drives all KPI calculations and charts. Having a stable CSV file means the app can be run and tested without any data pipeline.

**Dataset Schema:**

| Column | Type | Description |
|---|---|---|
| `player_id` | int | Unique identifier (1–N) |
| `player_name` | str | Full name (Firstname Lastname) |
| `team` | str | Club name (10 distinct clubs) |
| `position` | str | One of: Goalkeeper, Defender, Midfielder, Forward |
| `season` | str | One of: 2021-22, 2022-23, 2023-24 |
| `age` | int | 18–36 |
| `appearances` | int | 1–38 |
| `goals` | int | Position-realistic range |
| `assists` | int | Position-realistic range |
| `shots` | int | ≥ goals |
| `shots_on_target` | int | Between goals and shots |
| `passes` | int | Per position range |
| `key_passes` | int | ≤ passes fraction |
| `tackles` | int | Per position range |
| `interceptions` | int | Per position range |
| `saves` | int | GK-specific, 0 for outfield |
| `clean_sheets` | int | GK/Defender realistic |
| `yellow_cards` | int | 0–10 |
| `red_cards` | int | 0–3 |
| `minutes_played` | int | appearances × ~80 ± noise |
| `player_rating` | float | 5.0–9.5, weighted by performance |

**KPI Calculations (derived at runtime, not hardcoded):**
- **Total Players** — `len(df['player_id'].unique())`
- **Total Goals** — `df['goals'].sum()`
- **Total Assists** — `df['assists'].sum()`
- **Total Minutes Played** — `df['minutes_played'].sum()`
- **Average Player Rating** — `df['player_rating'].mean()`

**Reproducibility:** Use `numpy.random.seed(42)` so the CSV is deterministic.

**Synthetic Data Disclaimer:** A bold, visible disclaimer will appear in the app sidebar and README: *"All data is synthetically generated for demonstration purposes only. It does not represent any real player or club."*

**Expected Outcomes:**
- `football_players.csv` present in project root
- At least 100 rows (target: ~300 rows — ~100 players × 3 seasons)
- All columns present, no null values
- Position-realistic stat distributions (GKs have saves, Forwards have goals, etc.)

**Todo List:**
1. Write a standalone Python script (`generate_data.py`) that uses NumPy with seed 42
2. Define 10 team names and 4 positions
3. Generate 100 unique players, each appearing in 1–3 seasons (yielding ~200–300 rows total)
4. Apply per-position stat scaling (Forwards get highest goals/shots, GKs get saves, etc.)
5. Compute `player_rating` as a weighted formula: `5 + 0.1*goals + 0.07*assists + 0.03*key_passes - 0.02*yellow_cards`, clipped to [5.0, 9.5]
6. Export to `football_players.csv`
7. Inline the generator logic at the top of `app.py` (no separate script needed in the final deliverable) so the CSV is regenerated if missing

**Relevant Context:** No existing files. NumPy and Pandas are the only dependencies for this step.

---

### Sub-Task 2 — Project Skeleton (`requirements.txt`, `app.py` shell, `README.md`)

**Status:** [ ] pending

**Intent:**
Establish the runnable project skeleton before any page logic is written. This gives a working entry point, a dependency manifest, and a README that guides any reader through setup and deployment.

**`requirements.txt` contents:**
```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.26.0
plotly>=5.20.0
```

**`app.py` structure (shell only — no page logic yet):**
```
imports
─── load_data()          # reads CSV, regenerates if missing
─── apply_filters()      # applies sidebar widget selections to the dataframe
─── main()
    ├── st.set_page_config(...)
    ├── inject_custom_css()
    ├── render_sidebar()      # season/team/position/player filters + disclaimer
    └── page router           # st.sidebar radio → render_overview | render_player_analysis | render_team_analysis | render_position_analysis | render_data_table
```

**`README.md` sections:**
1. Project description + disclaimer
2. Prerequisites (Python 3.10+)
3. Local setup (`pip install -r requirements.txt` → `streamlit run app.py`)
4. Deployment on Streamlit Community Cloud (connect repo, set main file)
5. Dataset schema reference
6. Screenshot placeholder

**Expected Outcomes:**
- `requirements.txt` is valid and installable
- `app.py` runs without error, shows an empty app with sidebar navigation
- `README.md` is complete and accurate

**Todo List:**
1. Create `requirements.txt` with pinned minimum versions
2. Create `app.py` with imports, `load_data()`, `apply_filters()`, `inject_custom_css()` (empty for now), `render_sidebar()`, and the page router inside `main()`
3. Create `README.md` with all sections listed above

**Relevant Context:** Streamlit page config must be the first Streamlit call in the script.

---

### Sub-Task 3 — Overview Page (KPI Cards + Summary Charts)

**Status:** [ ] pending

**Intent:**
Implement the `render_overview()` function. This is the landing page — it must immediately communicate the scale of the dataset and show high-level trends.

**Layout:**
```
Row 1: [Total Players] [Total Goals] [Total Assists] [Total Minutes] [Avg Rating]
Row 2: [Goals by Season bar chart] [Top 10 Scorers bar chart]
Row 3: [Position distribution donut] [Team goals breakdown bar chart]
```

**KPI Card Design:** Use `st.metric()` with delta indicators (e.g. change from previous season if a single season is selected, or "All seasons" label otherwise).

**Chart Choices:**
| Chart | Type | Reason |
|---|---|---|
| Goals by Season | Grouped bar (Plotly) | Shows trend across seasons |
| Top 10 Scorers | Horizontal bar | Easy name-to-value reading |
| Position distribution | Donut/pie | Part-to-whole proportions |
| Team goals | Vertical bar | Cross-team comparison |

**Expected Outcomes:**
- `render_overview(filtered_df)` function is complete
- All 5 KPI metrics render from filtered data
- All 4 charts render with correct labels, tooltips, and dark theme colours

**Todo List:**
1. Implement `render_overview(df)` in `app.py`
2. Compute the 5 KPIs from `df` (no hardcoding)
3. Render KPI row using `st.columns(5)` and `st.metric()`
4. Build Goals by Season chart with `px.bar`
5. Build Top 10 Scorers chart with `px.bar` (horizontal, sorted)
6. Build Position distribution with `px.pie` (hole=0.4 for donut)
7. Build Team goals chart with `px.bar`
8. Apply consistent dark-green Plotly template to all charts

**Relevant Context:** All charts receive the already-filtered dataframe — no re-filtering inside chart functions.

---

### Sub-Task 4 — Player Analysis Page

**Status:** [ ] pending

**Intent:**
Implement `render_player_analysis()`. This page lets users drill into individual players and compare two players side-by-side.

**Layout:**
```
Section A: Player Comparison
  ├── Two selectboxes (Player A, Player B)
  └── Side-by-side stat cards + radar chart

Section B: Goals vs Assists Scatter
  └── Scatter plot coloured by position, sized by appearances, with player name on hover

Section C: Shots vs Goals Analysis
  └── Scatter plot with conversion rate (goals/shots) on hover, trend line
```

**Chart Choices:**
| Chart | Type | Reason |
|---|---|---|
| Player radar | Plotly go.Scatterpolar | Multi-dimensional player profile at a glance |
| Goals vs Assists | px.scatter | Identifies dual-threat players |
| Shots vs Goals | px.scatter with trendline | Reveals clinical finishers vs volume shooters |

**Radar Normalisation:** Each stat (goals, assists, shots_on_target, key_passes, tackles, rating) is normalised to 0–1 within the filtered dataset so the radar axes are comparable.

**Expected Outcomes:**
- `render_player_analysis(df)` is complete
- Radar chart renders for any two valid player selections
- Scatter plots render with correct hover data and colour coding

**Todo List:**
1. Implement `render_player_analysis(df)` in `app.py`
2. Build player comparison widget with two `st.selectbox` controls
3. Normalise selected stats for radar chart
4. Render radar chart using `go.Figure` + `go.Scatterpolar`
5. Build Goals vs Assists scatter with `px.scatter`, colour=position, size=appearances
6. Add conversion rate column `goals / shots.replace(0,1)` for hover text
7. Build Shots vs Goals scatter with `px.scatter`, `trendline="ols"` (requires `statsmodels` — add to requirements if used, or compute manually to avoid extra dependency)
8. Handle edge case: if fewer than 2 players pass the filter, show `st.info()` message

**Relevant Context:** `trendline="ols"` in Plotly Express requires `statsmodels`. To keep dependencies minimal, compute a manual linear regression using NumPy and draw it as a separate `go.Scatter` trace instead.

---

### Sub-Task 5 — Team Analysis Page

**Status:** [ ] pending

**Intent:**
Implement `render_team_analysis()`. Aggregates player-level stats to team level and surfaces cross-team comparisons.

**Layout:**
```
Row 1: [Team Goals bar] [Team Assists bar]
Row 2: [Squad size bar] [Avg Rating per team bar]
Row 3: [Stacked bar: goals by position per team]
```

**Aggregation Logic:**
```python
team_df = df.groupby('team').agg(
    total_goals=('goals', 'sum'),
    total_assists=('assists', 'sum'),
    squad_size=('player_id', 'nunique'),
    avg_rating=('player_rating', 'mean')
).reset_index()
```

**Expected Outcomes:**
- `render_team_analysis(df)` is complete
- All team-level aggregations are computed from `df`, not hardcoded
- Charts display correctly even when filter reduces to one team (graceful degradation with `st.info()`)

**Todo List:**
1. Implement `render_team_analysis(df)` in `app.py`
2. Compute `team_df` aggregation
3. Render Team Goals and Team Assists as side-by-side `px.bar` charts
4. Render Squad Size and Avg Rating as side-by-side `px.bar` charts
5. Build stacked position-per-team goals bar chart using `px.bar` with `color='position'`
6. Add guard: if `df` is empty after filters, display `st.warning()` and return early

**Relevant Context:** The stacked bar chart requires a `groupby(['team', 'position'])` aggregation on goals.

---

### Sub-Task 6 — Position Analysis Page

**Status:** [ ] pending

**Intent:**
Implement `render_position_analysis()`. Compares performance distributions across the four positions: Goalkeeper, Defender, Midfielder, Forward.

**Layout:**
```
Row 1: Position KPI cards (avg goals, avg assists, avg rating, avg tackles per position)
Row 2: [Box plot: rating by position] [Box plot: goals by position]
Row 3: [Bar: avg key passes by position] [Bar: avg saves by position (GK focus)]
```

**Chart Choices:**
| Chart | Type | Reason |
|---|---|---|
| Rating/Goals box plots | px.box | Shows distribution and outliers, not just averages |
| Avg key passes | px.bar | Simple cross-position comparison |
| Avg saves | px.bar | Highlights GK uniqueness |

**Expected Outcomes:**
- `render_position_analysis(df)` is complete
- Box plots correctly show distribution per position
- GK-specific stats (saves, clean sheets) are highlighted separately

**Todo List:**
1. Implement `render_position_analysis(df)` in `app.py`
2. Compute per-position averages for KPI cards
3. Render 4 KPI cards in a row using `st.columns(4)`
4. Build rating-by-position box plot with `px.box`
5. Build goals-by-position box plot with `px.box`
6. Build avg key passes bar chart with `px.bar`
7. Build avg saves bar chart (full dataset so GK bar is meaningful) with `px.bar`

**Relevant Context:** Saves data is only meaningful for Goalkeepers — ensure the chart labels make this clear (axis title: "Avg Saves (GK-relevant)").

---

### Sub-Task 7 — Data Table Page (Search, Filter, Download)

**Status:** [ ] pending

**Intent:**
Implement `render_data_table()`. Provides a searchable, sortable table of player stats and a CSV download button for the filtered dataset.

**Layout:**
```
Search bar (text input → filters player_name column)
st.dataframe(filtered results, use_container_width=True)
Download CSV button
```

**Input Validation:**
- If search string returns 0 rows: `st.info("No players match your search.")`
- If overall filtered dataset is empty: `st.warning("No data matches the selected filters.")`

**Expected Outcomes:**
- `render_data_table(df)` is complete
- Search box filters by player name (case-insensitive substring match)
- `st.download_button` produces a valid CSV of the visible rows
- Column display order is logical (player_name, team, position, season, goals, assists, … rating)

**Todo List:**
1. Implement `render_data_table(df)` in `app.py`
2. Add `st.text_input("Search player name…")` and apply case-insensitive `.str.contains()` filter
3. Define display column order
4. Render `st.dataframe()` with `use_container_width=True`
5. Add `st.download_button()` using `df.to_csv(index=False).encode('utf-8')` as data

**Relevant Context:** `st.download_button` requires `mime="text/csv"` and a filename argument.

---

### Sub-Task 8 — UI Theming, CSS, and Final Polish

**Status:** [ ] pending

**Intent:**
Apply the dark, football-inspired green pitch theme across the entire app. Inject custom CSS into `inject_custom_css()` and set a consistent Plotly template. Add the synthetic data disclaimer. Final review pass for input validation and error messages.

**Colour Palette:**
| Role | Hex |
|---|---|
| Background | `#0a0f0d` (near black) |
| Sidebar background | `#0d1f17` (deep forest green) |
| Primary accent | `#00ff87` (pitch green neon) |
| Secondary accent | `#00c85a` |
| Card/surface | `#132218` |
| Text primary | `#e8f5e9` |
| Text secondary | `#a5d6a7` |

**Plotly Template:** Define a custom Plotly layout template dict (dark background, green gridlines, light text) and apply it to every figure via `fig.update_layout(template=custom_template)`.

**Custom CSS targets (via `st.markdown` with `unsafe_allow_html=True`):**
- `.stApp` background
- `section[data-testid="stSidebar"]` background
- `div[data-testid="metric-container"]` card styling
- Button (`stDownloadButton`) styling

**Final Validation Checklist:**
- All sidebar filters show "All" options as default
- Empty-state messages appear when filters return no data
- No hardcoded KPI values anywhere in `app.py`
- Disclaimer visible in sidebar
- App title and favicon set via `st.set_page_config`

**Expected Outcomes:**
- App has a cohesive dark green football theme
- All charts use the custom Plotly template
- Disclaimer is visible
- All edge cases (empty filter results, single-player dataset) handled gracefully

**Todo List:**
1. Define the colour palette constants at the top of `app.py`
2. Implement `inject_custom_css()` with the CSS block above
3. Define `PLOTLY_TEMPLATE` dict and apply to all `fig.update_layout()` calls
4. Add synthetic data disclaimer to sidebar (`st.sidebar.warning()`)
5. Review all pages for hardcoded values and replace with computed ones
6. Test all sidebar filter combinations including edge cases
7. Set `st.set_page_config(page_title="⚽ Football Analytics", page_icon="⚽", layout="wide")`

---

## File Delivery Summary

| File | Description |
|---|---|
| `app.py` | Main Streamlit application (~600–800 lines) |
| `football_players.csv` | Synthetic dataset (~300 rows, 21 columns) |
| `requirements.txt` | 4 dependencies with minimum versions |
| `README.md` | Setup, run, deploy, schema, disclaimer |

---

## Architecture Diagram (textual)

```
app.py
├── Constants (colours, column order)
├── generate_synthetic_data()   → football_players.csv
├── load_data()                 → pd.DataFrame
├── apply_filters(df, filters)  → pd.DataFrame (filtered)
├── inject_custom_css()
├── render_sidebar(df)          → filter dict
├── render_overview(df)
├── render_player_analysis(df)
├── render_team_analysis(df)
├── render_position_analysis(df)
├── render_data_table(df)
└── main()
```
