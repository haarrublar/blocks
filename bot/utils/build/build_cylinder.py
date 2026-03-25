def get_cylinder_points(x, y, z, r, h, quad):
    """
    Variables: r (radius), h (height), quad (NW, NE, SW, SE)
    Anchor (x, z) is the corner of the cylinder's 2R+1 bounding box.
    """
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1
    
    xc = x + (sx * r)
    zc = z + (sz * r)
    
    points = []
    threshold = (r + 0.5)**2 
    
    for dy in range(h):
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if dx**2 + dz**2 <= threshold:
                    points.append((xc + dx, y + dy, zc + dz))
    return points

def build_cylinder(x, y, z, r, h, quad='NE', material="concrete", color=None, hollow=False):
    # Standardized: y is the base layer.
    y_start = y
    y_end = y + (h - 1)
    
    if color and material not in ["stone", "obsidian", "glowstone", "air"]:
        full_id = f"{color}_{material}"
    else:
        full_id = material
    
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1
    
    xc = x + (sx * r)
    zc = z + (sz * r)
    
    commands = []

    for dx in range(-r, r + 1):
        z_width = r - abs(dx)
        curr_x = xc + dx
        commands.append(f"/fill {curr_x} {y_start} {zc - z_width} {curr_x} {y_end} {zc + z_width} {full_id}")

    if hollow and r > 0:
        for dx in range(-(r - 1), r):
            z_inner = (r - 1) - abs(dx)
            curr_x = xc + dx
            commands.append(f"/fill {curr_x} {y_start + 1} {zc - z_inner} {curr_x} {y_end} {zc + z_inner} air")

    bounds = {
        "x_min": xc - r, "x_max": xc + r,
        "z_min": zc - r, "z_max": zc + r,
        "y_min": y_start, "y_max": y_end,
        "top": y_end + 1,
        "center_x": xc, "center_z": zc
    }

    return {"commands": commands, "bounds": bounds}

