def get_rectangular_coords(x, y, z, w, l, h, quad):
    """
    Calculates the two corner points (x1,y1,z1 and x2,y2,z2) for a Minecraft /fill box.
    
    Args:
        x, y, z : Player position (origin)
        w, l, h : Width (X), Length (Z), and Height (Y) of the rectangle
        quad    : "NW"|"NE"|"SW"|"SE" determines the growth direction
    """
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1
    
    x1 = x + (sx)
    z1 = z + (sz)
    x2 = x1 + (sx * (w - 1))
    z2 = z1 + (sz * (l - 1))
    y2 = y + (h - 1)
    
    return (x1, y, z1), (x2, y2, z2)

def build_rectangle(x, y, z, w, l, h, quad='NE', material="stone", color=None, mode="replace"):
    y_start = y
    y_end = y + (h - 1)
    
    (x1, y1, z1), (x2, y2, z2) = get_rectangular_coords(x, y_start, z, w, l, h, quad)
    
    full_id = f"{color}_{material}" if color else material
    command = f"/fill {x1} {y1} {z1} {x2} {y2} {z2} {full_id} {mode}"

    bounds = {
            "x_min": min(x1, x2), "x_max": max(x1, x2),
            "z_min": min(z1, z2), "z_max": max(z1, z2),
            "y_min": y_start, "y_max": y_end,
            "top": y_end + 1,
            "anchor_x": x, "anchor_z": z
        }
    
    return {
        "commands": [command],
        "bounds": bounds
    }

