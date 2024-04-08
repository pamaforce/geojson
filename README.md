# GeoJSON 数据下载器及坐标系转换器

这个项目包含用于从阿里云的地理数据服务下载GeoJSON数据的Python脚本，把`GCJ-02`坐标系的GeoJSON数据批量转换为`WGS-84`坐标系的Python脚本，以及国内精确到`district`级别的所有GeoJSON数据（两种坐标系都有，但暂不包括南海九段线的数据，即`adcode`为`100000_JD`的数据）。

## 主要特点

- 使用递归的方式遍历指定`adcode`下的所有地区数据。
- 及时捕获运行脚本时可能发生的错误并输出。
- 拥有一个多线程下载的高效率版本，但是需要注意设置速率限制。
- 提供一个将GeoJSON的`GCJ-02`坐标点批量转换到`WGS-84`坐标系的功能。
- 使用实时更新的进度条展示下载及转换的进度信息。

## 文件结构

- `download.py`: 主要的Python脚本，用于下载GeoJSON数据。
- `geojson_gcj02/`: 这个文件夹包含下载的GeoJSON数据，按照行政区划代码（adcode）进行组织，为`GCJ-02`坐标系。
- `geojson_wgs84/`: 这个文件夹包含转换后的GeoJSON数据，按照行政区划代码（adcode）进行组织，为`WGS-84`坐标系。
- `requirements.txt`: 包含`download.py`所需的所有依赖。
- `gcj2wgs.py`: 把`GCJ-02`坐标系的GeoJSON数据批量转换为`WGS-84`坐标系的Python脚本。
- `download_multithread.py`: 下载器的多线程试验版本。

## 如何使用

1. 确保你已经安装了Python和所有必要的依赖。你可以通过运行以下命令来安装依赖：

```sh
pip install -r requirements.txt
```
2. 运行download.py脚本来开始下载数据：

```sh
python download.py
```
3. 运行gcj2wgs.py脚本来开始转换数据：

```sh
python gcj2wgs.py
```

## 注意事项
- 请确保你有足够的磁盘空间来存储下载的数据。
- 下载过程可能需要一些时间，具体取决于你的网络速度和阿里云服务器的响应速度。
- 多线程版本由于速度过快会受到限制，请慎用。
- 数据获取日期为`2024/4/7`，数据来源为`https://geo.datav.aliyun.com/areas_v3/bound/geojson?code={adcode}[_full]`
- 注意根据数据源的描述，页面数据来源于高德开放平台，所以下载的GeoJSON坐标系应为`GCJ-02`。

## 许可证
这个项目是在MIT许可证下发布的。详情请查看[LICENSE](LICENSE)文件。
