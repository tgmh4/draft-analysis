import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ---------------------------
# Helpers
# ---------------------------

@st.cache_data
def get_match_data(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    response = requests.get(url)
    return response.json()

@st.cache_data
def get_hero_stats():
    url = "https://api.opendota.com/api/heroes"
    response = requests.get(url)
    return {hero['id']: hero for hero in response.json()}

def hero_tile(img_url, order, label, is_pick=True):
    order_display = order + 1  # start numbering at 1
    if is_pick:
        return f"""
        <div style="position:relative; display:inline-block; text-align:center;">
            <img src="{img_url}" width="80" style="border-radius:6px;">
            <div style="position:absolute; top:2px; left:4px;
                        background-color:rgba(0,0,0,0.1); color:white;
                        font-size:10px; padding:1px 4px; border-radius:3px;">
                {order_display}
            </div>
            <div style="font-size:12px; margin-top:2px;">{label}</div>
        </div>
        """
    else:
        return f"""
        <div style="position:relative; display:inline-block; text-align:center;">
            <img src="{img_url}" width="80" style="filter:grayscale(100%); opacity:0.5; border-radius:6px;">
            <div style="position:absolute; top:2px; left:4px;
                        background-color:rgba(0,0,0,0.1); color:white;
                        font-size:10px; padding:1px 4px; border-radius:3px;">
                {order_display}
            </div>
            <div style="font-size:12px; margin-top:2px;">{label}</div>
        </div>
        """

def plot_advantage_graph(match_data):
    xp = match_data.get("radiant_xp_adv", [])
    gold = match_data.get("radiant_gold_adv", [])

    if not xp or not gold:
        st.info("No gold/XP advantage data available for this match.")
        return

    time_axis = list(range(len(xp)))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(time_axis, xp, label="XP Advantage", color="blue")
    ax.plot(time_axis, gold, label="Gold Advantage", color="gold")

    ax.set_xlabel("Minutes")
    ax.set_ylabel("Advantage")
    ax.set_title("Team Advantage Over Time")

    tick_positions = range(0, len(time_axis), 3)
    tick_labels = [f"{t}:00" for t in tick_positions]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, fontsize=7)

    ax.axhline(0, color="black", linewidth=1)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_facecolor("lightgray")

    st.pyplot(fig)

# ---------------------------
# UI
# ---------------------------

st.title("Dota 2 Match Dashboard")

match_id = st.text_input("Enter Match ID", value="8448961923")

if match_id:
    try:
        match_data = get_match_data(match_id)
        hero_stats = get_hero_stats()

        picks_bans = match_data.get("picks_bans", [])
        draft_timings = match_data.get("draft_timings", [])

        if picks_bans:
            st.subheader("Pick/Ban Phase")

            picks_bans = sorted(picks_bans, key=lambda x: x["order"])
            timing_lookup = {dt["order"]: dt for dt in draft_timings}

            st.markdown("**Radiant**")
            radiant = [pb for pb in picks_bans if pb["team"] == 0]
            cols_r = st.columns(len(radiant))
            for i, pb in enumerate(radiant):
                hero = hero_stats.get(pb["hero_id"])
                if hero:
                    hero_code = hero["name"].replace("npc_dota_hero_", "")
                    img_url = f"https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/{hero_code}_full.png"
                    dt = timing_lookup.get(pb.get("order"))
                    label = f"🕒 {dt['total_time_taken']}s" if dt else ""
                    html = hero_tile(img_url, pb["order"], label, is_pick=pb["is_pick"])
                    cols_r[i].markdown(html, unsafe_allow_html=True)

            st.markdown("**Dire**")
            dire = [pb for pb in picks_bans if pb["team"] == 1]
            cols_d = st.columns(len(dire))
            for i, pb in enumerate(dire):
                hero = hero_stats.get(pb["hero_id"])
                if hero:
                    hero_code = hero["name"].replace("npc_dota_hero_", "")
                    img_url = f"https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/{hero_code}_full.png"
                    dt = timing_lookup.get(pb.get("order"))
                    label = f"🕒 {dt['total_time_taken']}s" if dt else ""
                    html = hero_tile(img_url, pb["order"], label, is_pick=pb["is_pick"])
                    cols_d[i].markdown(html, unsafe_allow_html=True)

            # ---------------------------
            # Advantage Graph
            # ---------------------------
            st.subheader("Team Advantage Graph")
            plot_advantage_graph(match_data)


            # ---------------------------
            # Role Coverage Heatmap
            # ---------------------------
            st.subheader("Role Coverage Heatmap")

            heroes = requests.get("https://api.opendota.com/api/heroes").json()
            df_roles = []
            for h in heroes:
                for r in h["roles"]:
                    df_roles.append({"hero_id": h["id"], "role": r})
            df_roles = pd.DataFrame(df_roles)

            radiant_ids = [p["hero_id"] for p in match_data["players"] if p["isRadiant"]]
            dire_ids = [p["hero_id"] for p in match_data["players"] if not p["isRadiant"]]

            df_radiant = df_roles[df_roles["hero_id"].isin(radiant_ids)]
            df_dire = df_roles[df_roles["hero_id"].isin(dire_ids)]

            all_roles = sorted(df_roles["role"].unique())
            rad_counts = df_radiant["role"].value_counts().reindex(all_roles, fill_value=0)
            dire_counts = df_dire["role"].value_counts().reindex(all_roles, fill_value=0)

            role_counts = pd.DataFrame({
                "Role": all_roles,
                "Radiant": rad_counts.values,
                "Dire": dire_counts.values
            })

            overlap = st.checkbox("Show overlap in one chart", value=False)

            if overlap:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.heatmap(
                    role_counts.set_index("Role")[["Radiant", "Dire"]],
                    annot=True, fmt="d", cmap="coolwarm", cbar=True, ax=ax
                )
                ax.set_title("Radiant vs Dire Role Coverage")
                st.pyplot(fig)
            else:
                fig1, ax1 = plt.subplots(figsize=(4, 4))
                sns.heatmap(
                    role_counts.set_index("Role")[["Radiant"]],
                    annot=True, fmt="d", cmap="Greens", cbar=False, ax=ax1
                )
                ax1.set_title("Radiant Role Coverage")
                st.pyplot(fig1)

                fig2, ax2 = plt.subplots(figsize=(4, 4))
                sns.heatmap(
                    role_counts.set_index("Role")[["Dire"]],
                    annot=True, fmt="d", cmap="Reds", cbar=False, ax=ax2
                )
                ax2.set_title("Dire Role Coverage")
                st.pyplot(fig2)


        else:
            st.info("No pick/ban data available for this match.")

    except Exception as e:
        st.error(f"Failed to fetch match data: {e}")