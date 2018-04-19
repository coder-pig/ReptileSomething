import requests
import re

music_pattern = re.compile(r'"url":"(.*?.mp3)",', re.S)

resp = requests.get("https://app.sikegroup.com/admin.php/App162/app_play_list_detail?id=49&userid=&page=1").text
results = music_pattern.findall(resp)
for result in results:
    resp = requests.get(result.replace('\\', ''))
    print(result.replace('\\', '') + "~" + str(resp.status_code))

