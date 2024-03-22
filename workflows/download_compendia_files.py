import os
import requests

def download_file(file_url, local_path):
    response = requests.get(file_url)
    with open(local_path, 'wb') as f:
        f.write(response.content)

def download_missing_file(url, local_path):
    if not os.path.exists(local_path):
        print(f"Downloading: {url}")
        download_file(url, local_path)
    else:
        print(f"{local_path} already exists locally. Skipping download.")


if __name__=="__main__":
    obj = snakemake.params.file_info_obj
    download_missing_file(obj['url'], snakemake.params.destination_path + obj['file'])


