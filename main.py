import requests
import json

# 高德地图 API 的 Key
API_KEY = '5b3ee23a39c21e3aee99ef5f55eaef6f'  # 替换为你的高德地图 API Key

def get_districts(province_name):
    """
    获取指定省份的行政区划信息
    """
    url = f"https://restapi.amap.com/v3/config/district?keywords={province_name}&subdistrict=2&showbiz=false&extensions=all&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

def extract_and_save_cities(response_data):
    """
    提取城市信息并保存到文件
    """
    cities = []
    for province in response_data.get("districts", []):
        for city in province.get("districts", []):
            cities.append({
                "adcode": city["adcode"],
                "name": city["name"],
                "center": city["center"]
            })

    # 保存到文件
    with open("cities.txt", "w", encoding="utf-8") as f:
        for city in cities:
            f.write(f"{city['name']}, {city['adcode']}, {city['center']}\n")

def extract_and_save_districts(response_data):
    """
    提取区县信息并保存到文件
    """
    districts = []
    for province in response_data.get("districts", []):
        for city in province.get("districts", []):
            for district in city.get("districts", []):
                districts.append({
                    "adcode": district["adcode"],
                    "name": district["name"],
                    "center": district["center"],
                    "city": city["name"]
                })

    # 保存到文件
    with open("districts.txt", "w", encoding="utf-8") as f:
        for district in districts:
            f.write(f"{district['name']}, {district['adcode']}, {district['center']}, {district['city']}\n")

if __name__ == "__main__":
    province_name = input("请输入省份名称（如山东省）：")
    response_data = get_districts(province_name)
    if response_data:
        extract_and_save_cities(response_data)
        extract_and_save_districts(response_data)
        print("城市和区县信息已分别保存到 cities.txt 和 districts.txt 文件中。")