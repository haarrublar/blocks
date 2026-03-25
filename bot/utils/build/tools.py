TOOLS = [
    {
        "name": "build_rectangle",
        "description": "Calculates Minecraft /fill commands for a rectangular structure. Best for rooms, walls, and floors. Follows syntax: /fill x1 y1 z1 x2 y2 z2 [color]_[block] [mode].",
        "input_schema": {
            "type": "object",
            "properties": {
                "x": {"type": "integer"}, "y": {"type": "integer"}, "z": {"type": "integer"},
                "w": {"type": "integer", "description": "Width (X-axis)."},
                "l": {"type": "integer", "description": "Length/Depth (Z-axis)."},
                "h": {"type": "integer", "description": "Total height (Y-axis)."},
                "quad": {
                    "type": "string", 
                    "enum": ["NW", "NE", "SW", "SE"], 
                    "description": "Growth direction relative to anchor."
                },
                "color": {
                    "type": "string",
                    "description": "Optional color prefix (e.g., 'blue', 'red', 'lime').",
                    "enum": ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]
                },
                "material": {
                    "type": "string",
                    "description": "The base block type. If a color is provided, it combines as color_material.",
                    "enum": [
                        "stone", "stone_bricks", "cobblestone", "mossy_cobblestone",
                        "wool", "concrete", "terracotta", "glass", "stained_glass",
                        "planks", "log", "wood", "bricks", "sandstone",
                        "obsidian", "glowstone", "sea_lantern", "lapis_block", "gold_block", "air"
                    ]
                },
                "mode": {
                    "type": "string",
                    "default": "replace",
                    "enum": ["replace", "hollow", "outline", "keep", "destroy"],
                    "description": "Minecraft fill mode logic."
                },
                "hollow": {"type": "boolean", "default": False},
            },
            "required": ["x", "y", "z", "w", "l", "h", "quad", "material"]
        }
    },
    {
        "name": "build_cylinder",
        "description": "Generates a rhombus-shaped cylinder. Ideal for towers. Anchor is the quadrant tip.",
        "input_schema": {
            "type": "object",
            "properties": {
                "x": {"type": "integer"}, "y": {"type": "integer"}, "z": {"type": "integer"},
                "r": {"type": "integer", "description": "Radius from center to diamond tips."},
                "h": {"type": "integer", "description": "Total height (Y-axis)."},
                "quad": {"type": "string", "enum": ["NW", "NE", "SW", "SE"]},
                "color": {
                    "type": "string", 
                    "enum": ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]
                },
                "material": {
                    "type": "string", 
                    "enum": [
                        "stone", "stone_bricks", "cobblestone", "mossy_cobblestone",
                        "wool", "concrete", "terracotta", "glass", "stained_glass",
                        "planks", "log", "wood", "bricks", "sandstone",
                        "obsidian", "glowstone", "sea_lantern", "lapis_block", "gold_block", "air"
                    ]
                },
                "hollow": {"type": "boolean", "default": False},
            },
            "required": ["x", "y", "z", "r", "h", "quad", "material"]
        }
    }
]