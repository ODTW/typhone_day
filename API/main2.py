# get_day_off.py Ver 0.3
# 2024.10.28
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

import json
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


def get_day_off_table(html=""):
    results = {
        "url": url,
        "checked_at": datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
        "updated_at": "",
        "status_code": 0,
        "data": {},
    }
    if not html:
        s = httpx.get(url, headers=headers)
        results["status_code"] = s.status_code

        if s.status_code != 200:
            results["error"] = "page load error"
            return results
        s = BeautifulSoup(s.content, "lxml")

    else:
        s = html
        s = BeautifulSoup(s, "lxml")

    site_title = s.title.text.strip()
    if "天然災害停止上班及上課" not in site_title:
        results["error"] = "wrong page - " + site_title
        return results

    results["updated_at"] = (
        s.find("div", class_="Content_Updata")
        .find("h4")
        .text.split("\n")[1]
        .strip()
        .split("：")[1]
        .replace("/", ".")
    )

    today = datetime.strptime(results["updated_at"], "%Y.%m.%d %H:%M:%S").date()
    today_str = today.strftime("%Y.%m.%e")
    tomorrow = today + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y.%m.%e")

    city_table = s.find("tbody", class_="Table_Body").find_all("tr")

    # print([x for x in city_table if len(x.find_all("td")) > 1])
    # 無停班停課
    try:
        ann_status = city_table[0].find("h2").text
        if "無停班停課" in ann_status:
            results["data"] = {"all": [1, 1]}
        else:
            results["data"] = {"all": ann_status}
    except AttributeError:
        pass
    else:
        return results

    # 停班停課
    for city in city_table:
        city_cols = city.find_all("td")
        city_final = {}
        city_final_list = []

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
                    city_final[city_name] = reformat_status(
                        status_row, today_str, tomorrow_str
                    )
                    city_final_list.append([city_name, *city_final[city_name]])
                else:
                    # 多重公告，地區或學校停班聽課
                    sub_zone, sub_status = [x.strip() for x in status_row.split(":")]
                    if city_name in sub_zone or city_name + "立" in sub_zone:
                        sub_zone = sub_zone.replace(city_name + "立", "")
                        sub_zone = sub_zone.replace(city_name, "")

                    # Multiple zones in one row
                    if "、" in sub_zone:
                        for zone_name in sub_zone.split("、"):
                            city_final[zone_name] = reformat_status(
                                sub_status, today_str, tomorrow_str
                            )
                            city_final_list.append([zone_name, *city_final[zone_name]])
                    else:
                        city_final[sub_zone] = reformat_status(
                            sub_status, today_str, tomorrow_str
                        )
                        city_final_list.append([sub_zone, *city_final[sub_zone]])

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

        results["data"][city_name] = city_final_list
    return results


def reformat_status(status, today, tomorrow):
    formated_status = []
    if "今天" in status:
        formated_status.append(today)
        status = status.replace("今天", "")
    elif "明天" in status:
        formated_status.append(tomorrow)
        status = status.replace("明天", "")
    else:
        formated_status.append("No Date")

    if "、" in status:
        work_day, school_day = status.split("、")
    else:
        print(status)
        work_day, school_day = "照常"

    if "停止" in work_day:
        formated_status.append("0")
    else:
        formated_status.append("1")
    if "停止" in school_day:
        formated_status.append("0")
    else:
        formated_status.append("1")

    return formated_status


def save_to_dataset(results):
    date_now = datetime.now().strftime("%Y-%m-%d")
    with open(
        os.path.join(root_dir, "Data", date_now + ".json"), "w", encoding="utf-8"
    ) as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    with open("..\\Data\\dummy.html", "r") as f:
        dummy = f.read()

    results = get_day_off_table()
    save_to_dataset(results)
