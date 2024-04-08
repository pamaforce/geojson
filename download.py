import os
import requests
import json
from tqdm import tqdm

adcode = '100000'
processed = set()  # 创建一个集合来跟踪已处理的 adcode

def download_json(adcode):
    urls = [
        f'https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json',
        f'https://geo.datav.aliyun.com/areas_v3/bound/{adcode}.json'
    ]

    last_exception = None
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            return json_data
        except requests.exceptions.RequestException as e:
            last_exception = e
            
    if last_exception:
        print(f'Failed to download JSON for adcode: {adcode}')
        print(f'Error: {last_exception}')
    return None

def create_folder(path):
    os.makedirs(path, exist_ok=True)

def save_json(file_path, json_data):
    with open(file_path, 'w') as file:
        json.dump(json_data, file, ensure_ascii=False)

def process_json_data(adcode, path, pbar):
    if adcode in processed:
        return
    processed.add(adcode)
    
    json_data = download_json(adcode)
    if json_data is None:
        return
    full_path = os.path.join(path, adcode)
    create_folder(full_path)
    file_path = os.path.join(full_path, f'{adcode}.json')
    save_json(file_path, json_data)
    features = json_data.get('features', [])
    
    # 更新进度条的总数
    pbar.total += len(features) - 1  # 减1是因为当前adcode已被处理
    pbar.update(1)

    for feature in features:
        new_adcode = str(feature['properties']['adcode'])
        if new_adcode != adcode:
            process_json_data(new_adcode, full_path, pbar)

root_path = 'geojson_gcj02'
create_folder(root_path)

# 获取初始的features数
initial_json_data = download_json(adcode)
initial_features = initial_json_data.get('features', [])
initial_total = len(initial_features)
with tqdm(total=initial_total, desc="总进度（实时更新）", unit='feature') as pbar:
    # 处理第一个adcode
    process_json_data(adcode, root_path, pbar)