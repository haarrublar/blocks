import math
import os
import json
import uuid
from fastmcp import FastMCP

HISTORY_FILE = "./.gemini/build_history.json"

mcp = FastMCP(name="minecraft")

@mcp.tool
def build_rectangle(x1, y1, z1, x2, y2, z2, id, material="stone", color=None, mode="replace", no_ceiling=False):
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
    
    return {"id": id, "commands": commands, "bounds": bounds}

@mcp.tool
def build_cylinder(xc, y_min, zc, r, h, id, material="stone_bricks", color=None, mode="replace"):
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

    return {"id": id, "commands": commands, "bounds": bounds}


@mcp.tool
def append_build_log(content: dict, filename: str = "build_log.json"):
    """
    Appends a single build record to a flat list in a file.
    No session management required.
    """
    import os
    import json

    records = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                records = json.load(f)
                if not isinstance(records, list):
                    records = [] 
            except json.JSONDecodeError:
                records = []

    records.append(content)

    with open(filename, "w") as f:
        json.dump(records, f, indent=4)

    return f"✅ Build saved to {filename}"

if __name__ == "__main__":
    mcp.run()