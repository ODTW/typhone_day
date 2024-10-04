import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from rich import print

url = "https://www.dgpa.gov.tw/typh/daily/nds.html"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

s = httpx.get(url, headers=headers)
s = BeautifulSoup(s.content, "lxml")

results = {}

results['update_at'] = s.find('div', class_='f_right Content_Updata')
results['update_at'] = results['update_at'].find('h4').text.split('\r\n')[1].strip().split('：')[1]
today = datetime.strptime(results['update_at'], "%Y/%m/%d %H:%M:%S").date()
tomorrow = today + timedelta(days=1)


table_list = s.find('tbody', class_="Table_Body").find_all('tr')

for item in table_list:
    city_status = item.find_all('td')

    if city_status[0].get('headers') and city_status[0].get('headers')[0] == 'city_Name':
        if city_status[1].get('headers') and city_status[1].get('headers')[0] == 'StopWorkSchool_Info':
            results[city_status[0].text] = city_status[1].text.split('。')[:-1]
    else:
        continue
    results[city_status[0].text] = [res.strip() for res in results[city_status[0].text]]
    final_result = []
    for res in results[city_status[0].text]:
        sub_region = city_status[0].text
        if ':' in res:
            sub_region, res = res.split(':')
        res_date = today if res[:2] == '今天' else tomorrow
        try:
            res_work, res_class = res[2:].split('、')
            res_work = '1' if "照常" in res_work else '0'
            res_class = '1' if "照常" in res_class else '0'
        except ValueError:
            if "停止上班及上課" in res[2:]:
                res_work = '0'
                res_class = '0'
            elif "停止上班" in res[2:]:
                res_work = '0'
            elif "停止上課" in res[2:]:
                res_class = '0'
            else:
                res_work = '1'
                res_class = '1'
        if '、' in sub_region:
            for region in sub_region.split('、'):
                final_result.append([region, res_date, res_work, res_class])
        else:
            final_result.append([sub_region, res_date, res_work, res_class])

    results[city_status[0].text] = final_result


print(results)
