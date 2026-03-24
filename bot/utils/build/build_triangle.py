def get_triangle_coords(x, y, z, r, h, s, quad, apex_dir, foundation=True, hollow=False):
    """
    Anchors the base using quadrant/buffer, then points the apex.
    Returns a list of row dicts ready to be sent as /fill commands.

    Args:
        x, y, z   : player position
        r         : half-width of base (base = 2r+1 wide)
        h         : height in blocks (vertical)
        s         : safety buffer
        quad      : "NW"|"NE"|"SW"|"SE"
        apex_dir  : "N"|"S"|"E"|"W"
        hollow    : if True, only outline rows are returned
        
    foundation=True:
        Pass 1 → solid h=1 at y-1 (clears grass, sets base floor)
        Pass 2 → actual structure at y with hollow/h as specified
    """
    sz = 1 if "S" in quad else -1

    # Base center — faithful to original (only Z is offset by quadrant)
    base_x = x
    base_z = z + (sz * (s + 1 + r))

    # Apex offset from base center
    if apex_dir == "N":
        apex_z = base_z - r
        z_step = -1
    elif apex_dir == "S":
        apex_z = base_z + r
        z_step = 1
    else:
        raise ValueError(f"apex_dir '{apex_dir}' (E/W) not supported in N/S quad anchor mode")

    y_end = y + (h - 1)
    rows = []

    for i in range(r + 1):          # i=0 → base, i=r → apex
        half_w  = r - i
        current_z = base_z + (z_step * i)
        x1 = base_x - half_w
        x2 = base_x + half_w

        is_edge = (i == 0 or i == r)

        if hollow and not is_edge:
            # Only the two side-edge blocks, skip interior
            rows.append({"x1": x1, "y1": y, "z1": current_z,
                         "x2": x1, "y2": y_end, "z2": current_z, "edge": True})
            rows.append({"x1": x2, "y1": y, "z1": current_z,
                         "x2": x2, "y2": y_end, "z2": current_z, "edge": True})
        else:
            rows.append({"x1": x1, "y1": y, "z1": current_z,
                         "x2": x2, "y2": y_end, "z2": current_z, "edge": is_edge})

    return rows

def build_triangle(x, y, z, r, h, apex_dir = 'N', 
                   quad = 'NE', s=4, material="stone", hollow=False, foundation=True, bot=None):

    y_start = (y - 1) if (foundation or hollow) else y
    rows = get_triangle_coords(x, y_start, z, r, h, s, quad, apex_dir, hollow=hollow)

    commands = [
        f"/fill {row['x1']} {row['y1']} {row['z1']} "
        f"{row['x2']} {row['y2']} {row['z2']} {material}"
        for row in rows
    ]

    return commands