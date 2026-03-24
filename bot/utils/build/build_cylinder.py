import math

def get_cylinder_points(x, y, z, r, h, s, quad):
    """
    Variables: r (radius), h (height), s (buffer), quad (NW, NE, SW, SE)
    Functionality: Returns a list of (x, y, z) points forming a solid or hollow cylinder.
    """
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1
    
    xc = x + (sx * (r + s + 1))
    zc = z + (sz * (r + s + 1))
    points = []
    
    for dy in range(h):
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if dx**2 + dz**2 <= (r + 0.5)**2:
                    points.append((xc + dx, y + dy, zc + dz))
    return points


def build_cylinder(x, y, z, r, h, s=4, quad='NE', 
                   material="red_concrete", hollow=True, foundation=True):
    """
    Creates a diamond-shaped (rhombus) cylinder.
    Uses a solid shell pass and an inner 'air' pass for perfect hollowing.
    """
    y_start = (y - 1) if (foundation or hollow) else y
    y_end = y_start + (h - 1)
    
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1
    xc = x + (sx * (r + s + 1))
    zc = z + (sz * (r + s + 1))
    
    commands = []

    for dx in range(-r, r + 1):
        z_width = r - abs(dx)
        x_pos = xc + dx
        commands.append(f"/fill {x_pos} {y_start} {zc - z_width} {x_pos} {y_end} {zc + z_width} {material}")

    if hollow and r > 0:
        for dx in range(-(r - 1), r):
            z_inner = (r - 1) - abs(dx)
            x_pos = xc + dx
            commands.append(f"/fill {x_pos} {y_start + 1} {zc - z_inner} {x_pos} {y_end} {zc + z_inner} air")

    return commands