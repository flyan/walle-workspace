# -*- coding: utf-8 -*-
import requests
import re
import urllib.parse
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Try to find 新智元 WeChat public account __biz through different approaches

# 1. Try Google search for the biz value
print("=== Trying Google search for biz ===")
try:
    query = '新智元 微信公众号 __biz'
    encoded = urllib.parse.quote_plus(query)
    url = f'https://www.google.com/search?q={encoded}'
    resp = requests.get(url, headers=headers, timeout=15)
    biz = re.findall(r'__biz=([a-zA-Z0-9+/=]+)', resp.text)
    print(f'Google biz values: {biz[:5] if biz else "None"}')
    if biz:
        for b in biz[:3]:
            print(f'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={b}')
except Exception as e:
    print(f'Google error: {e}')

# 2. Try Bing search for the biz value
print("\n=== Trying Bing search for biz ===")
try:
    query = '新智元 微信公众号 __biz mp.weixin.qq.com'
    encoded = urllib.parse.quote_plus(query)
    url = f'https://cn.bing.com/search?q={encoded}'
    resp = requests.get(url, headers=headers, timeout=15)
    biz = re.findall(r'__biz=([a-zA-Z0-9+/=]+)', resp.text)
    print(f'Bing biz values: {biz[:5] if biz else "None"}')
    if biz:
        for b in biz[:3]:
            print(f'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={b}')
except Exception as e:
    print(f'Bing error: {e}')

# 3. Try to access Sogou with different parameters to get the biz
print("\n=== Trying Sogou account search for biz ===")
try:
    query = '新智元'
    encoded = urllib.parse.quote(query)
    url = f'https://weixin.sogou.com/weixin?type=1&query={encoded}&ie=utf8'
    resp = requests.get(url, headers=headers, timeout=15)
    
    # Look for any biz values or profile URLs
    biz = re.findall(r'__biz=([a-zA-Z0-9+/=]+)', resp.text)
    print(f'Sogou biz values: {biz[:5] if biz else "None"}')
    
    # Look for profile URLs
    profiles = re.findall(r'profile_ext\?action=home[^"\']+', resp.text)
    print(f'Profile URLs: {profiles[:5] if profiles else "None"}')
    
    # Look for any mp.weixin.qq.com URLs
    mp_urls = re.findall(r'mp\.weixin\.qq\.com[^\s"\'<>]+', resp.text)
    print(f'MP URLs: {mp_urls[:5] if mp_urls else "None"}')
    
except Exception as e:
    print(f'Sogou error: {e}')

# 4. Try common WeChat article aggregators
print("\n=== Trying WeChat article aggregators ===")
agg_urls = [
    'https://www.wechat.com/article.html?biz=MjM5NTE3NjA4MQ==',
    'https://weixin.sogou.com/weixin?type=1&s_from=input&query=新智元',
]

for url in agg_urls:
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        biz = re.findall(r'__biz=([a-zA-Z0-9+/=]+)', resp.text)
        if biz:
            print(f'{url}: biz found - {biz}')
        else:
            print(f'{url}: no biz')
    except Exception as e:
        print(f'{url}: error - {e}')
