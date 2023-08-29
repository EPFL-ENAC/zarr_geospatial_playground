import os

import zarr
from osgeo import gdal


def create_empty_zarr_file(file_path_zarr, chunks=(2000, 2000)):
    zarr.zeros(shape=(0,), dtype=int, store=file_path_zarr, overwrite=True)


def geotiffs_to_zarr(file_paths_in: list, file_path_out: str, band: int = 1, geotiffs_metadata: dict = {}):
    # define shape of the zarr array
    dimention_x = int((geotiffs_metadata["max_x"] - geotiffs_metadata["min_x"]) / geotiffs_metadata["x_size"])
    dimention_y = int((geotiffs_metadata["max_y"] - geotiffs_metadata["min_y"]) / geotiffs_metadata["y_size"])

    # Create an empty Zarr store
    shape = (dimention_y, dimention_x)
    dtype = "f4"

    # Create an empty Zarr array and save it to the specified file path
    zarr_array = zarr.zeros(shape, dtype=dtype, store=file_path_out, overwrite=True)

    # create attribute transform
    zarr_array.attrs["transform"] = (
        geotiffs_metadata["min_x"],
        geotiffs_metadata["x_size"],
        0.0,
        geotiffs_metadata["max_y"],
        -geotiffs_metadata["y_size"],
        0.0,
    )

    for image_path in file_paths_in:
        file_name = os.path.basename(image_path)
        print("Image name :", file_name)
        geotiff_dataset = gdal.Open(image_path)
        geotransform = geotiff_dataset.GetGeoTransform()
        pict_x_min = geotransform[0]
        pict_y_max = geotransform[3]

        x_dist_from_zarr_origin = int(pict_x_min - geotiffs_metadata["min_x"])
        array_x_start = int(x_dist_from_zarr_origin / geotiffs_metadata["x_size"])
        array_x_end = int(array_x_start + geotiffs_metadata["width"] / geotiffs_metadata["x_size"])

        y_dist_from_zarr_origin = int(geotiffs_metadata["max_y"] - pict_y_max)
        array_y_start = int(y_dist_from_zarr_origin / geotiffs_metadata["y_size"])
        array_y_end = int(array_y_start + geotiffs_metadata["height"] / geotiffs_metadata["y_size"])

        list(range(array_x_start, array_x_end))
        list(range(array_y_start, array_y_end))

        # print(array_x_start,":",array_x_end," - ",array_y_start,":",array_y_end)

        band_data = geotiff_dataset.GetRasterBand(band).ReadAsArray()
        zarr_array[array_y_start:array_y_end, array_x_start:array_x_end] = band_data
