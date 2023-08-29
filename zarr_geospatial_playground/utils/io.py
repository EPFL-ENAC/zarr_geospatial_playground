import os


def unique_value_from_list(input_list: list) -> str:
    """Get unique value from a list.

    Parameters
    ----------
    input_list : list
        list of values

    Returns
    -------
    str
        unique value

    Raises
    ------
    Exception
        All list element must have the same value
    """
    unique_value = list(set(input_list))
    if len(unique_value) != 1:
        raise Exception("All files have the same size")
    return unique_value[0]


def create_list_geotiff_in_folder(path_folder: str) -> list:
    """Create a list of geotiff files in a folder.

    Parameters
    ----------
    path_folder : str
        path to folder

    Returns
    -------
    list
        list of geotiff files
    """
    list_geotiff = []
    for root, dirs, files in os.walk(path_folder):
        for file in files:
            if file.endswith(".tif"):
                list_geotiff.append(os.path.join(root, file))
    return list_geotiff
