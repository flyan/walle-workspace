# -*- coding: utf-8 -*-
import requests
import re
import json
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# Search for articles from 新智元 using Sogou WeChat article search
query = '新智元'
encoded_query = urllib.parse.quote(query)
url = f'https://weixin.sogou.com/weixin?type=2&query={encoded_query}&ie=utf8&tsn=2&ft=&et='

print(f"Searching with URL: {url}")

response = requests.get(url, headers=headers, timeout=15)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

# Search for article URLs
urls = re.findall(r'https?://mp\.weixin\.qq\.com/s[^\s\'"<>]+', response.text)
print(f"\nFound {len(urls)} article URLs")
for u in urls[:10]:
    print(u)

# Look for any JSON data
json_matches = re.findall(r'\{[^{}]*"url"[^{}]*\}', response.text)
print(f"\nFound {len(json_matches)} JSON matches with url")

# Print content around the article links
if 'mp.weixin.qq.com' in response.text:
    idx = response.text.find('mp.weixin.qq.com')
    print(f"\nContext around first mp.weixin.qq.com occurrence:")
    print(response.text[max(0, idx-200):idx+500])
