TOOLS = [
    {
        "name": "build_rectangle",
        "description": "Calculates Minecraft /fill commands for a rectangular structure. Use this for rooms, walls, and towers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "w": {"type": "integer", "description": "Width of the structure (X-axis)."},
                "l": {"type": "integer", "description": "Length/Depth of the structure (Z-axis)."},
                "h": {"type": "integer", "description": "Total height (Y-axis)."},
                "quad": {
                    "type": "string", 
                    "enum": ["NW", "NE", "SW", "SE"], 
                    "description": "Direction relative to the player to place the build."
                },
                "material": {"type": "string", "default": "stone", "description": "Block type (e.g., stone, oak_planks)."},
                "hollow": {
                    "type": "boolean", 
                    "default": True, 
                    "description": "True to create a room with an interior air space. False for a solid block."
                },
                "foundation": {
                    "type": "boolean", 
                    "default": True, 
                    "description": "True to start the building 1 block deep (y-1) for a clean floor."
                }
            },
            "required": ["w", "l", "h", "quad"]
        }
    },
    {
        "name": "build_triangle",
        "description": "Calculates Minecraft /fill commands for a triangular structure. Use this for roofs, wedges, and pointed shapes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "r": {"type": "integer", "description": "Half-width of the base. Base will be 2r+1 blocks wide."},
                "h": {"type": "integer", "description": "Total height (Y-axis)."},
                "quad": {"type": "string", "enum": ["NW", "NE", "SW", "SE"], "description": "Direction relative to player."},
                "apex_dir": {"type": "string", "enum": ["N", "S"], "description": "Direction the tip of the triangle points."},
                "material": {"type": "string", "default": "stone", "description": "Block type (e.g., stone, oak_planks)."},
                "hollow": {"type": "boolean", "default": False, "description": "True for outline only, False for solid."},
                "foundation": {"type": "boolean", "default": True, "description": "True to dig 1 block down for a clean floor."}
            },
            "required": ["r", "h", "quad", "apex_dir"]
        }
    },
    {
        "name": "build_cylinder",
        "description": "Generates a diamond-shaped (rhombus) cylindrical structure. Uses a 45-degree diagonal grid for an airtight, geometric Minecraft look.",
        "input_schema": {
            "type": "object",
            "properties": {
                "r": {"type": "integer", "description": "Radius from the center to the points of the diamond."},
                "h": {"type": "integer", "description": "Total height (Y-axis)."},
                "quad": {
                    "type": "string", 
                    "enum": ["NW", "NE", "SW", "SE"], 
                    "description": "Direction relative to the player."
                },
                "material": {"type": "string", "default": "stone", "description": "Block ID (e.g., red_concrete)."},
                "hollow": {"type": "boolean", "default": True, "description": "True to carve out the interior with air."},
                "foundation": {"type": "boolean", "default": True, "description": "True to sink the floor 1 block into the ground."}
            },
            "required": ["r", "h", "quad"]
        }
    } 
]