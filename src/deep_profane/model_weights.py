from tqdm import tqdm

import requests
import os
import zipfile

url = "https://github.com/daoern/deep-profane/releases/download/test/"

def fetch_weights(model_name):
    weights_path = f'weights/{model_name}/'
    # check if there's local cache
    if os.path.exists(weights_path):
        return weights_path

    # create weight caches
    if not os.path.exists('weights'):
        os.makedirs('weights')

    mw_filename = f'{model_name}.zip'
    mw_filepath = 'weights/'+mw_filename

    response = requests.get(url+mw_filename, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024 * 1000 #1 Kibibyte * 1000 = 1MB
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(mw_filepath, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, weight file download unsuccessful")

    with zipfile.ZipFile(mw_filepath, 'r') as zip_ref:
        zip_ref.extractall('weights')

    return weights_path