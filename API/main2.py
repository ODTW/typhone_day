# get_day_off.py Ver 0.2
# 2024.10.25
# Get Typhone Day_off announcement from DGPA at https://www.dgpa.gov.tw/typh/daily/nds.html
# 1. get update_time
# 2. check if there is announcement
# 3. get cities list + status
# 4. transform cities status => region / school - work[1/0] - school[1/0]
#    1 = normal
#    0 = day off
# 5. save to Data\[date].json
#   {
#       "update_at": "datetime"
#       "data": {
#               "city_name" : [
#                       "region_name/school", "date", "work[1/0]", "school[1/0]"
#                   ]
#           }
#   }

import os
from datetime import datetime, timedelta

import httpx
from bs4 import BeautifulSoup
from rich import print

url = "https://www.dgpa.gov.tw/typh/daily/nds.html"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

curr_path = os.getcwd()
root_dir = os.path.dirname(curr_path)


def get_day_off_table():
    results = {
        "checked_at": datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
        "updated_at": "",
        "status_code": 0,
    }

    s = httpx.get(url, headers=headers)
    results["status_code"] = s.status_code

    if s.status_code != 200:
        results["error"] = "page load error"
        return results

    s = BeautifulSoup(s.content, "lxml")
    site_title = s.title.text.strip()
    if "天然災害停止上班及上課" not in site_title:
        results["error"] = "wrong page - " + site_title
        return results

    results["updated_at"] = (
        s.find("div", class_="f_right Content_Updata")
        .find("h4")
        .text.split("\r\n")[1]
        .strip()
        .split("：")[1]
        .replace("/", ".")
    )

    today = datetime.strptime(results["updated_at"], "%Y.%m.%d %H:%M:%S").date()
    tomorrow = today + timedelta(days=1)

    city_table = s.find("tbody", class_="Table_Body").find_all("tr")

    # 無停班停課
    try:
        ann_status = city_table[0].find("h2").text
        if "無停班停課" in ann_status:
            results["data"] = {"all": [1, 1]}
        else:
            results["data"] = {"all": ann_status}
    except AttributeError:
        results["error"] = "Table AttributeError: " + url
    else:
        return results

    # 停班停課
    for city in city_table:
        city_cols = city.find_all("td")
        city_final = {}

        # 非停班停課公告
        if len(city_cols) != 2:
            continue

        # 表格: 地方名稱, 停班停課狀態
        city_name, city_status = city_cols

        if city_name.get("headers") and city_name.get("headers")[0] == "city_Name":
            city_name = city_name.text.strip()
        else:
            # 表格非地方名稱 - 非停班停課公告
            continue

        if (
            city_status.get("headers")
            and city_status.get("headers")[0] == "StopWorkSchool_Info"
        ):
            # 停班停課公告
            city_status = [
                x.strip() for x in city_status.text.strip().split("。") if x != ""
            ]

            for status_row in city_status:
                if ":" not in status_row:
                    # 地方政府單一公告
                    city_final[city_name] = status_row
                else:
                    # 多重公告，地區或學校停班聽課
                    sub_zone, sub_status = [x.strip() for x in status_row.split(":")]
                    # Multiple zones in one row
                    if "、" in sub_zone:
                        for zone_name in sub_zone.split("、"):
                            city_final[zone_name] = sub_status
                    else:
                        city_final[sub_zone] = sub_status

                # finale format: 'city_name/zone_name' = city(zone)_status
                # 今天停止上班、停止上課
                # 今天照常上班、照常上課
                # '臺北市士林區陽明山國民小學': '今天停止上班、停止上課',
                # '臺北市北投區湖田里': '今天停止上班、停止上課',
                # '臺北市立格致國民中學': '今天停止上班、停止上課',
                # '臺北市湖田實驗國民小學': '今天停止上班、停止上課',
                # '臺北市華岡藝術學校': '今天停止上班、停止上課'

        else:
            print(f":: {city_name} - {city_status}")
            continue

        results["data"][city_name] = city_final
    return results


if __name__ == "__main__":
    results = get_day_off_table()
    print(results)
    # save_to_dataset(results)
