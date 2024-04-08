import os
import json
from tqdm import tqdm
from coord_convert.transform import gcj2wgs

def convert_coordinates(coords):
    if isinstance(coords[0], list):
        return [convert_coordinates(sub_coords) for sub_coords in coords]
    else:
        lng, lat = coords
        converted_lng, converted_lat = gcj2wgs(lng, lat)
        return [converted_lng, converted_lat]

def convert_file(input_path, output_path):
    with open(input_path, 'r') as f:
        geojson_data = json.load(f)

    for feature in geojson_data['features']:
        geom_type = feature['geometry']['type']
        coordinates = feature['geometry']['coordinates']

        if geom_type in ['Point', 'LineString', 'MultiPoint']:
            feature['geometry']['coordinates'] = convert_coordinates(coordinates)
        elif geom_type in ['Polygon', 'MultiLineString']:
            feature['geometry']['coordinates'] = [convert_coordinates(ring) for ring in coordinates]
        elif geom_type == 'MultiPolygon':
            feature['geometry']['coordinates'] = [[convert_coordinates(ring) for ring in polygon] for polygon in coordinates]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(geojson_data, f, ensure_ascii=False)

def convert_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_count = sum(len(files) for _, _, files in os.walk(input_dir))
    progress_bar = tqdm(total=file_count, desc="Converting files")

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)
                convert_file(input_path, output_path)
                progress_bar.update()

    progress_bar.close()

convert_directory('geojson_gcj02', 'geojson_wgs84')