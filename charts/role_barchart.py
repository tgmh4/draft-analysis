# charts/role_barchart.py
import matplotlib.pyplot as plt
import pandas as pd
import requests

def plot_role_barchart(match_data):
    """Plot a mirrored horizontal bar chart of role counts (Radiant vs Dire)."""

    # Fetch hero role metadata
    heroes = requests.get("https://api.opendota.com/api/heroes").json()
    df_roles = []
    for h in heroes:
        for r in h["roles"]:
            df_roles.append({"hero_id": h["id"], "role": r})
    df_roles = pd.DataFrame(df_roles)

    # Match heroes by side
    radiant_ids = [p["hero_id"] for p in match_data["players"] if p["isRadiant"]]
    dire_ids = [p["hero_id"] for p in match_data["players"] if not p["isRadiant"]]

    radiant_df = df_roles[df_roles["hero_id"].isin(radiant_ids)]
    dire_df = df_roles[df_roles["hero_id"].isin(dire_ids)]

    all_roles = sorted(df_roles["role"].unique())
    rad_counts = radiant_df["role"].value_counts().reindex(all_roles, fill_value=0)
    dire_counts = dire_df["role"].value_counts().reindex(all_roles, fill_value=0)

    # Plot mirrored bar chart
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="black")
    y_pos = range(len(all_roles))

    ax.barh(y_pos, -rad_counts.values, color="#4CAF50", label="Radiant")  # left
    ax.barh(y_pos, dire_counts.values, color="#F44336", label="Dire")     # right

    ax.set_yticks(y_pos)
    ax.set_yticklabels(all_roles, color="white")
    ax.axvline(0, color="white", linewidth=1)

    ax.set_title("Role Distribution (Radiant vs Dire)", color="white")

    # Style tweaks
    ax.tick_params(colors="white")


    fig.tight_layout()
    return fig