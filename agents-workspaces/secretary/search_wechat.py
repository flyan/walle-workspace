# -*- coding: utf-8 -*-
import requests
import re
import urllib.parse
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://weixin.sogou.com/',
}

query = '新智元'
encoded = urllib.parse.quote(query)

# Try Sogou WeChat article search with recent time filter
url = f'https://weixin.sogou.com/weixin?type=2&query={encoded}&ie=utf8&tsn=2&ft=&et='
print(f"URL: {url}")

resp = requests.get(url, headers=headers, timeout=15)
print(f"Status: {resp.status_code}")
print(f"Content length: {len(resp.text)}")

text = resp.text

# Look for JSON data with article URLs
article_urls = re.findall(r'"url":"(https?://mp\.weixin\.qq\.com/s/[^"]+)"', text)
print(f'Article URLs found: {len(article_urls)}')
for u in article_urls[:10]:
    print(u)

# Also check for any mp.weixin.qq.com links
mp_urls = re.findall(r'https?://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+', text)
print(f'MP URLs found: {len(mp_urls)}')
for u in mp_urls[:10]:
    print(u)

# Check for biz values
biz_values = re.findall(r'__biz=([a-zA-Z0-9+/=]+)', text)
print(f'Biz values: {biz_values[:5] if biz_values else "None"}')

# Check for title matches
titles = re.findall(r'"title":"([^"]+)"', text)
print(f'Titles found: {titles[:5] if titles else "None"}')

if not article_urls and not mp_urls:
    print('No article URLs found')
    # Look for any JSON structures
    json_matches = re.findall(r'\{[^{}]{100,}\}', text)
    print(f'JSON-like blocks: {len(json_matches)}')
    for i, jm in enumerate(json_matches[:3]):
        print(f"JSON block {i}: {jm[:200]}")
