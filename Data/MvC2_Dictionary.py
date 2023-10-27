MvC2_NameToUnitIDs = {
  0x00: 'Ryu',
  0x01: 'Zangief',
  0x02: 'Guile',
  0x03: 'Morrigan',

  0x04: 'Anakaris',
  0x05: 'Strider',
  0x06: 'Cyclops',
  0x07: 'Wolverine',

  0x08: 'Psylocke',
  0x09: 'Iceman',
  0x0A: 'Rogue',
  0x0B: 'CapAmerica',

  0x0C: 'Spiderman',
  0x0D: 'Hulk',
  0x0E: 'Venom',
  0x0F: 'DrDoom',

  0x10: 'TronBonne',
  0x11: 'Jill',
  0x12: 'Hayato',
  0x13: 'Ruby',

  0x14: 'SonSon',
  0x15: 'Amingo',
  0x16: 'Marrow',
  0x17: 'Cable',

  0x18: 'Abyss_1stForm',
  0x19: 'Abyss_2ndForm',
  0x1A: 'Abyss_3rdForm',
  0x1B: 'ChunLi',

  0x1C: 'Megaman',
  0x1D: 'Roll',
  0x1E: 'Gouki',
  0x1F: 'BBHood',

  0x20: 'Felicia',
  0x21: 'Charlie',
  0x22: 'Sakura',
  0x23: 'Dan',

  0x24: 'Cammy',
  0x25: 'Dhalsim',
  0x26: 'MBison',
  0x27: 'Ken',

  0x28: 'Gambit',
  0x29: 'Juggernaut',
  0x2A: 'Storm',
  0x2B: 'Sabretooth',
  0x2C: 'Magneto',
  0x2D: 'Shuma',
  0x2E: 'WarMachine',
  0x2F: 'SilverSamurai',
  0x30: 'OmegaRed',
  0x31: 'Spiral',
  0x32: 'Colossus',
  0x33: 'Ironman',
  0x34: 'Sentinel',
  0x35: 'Blackheart',
  0x36: 'Thanos',
  0x37: 'Jin',
  0x38: 'CapCom',
  0x39: 'Bonerine',
  0x3A: 'Kobun',
}
rawName_dict = {
  0x00: '0x00_Ryu-W-508-H-369.raw',
  0x02: '0x02_Guile-W-1017-H-240.raw',
  0x04: '0x04_Anakaris-W-901-H-288.raw',
  0x05: '0x05_Strider-W-942-H-298.raw',
  0x06: '0x06_Cyclops-W-600-H-246.raw',

  # 0x08: '0x08_Psylocke-W-533-H-204.raw',  # Chloe
  0x08: '0x08_Psylocke_TVi-W-872-H-418.raw',  # Condensed
  0x0A: '0x0A_Rogue-W-592-H-249.raw',
  0x0C: '0x0C_Spiderman-W-559-H-269.raw',
  0x0E: '0x0E_Venom-W-860-H-480.raw',
  0x0F: '0x0F_DrDoom-W-974-H-409.raw',
  0x10: '0x10_TronBonne-W-1001-H-262.raw',
  0x13: '0x13_RubyHeart-W-914-H-355.raw',
  0x17: '0x17_Cable-W-746-H-510.raw',
  0x1C: '0x1C_Megaman-W-522-H-193.raw',
  0x1E: '0x1E_Gouki-W-531-H-227.raw',
  0x24: '0x24_Cammy-W-515-H-223.raw',
  0x25: '0x25_Dhalsim-W-709-H-298.raw',
  0x27: '0x27_Ken-W-715-H-208.raw',
  0x29: '0x29_Juggernaut-W-1005-H-278.raw',
  0x2A: '0x2A_Storm-W-752-H-275.raw',
  0x2C: '0x2C_Magneto-W-518-H-296.raw',
  0x31: '0x31_Spiral-W-765-H-237.raw',
  0x32: '0x32_Colossus-W-1631-H-2453.raw',  # MvC2 Action Portrait
  # 0x32: '0x32_Colossus-W-721-H-297.raw',
  0x33: '0x33_IronMan-W-860-H-480.raw',
  0x34: '0x34_Sentinel-W-620-H-428.raw',
  0x35: '0x35_Blackheart-W-743-H-313.raw',
  0x38: '0x38_CapCom-W-791-H-437.raw',
}

slotID_dict = {
  'slot0': 0x00,
  'slot1': 0x01,
  'slot2': 0x02,
  'slot3': 0x03,
  'slot4': 0x04,
  'slot5': 0x05,
  # Palette Expansion
  'slot6': 0x06,
  'slot7': 0x07,
  'slot8': 0x08,
  'slot9': 0x09,
  'slotA': 0x0A,
  'slotB': 0x0B,
  'slotC': 0x0C,
  'slotD': 0x0D,
  'slotE': 0x0E,
  'slotF': 0x0F,
}
slotNameBase6_dict = {
  0x00: 'LP',
  0x01: 'LK',
  0x02: 'HP',
  0x03: 'HK',
  0x04: 'A1',
  0x05: 'A2',
}
labelNameBase6_dict = {
  0x00: '00_LP',
  0x01: '01_LK',
  0x02: '02_HP',
  0x03: '03_HK',
  0x04: '04_A1',
  0x05: '05_A2',
}
slotNameExp12_dict = {
  0x00: 'LP',
  0x01: 'LK',
  0x02: 'HP',
  0x03: 'HK',
  0x04: 'A1',
  0x05: 'A2',
  0x06: 'Start+LP',
  0x07: 'Start+LK',
  0x08: 'Start+HP',
  0x09: 'Start+HK',
  0x0A: 'Start+A1',
  0x0B: 'Start+A2',
}
labelNameExp12_dict = {
  0x00: '00_LP',
  0x01: '01_LK',
  0x02: '02_HP',
  0x03: '03_HK',
  0x04: '04_A1',
  0x05: '05_A2',
  0x06: '06_startLP',
  0x07: '07_startLK',
  0x08: '08_startHP',
  0x09: '09_startHK',
  0x0A: '0A_startA1',
  0x0B: '0B_startA2',
}

slotNameExp16_dict = {
  0x00: 'LP',
  0x01: 'LK',
  0x02: 'HP',
  0x03: 'HK',
  0x04: 'A1+LP',
  0x05: 'A1+LK',
  0x06: 'A1+HP',
  0x07: 'A1+HK',
  0x08: 'A2+LP',
  0x09: 'A2+LK',
  0x0A: 'A2+HP',
  0x0B: 'A2+HK',
  0x0C: 'A1+A2+LP',
  0x0D: 'A1+A2+LK',
  0x0E: 'A1+A2+HP',
  0x0F: 'A1+A2+HK',
}
labelNameExp16_dict = {
  0x00: '00_LP',
  0x01: '01_LK',
  0x02: '02_HP',
  0x03: '03_HK',
  0x04: '04_A1LP',
  0x05: '05_A1LK',
  0x06: '06_A1HP',
  0x07: '07_A1HK',
  0x08: '08_A2LP',
  0x09: '09_A2LK',
  0x0A: '0A_A2HP',
  0x0B: '0B_A2HK',
  0x0C: '0C_A1A2LP',
  0x0D: '0D_A1A2LK',
  0x0E: '0E_A1A2HP',
  0x0F: '0F_A1A2HK',
}
paletteID_dict = {
  0x00: 'main0',
  0x01: 'main1',
  0x02: 'main2',
  0x03: 'main3',
  0x04: 'main4',
  0x05: 'main5',
  0x06: 'main6',
  0x07: 'main7',

  0x08: 'INVALID',
  0x09: 'INVALID',
  0x0A: 'INVALID',
  0x0B: 'INVALID',
  0x0C: 'INVALID',
  0x0D: 'INVALID',
  0x0E: 'INVALID',
  0x0F: 'INVALID',

  0x10: 'status00',
  0x11: 'status01',
  0x12: 'status02',
  0x13: 'status03',
  0x14: 'status04',
  0x15: 'status05',
  0x16: 'status06',
  0x17: 'status07',
  0x18: 'status08',
  0x19: 'status09',
  0x1A: 'status0A',
  0x1B: 'status0B',
  0x1C: 'status0C',
  0x1D: 'status0D',
  0x1E: 'status0E',
  0x1F: 'status0F',

  0x80: 'extra00',
  0x81: 'extra01',
  0x82: 'extra02',
  0x83: 'extra03',
  0x84: 'extra04',
  0x85: 'extra05',
  0x86: 'extra06',
  0x87: 'extra07',
  0x88: 'extra08',
  0x89: 'extra09',
  0x8A: 'extra0A',
  0x8B: 'extra0B',
  0x8C: 'extra0C',
  0x8D: 'extra0D',
  0x8E: 'extra0E',
  0x8F: 'extra0F',
  0x90: 'extra10',
  0x91: 'extra11',
  0x92: 'extra12',
  0x93: 'extra13',
  0x94: 'extra14',
  0x95: 'extra15',
  0x96: 'extra16',
  0x97: 'extra17',
  0x98: 'extra18',
  0x99: 'extra19',
  0x9A: 'extra1A',
  0x9B: 'extra1B',
  0x9C: 'extra1C',
  0x9D: 'extra1D',
  0x9E: 'extra1E',
  0x9F: 'extra1F',
  0xA0: 'extra20',
  0xA1: 'extra21',
  0xA2: 'extra22',
  0xA3: 'extra23',
  0xA4: 'extra24',
  0xA5: 'extra25',
  0xA6: 'extra26',
  0xA7: 'extra27',
  0xA8: 'extra28',
  0xA9: 'extra29',
  0xAA: 'extra2A',
  0xAB: 'extra2B',
  0xAC: 'extra2C',
  0xAD: 'extra2D',
  0xAE: 'extra2E',
  0xAF: 'extra2F',
  0xB0: 'extra30',
  0xB1: 'extra31',
  0xB2: 'extra32',
  0xB3: 'extra33',
  0xB4: 'extra34',
  0xB5: 'extra35',
  0xB6: 'extra36',
  0xB7: 'extra37',
  0xB8: 'extra38',
  0xB9: 'extra39',
  0xBA: 'extra3A',
  0xBB: 'extra3B',
  0xBC: 'extra3C',
  0xBD: 'extra3D',
  0xBE: 'extra3E',
  0xBF: 'extra3F',
  0xC0: 'extra40',
  0xC1: 'extra41',
  0xC2: 'extra42',
  0xC3: 'extra43',
  0xC4: 'extra44',
  0xC5: 'extra45',
  0xC6: 'extra46',
  0xC7: 'extra47',
  0xC8: 'extra48',
  0xC9: 'extra49',
  0xCA: 'extra4A',
  0xCB: 'extra4B',
  0xCC: 'extra4C',
  0xCD: 'extra4D',
  0xCE: 'extra4E',
  0xCF: 'extra4F',
  0xD0: 'extra50',
  0xD1: 'extra51',
  0xD2: 'extra52',
  0xD3: 'extra53',
  0xD4: 'extra54',
  0xD5: 'extra55',
  0xD6: 'extra56',
  0xD7: 'extra57',
}
oldPointer_dict = {
  '0x00': 451648,
  '0x01': 815488,
  '0x02': 532992,
  '0x03': 740096,
  '0x04': 1084224,
  '0x05': 816640,
  '0x06': 878432,
  '0x07': 959744,
  '0x08': 987424,
  '0x09': 895424,
  '0x0A': 875616,
  '0x0B': 907392,
  '0x0C': 826528,
  '0x0D': 1087328,
  '0x0E': 1127936,
  '0x0F': 1057312,
  '0x10': 1073056,
  '0x11': 832288,
  '0x12': 970400,
  '0x13': 1019104,
  '0x14': 1085600,
  '0x15': 1082816,
  '0x16': 935424,
  '0x17': 1030656,
  '0x18': 899040,
  '0x19': 511328,
  '0x1A': 824704,
  '0x1B': 457984,
  '0x1C': 534784,
  '0x1D': 390592,
  '0x1E': 478592,
  '0x1F': 1088128,
  '0x20': 1140960,
  '0x21': 379264,
  '0x22': 746336,
  '0x23': 252736,
  '0x24': 586688,
  '0x25': 679680,
  '0x26': 475264,
  '0x27': 481984,
  '0x28': 888608,
  '0x29': 1163328,
  '0x2A': 1038528,
  '0x2B': 985536,
  '0x2C': 1075040,
  '0x2D': 884032,
  '0x2E': 973184,
  '0x2F': 1093280,
  '0x30': 965440,
  '0x31': 1068128,
  '0x32': 1153696,
  '0x33': 985984,
  '0x34': 1136672,
  '0x35': 1140416,
  '0x36': 908384,
  '0x37': 867392,
  '0x38': 910208,
  '0x39': 977632,
  '0x3A': 348928,
}