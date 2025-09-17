import streamlit as st
from components.hero_tile import hero_tile

def render_draft(picks_bans, hero_stats, draft_timings):
    if not picks_bans:
        st.info("No pick/ban data available for this match.")
        return

    picks_bans = sorted(picks_bans, key=lambda x: x["order"])
    timing_lookup = {dt["order"]: dt for dt in draft_timings}

    radiant = [pb for pb in picks_bans if pb["team"] == 0]
    dire = [pb for pb in picks_bans if pb["team"] == 1]

    # Radiant row
    radiant_html = "<div style='background:#1e4620;padding:8px;display:flex;gap:8px;flex-wrap:wrap;'>"
    for pb in radiant:
        hero = hero_stats.get(pb["hero_id"])
        if not hero:
            continue
        code = hero["name"].replace("npc_dota_hero_", "")
        img_url = f"https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/{code}_full.png"
        dt = timing_lookup.get(pb.get("order"))
        label = f"🕒 {dt['total_time_taken']}s" if dt else ""
        radiant_html += hero_tile(img_url, order=pb["order"], label=label, is_pick=pb["is_pick"])
    radiant_html += "</div>"

    st.components.v1.html(radiant_html, height=130, scrolling=False)

    # Dire row
    dire_html = "<div style='background:#601010;padding:8px;display:flex;gap:8px;flex-wrap:wrap;'>"
    for pb in dire:
        hero = hero_stats.get(pb["hero_id"])
        if not hero:
            continue
        code = hero["name"].replace("npc_dota_hero_", "")
        img_url = f"https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/{code}_full.png"
        dt = timing_lookup.get(pb.get("order"))
        label = f"🕒 {dt['total_time_taken']}s" if dt else ""
        dire_html += hero_tile(img_url, order=pb["order"], label=label, is_pick=pb["is_pick"])
    dire_html += "</div>"

    st.components.v1.html(dire_html, height=130, scrolling=False)