import os
import string

from osgeo import gdal


def multiple_tiff_to_one(list_path_input, file_path_out):
    # Create a dictionary to store the original file names as keys and new short file names as values
    original_names = {}
    # Create list of characters (numbers and letters) to use for unique file names
    characters = string.digits + string.ascii_letters
    j = 0
    # Rename all the files in the current directory to have unique short names of 2 characters
    for i, file in enumerate(list_path_input):
        new_name = "".join(characters[i % len(characters)] + characters[i // len(characters)] + ".t")
        # Check if the new name already exists, ignoring the case
        while os.path.exists(new_name) or new_name.lower() in [f.lower() for f in os.listdir()]:
            i += 1
            new_name = "".join(characters[i % len(characters)] + characters[i // len(characters)] + ".t")
        os.rename(file, new_name)
        original_names[new_name] = file
        list_path_input[j] = new_name
        j += 1

    " ".join(list_path_input)

    # Build VRT from input files
    vrt_file = "merged.vrt"
    gdal.BuildVRT(vrt_file, list_path_input)

    # Translate VRT to TIFF
    gdal.Translate(file_path_out, vrt_file)

    # Rename the files back to their original names
    for new_name, original_name in original_names.items():
        os.rename(new_name, original_name)

    # remove the vrt file
    os.remove(vrt_file)
