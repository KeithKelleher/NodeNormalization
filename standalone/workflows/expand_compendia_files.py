import os
import json
import requests

def yield_data_file(file_list, base_url):
    for file in file_list:
        index = 0
        found_pieces = False

        while True:
            file_segment = f"{file}.{str(index).zfill(2)}"
            file_url = f"{base_url}{file_segment}"
            response = requests.head(file_url)
            if response.status_code == 200:
                found_pieces = True
                file_size = int(response.headers.get('content-length', 0))
                yield {
                    'file': file_segment,
                    'url': file_url,
                    'size': file_size
                }
                index += 1
            elif response.status_code == 404:
                break
            else:
                print(f"Error: Unexpected status code {response.status_code}")
                break

        if not found_pieces:
            file_url = f"{base_url}{file}"
            response = requests.head(file_url)
            if response.status_code == 200:
                file_size = int(response.headers.get('content-length', 0))
                yield {
                    'file': file,
                    'url': file_url,
                    'size': file_size
                }
            else:
                print(f"Found no file or segmented files for: {file}")


def get_conflation_info(config_file):
    conflation_url = os.environ.get('COMPENDIUM_URL') + 'conflation/'
    with open(config_file, 'r') as file:
        config = json.load(file)
        conflation_files = [conf['file'] for conf in config['conflations']]
        return [
            file_info for file_info in yield_data_file(conflation_files, conflation_url)
        ]

def get_compendium_info(config_file):
    compendium_url = os.environ.get('COMPENDIUM_URL') + 'compendia/'
    with open(config_file, 'r') as file:
        config = json.load(file)
        data_files = config['data_files']
        return [
            file_info for file_info in yield_data_file(data_files, compendium_url)
        ]