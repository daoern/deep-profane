from tqdm import tqdm
import requests

url = "http://www.ovh.net/files/10Mb.dat" #big file test
# Streaming, so we can iterate over the response.
response = requests.get(url, stream=True)
total_size_in_bytes= int(response.headers.get('content-length', 0))
block_size = 1024 #1 Kibibyte
progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
with open('test.dat', 'wb') as file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)
progress_bar.close()
if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
    print("ERROR, something went wrong")

def fetch_weights(model_name):
    
    return f'weights/{model_name}/'