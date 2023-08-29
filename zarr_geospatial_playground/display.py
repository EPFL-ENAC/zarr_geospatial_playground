import rasterio
import zarr
from rasterio.plot import show
from rasterio.transform import Affine
from rasterio.windows import Window


def coordinates_to_pixel_coordinates(pict_x: int, pict_y: int, pict_dim_x: int, pict_dim_y: int, bbox: int) -> tuple:
    """Convert coordinates to pixel coordinates.

    Parameters
    ----------
    pict_x : int
        Coordinate x of the origin of the picture
    pict_y : int
        Coordinate y of the origin of the picture
    pict_dim_x : int
        Size of the pixel in x
    pict_dim_y : int
        Size of the pixel in y
    bbox : int
        Bounding box with coordinates in the form (x_min,y_min,x_max,y_max)

    Returns
    -------
    tuple
        tuple of pixel coordinates (index_x_start,index_x_end,index_y_start,index_y_end)
    """

    distance_x_start_origin = int(bbox[0] - pict_x)
    index_x_start = int(distance_x_start_origin / pict_dim_x)
    distance_x_end_origin = int(bbox[2] - pict_x)
    index_x_end = int(distance_x_end_origin / pict_dim_x)

    distance_y_end_origin = int(pict_y - bbox[1])
    index_y_end = int(distance_y_end_origin / pict_dim_y)
    distance_y_start_origin = int(pict_y - bbox[3])
    index_y_start = int(distance_y_start_origin / pict_dim_y)

    return index_x_start, index_x_end, index_y_start, index_y_end


def read_zarr(zarr_path: str, bbox: tuple = None):
    """
    Read a Zarr file and return the data as a NumPy array.

    Args:
        zarr_path (str): Path to the Zarr file.

    Returns:
        data (numpy.ndarray): The data from the Zarr file as a NumPy array.
    """
    # Open the Zarr array for reading

    zarr_array = zarr.open(zarr_path, mode="r")

    pict_x_min = zarr_array.attrs["transform"][0]
    pict_x_dim = zarr_array.attrs["transform"][1]
    pict_y_max = zarr_array.attrs["transform"][3]
    pict_y_dim = abs(zarr_array.attrs["transform"][4])

    if bbox:
        index_x_start, index_x_end, index_y_start, index_y_end = coordinates_to_pixel_coordinates(
            pict_x_min, pict_y_max, pict_x_dim, pict_y_dim, bbox
        )
        print(index_x_start, index_x_end, index_y_start, index_y_end)
        data = zarr_array[index_y_start:index_y_end, index_x_start:index_x_end]
    else:
        data = zarr_array[:]

    # create a affine transform for the raster
    affine = Affine(
        zarr_array.attrs["transform"][1],
        zarr_array.attrs["transform"][2],
        zarr_array.attrs["transform"][0],
        zarr_array.attrs["transform"][5],
        zarr_array.attrs["transform"][4],
        zarr_array.attrs["transform"][3],
    )

    ax = show(data, transform=affine, cmap="terrain")
    ax.set_aspect("equal")


def read_geotiff(geotiff_path, band: int = 1, bbox: tuple = None):
    """
    Display a GeoTIFF image in a Jupyter Notebook.

    Args:
        geotiff_path (str): Path to the input GeoTIFF file.

    Returns:
        None
    """
    print(geotiff_path)
    # Open the GeoTIFF file for reading
    with rasterio.open(geotiff_path) as raster:
        # get number of bands
        # print(f"Number of bands: {num_bands}")
        # print(f"Coordinate system: {coortdinate_system}")
        # print(f"Bounding box: {bounbding_box}")
        # print(f"Meta data: {meta_data}")
        transform = raster.transform
        # print(type(transform))
        # print(f"Transform: {transform}")

        pict_x_min = transform[2]
        pict_y_max = transform[5]
        pict_x_dim = transform[0]
        pict_y_dim = abs(transform[4])

        index_x_start, index_x_end, index_y_start, index_y_end = coordinates_to_pixel_coordinates(
            pict_x_min, pict_y_max, pict_x_dim, pict_y_dim, bbox
        )

        # Read the GeoTIFF data into a NumPy array
        width = index_x_end - index_x_start
        height = index_y_end - index_y_start

        if bbox:
            data = raster.read(band, window=Window(index_x_start, index_y_start, width, height))
        else:
            data = raster.read(band)

        # Display the GeoTIFF image using Matplotlib

        show(data, transform=raster.transform, cmap="terrain")
