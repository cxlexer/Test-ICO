import requests
import pprint
import json

response = requests.get("https://api.icowatchlist.com/public/v1/finished")
data = response.text
parsed = json.loads(data)
with open('api_data.json', 'w') as outfile:
    json.dump(parsed, outfile)

urls = []
with open('ico_urls.txt', 'w') as f:
    for item in parsed['ico']['finished']:
        f.write("%s\n" % item['icowatchlist_url'])
        urls.append(item['icowatchlist_url'])

print(urls)