def get_rectangular_coords(x, y, z, w, l, h, s, quad):
    """
    Calculates the two corner points (x1,y1,z1 and x2,y2,z2) for a Minecraft /fill box.
    
    Args:
        x, y, z : Player position (origin)
        w, l, h : Width (X), Length (Z), and Height (Y) of the rectangle
        s       : Safety buffer (blocks of air between player and structure)
        quad    : "NW"|"NE"|"SW"|"SE" determines the growth direction
    """
    sx = 1 if "E" in quad else -1
    sz = 1 if "S" in quad else -1

    x1 = x + (sx * (s + 1))
    z1 = z + (sz * (s + 1))
    x2 = x1 + (sx * (w - 1))
    z2 = z1 + (sz * (l - 1))
    y2 = y + (h - 1)

    return (x1, y, z1), (x2, y2, z2)

def build_rectangle(x, y, z, w, l, h, s = 4, quad = 'NE', 
                    material="stone", hollow=False, foundation=True):
    """
    Generates a list of /fill commands to construct a rectangle.
    Logic:
    - If 'foundation' or 'hollow' is True, the start Y is shifted to y-1. 
    - This allows the building to sit inside the ground.
    - If 'hollow' is True, a second /fill command with 'air' clears the 
      interior from y-1 upward, leaving only the 1-block thick borders/walls.
    """
    y_start = (y - 1) if (foundation or hollow) else y
    (x1, y1, z1), (x2, y2, z2) = get_rectangular_coords(x, y_start, z, w, l, h, s, quad)
    commands = [f"/fill {x1} {y1} {z1} {x2} {y2} {z2} {material}"]

    if hollow:
        ix1, ix2 = sorted([x1, x2])
        iz1, iz2 = sorted([z1, z2])
        commands.append(f"/fill {ix1+1} {y1} {iz1+1} {ix2-1} {y2} {iz2-1} air")

    return commands

