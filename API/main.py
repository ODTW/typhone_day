# main.py Ver 0.1.xx
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

import json
import os
from datetime import datetime, timedelta

import httpx
from bs4 import BeautifulSoup

url = "https://www.dgpa.gov.tw/typh/daily/nds.html"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

curr_path = os.getcwd()
root_dir = os.path.dirname(curr_path)


def get_day_off_table():
    """Check day_off announcement
    return a dict of announucement
    """
    s = httpx.get(url, headers=headers)
    s = BeautifulSoup(s.content, "lxml")

    results = {
        "update_at": "",
        "data": {},
    }

    results["update_at"] = s.find("div", class_="f_right Content_Updata")
    results["update_at"] = (
        results["update_at"].find("h4").text.split("\r\n")[1].strip().split("：")[1]
    )
    today = datetime.strptime(results["update_at"], "%Y/%m/%d %H:%M:%S").date()
    tomorrow = today + timedelta(days=1)

    city_list = s.find("tbody", class_="Table_Body").find_all("tr")

    for city in city_list:
        city_result = {}  # temp status result for city
        city_status = city.find_all("td")

        if len(city_status) == 1:
            try:
                ann_status = city_status[0].find("h2").text
                results["data"] = {"all": ann_status}
            except AttributeError:
                # no city name nor non-announcement ?
                print("Please check " + url)
                results["data"] = {"all": "AttributeError"}
            return results

        # Get each Local Gov name and status
        if (
            city_status[0].get("headers")
            and city_status[0].get("headers")[0] == "city_Name"
        ):
            city_name = city_status[0].text
            if (
                city_status[1].get("headers")
                and city_status[1].get("headers")[0] == "StopWorkSchool_Info"
            ):
                city_result[city_name] = city_status[1].text.split("。")[:-1]

        # Get status of 上班 + 上課
        city_result[city_status[0].text] = [
            res.strip() for res in city_result[city_status[0].text]
        ]
        final_result = []

        # reformat status to "sub_region", "date", "work[1/0]", "schoole[1/0]"
        for res in city_result[city_status[0].text]:
            sub_region = city_status[0].text

            # the status is for a sub region(s) or school
            if ":" in res:
                sub_region, res = res.split(":")
                if sub_region != city_name:
                    if city_name + "立" in sub_region:
                        sub_region = sub_region.replace(city_name + "立", "")
                    sub_region = sub_region.replace(city_name, "")

            # Check the date of announcement
            res_date = today if res[:2] == "今天" else tomorrow
            res_date = res_date.strftime("%Y-%m-%d")

            # mark as 1 if normal, and 0 if day_off is announced
            try:
                res_work, res_class = res[2:].split("、")
                res_work = "1" if "照常" in res_work else "0"
                res_class = "1" if "照常" in res_class else "0"
            except ValueError:
                if "停止上班及上課" in res[2:]:
                    res_work = "0"
                    res_class = "0"
                elif "停止上班" in res[2:]:
                    res_work = "0"
                elif "停止上課" in res[2:]:
                    res_class = "0"
                else:
                    res_work = "1"
                    res_class = "1"

            # if multiple regions in list
            if "、" in sub_region:
                for region in sub_region.split("、"):
                    final_result.append([region, res_date, res_work, res_class])
            else:
                final_result.append([sub_region, res_date, res_work, res_class])

        # result = {}
        # result[city_status[0].text] = final_result
        results["data"][city_status[0].text] = final_result

    return results


def save_to_dataset(results):
    date_now = datetime.now().strftime("%Y-%m-%d")
    with open(
        os.path.join(root_dir, "Data", date_now + ".json"), "w", encoding="utf-8"
    ) as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    results = get_day_off_table()
    save_to_dataset(results)
