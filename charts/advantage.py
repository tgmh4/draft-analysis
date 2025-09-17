# charts/advantage.py

import matplotlib.pyplot as plt

def plot_advantage_graph(match_data):
    """Generate XP and Gold advantage line chart. Returns matplotlib fig."""
    xp = match_data.get("radiant_xp_adv", [])
    gold = match_data.get("radiant_gold_adv", [])

    if not xp or not gold:
        return None  # Let caller handle empty data

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

    return fig