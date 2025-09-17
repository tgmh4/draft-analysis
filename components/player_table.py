import streamlit as st
from components.hero_tile import hero_tile

def render_player_table(match_data, hero_stats):
    players = match_data.get("players", [])
    if not players:
        st.info("No player data available for this match.")
        return

    role_map = {1:"Safe Lane", 2:"Mid Lane", 3:"Off Lane", 4:"Support", 5:"Hard Support"}

    def build_table(team_players, team_class, team_name):
        table_html = (
            "<table class='player-table'>"
            "<thead><tr><th>Hero</th><th>Lane</th><th>Player</th>"
            "<th>KDA</th><th>Net Worth</th><th>GPM</th><th>XPM</th></tr></thead><tbody>"
        )

        sum_kills = sum_deaths = sum_assists = 0
        sum_net = sum_gpm = sum_xpm = 0

        for p in team_players:
            hero = hero_stats.get(p.get("hero_id"))
            if not hero:
                continue
            code = hero["name"].replace("npc_dota_hero_", "")
            img_url = f"https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/{code}_full.png"

            k, d, a = p.get("kills",0), p.get("deaths",0), p.get("assists",0)
            kda = f"{k}/{d}/{a}"
            lane = role_map.get(p.get("lane_role"), "Unknown")
            net, gpm, xpm = p.get("net_worth",0), p.get("gold_per_min",0), p.get("xp_per_min",0)
            lvl = p.get("level", 0)

            sum_kills += k; sum_deaths += d; sum_assists += a
            sum_net += net; sum_gpm += gpm; sum_xpm += xpm

            hero_html = hero_tile(img_url, level=lvl, is_pick=True, size=80)

            table_html += (
                f"<tr class='{team_class}'>"
                f"<td>{hero_html}</td>"
                f"<td>{lane}</td>"
                f"<td>{p.get('personaname','Anonymous')}</td>"
                f"<td>{kda}</td>"
                f"<td>{net}</td>"
                f"<td>{gpm}</td>"
                f"<td>{xpm}</td>"
                "</tr>"
            )

        # Totals row
        table_html += (
            f"<tr style='font-weight:bold;background:#333;color:#fff;'>"
            f"<td colspan='3'>Total</td>"
            f"<td>{sum_kills}/{sum_deaths}/{sum_assists}</td>"
            f"<td>{sum_net}</td>"
            f"<td>{sum_gpm}</td>"
            f"<td>{sum_xpm}</td>"
            "</tr></tbody></table>"
        )
        return table_html

    radiant = [p for p in players if p.get("isRadiant")]
    dire = [p for p in players if not p.get("isRadiant")]

    st.markdown(build_table(radiant, "radiant-row", "Radiant"), unsafe_allow_html=True)
    st.markdown(build_table(dire, "dire-row", "Dire"), unsafe_allow_html=True)