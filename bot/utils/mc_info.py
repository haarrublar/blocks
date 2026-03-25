MCINFO =  {
  "system_metadata": {
    "version": "1.2",
    "target_app": "Minecraft Java/Bedrock",
    "description": "Contextual guide for structural generation and block selection."
  },
  "syntax_rules": {
    "fill_region": "/fill <x1> <y1> <z1> <x2> <y2> <z2> <ID_CONSTANT> <MODE_CONSTANT>",
    "place_block": "/setblock <x> <y> <z> <ID_CONSTANT> [replace|keep|destroy]",
    "coordinate_format": "Use relative (~) or absolute integers. Calculate x2/y2/z2 based on width/height/length."
  },
  "variable_mapping": {
    "<ID_CONSTANT>": {
      "source_path": "material_palette.*.id",
      "instruction": "Select the literal string from the 'id' field only. Ignore 'usage' and 'placement' during command assembly."
    },
    "<MODE_CONSTANT>": {
      "source_path": "fill_modes.*",
      "instruction": "Select the key name of the mode that matches the structural goal."
    }
  },
  "fill_modes": {
    "replace": "Default mode. Fills the entire volume solid.",
    "hollow": "Rectangle only: Creates a hollow shell with air inside. Best for rooms.",
    "outline": "Rectangle only: Creates a shell but preserves existing blocks inside.",
    "keep": "Fills only air blocks. Great for adding detail to any shape.",
    "destroy": "Replaces blocks and drops them as items (mining style)."
  },
  "material_palette": {
    "stone_variants": [
      { "id": "stone", "usage": "Basic solid construction" },
      { "id": "stone_bricks", "usage": "Refined/clean walls" },
      { "id": "cobblestone", "usage": "Rough/rustic foundations" }
    ],
    "wood_variants": [
      { "id": "oak_planks", "usage": "Core building material" },
      { "id": "spruce_planks", "usage": "Darker aesthetic wood" },
      { "id": "oak_log", "usage": "Natural pillars and framing" }
    ],
    "decorative": [
      { "id": "sandstone", "usage": "Light/warm walls" },
      { "id": "glass", "usage": "Transparent windows" },
      { "id": "bricks", "usage": "Classic sturdy exterior" },
      { "id": "bookshelf", "usage": "Interior library/decor" }
    ],
    "lighting": [
      { "id": "torch", "placement": "walls/floor", "intensity": "low" },
      { "id": "glowstone", "placement": "ceiling/floors", "intensity": "high" },
      { "id": "redstone_lamp", "placement": "ceiling", "intensity": "high" },
      { "id": "sea_lantern", "placement": "modern/underwater", "intensity": "high" }
    ],
    "nature": [
      { "id": "grass_block", "usage": "Ground and landscaping" },
      { "id": "snow_block", "usage": "Cold environments" },
      { "id": "mycelium", "usage": "Fungal/dark terrain" }
    ],
    "utility": [
      { "id": "oak_stairs", "usage": "Angled roofs and seating" },
      { "id": "stone_slab", "usage": "Half-height detailing" }
    ],
    "special": [
      { "id": "obsidian", "usage": "Blast-resistant structures" },
      { "id": "ice", "usage": "Slippery surfaces" },
      { "id": "lava", "usage": "Hazardous light/traps" }
    ]
  },
  "special_logic": {
    "doors": "Requires two /setblock commands: [half=lower] and [half=upper].",
    "slabs": "Specify [type=top] or [type=bottom] for placement height.",
    "stairs": "Specify [facing=north|south|east|west] and [half=bottom|top]."
  },
  "output_constraints": [
    "NEVER include the words 'usage', 'placement', or 'intensity' in the final command.",
    "Always resolve <ID_CONSTANT> to a single string from the palette.",
    "If a light source is requested for a ceiling, prioritize 'glowstone' or 'sea_lantern'."
  ]
}
