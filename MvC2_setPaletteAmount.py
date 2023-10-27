from MvC2_PalExp import MvC2_Dictionary as MvC2D
desired_palette_amount = 16
dir = '.\\PLDATs\\setPaletteAmount\\'
edit_palette_amount = True
if edit_palette_amount:
    for chrID in range(0, 0x3B):
        char_ID_str = '%02X' % chrID
        chrID_str = '0x%02X' % chrID
        pldat_filename = 'PL' + char_ID_str + '_DAT.BIN'
        pldat_file = open(dir + pldat_filename, 'r+b')
        pointer_list = MvC2D.oldPointer_dict
        paletteAmountLoc = pointer_list[chrID_str]
        pldat_file.seek(paletteAmountLoc, 0)
        pldat_file.write(desired_palette_amount.to_bytes(1, byteorder='big'))