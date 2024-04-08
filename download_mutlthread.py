import os
import requests
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

adcode = '100000'
processed = set()
session = requests.Session()  # 使用会话对象

def download_json(adcode):
    urls = [
        f'https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json',
        f'https://geo.datav.aliyun.com/areas_v3/bound/{adcode}.json'
    ]

    last_exception = None
    for url in urls:
        try:
            with session.get(url, stream=True) as response:  # 流式请求
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            last_exception = e
            
    if last_exception:
        print(f'Failed to download JSON for adcode: {adcode}')
        print(f'Error: {last_exception}')
    return None

def process_json_data(adcode, path, pbar):
    if adcode in processed:
        return
    processed.add(adcode)
    
    json_data = download_json(adcode)
    if json_data is None:
        return
    full_path = os.path.join(path, adcode)
    os.makedirs(full_path, exist_ok=True)
    file_path = os.path.join(full_path, f'{adcode}.json')
    
    with open(file_path, 'w') as file:
        # 如果文件非常大，考虑使用 gzip.open 替代 open
        json.dump(json_data, file, ensure_ascii=False)
    
    features = json_data.get('features', [])
    pbar.total += len(features) - 1
    pbar.update(1)

    # 使用线程池并行处理新的 adcode
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_json_data, str(feature['properties']['adcode']), full_path, pbar) for feature in features if str(feature['properties']['adcode']) != adcode]
        for future in futures:
            future.result()  # 等待所有提交的任务完成

root_path = 'geojson_gcj02'
os.makedirs(root_path, exist_ok=True)

initial_json_data = download_json(adcode)
initial_features = initial_json_data.get('features', [])
initial_total = len(initial_features)

with tqdm(total=initial_total, desc="总进度（实时更新）", unit='feature') as pbar:
    process_json_data(adcode, root_path, pbar)