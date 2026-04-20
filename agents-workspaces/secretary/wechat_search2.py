# -*- coding: utf-8 -*-
import requests
import re
import urllib.parse
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Try to find 新智元 WeChat public account via Sogou account search
query = '新智元'
encoded_query = urllib.parse.quote(query)
url = f'https://weixin.sogou.com/weixin?type=1&query={encoded_query}&ie=utf8'

print(f"Searching account with URL: {url}")

response = requests.get(url, headers=headers, timeout=15)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

# Look for account info
# Search for biz values or URLs
biz_matches = re.findall(r'biz=[^&"\']+', response.text)
print(f"\nFound biz values: {biz_matches[:5] if biz_matches else 'None'}")

# Search for account profile URLs
profile_urls = re.findall(r'https?://mp\.weixin\.qq\.com/mp/profile_ext[^\s\'"<>]+', response.text)
print(f"\nFound profile URLs: {profile_urls[:5] if profile_urls else 'None'}")

# Print a section of the HTML to understand the structure
print("\nHTML structure (3000-6000 chars):")
print(response.text[3000:6000])

# Try to find any JSON data that might contain account info
json_pattern = re.findall(r'\{[^{}]{50,}\}', response.text)
print(f"\nFound {len(json_pattern)} JSON-like blocks")
