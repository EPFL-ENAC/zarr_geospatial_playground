import rasterio
from utils.io import unique_value_from_list


def read_geotiff_metadata(file_path: str) -> dict:
    """Read geotiff metadata.

    Parameters
    ----------
    file_path : str
        path to geotiff file

    Returns
    -------
    dict
        dictionary of geotiff metadata
    """
    with rasterio.open(file_path) as src:
        metadata = {
            "driver": src.driver,
            "crs": src.crs.to_dict(),
            "transform": src.transform.to_gdal(),
            "width": src.width,
            "height": src.height,
            "count": src.count,  # Number of bands
            # Add more metadata attributes as needed
        }

    return metadata


def get_geotiffs_geometadata(file_paths: list = []) -> dict:
    # define empty lists to store the metadata elements
    x_coordinates = []
    y_coordinates = []
    x_sizes = []
    y_sizes = []
    widths = []
    heights = []

    # read metadata for each raster
    for raster in file_paths:
        metadata = read_geotiff_metadata(raster)
        x_coordinates.append(metadata["transform"][0])
        y_coordinates.append(metadata["transform"][3])
        x_sizes.append(metadata["transform"][1])
        y_sizes.append(metadata["transform"][5])
        widths.append(metadata["width"])
        heights.append(metadata["height"])

    # Get a unique value for each metadata element. Valid only if all rasters have the same size
    x_size = abs(unique_value_from_list(x_sizes))
    y_size = abs(unique_value_from_list(y_sizes))
    width = abs(unique_value_from_list(widths)) * x_size
    height = abs(unique_value_from_list(heights)) * y_size

    multiple_rasters_metadata = {}
    multiple_rasters_metadata["max_x"] = max(x_coordinates) + width
    multiple_rasters_metadata["min_x"] = min(x_coordinates)
    multiple_rasters_metadata["max_y"] = max(y_coordinates)
    multiple_rasters_metadata["min_y"] = min(y_coordinates) - height
    multiple_rasters_metadata["x_size"] = x_size
    multiple_rasters_metadata["y_size"] = y_size
    multiple_rasters_metadata["width"] = width
    multiple_rasters_metadata["height"] = height

    return multiple_rasters_metadata
