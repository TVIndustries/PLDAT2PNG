import os
import sys
import numpy as np
from PIL import Image
import binascii
from Data import MvC2_Dictionary

# STDOUT handling (some constants)
# Save a reference to the original standard output
original_stdout = sys.__stdout__


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


def print_header(param_str):
    
    reg = sys.stdout
    sys.stdout = original_stdout

    prefix_str = ('\n ' + '*' * 99) + '\n * > '
    suffix_str = ('\n ' + '*' * 99)
    print(prefix_str + param_str + suffix_str)
    sys.stdout = reg
    return
# Function: get_immediate_subdirectories


def get_immediate_subdirectories(a_dir):
    """
    Returns a list of immediate subdirectories in a given directory.

    :param a_dir: Directory path
    :return: List of subdirectory names
    """
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

# Function: crc32_from_file


def crc32_from_file(filename):
    """
    Calculates the CRC32 checksum of a file.

    :param filename: Path to the file
    :return: CRC32 checksum as a formatted string
    """
    buf = open(filename, 'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)

    return "%08X" % buf

# Function: process_mem_block


def process_mem_block(p_mem_block):
    """
    Processes a memory block and returns a CRC32 checksum.

    :param p_mem_block: Memory block
    :return: CRC32 checksum as an integer
    """
    crc32 = binascii.crc32(p_mem_block) & 0xFFFFFFFF
    return crc32


# Function: process_all_characters
def process_all_characters(directory, rawDirectory, exportedPreviewsDir, duplicates_once, labeled_output):
    """
    Processes palette data for all available characters.

    :param directory: Directory with character data
    :param rawDirectory: Directory with raw character images
    :param exportedPreviewsDir: Directory to save preview images
    :param duplicates_once: Flag to indicate whether to process duplicate palette data
    :param labeled_output: Flag to indicate whether to create labeled output
    """
    for chrID in MvC2_Dictionary.rawName_dict:

        process_single_character(chrID, directory, rawDirectory,
                                 exportedPreviewsDir, duplicates_once, labeled_output)

# Function: process_single_character


def process_single_character(chrID, directory, rawDirectory, exportedPreviewsDir, duplicates_once, labeled_output):
    """
    Processes palette data for a single character.

    :param chrID: Character ID
    :param directory: Directory with character data
    :param rawDirectory: Directory with raw character images
    :param exportedPreviewsDir: Directory to save preview images
    :param duplicates_once: Flag to indicate whether to process duplicate palette data
    :param labeled_output: Flag to indicate whether to create labeled output
    """
    print_header("Processing 0x%02X_%s via \'PL%02X_DAT.BIN\'" 
                 % (chrID,MvC2_Dictionary.MvC2_NameToUnitIDs[chrID],chrID))
    rawName = MvC2_Dictionary.rawName_dict[chrID]
    rawFile = ''
    if os.path.isfile(rawDirectory + rawName):
        rawFile = open(rawDirectory + rawName, 'rb')
        print('Using:', rawName, 'as preview.')
    else:
        exit_script(
            "Could not find raw file. Please check Dictionary and Directory.")
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
            print("[d]", directory + subFolder)
            target_fileName = 'PL%02X_DAT.BIN' % chrID
            print('[i]', target_fileName)
            f_name_list = []
            for f_name in os.listdir(directory + subFolder):
                if f_name.endswith(target_fileName):
                    f_name_list.append(f_name)
            for f_name in f_name_list:
                curCRC32 = crc32_from_file(directory + subFolder + f_name)
                curSet = (f_name, curCRC32)
                if curSet not in crcList:
                    crcList.append(curSet)
                    print(subFolder + f_name, ': ', curCRC32)
                    chrName = MvC2_Dictionary.MvC2_NameToUnitIDs[chrID]
                    chrDir = '0x%02X_%s\\' % (chrID, chrName)
                    os.makedirs(exportedPreviewsDir + chrDir, exist_ok=True)
                    targetDir = exportedPreviewsDir + chrDir
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
                        print('[i] Original 6 Palette Found:',
                              subFolder + f_name, ', ', curCRC32)
                        slotAmount = 6

                    else:
                        print('[i] Custom PLDAT Found:',
                              subFolder + f_name, ', ', curCRC32)
                        chrID_str = '0x%02X' % chrID
                        expectedLoc = MvC2_Dictionary.oldPointer_dict[chrID_str]
                        PL_file.seek(expectedLoc, 0)
                        slotAmount_read = int.from_bytes(
                            PL_file.read(1), 'little')
                        if slotAmount_read == 0:
                            print('[e] ERROR Slot Amount ZERO Detected')
                            continue
                        else:
                            slotAmount = slotAmount_read
                            print('[i] Slot Amount Detected:', slotAmount)
                            print('[v] Found @ PLDAT Offset: 0x%08X' %
                                  expectedLoc)
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
                        mem_block_crc32 = binascii.crc32(
                            mem_block) & 0xFFFFFFFF
                        mem_block_crc32_str = '%08x' % mem_block_crc32
                        cur_block_set = (chrID, mem_block_crc32_str)
                        if (cur_block_set not in crcList) or (not duplicates_once) or labeled_output:
                            crcList.append(cur_block_set)
                            print(cur_block_set)
                            PL_file.seek(slot_start_loc, 0)

                            # 0x20 Per Row, 8 Rows Per Slot => 2 bytes per color, 0x10 colors per row,
                            # 8 rows per slot
                            slotName = slotName_dict[slotNumber]
                            paletteArray = []
                            for i in range(0, 0x80):
                                colorData = int.from_bytes(
                                    PL_file.read(2), 'little')
                                red = (((colorData & 0x0F00) >> 8)
                                       * 0x11) & 0xFF
                                grn = (((colorData & 0x00F0) >> 4)
                                       * 0x11) & 0xFF
                                blu = (((colorData & 0x000F) >> 0)
                                       * 0x11) & 0xFF
                                colorGrp = (red, grn, blu)
                                paletteArray.append(colorGrp)

                            for i in range(0, 0x80):
                                paletteArray.append((0, 0, 0))

                            strFmt = '{0:s}_0x{1:02X}_{2:s}_Slot{3:02X}_{4:s}.png'
                            newFilename = strFmt.format(
                                sbFolder, chrID, chrName, slotNumber, slotName)
                            img_pil = Image.fromarray(rawArray)
                            img_pil = img_pil.convert('P')
                            palette = [
                                value for color in paletteArray for value in color]
                            img_pil.putpalette(palette, rawmode='RGB')
                            img_pil.save(targetDir + newFilename, optimize=True, format="PNG",
                                         transparency=0)

                            if labeled_output:
                                label_image_filename = ".\\Data\\Images\\%s.png" % labelImage_dict[
                                    slotNumber]
                                label_image = Image.open(label_image_filename)
                                main_image = Image.open(
                                    targetDir + newFilename)

                                # Calculate the padding (in pixels) between the label and main image
                                padding_x = 10  # Adjust the horizontal padding as needed

                                # Calculate the height to match the main image and maintain aspect ratio
                                new_height = main_image.height
                                new_width = int(
                                    label_image.width * (new_height / label_image.height))

                                # Resize the label image while maintaining its aspect ratio
                                label_image = label_image.resize(
                                    (new_width, new_height), Image.LANCZOS)

                                # Calculate the size of the combined image
                                combined_width = label_image.width + padding_x + main_image.width
                                combined_height = max(
                                    label_image.height, main_image.height)

                                # Create a new image with the calculated size
                                combined_image = Image.new(
                                    "RGBA", (combined_width, combined_height))

                                # Paste the label image on the left
                                combined_image.paste(label_image, (0, 0))

                                # Paste the main image on the right with padding
                                combined_image.paste(
                                    main_image, (label_image.width + padding_x, 0))

                                # Save or display the combined image
                                strFmt = 'Parts_{0:s}_0x{1:02X}_{2:s}_Slot{3:02X}_{4:s}.png'
                                newFilename = strFmt.format(
                                    sbFolder, chrID, chrName, slotNumber, slotName)

                                combined_image.save(
                                    labelPartsDir + newFilename)
                                img_temp = Image.open(
                                    labelPartsDir + newFilename)
                                images.append(img_temp)
                                # combined_image.show()
                        else:
                            print('[!] Duplicate slot found:',
                                  mem_block_crc32_str)
                            continue

                    if labeled_output:
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
                        else:
                            exit_script(
                                'Wrong palette amount logged for this PLDAT.')

                        # Calculate the width and height of the combined image
                        max_width = max(img.width for img in images)
                        max_height = max(img.height for img in images)

                        # Calculate the dimensions of each cell
                        cell_width = max_width
                        cell_height = max_height

                        # Create a new image with the calculated size
                        combined_width = columns * cell_width
                        combined_height = rows * cell_height
                        combined_image = Image.new(
                            "RGBA", (combined_width, combined_height))

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
                    print('[!] Duplicate found:',
                          subFolder + f_name, ', ', curCRC32)
                    continue
            # print(crcList)
            print('[f] Finished ' + sbFolder + '\n')
            print('-' * 100)
    except ExitError as e:
        sys.stdout = original_stdout
        print(" Failed:", e)
    # ... (continue with existing code for character processing)


def main():
    directory = ".\\Mixes\\"
    mode = 'SingleCharacter'  # SingleCharacter, AllAvailable
    duplicates_once = True
    labeled_output = False
    chrID = '0x2A'
    rawDirectory = '.\\RAWs\\'
    exportedPreviewsDir = '.\\ExportedPreviews\\'
    os.makedirs(exportedPreviewsDir, exist_ok=True)  # Output folder

    if mode == 'AllAvailable':
        print("\nProcessing with mode \'AllAvailable\' ... using available .raw files.")
        process_all_characters(
            directory, rawDirectory, exportedPreviewsDir, duplicates_once, labeled_output)

    elif mode == 'SingleCharacter':
        chrID = int(chrID, 16)
        print("\nProcessing with mode \'SingleCharacter\' ... attempting to process all \'PL%02X_DAT.BIN\'" % chrID)
        process_single_character(chrID, directory, rawDirectory,
                                 exportedPreviewsDir, duplicates_once, labeled_output)

    else:
        print('WRONG MODE SELECTED: Should be either AllAvailable or SingleCharacter (and setting the characterID)')


if __name__ == "__main__":
    main()
