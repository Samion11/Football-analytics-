"""
app.py  --  Football Player Performance Analytics Dashboard
============================================================
Synthetic data only. Powered by Streamlit + Plotly.

All data is synthetically generated for demonstration purposes only.
It does not represent any real player or club.
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
BG = "#0a0f0d"
SIDEBAR_BG = "#0d1f17"
ACCENT = "#00ff87"
ACCENT2 = "#00c85a"
SURFACE = "#132218"
TEXT_PRIMARY = "#e8f5e9"
TEXT_SECONDARY = "#a5d6a7"

# ---------------------------------------------------------------------------
# Plotly custom template
# ---------------------------------------------------------------------------
PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(color=TEXT_PRIMARY, family="Segoe UI, sans-serif"),
        title=dict(font=dict(color=ACCENT, size=15)),
        xaxis=dict(
            gridcolor="#1e3a2a",
            zerolinecolor="#1e3a2a",
            tickfont=dict(color=TEXT_SECONDARY),
        ),
        yaxis=dict(
            gridcolor="#1e3a2a",
            zerolinecolor="#1e3a2a",
            tickfont=dict(color=TEXT_SECONDARY),
        ),
        legend=dict(
            bgcolor=SURFACE,
            bordercolor="#1e3a2a",
            font=dict(color=TEXT_SECONDARY),
        ),
        colorway=[ACCENT, "#00b4d8", "#f4a261", "#e63946", "#a8dadc",
                  "#457b9d", "#2a9d8f", "#e9c46a", "#f3722c", "#90be6d"],
    )
)

POSITION_COLORS = {
    "Goalkeeper": "#e9c46a",
    "Defender":   "#00b4d8",
    "Midfielder": ACCENT,
    "Forward":    "#e63946",
}

DISPLAY_COLUMNS = [
    "player_name", "team", "position", "season", "age", "appearances",
    "goals", "assists", "shots", "shots_on_target", "passes", "key_passes",
    "tackles", "interceptions", "saves", "clean_sheets",
    "yellow_cards", "red_cards", "minutes_played", "player_rating",
]

# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------

def generate_synthetic_data(output_path: str = "football_players.csv") -> pd.DataFrame:
    """Regenerate the synthetic dataset if the CSV is absent."""
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
        "Cristiano", "Neymar", "Karim", "Antoine", "Kylian", "Erling", "Vinicius",
        "Pedri", "Gavi", "Jude", "Phil", "Mason", "Harry",
    ]
    LAST_NAMES = [
        "Silva", "Muller", "Garcia", "Rossi", "Fernandez", "Okafor", "Takahashi",
        "Hernandez", "Becker", "Schmidt", "Diaz", "Moreira", "Pereira", "Santos",
        "Gomez", "Vargas", "Reyes", "Kim", "Nakamura", "Chen", "Lopez", "Martinez",
        "Sanchez", "Torres", "Ramirez", "Flores", "Mendoza", "Castillo", "Morales",
        "Ortega", "Ramos", "Delgado", "Castro", "Gutierrez", "Ruiz", "Alvarez",
        "Hoffmann", "Weber", "Wagner", "Fischer", "Schneider", "Meyer", "Braun",
        "Hartmann", "Lehmann", "Koch", "Wolf", "Richter", "Klein", "Schroeder",
    ]
    SEASONS = ["2021-22", "2022-23", "2023-24"]

    rng = np.random.default_rng(SEED)
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
    pos_weights = [0.10, 0.30, 0.35, 0.25]
    positions_assigned = rng.choice(POSITIONS, size=NUM_PLAYERS, p=pos_weights)

    def _rng_int(lo, hi):
        return int(rng.integers(lo, hi + 1))

    pos_ranges = {
        "goals":         {"Forward": (5, 30), "Midfielder": (1, 12), "Defender": (0, 5), "Goalkeeper": (0, 1)},
        "assists":       {"Forward": (2, 15), "Midfielder": (3, 18), "Defender": (0, 7), "Goalkeeper": (0, 2)},
        "passes":        {"Forward": (400, 1200), "Midfielder": (900, 2500), "Defender": (700, 2000), "Goalkeeper": (300, 1000)},
        "tackles":       {"Forward": (5, 30), "Midfielder": (20, 80), "Defender": (40, 120), "Goalkeeper": (0, 5)},
        "interceptions": {"Forward": (2, 20), "Midfielder": (15, 60), "Defender": (30, 100), "Goalkeeper": (0, 3)},
    }

    rows = []
    for pid, (name, team, pos) in enumerate(zip(names, teams_assigned, positions_assigned), start=1):
        n_seasons = int(rng.choice([1, 2, 3], p=[0.20, 0.40, 0.40]))
        player_seasons = list(rng.choice(SEASONS, size=n_seasons, replace=False))
        age_start = int(rng.integers(18, 34))
        for s_idx, season in enumerate(player_seasons):
            age = min(age_start + s_idx, 36)
            appearances = _rng_int(5, 38)
            goals     = _rng_int(*pos_ranges["goals"][pos])
            assists   = _rng_int(*pos_ranges["assists"][pos])
            shots     = max(goals, _rng_int(goals, goals + max(1, goals * 3) + 10))
            shots_on_target = _rng_int(goals, shots)
            passes    = _rng_int(*pos_ranges["passes"][pos])
            key_passes = _rng_int(0, max(1, passes // 20))
            tackles   = _rng_int(*pos_ranges["tackles"][pos])
            interceptions = _rng_int(*pos_ranges["interceptions"][pos])
            saves      = _rng_int(30, 130) if pos == "Goalkeeper" else 0
            clean_sheets = _rng_int(2, 15) if pos in ("Goalkeeper", "Defender") else _rng_int(0, 4)
            yellow_cards = _rng_int(0, 10)
            red_cards    = _rng_int(0, 3)
            minutes_played = int(appearances * (75 + rng.integers(-10, 16)))
            raw_rating = 5.0 + 0.1 * goals + 0.07 * assists + 0.03 * key_passes - 0.02 * yellow_cards
            raw_rating += float(rng.uniform(-0.3, 0.3))
            player_rating = round(float(np.clip(raw_rating, 5.0, 9.5)), 2)
            rows.append({
                "player_id": pid, "player_name": name, "team": team,
                "position": pos, "season": season, "age": age,
                "appearances": appearances, "goals": goals, "assists": assists,
                "shots": shots, "shots_on_target": shots_on_target,
                "passes": passes, "key_passes": key_passes, "tackles": tackles,
                "interceptions": interceptions, "saves": saves,
                "clean_sheets": clean_sheets, "yellow_cards": yellow_cards,
                "red_cards": red_cards, "minutes_played": minutes_played,
                "player_rating": player_rating,
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return df


@st.cache_data
def load_data() -> pd.DataFrame:
    csv_path = "football_players.csv"
    if not os.path.exists(csv_path):
        return generate_synthetic_data(csv_path)
    return pd.read_csv(csv_path)


def apply_filters(df: pd.DataFrame, seasons, teams, positions, player_name: str) -> pd.DataFrame:
    if seasons:
        df = df[df["season"].isin(seasons)]
    if teams:
        df = df[df["team"].isin(teams)]
    if positions:
        df = df[df["position"].isin(positions)]
    if player_name and player_name != "All":
        df = df[df["player_name"] == player_name]
    return df

# ---------------------------------------------------------------------------
# CSS injection
# ---------------------------------------------------------------------------

def inject_custom_css():
    st.markdown(
        f"""
        <style>
        /* ---- App background ---- */
        .stApp {{
            background-color: {BG};
            color: {TEXT_PRIMARY};
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background-color: {SIDEBAR_BG} !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {{
            color: {TEXT_SECONDARY} !important;
        }}

        /* ---- Metric cards ---- */
        div[data-testid="metric-container"] {{
            background-color: {SURFACE};
            border: 1px solid #1e3a2a;
            border-radius: 8px;
            padding: 12px 16px;
        }}
        div[data-testid="metric-container"] label {{
            color: {TEXT_SECONDARY} !important;
            font-size: 0.78rem !important;
        }}
        div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
            color: {ACCENT} !important;
            font-size: 1.6rem !important;
        }}

        /* ---- Download button ---- */
        div[data-testid="stDownloadButton"] > button {{
            background-color: {ACCENT2};
            color: #000;
            border: none;
            border-radius: 6px;
            font-weight: 600;
        }}
        div[data-testid="stDownloadButton"] > button:hover {{
            background-color: {ACCENT};
        }}

        /* ---- Headers ---- */
        h1, h2, h3 {{
            color: {ACCENT} !important;
        }}

        /* ---- Dataframe ---- */
        .stDataFrame {{
            background-color: {SURFACE};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_sidebar(df: pd.DataFrame) -> dict:
    st.sidebar.title("⚽ Football Analytics")
    st.sidebar.markdown("---")

    st.sidebar.warning(
        "**SYNTHETIC DATA NOTICE**\n\n"
        "All data is synthetically generated for demonstration purposes only. "
        "It does not represent any real player or club."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filters")

    all_seasons = sorted(df["season"].unique().tolist())
    seasons = st.sidebar.multiselect("Season", all_seasons, default=all_seasons, key="sel_season")

    filtered_teams = df[df["season"].isin(seasons)] if seasons else df
    all_teams = sorted(filtered_teams["team"].unique().tolist())
    teams = st.sidebar.multiselect("Team", all_teams, default=all_teams, key="sel_team")

    all_positions = sorted(df["position"].unique().tolist())
    positions = st.sidebar.multiselect("Position", all_positions, default=all_positions, key="sel_pos")

    # Player filter — applied after other filters
    temp_df = apply_filters(df, seasons, teams, positions, player_name="")
    all_players = ["All"] + sorted(temp_df["player_name"].unique().tolist())
    player_name = st.sidebar.selectbox("Player", all_players, key="sel_player")

    page = st.sidebar.radio(
        "Page",
        ["Overview", "Player Analysis", "Team Analysis", "Position Analysis", "Data Table"],
        key="nav_page",
    )

    return {
        "seasons": seasons,
        "teams": teams,
        "positions": positions,
        "player_name": player_name,
        "page": page,
    }

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _apply_template(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        title_text=title,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig

# ---------------------------------------------------------------------------
# Page: Overview
# ---------------------------------------------------------------------------

def render_overview(df: pd.DataFrame):
    st.header("Overview")

    if df.empty:
        st.warning("No data matches the selected filters.")
        return

    # KPI row
    total_players  = df["player_id"].nunique()
    total_goals    = int(df["goals"].sum())
    total_assists  = int(df["assists"].sum())
    total_minutes  = int(df["minutes_played"].sum())
    avg_rating     = round(df["player_rating"].mean(), 2)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Players",     f"{total_players:,}")
    c2.metric("Total Goals",       f"{total_goals:,}")
    c3.metric("Total Assists",     f"{total_assists:,}")
    c4.metric("Total Minutes",     f"{total_minutes:,}")
    c5.metric("Avg Player Rating", f"{avg_rating:.2f}")

    st.markdown("---")

    # Row 2 charts
    col1, col2 = st.columns(2)

    with col1:
        goals_by_season = df.groupby("season", as_index=False)["goals"].sum().sort_values("season")
        fig = px.bar(goals_by_season, x="season", y="goals",
                     labels={"season": "Season", "goals": "Total Goals"},
                     color="season",
                     color_discrete_sequence=[ACCENT, ACCENT2, "#00b4d8"])
        _apply_template(fig, "Goals by Season")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_scorers = (df.groupby("player_name", as_index=False)["goals"].sum()
                         .sort_values("goals", ascending=False)
                         .head(10))
        fig2 = px.bar(top_scorers, x="goals", y="player_name", orientation="h",
                      labels={"goals": "Goals", "player_name": "Player"},
                      color="goals",
                      color_continuous_scale=[[0, ACCENT2], [1, ACCENT]])
        fig2.update_layout(yaxis={"categoryorder": "total ascending"})
        _apply_template(fig2, "Top 10 Scorers")
        st.plotly_chart(fig2, use_container_width=True)

    # Row 3 charts
    col3, col4 = st.columns(2)

    with col3:
        pos_dist = df.groupby("position", as_index=False)["player_id"].nunique()
        pos_dist.columns = ["position", "count"]
        fig3 = px.pie(pos_dist, names="position", values="count",
                      hole=0.4,
                      color="position",
                      color_discrete_map=POSITION_COLORS)
        _apply_template(fig3, "Player Distribution by Position")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        team_goals = df.groupby("team", as_index=False)["goals"].sum().sort_values("goals", ascending=False)
        fig4 = px.bar(team_goals, x="team", y="goals",
                      labels={"team": "Team", "goals": "Total Goals"},
                      color="goals",
                      color_continuous_scale=[[0, ACCENT2], [1, ACCENT]])
        fig4.update_layout(xaxis_tickangle=-35)
        _apply_template(fig4, "Team Goals Breakdown")
        st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------------------------------
# Page: Player Analysis
# ---------------------------------------------------------------------------

def render_player_analysis(df: pd.DataFrame):
    st.header("Player Analysis")

    if df["player_id"].nunique() < 2:
        st.info("Please adjust your filters so that at least 2 players are available for comparison.")
        return

    # --- Section A: Player comparison ---
    st.subheader("Player Comparison")
    all_names = sorted(df["player_name"].unique().tolist())
    col_a, col_b = st.columns(2)
    with col_a:
        player_a = st.selectbox("Player A", all_names, index=0, key="pa_a")
    with col_b:
        player_b = st.selectbox("Player B", all_names, index=min(1, len(all_names) - 1), key="pa_b")

    radar_stats = ["goals", "assists", "shots_on_target", "key_passes", "tackles", "player_rating"]

    def _norm(series: pd.Series) -> pd.Series:
        lo, hi = series.min(), series.max()
        if hi == lo:
            return series * 0.0
        return (series - lo) / (hi - lo)

    norm_df = df.copy()
    for col in radar_stats:
        norm_df[col] = _norm(df[col])

    def _agg_player(name: str) -> pd.Series:
        sub = norm_df[norm_df["player_name"] == name]
        return sub[radar_stats].mean()

    stats_a = _agg_player(player_a)
    stats_b = _agg_player(player_b)

    fig_radar = go.Figure()
    categories = ["Goals", "Assists", "Shots on Target", "Key Passes", "Tackles", "Rating"]
    fig_radar.add_trace(go.Scatterpolar(
        r=list(stats_a) + [stats_a.iloc[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=player_a,
        line_color=ACCENT,
        fillcolor=ACCENT + "33",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=list(stats_b) + [stats_b.iloc[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=player_b,
        line_color="#00b4d8",
        fillcolor="#00b4d833",
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor=SURFACE,
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#1e3a2a", color=TEXT_SECONDARY),
            angularaxis=dict(gridcolor="#1e3a2a", color=TEXT_PRIMARY),
        ),
        paper_bgcolor=SURFACE,
        font=dict(color=TEXT_PRIMARY),
        legend=dict(bgcolor=SURFACE, font=dict(color=TEXT_SECONDARY)),
        title_text="Normalised Player Radar",
        title_font_color=ACCENT,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # --- Section B: Goals vs Assists scatter ---
    st.subheader("Goals vs Assists")
    scatter_df = df.groupby(["player_name", "position"], as_index=False).agg(
        goals=("goals", "sum"),
        assists=("assists", "sum"),
        appearances=("appearances", "sum"),
    )
    fig_scat = px.scatter(
        scatter_df, x="assists", y="goals",
        color="position", size="appearances",
        hover_name="player_name",
        color_discrete_map=POSITION_COLORS,
        labels={"assists": "Total Assists", "goals": "Total Goals"},
        size_max=25,
    )
    _apply_template(fig_scat, "Goals vs Assists (sized by appearances)")
    st.plotly_chart(fig_scat, use_container_width=True)

    # --- Section C: Shots vs Goals with manual trend line ---
    st.subheader("Shots vs Goals (Conversion Rate)")
    sg_df = df.groupby("player_name", as_index=False).agg(
        goals=("goals", "sum"),
        shots=("shots", "sum"),
    )
    sg_df["conversion_rate"] = (sg_df["goals"] / sg_df["shots"].replace(0, 1) * 100).round(1)
    sg_df["hover"] = sg_df.apply(
        lambda r: f"{r['player_name']}<br>Goals: {r['goals']}<br>Shots: {r['shots']}<br>Conv: {r['conversion_rate']}%",
        axis=1,
    )

    fig_sg = px.scatter(
        sg_df, x="shots", y="goals",
        color="conversion_rate",
        hover_name="player_name",
        hover_data={"conversion_rate": True, "shots": True, "goals": True},
        color_continuous_scale=[[0, ACCENT2], [1, ACCENT]],
        labels={"shots": "Total Shots", "goals": "Total Goals", "conversion_rate": "Conv %"},
    )

    # Manual trend line via NumPy
    x_vals = sg_df["shots"].values.astype(float)
    y_vals = sg_df["goals"].values.astype(float)
    if len(x_vals) > 1:
        m, b = np.polyfit(x_vals, y_vals, 1)
        x_line = np.array([x_vals.min(), x_vals.max()])
        y_line = m * x_line + b
        fig_sg.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode="lines",
            name="Trend",
            line=dict(color="#e9c46a", dash="dash", width=2),
        ))

    _apply_template(fig_sg, "Shots vs Goals with Trend Line")
    st.plotly_chart(fig_sg, use_container_width=True)

# ---------------------------------------------------------------------------
# Page: Team Analysis
# ---------------------------------------------------------------------------

def render_team_analysis(df: pd.DataFrame):
    st.header("Team Analysis")

    if df.empty:
        st.warning("No data matches the selected filters.")
        return

    if df["team"].nunique() < 2:
        st.info("Showing data for a single team. Select more teams in the sidebar for cross-team comparison.")

    team_df = df.groupby("team").agg(
        total_goals=("goals", "sum"),
        total_assists=("assists", "sum"),
        squad_size=("player_id", "nunique"),
        avg_rating=("player_rating", "mean"),
    ).reset_index()
    team_df["avg_rating"] = team_df["avg_rating"].round(2)
    team_df = team_df.sort_values("total_goals", ascending=False)

    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(team_df, x="team", y="total_goals",
                     labels={"team": "Team", "total_goals": "Total Goals"},
                     color="total_goals",
                     color_continuous_scale=[[0, ACCENT2], [1, ACCENT]])
        fig.update_layout(xaxis_tickangle=-35)
        _apply_template(fig, "Total Goals per Team")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(team_df, x="team", y="total_assists",
                      labels={"team": "Team", "total_assists": "Total Assists"},
                      color="total_assists",
                      color_continuous_scale=[[0, ACCENT2], [1, ACCENT]])
        fig2.update_layout(xaxis_tickangle=-35)
        _apply_template(fig2, "Total Assists per Team")
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2
    col3, col4 = st.columns(2)
    with col3:
        fig3 = px.bar(team_df, x="team", y="squad_size",
                      labels={"team": "Team", "squad_size": "Squad Size"},
                      color="squad_size",
                      color_continuous_scale=[[0, ACCENT2], [1, ACCENT]])
        fig3.update_layout(xaxis_tickangle=-35)
        _apply_template(fig3, "Squad Size per Team")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.bar(team_df, x="team", y="avg_rating",
                      labels={"team": "Team", "avg_rating": "Avg Rating"},
                      color="avg_rating",
                      color_continuous_scale=[[0, ACCENT2], [1, ACCENT]])
        fig4.update_layout(xaxis_tickangle=-35)
        _apply_template(fig4, "Average Player Rating per Team")
        st.plotly_chart(fig4, use_container_width=True)

    # Row 3: stacked goals by position per team
    st.subheader("Goals by Position per Team")
    pos_team = df.groupby(["team", "position"], as_index=False)["goals"].sum()
    fig5 = px.bar(pos_team, x="team", y="goals",
                  color="position",
                  barmode="stack",
                  color_discrete_map=POSITION_COLORS,
                  labels={"team": "Team", "goals": "Goals", "position": "Position"})
    fig5.update_layout(xaxis_tickangle=-35)
    _apply_template(fig5, "Goals Breakdown by Position per Team")
    st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------------------------------
# Page: Position Analysis
# ---------------------------------------------------------------------------

def render_position_analysis(df: pd.DataFrame):
    st.header("Position Analysis")

    if df.empty:
        st.warning("No data matches the selected filters.")
        return

    pos_agg = df.groupby("position").agg(
        avg_goals=("goals", "mean"),
        avg_assists=("assists", "mean"),
        avg_rating=("player_rating", "mean"),
        avg_tackles=("tackles", "mean"),
    ).reset_index()
    pos_agg = pos_agg.round(2)

    # KPI cards per position
    st.subheader("Average Stats by Position")
    cols = st.columns(len(pos_agg))
    for col, (_, row) in zip(cols, pos_agg.iterrows()):
        with col:
            st.markdown(f"**{row['position']}**")
            st.metric("Avg Goals",    f"{row['avg_goals']:.1f}")
            st.metric("Avg Assists",  f"{row['avg_assists']:.1f}")
            st.metric("Avg Rating",   f"{row['avg_rating']:.2f}")
            st.metric("Avg Tackles",  f"{row['avg_tackles']:.1f}")

    st.markdown("---")

    # Box plots
    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(df, x="position", y="player_rating",
                     color="position",
                     color_discrete_map=POSITION_COLORS,
                     labels={"position": "Position", "player_rating": "Rating"},
                     points="outliers")
        _apply_template(fig, "Player Rating Distribution by Position")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.box(df, x="position", y="goals",
                      color="position",
                      color_discrete_map=POSITION_COLORS,
                      labels={"position": "Position", "goals": "Goals"},
                      points="outliers")
        _apply_template(fig2, "Goals Distribution by Position")
        st.plotly_chart(fig2, use_container_width=True)

    # Bar charts
    col3, col4 = st.columns(2)
    with col3:
        kp_agg = df.groupby("position", as_index=False)["key_passes"].mean().round(1)
        kp_agg.columns = ["position", "avg_key_passes"]
        fig3 = px.bar(kp_agg, x="position", y="avg_key_passes",
                      color="position",
                      color_discrete_map=POSITION_COLORS,
                      labels={"position": "Position", "avg_key_passes": "Avg Key Passes"})
        _apply_template(fig3, "Average Key Passes by Position")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        saves_agg = df.groupby("position", as_index=False)["saves"].mean().round(1)
        saves_agg.columns = ["position", "avg_saves"]
        fig4 = px.bar(saves_agg, x="position", y="avg_saves",
                      color="position",
                      color_discrete_map=POSITION_COLORS,
                      labels={"position": "Position", "avg_saves": "Avg Saves (GK-relevant)"})
        _apply_template(fig4, "Average Saves by Position (GK-relevant)")
        st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------------------------------
# Page: Data Table
# ---------------------------------------------------------------------------

def render_data_table(df: pd.DataFrame):
    st.header("Data Table")

    if df.empty:
        st.warning("No data matches the selected filters.")
        return

    search = st.text_input("Search player name...", key="dt_search")
    display_df = df[DISPLAY_COLUMNS].copy()

    if search:
        display_df = display_df[display_df["player_name"].str.contains(search, case=False, na=False)]
        if display_df.empty:
            st.info("No players match your search.")
            return

    st.markdown(f"**{len(display_df):,}** rows")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name="football_players_filtered.csv",
        mime="text/csv",
    )

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(
        page_title="Football Analytics",
        page_icon="soccer",
        layout="wide",
    )
    inject_custom_css()

    df = load_data()
    filters = render_sidebar(df)
    filtered_df = apply_filters(
        df,
        filters["seasons"],
        filters["teams"],
        filters["positions"],
        filters["player_name"],
    )

    page = filters["page"]
    if page == "Overview":
        render_overview(filtered_df)
    elif page == "Player Analysis":
        render_player_analysis(filtered_df)
    elif page == "Team Analysis":
        render_team_analysis(filtered_df)
    elif page == "Position Analysis":
        render_position_analysis(filtered_df)
    elif page == "Data Table":
        render_data_table(filtered_df)


if __name__ == "__main__":
    main()
