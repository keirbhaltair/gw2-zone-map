portals: dict[str, list[tuple[float, float] | tuple[float, float, float, float]]] = {
    'neighbor': [
        (23917, 21207, 24102, 22074),  # Amnytas - The Wizard's Tower
        (29185, 100890, 28630, 100660),  # Arborstone - New Kaineng City
        (29386, 101353),  # Arborstone - The Echovald Wilds (W)
        (30027, 101563),  # Arborstone - The Echovald Wilds (E)
        (34667, 33685, 35414, 33650),  # Auric Basin - Gilded Hollow
        (35328, 35000),  # Auric Basin - Tangled Depths
        (33601, 32512),  # Auric Basin - Verdant Brink
        (54109, 24576),  # Bitterfrost Frontier - Frostgorge Sound
        (56957, 29952),  # Black Citadel - Diessa Plateau
        (57856, 30642),  # Black Citadel - Plains of Ashford
        (62221, 32640),  # Blazeridge Steppes - Fields of Ruin (W)
        (63746, 32640),  # Blazeridge Steppes - Fields of Ruin (E)
        (61952, 28907),  # Blazeridge Steppes - Iron Marches
        (61952, 31250),  # Blazeridge Steppes - Plains of Ashford
        (49465, 33014),  # Bloodtide Coast - Chantry of Secrets
        (49587, 32256),  # Bloodtide Coast - Lion's Arch
        (50432, 32410),  # Bloodtide Coast - Lornar's Pass (N)
        (50432, 34198),  # Bloodtide Coast - Lornar's Pass (S)
        (48298, 35456),  # Bloodtide Coast - Sparkfly Fen (W)
        (50068, 35456),  # Bloodtide Coast - Sparkfly Fen (E)
        (42112, 32688),  # Brisban Wildlands - Caledon Forest
        (38656, 33348),  # Brisban Wildlands - Dry Top
        (42112, 30980),  # Brisban Wildlands - Kessex Hills
        (40789, 33536),  # Brisban Wildlands - Metrica Province
        (38656, 31787),  # Brisban Wildlands - The Silverwastes
        (43853, 32512),  # Caledon Forest - Kessex Hills
        (42112, 34045),  # Caledon Forest - Metrica Province
        (42723, 36480),  # Caledon Forest - The Grove
        (60724, 42304),  # Crystal Oasis - Desert Highlands
        (61224, 44864),  # Crystal Oasis - Elon Riverlands
        (59530, 29952),  # Diessa Plateau - Plains of Ashford
        (56320, 28375),  # Diessa Plateau - Wayfarer Foothills
        (44928, 26911),  # Divinity's Reach - Lake Doric
        (43994, 26969, 42968, 23710),  # Divinity's Reach - Lowland Shore
        (43932, 28032),  # Divinity's Reach - Queensdale
        (65535, 59576),  # Domain of Kourna - Domain of Vabbi
        (67060, 55552, 66275, 56376),  # Domain of Vabbi - Jahai Bluffs
        (63616, 52695, 61824, 52684),  # Domain of Vabbi - The Desolation
        (64565, 52352),  # Domain of Vabbi - Windswept Haven
        (33076, 102081),  # Dragon's End - The Echovald Wilds
        (35700, 36096),  # Dragon's Stand - Tangled Depths (W)
        (37104, 36096),  # Dragon's Stand - Tangled Depths (E)
        (53695, 31360),  # Dredgehaunt Cliffs - Hoelbrak
        (52224, 32856),  # Dredgehaunt Cliffs - Lornar's Pass
        (53414, 34560),  # Dredgehaunt Cliffs - Timberline Falls
        (60095, 48192),  # Elon Riverlands - The Desolation (W)
        (61434, 48192),  # Elon Riverlands - The Desolation (E)
        (56576, 26174),  # Fireheart Rise - Frostgorge Sound
        (59904, 27082),  # Fireheart Rise - Iron Marches
        (53756, 27648),  # Frostgorge Sound - Snowden Drifts
        (55830, 27648),  # Frostgorge Sound - Wayfarer Foothills
        (47113, 28672),  # Gendarran Fields - Harathi Hinterlands (W)
        (48510, 28672),  # Gendarran Fields - Harathi Hinterlands (E)
        (46208, 30565),  # Gendarran Fields - Kessex Hills
        (50432, 30014),  # Gendarran Fields - Lornar's Pass
        (48809, 30720),  # Gendarran Fields - Lion's Arch
        (50432, 29140),  # Gendarran Fields - Snowden Drifts
        (46208, 29081),  # Gendarran Fields - Queensdale
        (37396, 100747, 28541, 100046),  # Gyala Delve - New Kaineng City
        (46208, 26478),  # Harathi Hinterlands - Lake Doric
        (54528, 30863),  # Hoelbrak - Wayfarer Foothills
        (22285, 23842, 23646, 22331),  # Inner Nayos - The Wizard's Tower
        (21825, 104390, 24354, 102531),  # Isle of Reflection - Seitung Province
        (60989, 29952),  # Iron Marches - Plains of Ashford
        (40533, 16970, 43174, 21806),  # Janthir Syntri - Lowland Shore
        (43136, 30464),  # Kessex Hills - Queensdale (W)
        (44986, 30464),  # Kessex Hills - Queensdale (E)
        (50432, 31472),  # Lion's Arch - Lornar's Pass
        (51909, 29696),  # Lornar's Pass - Snowden Drifts
        (51871, 34560),  # Lornar's Pass - Timberline Falls
        (33755, 30976),  # Lost Precipice - Verdant Brink
        (44629, 41600),  # Malchor's Leap - Cursed Shore
        (47232, 40963),  # Malchor's Leap - Straits of Devastation
        (40046, 36435, 38884, 37220),  # Metrica Province - Rata Sum
        (50560, 39871),  # Mount Maelstrom - Straits of Devastation
        (52332, 37760),  # Mount Maelstrom - Timberline Falls
        (25000, 99779, 23880, 100457),  # New Kaineng City - Seitung Province
        (28840, 99952, 30909, 100890),  # New Kaineng City - The Echovald Wilds
        (26837, 24641, 24102, 22607),  # Skywatch Archipelago - The Wizard's Tower
        (54528, 27951),  # Snowden Drifts - Wayfarer Foothills
        (50560, 38111),  # Sparkfly Fen - Mount Maelstrom
        (49736, 38784),  # Sparkfly Fen - Straits of Devastation
        (36608, 31723),  # The Silverwastes - Verdant Brink
    ],
    'fractal': [
        (49392.2, 31889.7)
    ],
    'dungeon': [
        (60421.5, 30348.2),  # Ascalonian Catacombs
        (46046.0, 28325.0),  # Caudecus's Manor
        (42331.4, 32939.1),  # Twilight Arbor
        (52444.2, 34103.4),  # Sorrow's Embrace
        (59715.3, 25086.0),  # Citadel of Flame
        (55207.6, 25189.8),  # Honor of the Waves
        (53747.7, 38279.5),  # Crucible of Eternity
        (44802.4, 44060.5),  # The Ruined City of Arah
    ],
    'raid': [
        (49331.4, 32136.9),  # Lion's Arch Aerodrome hub
        (36533.9, 31050.6),  # Verdant Brink -> Forsaken Thicket
        (35494.9, 30669.7),  # Bloodstone Fen -> Bastion of the Penitent
        (51935.2, 32267.7),  # Lornar's Pass -> Hall of Chains
        (67349.2, 52779.2),  # Domain of Vabbi -> The Key of Ahdashim
    ],
    'strike/asura_gate': [
        (29806.9, 101538.1),  # Arborstone
        (57853.3, 21830.8),  # Eye of the North
    ],
    'strike': [
        (60113.2, 19683.9),  # Grothmar Valley -> Shiverpeaks Pass
        (57324, 18063),  # Bjora Marches -> Sanctum Arena
        (56027, 18873),  # Bjora Marches -> Whisper of Jormag
        (51143, 21776),  # Drizzlewood Coast -> Cold War
        (57621.8, 21596.3),  # Eye of the North -> Forging Steel
        # (29780.2, 101509),  # Arborstone hub
        (23717, 102637),  # Seitung Province -> Aetherblade Hideout
        (31046, 102233),  # The Echovald Wilds -> Xunlai Jade Junkyard
        (26196, 99894),  # New Kaineng City -> Kaineng Overlook
        (34433, 105132),  # Dragon's End -> Harvest Temple
        (49006.9, 31189.1),  # Lion's Arch -> Old Lion's Court
        (24108, 22416),  # The Wizard's Tower hub
    ],
    'asura_gate': [
        # (29833.7, 101567.3),  # Arborstone -> Lion's Arch
        (56816, 30443),  # Black Citadel -> Lion's Arch
        (49368, 32874),  # Chantry of Secrets -> Straits of Devastation
        (44706.68, 27352.05),  # Divinity's Reach -> Fields of Ruin
        (44108.81, 27388.08),  # Divinity's Reach -> Lion's Arch
        # (57853.3, 21830.8),  # Eye of the North
        (61826, 34803),  # Fields of Ruin -> Divinity's Reach
        (49473.9, 29003.23),  # Gendarran Fields -> Straits of Devastation
        (34387, 21244),  # Hearth's Glow gates
        (53266, 30656),  # Hoelbrak -> Lion's Arch
        (49399.7, 31138),  # Lion's Arch -> Cities
        (49415.9, 31729.1),  # Lion's Arch -> Mist Portals
        (50586, 31388.5),  # Lornar's Pass -> Straits of Devastation
        (38774.3, 36917.39),  # Rata Sum -> Lion's Arch
        (46642, 36713),  # Southsun Cove -> Lion's Arch
        (50184, 39787),  # Straits of Devastation -> Order Headquarters
        (43218.1, 37296.54),  # The Grove -> Lion's Arch
        (24560, 22335),  # The Wizard's Tower -> Lion's Arch
    ],
}

