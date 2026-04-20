# -*- coding: utf-8 -*-
import requests
import re
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Try different approaches to find 新智元 content

# 1. Try searching via DuckDuckGo for the WeChat account
print("=== Trying DuckDuckGo ===")
query = '新智元 微信公众号 AI'
encoded_query = urllib.parse.quote_plus(query)
url = f'https://duckduckgo.com/html/?q={encoded_query}&ia=web'

response = requests.get(url, headers=headers, timeout=15)
print(f"Status: {response.status_code}, Length: {len(response.text)}")

# Find WeChat-related URLs
wechat_urls = re.findall(r'https?://mp\.weixin\.qq\.com[^\s<>"]+', response.text)
print(f"Found WeChat URLs: {wechat_urls[:5] if wechat_urls else 'None'}")

# Find any URLs pointing to xinzhiyuan
xinzhiyuan_urls = re.findall(r'https?://[^\s<>"]*xinzhiyuan[^\s<>"]*', response.text, re.IGNORECASE)
print(f"Found xinzhiyuan URLs: {xinzhiyuan_urls[:5] if xinzhiyuan_urls else 'None'}")

# Print some content
print("\nContent preview (first 3000 chars):")
print(response.text[:3000])

# 2. Try to access the WeChat public account directly via known __biz
# (If we can find it)
print("\n\n=== Trying direct WeChat access ===")
# Try common WeChat article aggregators or the official account
