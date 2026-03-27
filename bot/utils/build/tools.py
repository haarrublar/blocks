TOOLS = [
    {
        "name": "build_rectangle",
        "description": "Calculates Minecraft /fill commands using two absolute corner points. Required for precision stacking and boundary locking. Coordinates are inclusive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "x1": {"type": "integer", "description": "X coordinate of the first corner."},
                "y1": {"type": "integer", "description": "Y coordinate of the first corner (Base)."},
                "z1": {"type": "integer", "description": "Z coordinate of the first corner."},
                "x2": {"type": "integer", "description": "X coordinate of the opposite corner."},
                "y2": {"type": "integer", "description": "Y coordinate of the opposite corner (Top)."},
                "z2": {"type": "integer", "description": "Z coordinate of the opposite corner."},
                "color": {
                    "type": "string",
                    "description": "Optional color prefix (e.g., 'white', 'lime', 'light_gray'). You are NOT restricted to a list. Use any valid Minecraft color prefix."
                },
                "material": {
                    "type": "string",
                    "description": "The Minecraft block ID. You are NOT restricted to a list. Use any valid namespaced ID (e.g., 'minecraft:water', 'minecraft:oak_stairs', 'minecraft:sea_lantern') according to Minecraft."
                },
                "mode": {
                    "type": "string",
                    "default": "replace",
                    "enum": ["replace", "hollow", "outline", "keep", "destroy"],
                    "description": "CRITICAL for 3D architecture. Use 'hollow' to create rooms with 1-block thick walls and empty air inside. Use 'replace' for solid floors, ceilings, or foundations. Use 'outline' for just the skeletal edges of a box."
                },
                "no_ceiling": {
                    "type": "boolean", 
                    "default": False, 
                    "description": "If true, the top layer of the rectangle is removed (replaced with air)."
                }
            },
            "required": ["x1", "y1", "z1", "x2", "y2", "z2", "material"]
        }
    },
    {
        "name": "build_cylinder",
        "description": "Builds a circular structure or tower based on a Center Point (xc, zc). Use your internal knowledge for colors and materials. Perfect for domes, pillars, and silos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "xc": {"type": "integer", "description": "Center X coordinate."},
                "y_min": {"type": "integer", "description": "The base Y level."},
                "zc": {"type": "integer", "description": "Center Z coordinate."},
                "r": {"type": "integer", "description": "Radius of the cylinder."},
                "h": {"type": "integer", "description": "Total height."},
                "color": {
                    "type": "string",
                    "description": "Optional color prefix (e.g., 'white', 'cyan', 'black'). You are NOT restricted to a list."
                },
                "material": {
                    "type": "string",
                    "description": "The base block ID (e.g., 'concrete', 'stained_glass', 'wool'). You are NOT restricted to a list."
                },
                "mode": {
                    "type": "string",
                    "default": "replace",
                    "enum": ["replace", "hollow"],
                    "description": "Use 'hollow' for accessible towers or pipes, 'replace' for solid pillars or filled domes."
                }
            },
            "required": ["xc", "y_min", "zc", "r", "h", "material"]
        }
    }
]