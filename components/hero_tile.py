def hero_tile(
    img_url,
    order=None,
    label=None,
    level=None,
    is_pick=True,
    size=80
):
    """
    Render a hero portrait tile with optional overlays.

    Args:
        img_url (str): Full hero portrait URL.
        order (int): Draft order number (for pick/ban phase).
        label (str): Text label to show under the portrait (e.g. time taken).
        level (int): Hero level (for player stats).
        is_pick (bool): If False, apply grayscale (for bans).
        size (int): Width of portrait in px.
    """

    overlays = ""

    # Draft order (top-right badge)
    if order is not None:
        order_display = (order or 0) + 1
        overlays += (
            f"<div style='position:absolute;top:0;right:0;"
            f"background:rgba(200,0,0,.6);color:#fff;font-size:10px;"
            f"padding:1px 3px;border-radius:3px;'>{order_display}</div>"
        )

    # Hero level (top-left badge)
    if level is not None:
        overlays += (
            f"<div style='position:absolute;top:0;left:0;"
            f"background:rgba(0,0,0,.7);color:#fff;font-size:11px;"
            f"padding:1px 4px;border-radius:3px;'>{level}</div>"
        )

    # Grayscale for bans
    gray = "filter:grayscale(100%);opacity:.5;" if not is_pick else ""

    # Build tile HTML
    html = (
        f"<div style='position:relative;display:inline-block;text-align:center;'>"
        f"<img src='{img_url}' width='{size}' style='{gray}border-radius:6px;'>"
        f"{overlays}"
    )

    # Optional label under portrait
    if label:
        html += f"<div style='font-size:12px;margin-top:2px;color:white;'>{label}</div>"

    html += "</div>"
    return html