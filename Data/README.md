# Data format

- 'update_at': last checked date + time
- 'city_name': Local Gov name
- 'city_name/region_name', day_off date, work, school
- work/school : 1 = normal / 0 = day off

```json
{
    'update_at': '2024/10/04 20:52:12',
    '基隆市': [['基隆市', datetime.date(2024, 10, 4), '1', '1']],
    '臺北市': [['臺北市', datetime.date(2024, 10, 4), '1', '1']],
    '新北市': [
        ['新北市', datetime.date(2024, 10, 4), '1', '1'],
        ['新北市萬里區崁腳國民小學', datetime.date(2024, 10, 4), '1', '0'],
        ['瑞芳區', datetime.date(2024, 10, 4), '0', '0'],
        ['萬里區', datetime.date(2024, 10, 5), '0', '0'],
        ['金山區', datetime.date(2024, 10, 5), '0', '0'],
        ['石門區', datetime.date(2024, 10, 5), '0', '0'],
        ['三芝區', datetime.date(2024, 10, 5), '0', '0']
    ]
}
```