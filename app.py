import streamlit as st
from utils.api import get_match_data, get_hero_stats
from components.hero_tile import hero_tile
from components.draft import render_draft
from charts.advantage import plot_advantage_graph
from charts.role_barchart import plot_role_barchart
from components.player_table import render_player_table
import requests

st.set_page_config(layout="wide")

match_id = st.text_input("Enter Match ID", value="8448961923")

# ---------------------------
# Global CSS Styling
# ---------------------------
st.markdown("""
<style>
    body {
        background-color: #111; 
        color: #ddd;
        font-family: "Segoe UI", Roboto, sans-serif;
    }
    h1, h2, h3, h4 {
        color: #fff;
        font-weight: 600;
    }
    table.player-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1em;
    }
    table.player-table th, table.player-table td {
        padding: 6px 10px;
        text-align: left;
        font-size: 14px;
        border-bottom: 1px solid #444;
    }
    table.player-table th {
        background-color: #222;
        color: #fff;
    }
    .radiant-row { background-color: #1e4620; color: white; }
    .dire-row { background-color: #601010; color: white; }
    .hero-img { vertical-align: middle; margin-right: 8px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# UI
# ---------------------------




if match_id:
    try:
        match_data = get_match_data(match_id)
        hero_stats = get_hero_stats()

        render_player_table(match_data, hero_stats)


        picks_bans = match_data.get("picks_bans", [])
        draft_timings = match_data.get("draft_timings", [])

        if picks_bans:
            st.subheader("Pick/Ban Phase")
            render_draft(picks_bans, hero_stats, draft_timings)

            # Side-by-side charts
            st.subheader("Match Analysis")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Team Advantage Graph")
                adv_fig = plot_advantage_graph(match_data)
                if adv_fig:
                    st.pyplot(adv_fig)
                else:
                    st.info("No advantage data available.")

            with col2:
                st.subheader("Role Coverage")

                fig = plot_role_barchart(match_data)
                st.pyplot(fig)


        else:
            st.info("No pick/ban data available for this match.")

    except Exception as e:
        st.error(f"Failed to fetch match data: {e}")