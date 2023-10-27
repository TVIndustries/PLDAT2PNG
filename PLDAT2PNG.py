import os
import numpy as np
from PIL import Image
import sys
# import shutil
import binascii
from Data import MvC2_Dictionary

# STDOUT handling (some constants)
original_stdout = sys.__stdout__  # Save a reference to the original standard output


# resets the original print() to terminal
#     in case sys.stdout has been changed
def og_stdout(param_str):
    reg = sys.stdout
    sys.stdout = original_stdout
    print(param_str)
    sys.stdout = reg
    return


class ExitError(Exception):
    pass


def exit_script(param_str):
    sys.stdout = original_stdout
    print('\n\n')
    prefix_str = ('\n\n ' + '*' * 99) + '\n   ERROR: \n      '
    suffix_str = ('\n\n ' + '*' * 99)
    raise ExitError(prefix_str + param_str + suffix_str)


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def crc32_from_file(filename):
    buf = open(filename, 'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf


def process_mem_block(p_mem_block):
    # Assuming that filenames are in the format "characterID_filename.ext"
    # Extract character ID from the filename
    crc32 = binascii.crc32(p_mem_block) & 0xFFFFFFFF
    return crc32


directory = ".\\Mixes\\"
mode = 'SingleCharacter'  # SingleCharacter, AllAvailable

duplicates_once = False
chrID = '0x2A'
rawDirectory = '.\\RAWs\\'
previewDir = '.\\ExportedPreviews\\'
os.makedirs(previewDir, exist_ok=True)

if mode == 'AllAvailable':
    for chrID in MvC2_Dictionary.rawName_dict:
        rawName = MvC2_Dictionary.rawName_dict[chrID]
        rawFile = ''
        if os.path.isfile(rawDirectory + rawName):
            rawFile = open(rawDirectory + rawName, 'rb')
            print('Using:', rawName, 'as preview.')
        else:
            exit_script("Could not find raw file. Please check Dictionary and Directory.")
        rawNameSplit = rawName.split('.')
        rawNameSplit = rawNameSplit[0].split('-')
        width = int(rawNameSplit[2])
        height = int(rawNameSplit[4])

        rawArray = np.zeros((height, width), np.uint8)
        for h in range(0, height):
            for w in range(0, width):
                rawData = int.from_bytes(rawFile.read(1), 'big')
                rawArray[h][w] = rawData & 0xFF
        rawFile.close()
        try:
            crcList = []
            for sbFolder in get_immediate_subdirectories(directory):
                subFolder = sbFolder + '\\'
                # print("[d]", directory + subFolder)
                target_fileName = 'PL%02X_DAT.BIN' % chrID
                print('[i]', target_fileName)
                f_name_list = []
                for f_name in f_name_list:
                    curCRC32 = crc32_from_file(directory + subFolder + f_name)
                    curSet = (f_name, curCRC32)
                    if curSet not in crcList:
                        crcList.append(curSet)
                        print(subFolder + f_name, ': ', curCRC32)
                        chrName = MvC2_Dictionary.MvC2_NameToUnitIDs[chrID]
                        chrDir = '0x%02X_%s\\' % (chrID, chrName)
                        os.makedirs(previewDir + chrDir, exist_ok=True)
                        targetDir = previewDir + chrDir
                        labelDir = targetDir + 'Labeled\\'
                        os.makedirs(labelDir, exist_ok=True)
                        labelPartsDir = labelDir + 'Parts\\'
                        os.makedirs(labelPartsDir, exist_ok=True)
                        PL_fileName = 'PL%02X_DAT.BIN' % chrID

                        PL_file = open(directory + subFolder + PL_fileName, 'rb')
                        PL_file.seek(0x08, 0)
                        mainPointer = int.from_bytes(PL_file.read(4), 'little')
                        compPointer = int.from_bytes(PL_file.read(4), 'little')
                        slotAmount = 6  # lower limit
                        slotName_dict = MvC2_Dictionary.slotNameBase6_dict
                        labelImage_dict = MvC2_Dictionary.labelNameBase6_dict
                        if compPointer > mainPointer:
                            print('[i] Original 6 Palette Found:', subFolder + f_name, ', ', curCRC32)
                            slotAmount = 6

                        else:
                            print('[i] Custom PLDAT Found:', subFolder + f_name, ', ', curCRC32)
                            chrID_str = '0x%02X' % chrID
                            expectedLoc = MvC2_Dictionary.oldPointer_dict[chrID_str]
                            PL_file.seek(expectedLoc, 0)
                            slotAmount_read = int.from_bytes(PL_file.read(1), 'little')
                            if slotAmount_read == 0:
                                print('[e] ERROR Slot Amount ZERO Detected')
                                continue
                            else:
                                slotAmount = slotAmount_read
                                print('[i] Slot Amount Detected:', slotAmount)
                                print('[v] Found @ PLDAT Offset: 0x%08X' % expectedLoc)
                                if slotAmount == 6:
                                    # Custom 6 Palette
                                    slotName_dict = MvC2_Dictionary.slotNameBase6_dict
                                    labelImage_dict = MvC2_Dictionary.labelNameBase6_dict
                                elif slotAmount == 12:
                                    # Custom 12 Palette
                                    slotName_dict = MvC2_Dictionary.slotNameExp12_dict
                                    labelImage_dict = MvC2_Dictionary.labelNameExp12_dict
                                elif slotAmount == 16:
                                    # Custom 12 Palette
                                    slotName_dict = MvC2_Dictionary.slotNameExp16_dict
                                    labelImage_dict = MvC2_Dictionary.labelNameExp16_dict

                        PL_file.seek(mainPointer, 0)
                        images = []
                        for slotNumber in range(0, slotAmount):
                            slot_start_loc = PL_file.tell()
                            mem_block = PL_file.read(0x100)
                            mem_block_crc32 = binascii.crc32(mem_block) & 0xFFFFFFFF
                            mem_block_crc32_str = '%08x' % mem_block_crc32
                            cur_block_set = (chrID, mem_block_crc32_str)
                            if (cur_block_set not in crcList) or (not duplicates_once):
                                crcList.append(cur_block_set)
                                print(cur_block_set)
                                PL_file.seek(slot_start_loc, 0)

                                # 0x20 Per Row, 8 Rows Per Slot => 2 bytes per color, 0x10 colors per row,
                                # 8 rows per slot
                                slotName = slotName_dict[slotNumber]
                                paletteArray = []
                                for i in range(0, 0x80):
                                    colorData = int.from_bytes(PL_file.read(2), 'little')
                                    red = (((colorData & 0x0F00) >> 8) * 0x11) & 0xFF
                                    grn = (((colorData & 0x00F0) >> 4) * 0x11) & 0xFF
                                    blu = (((colorData & 0x000F) >> 0) * 0x11) & 0xFF
                                    colorGrp = (red, grn, blu)
                                    paletteArray.append(colorGrp)

                                for i in range(0, 0x80):
                                    paletteArray.append((0, 0, 0))

                                strFmt = '{0:s}_0x{1:02X}_{2:s}_Slot{3:02X}_{4:s}.png'
                                newFilename = strFmt.format(sbFolder, chrID, chrName, slotNumber, slotName)
                                img_pil = Image.fromarray(rawArray)
                                img_pil = img_pil.convert('P')
                                palette = [value for color in paletteArray for value in color]
                                img_pil.putpalette(palette, rawmode='RGB')
                                img_pil.save(targetDir + newFilename, optimize=True, format="PNG",
                                             transparency=0)
                                label_image_filename = ".\\Data\\Images\\%s.png" % labelImage_dict[slotNumber]
                                label_image = Image.open(label_image_filename)
                                main_image = Image.open(targetDir + newFilename)

                                # Calculate the padding (in pixels) between the label and main image
                                padding_x = 10  # Adjust the horizontal padding as needed

                                # Calculate the height to match the main image and maintain aspect ratio
                                new_height = main_image.height
                                new_width = int(label_image.width * (new_height / label_image.height))

                                # Resize the label image while maintaining its aspect ratio
                                label_image = label_image.resize((new_width, new_height), Image.LANCZOS)

                                # Calculate the size of the combined image
                                combined_width = label_image.width + padding_x + main_image.width
                                combined_height = max(label_image.height, main_image.height)

                                # Create a new image with the calculated size
                                combined_image = Image.new("RGBA", (combined_width, combined_height))

                                # Paste the label image on the left
                                combined_image.paste(label_image, (0, 0))

                                # Paste the main image on the right with padding
                                combined_image.paste(main_image, (label_image.width + padding_x, 0))

                                # Save or display the combined image
                                strFmt = 'Parts_{0:s}_0x{1:02X}_{2:s}_Slot{3:02X}_{4:s}.png'
                                newFilename = strFmt.format(sbFolder, chrID, chrName, slotNumber, slotName)

                                combined_image.save(labelPartsDir + newFilename)
                                img_temp = Image.open(labelPartsDir + newFilename)
                                images.append(img_temp)
                                # combined_image.show()
                            else:
                                print('[!] Duplicate slot found:', mem_block_crc32_str)
                                continue
                        # Define the number of rows and columns
                        rows = 4
                        columns = 3
                        order = []
                        if slotAmount == 6:
                            rows = 2
                            columns = 3
                            order = [0, 2, 4, 1, 3, 5]
                        elif slotAmount == 12:
                            rows = 4
                            columns = 3
                            order = [0, 2, 4, 1, 3, 5, 6, 8, 10, 7, 9, 11]
                        elif slotAmount == 16:
                            rows = 4
                            columns = 4
                            order = [0, 1, 2, 3,
                                     4, 5, 6, 7,
                                     8, 9, 10, 11,
                                     12, 13, 14, 15]
                        # Calculate the width and height of the combined image
                        max_width = max(img.width for img in images)
                        max_height = max(img.height for img in images)

                        # Calculate the dimensions of each cell
                        cell_width = max_width
                        cell_height = max_height

                        # Create a new image with the calculated size
                        combined_width = columns * cell_width
                        combined_height = rows * cell_height
                        combined_image = Image.new("RGBA", (combined_width, combined_height))

                        # Paste each image into the combined image in the specified order
                        for i, img_index in enumerate(order):
                            img = images[img_index]
                            row = i // columns
                            col = i % columns
                            x_offset = col * cell_width
                            y_offset = row * cell_height
                            combined_image.paste(img, (x_offset, y_offset))

                        # Save the final combined image
                        strFmt = 'Combined_{0:s}_0x{1:02X}_{2:s}.png'
                        newFilename = strFmt.format(sbFolder, chrID, chrName)
                        combined_image.save(labelDir + newFilename)
                    else:
                        print('[!] Duplicate found:', subFolder + f_name, ', ', curCRC32)
                        continue
                # print(crcList)
                print('[f] Finished ' + sbFolder + '\n')
                print('-' * 100)
        except ExitError as e:
            sys.stdout = original_stdout
            print(" Failed:", e)
elif mode == 'SingleCharacter':
    chrID = int(chrID, 16)
    rawName = MvC2_Dictionary.rawName_dict[chrID]
    rawFile = open(rawDirectory + rawName, 'rb')
    rawNameSplit = rawName.split('.')
    rawNameSplit = rawNameSplit[0].split('-')
    width = int(rawNameSplit[2])
    height = int(rawNameSplit[4])

    rawArray = np.zeros((height, width), np.uint8)
    for h in range(0, height):
        for w in range(0, width):
            rawData = int.from_bytes(rawFile.read(1), 'big')
            rawArray[h][w] = rawData & 0xFF
    rawFile.close()
    try:
        crcList = []
        for sbFolder in get_immediate_subdirectories(directory):
            subFolder = sbFolder + '\\'
            # print(directory + subFolder)
            target_fileName = 'PL%02X_DAT.BIN' % chrID
            f_name_list = []
            for f_name in os.listdir(directory + subFolder):
                if f_name.endswith(target_fileName):
                    f_name_list.append(f_name)
                # if f_name.endswith('PL34_DAT.BIN'):
                #     print(f_name)
                #     f_name_list.append(f_name)

            for f_name in f_name_list:
                curCRC32 = crc32_from_file(directory + subFolder + f_name)
                curSet = (f_name, curCRC32)
                if curSet not in crcList:
                    crcList.append(curSet)
                    print(subFolder + f_name, ': ', curCRC32)
                    chrName = MvC2_Dictionary.MvC2_NameToUnitIDs[chrID]
                    chrDir = '0x%02X_%s\\' % (chrID, chrName)
                    os.makedirs(previewDir + chrDir, exist_ok=True)
                    targetDir = previewDir + chrDir
                    labelDir = targetDir + 'Labeled\\'
                    os.makedirs(labelDir, exist_ok=True)
                    labelPartsDir = labelDir + 'Parts\\'
                    os.makedirs(labelPartsDir, exist_ok=True)
                    PL_fileName = 'PL%02X_DAT.BIN' % chrID

                    PL_file = open(directory + subFolder + PL_fileName, 'rb')
                    PL_file.seek(0x08, 0)
                    mainPointer = int.from_bytes(PL_file.read(4), 'little')
                    compPointer = int.from_bytes(PL_file.read(4), 'little')
                    slotAmount = 6  # lower limit
                    slotName_dict = MvC2_Dictionary.slotNameBase6_dict
                    labelImage_dict = MvC2_Dictionary.labelNameBase6_dict
                    if compPointer > mainPointer:
                        print('[i] Original 6 Palette Found:', subFolder + f_name, ', ', curCRC32)
                        slotAmount = 6

                    else:
                        print('[i] Custom PLDAT Found:', subFolder + f_name, ', ', curCRC32)
                        chrID_str = '0x%02X' % chrID
                        expectedLoc = MvC2_Dictionary.oldPointer_dict[chrID_str]
                        PL_file.seek(expectedLoc, 0)
                        slotAmount_read = int.from_bytes(PL_file.read(1), 'little')
                        if slotAmount_read == 0:
                            print('[e] ERROR Slot Amount ZERO Detected')
                            continue
                        else:
                            slotAmount = slotAmount_read
                            print('[i] Slot Amount Detected:', slotAmount)
                            print('[v] Found @ PLDAT Offset: 0x%08X' % expectedLoc)
                            if slotAmount == 6:
                                # Custom 6 Palette
                                slotName_dict = MvC2_Dictionary.slotNameBase6_dict
                                labelImage_dict = MvC2_Dictionary.labelNameBase6_dict
                            elif slotAmount == 12:
                                # Custom 12 Palette
                                slotName_dict = MvC2_Dictionary.slotNameExp12_dict
                                labelImage_dict = MvC2_Dictionary.labelNameExp12_dict
                            elif slotAmount == 16:
                                # Custom 12 Palette
                                slotName_dict = MvC2_Dictionary.slotNameExp16_dict
                                labelImage_dict = MvC2_Dictionary.labelNameExp16_dict

                    PL_file.seek(mainPointer, 0)
                    images = []
                    for slotNumber in range(0, slotAmount):
                        slot_start_loc = PL_file.tell()
                        mem_block = PL_file.read(0x100)
                        mem_block_crc32 = binascii.crc32(mem_block) & 0xFFFFFFFF
                        mem_block_crc32_str = '%08x' % mem_block_crc32
                        cur_block_set = (chrID, mem_block_crc32_str)
                        if (cur_block_set not in crcList) or (not duplicates_once):
                            crcList.append(cur_block_set)
                            print(cur_block_set)
                            PL_file.seek(slot_start_loc, 0)

                            # 0x20 Per Row, 8 Rows Per Slot => 2 bytes per color, 0x10 colors per row,
                            # 8 rows per slot
                            slotName = slotName_dict[slotNumber]
                            paletteArray = []
                            for i in range(0, 0x80):
                                colorData = int.from_bytes(PL_file.read(2), 'little')
                                red = (((colorData & 0x0F00) >> 8) * 0x11) & 0xFF
                                grn = (((colorData & 0x00F0) >> 4) * 0x11) & 0xFF
                                blu = (((colorData & 0x000F) >> 0) * 0x11) & 0xFF
                                colorGrp = (red, grn, blu)
                                paletteArray.append(colorGrp)

                            for i in range(0, 0x80):
                                paletteArray.append((0, 0, 0))

                            strFmt = '{0:s}_0x{1:02X}_{2:s}_Slot{3:02X}_{4:s}.png'
                            newFilename = strFmt.format(sbFolder, chrID, chrName, slotNumber, slotName)
                            img_pil = Image.fromarray(rawArray)
                            img_pil = img_pil.convert('P')
                            palette = [value for color in paletteArray for value in color]
                            img_pil.putpalette(palette, rawmode='RGB')
                            img_pil.save(targetDir + newFilename, optimize=True, format="PNG",
                                         transparency=0)
                            label_image_filename = ".\\Data\\Images\\%s.png" % labelImage_dict[slotNumber]
                            label_image = Image.open(label_image_filename)
                            main_image = Image.open(targetDir + newFilename)

                            # Calculate the padding (in pixels) between the label and main image
                            padding_x = 10  # Adjust the horizontal padding as needed

                            # Calculate the height to match the main image and maintain aspect ratio
                            new_height = main_image.height
                            new_width = int(label_image.width * (new_height / label_image.height))

                            # Resize the label image while maintaining its aspect ratio
                            label_image = label_image.resize((new_width, new_height), Image.LANCZOS)

                            # Calculate the size of the combined image
                            combined_width = label_image.width + padding_x + main_image.width
                            combined_height = max(label_image.height, main_image.height)

                            # Create a new image with the calculated size
                            combined_image = Image.new("RGBA", (combined_width, combined_height))

                            # Paste the label image on the left
                            combined_image.paste(label_image, (0, 0))

                            # Paste the main image on the right with padding
                            combined_image.paste(main_image, (label_image.width + padding_x, 0))

                            # Save or display the combined image
                            strFmt = 'Parts_{0:s}_0x{1:02X}_{2:s}_Slot{3:02X}_{4:s}.png'
                            newFilename = strFmt.format(sbFolder, chrID, chrName, slotNumber, slotName)

                            combined_image.save(labelPartsDir + newFilename)
                            img_temp = Image.open(labelPartsDir + newFilename)
                            images.append(img_temp)
                            # combined_image.show()
                        else:
                            print('[!] Duplicate slot found:', mem_block_crc32_str)
                            continue
                    # Define the number of rows and columns
                    rows = 4
                    columns = 3
                    order = []
                    if slotAmount == 6:
                        rows = 2
                        columns = 3
                        order = [0, 2, 4, 1, 3, 5]
                    elif slotAmount == 12:
                        rows = 4
                        columns = 3
                        order = [0, 2, 4, 1, 3, 5, 6, 8, 10, 7, 9, 11]
                    elif slotAmount == 16:
                        rows = 4
                        columns = 4
                        order = [0,   1,  2,  3,
                                 4,   5,  6,  7,
                                 8,   9, 10, 11,
                                 12, 13, 14, 15]

                    # Calculate the width and height of the combined image
                    max_width = max(img.width for img in images)
                    max_height = max(img.height for img in images)

                    # Calculate the dimensions of each cell
                    cell_width = max_width
                    cell_height = max_height

                    # Create a new image with the calculated size
                    combined_width = columns * cell_width
                    combined_height = rows * cell_height
                    combined_image = Image.new("RGBA", (combined_width, combined_height))

                    # Paste each image into the combined image in the specified order
                    for i, img_index in enumerate(order):
                        img = images[img_index]
                        row = i // columns
                        col = i % columns
                        x_offset = col * cell_width
                        y_offset = row * cell_height
                        combined_image.paste(img, (x_offset, y_offset))

                    # Save the final combined image
                    strFmt = 'Combined_{0:s}_0x{1:02X}_{2:s}.png'
                    newFilename = strFmt.format(sbFolder, chrID, chrName)
                    combined_image.save(labelDir + newFilename)
                else:
                    print('[!] Duplicate found:', subFolder + f_name, ', ', curCRC32)
                    continue
            # print(crcList)
            print('[f] Finished ' + sbFolder + '\n')
            print('-' * 100)
    except ExitError as e:
        sys.stdout = original_stdout
        print(" Failed:", e)
else:
    print(' WRONG MODE SELECTED: Should be either AllAvailable or SingleCharacter (and setting the characterID)')
