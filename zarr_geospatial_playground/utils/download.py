import csv
import os

import pooch
from tqdm.notebook import tqdm


def get_list_of_urls_in_csv(csv_file_path: str) -> list:
    """Get a list of urls from a csv file.

    Parameters
    ----------
    csv_file_path : str
        path to csv file

    Returns
    -------
    list
        list of urls
    """
    with open(csv_file_path) as file:
        csv_reader = csv.reader(file)
        list_of_urls = [row[0] for row in csv_reader]
    return list_of_urls


def download_files(url_list: list, data_path: str) -> None:
    """Download files from a list of urls to a specified path.

    Parameters
    ----------
    url_list : list
        list of urls to download
    data_path : str
        path to download files to
    """
    for url in url_list:
        filename = os.path.basename(url)
        save_path = os.path.join(data_path, filename)
        if not os.path.exists(save_path):
            downloader = pooch.HTTPDownloader(progressbar=True)
            pooch.retrieve(
                url=url, known_hash=None, path=data_path, fname=filename, downloader=downloader, progressbar=tqdm
            )


if __name__ == "__main__":
    csv_file_path = r"C:\projects\zarr_geospatial_playground\zarr_geospatial_playground\data\urls.csv"
    data_path = r"C:\projects\zarr_geospatial_playground\zarr_geospatial_playground\data\input_csv_files"
    url_list = get_list_of_urls_in_csv(csv_file_path)
    download_files(url_list, data_path)
