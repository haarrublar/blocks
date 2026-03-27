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


import math

def build_cylinder(xc, y_min, zc, r, h, material="stone_bricks", color=None, mode="replace"):
    """
    Builds a cylinder using Center (xc, zc) and Radius (r).
    Intelligently merges colors and supports hollow interiors.
    """
    y_max = y_min + (h - 1)
    commands = []

    base_mat = material.replace("minecraft:", "").lower()
    if color:
        base_col = color.replace("minecraft:", "").lower()
        full_material = f"minecraft:{base_col}_{base_mat}"
    else:
        full_material = f"minecraft:{base_mat}"

    def get_fill_commands(radius, block_id, fill_mode):
        cmds = []
        for dx in range(-radius, radius + 1):
            dz_limit = int(math.sqrt(radius**2 - dx**2))
            curr_x = xc + dx
            z1 = zc - dz_limit
            z2 = zc + dz_limit
            cmds.append(f"/fill {curr_x} {y_min} {z1} {curr_x} {y_max} {z2} {block_id} {fill_mode}")
        return cmds

    commands.extend(get_fill_commands(r, full_material, mode))

    if mode == "hollow" and r > 0:
        commands.extend(get_fill_commands(r - 1, "minecraft:air", "replace"))

    bounds = {
        "x_min": xc - r, "x_max": xc + r,
        "z_min": zc - r, "z_max": zc + r,
        "y_min": y_min, "y_max": y_max,
        "top": y_max,
        "center_x": xc, "center_z": zc,
        "radius": r
    }

    return {"commands": commands, "bounds": bounds}