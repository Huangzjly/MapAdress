import requests
import pandas as pd

API_KEY = "5b3ee23a39c21e3aee99ef5f55eaef6f"  # 替换为你的高德 Key
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_district_data(city_name):
    """从高德API获取 city -> district -> street 的3级行政区划"""
    url = "https://restapi.amap.com/v3/config/district"
    params = {
        "keywords": city_name,
        "subdistrict": 3,
        "key": API_KEY,
        "extensions": "base"
    }
    response = requests.get(url, params=params, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def parse_city_structure(data, city_name):
    """解析 city -> district -> street，返回简化结构"""
    results = []
    try:
        for city in data.get("districts", []):
            for district in city.get("districts", []):
                print(f" 正在查询 {district['name']} 的街道信息...")
                for street in district.get("districts", []):
                    results.append({
                        "city": city_name,
                        "district": district["name"],
                        "street": street["name"],
                        "location": street["center"]
                    })
    except Exception as e:
        print(f"❌ 解析数据出错：{e}")
    return results

def save_to_excel(data, filename="城市行政区划.xlsx"):
    if not data:
        print("⚠️ 未获取到任何街道数据，Excel 文件未生成。")
        return
    df = pd.DataFrame(data)
    df.columns = ["城市", "区/县", "街道", "坐标"]
    df.to_excel(filename, index=False, engine="openpyxl")
    print(f"✅ 已保存到 {filename}，共 {len(df)} 条记录。")

if __name__ == "__main__":
    city_name = input("请输入城市名称（如“广州”）：").strip()
    print(f"🔍 正在查询 {city_name} 的行政区划信息...")
    data = get_district_data(city_name)
    if data:
        parsed = parse_city_structure(data, city_name)
        save_to_excel(parsed)
    else:
        print("❌ 请求失败，请检查网络或API Key。")
