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
    
    x1 = x
    z1 = z
    
    x2 = x1 + (sx * (w - 1))
    z2 = z1 + (sz * (l - 1))
    
    y2 = y + (h - 1)
    
    return (x1, y, z1), (x2, y2, z2)

def build_rectangle(x1, y1, z1, x2, y2, z2, material="stone", color=None, mode="replace", no_ceiling=False):
    """
    Builds a rectangle using absolute coordinates. 
    Intelligently merges colors and materials based on AI's internal knowledge.
    """
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    z_min, z_max = min(z1, z2), max(z1, z2)

    base_material = material.replace("minecraft:", "").lower()
    
    if color:
        base_color = color.replace("minecraft:", "").lower()
        full_material = f"minecraft:{base_color}_{base_material}"
    else:
        full_material = f"minecraft:{base_material}"

    commands = [f"/fill {x_min} {y_min} {z_min} {x_max} {y_max} {z_max} {full_material} {mode}"]

    if no_ceiling:
        commands.append(f"/fill {x_min} {y_max} {z_min} {x_max} {y_max} {z_max} minecraft:air replace")
    
    bounds = {
        "x_min": x_min, "x_max": x_max,
        "z_min": z_min, "z_max": z_max,
        "y_min": y_min, "y_max": y_max,
        "top": y_max
    }
    
    return {"commands": commands, "bounds": bounds}