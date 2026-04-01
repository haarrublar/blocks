TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "build_rectangle",
            "strict": True,
            "description": "Calculates Minecraft /fill commands using two absolute corner points. Required for precision stacking and boundary locking.",
            "parameters": {
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
                        "description": "Optional color prefix (e.g., 'white', 'lime')."
                    },
                    "material": {
                        "type": "string",
                        "description": "The Minecraft block ID (e.g., 'minecraft:stone')."
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["replace", "hollow", "outline", "keep", "destroy"],
                        "description": "Use 'hollow' for walls, 'replace' for solid structures."
                    },
                    "no_ceiling": {
                        "type": "boolean",
                        "description": "If true, the top layer is removed."
                    }
                },
                "required": ["x1", "y1", "z1", "x2", "y2", "z2", "material", "mode", "no_ceiling", "color"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "build_cylinder",
            "strict": True,
            "description": "Builds a circular structure or tower based on a Center Point (xc, zc).",
            "parameters": {
                "type": "object",
                "properties": {
                    "xc": {"type": "integer", "description": "Center X coordinate."},
                    "y_min": {"type": "integer", "description": "The base Y level."},
                    "zc": {"type": "integer", "description": "Center Z coordinate."},
                    "r": {"type": "integer", "description": "Radius of the cylinder."},
                    "h": {"type": "integer", "description": "Total height."},
                    "color": {
                        "type": "string",
                        "description": "Optional color prefix."
                    },
                    "material": {
                        "type": "string",
                        "description": "The base block ID."
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["replace", "hollow"],
                        "description": "Use 'hollow' for accessible towers."
                    }
                },
                "required": ["xc", "y_min", "zc", "r", "h", "material", "mode", "color"],
                "additionalProperties": False
            }
        }
    }
]