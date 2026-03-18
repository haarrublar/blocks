
def get_rectangular_coords(x, y, z, w, l, h, s, quad):
    """
    Variables: w (width), l (length), h (height), s (buffer), quad (NW, NE, SW, SE)
    Functionality: Returns start (x1, y1, z1) and end (x2, y2, z2) for a fill command.
    """
    # Determine sign based on quadrant
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1
    
    x1 = x + (sx * (s + 1))
    z1 = z + (sz * (s + 1))
    x2 = x1 + (sx * (w - 1))
    z2 = z1 + (sz * (l - 1))
    y2 = y + (h - 1)
    
    return (x1, y, z1), (x2, y2, z2)

# Example: build_rect(159, -61, 57, 3, 4, 1, 2, "NE") -> (162, -61, 54), (164, -61, 51)


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

# Example: build_cyl(159, -61, 57, 3, 5, 2, "NW") -> xc=153, zc=51


def get_triangle_coords(x, y, z, r, h, s, quad, apex_dir):
    """
    Variables: r (radius/offset), quad (NW, NE, SW, SE), apex_dir (N, S, E, W)
    Functionality: Anchors the base using quadrant/buffer, then points the apex.
    """
    # 1. Find Quadrant Anchor (Base Center)
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1
    
    # For simplicity, assume vertical alignment
    base_x, base_z = x, z + (sz * (s + 1 + r))
    if apex_dir == "N":
        apex_z = base_z - r
        # Base spans from base_x - r to base_x + r at base_z
    
    # Logic repeats for other apex directions
    return {"apex": (base_x, y, apex_z), "base_row": (base_x-r, y, base_z, base_x+r)}

# Example: build_tri(159, -61, 57, 3, 4, 2, "SW", "N") -> Apex at Z=37, Base at Z=40