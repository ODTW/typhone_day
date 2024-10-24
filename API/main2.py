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

url = "https://www.dgpa.gov.tw/typh/daily/nds.html"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

curr_path = os.getcwd()
root_dir = os.path.dirname(curr_path)
