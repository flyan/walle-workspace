# -*- coding: utf-8 -*-
import requests
import re
import json
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Try to find 新智元 WeChat account via their known website
# They are a well-known AI news outlet in China

print("=== Trying to find 新智元 via website ===")

# Try their official website
urls_to_try = [
    'https://www.xinzhiyuan.cn',
    'https://xinzhiyuan.cn',
    'https://www.ai-xinzhiyuan.com',
    'https://xinzhiyuan.com',
]

for url in urls_to_try:
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        print(f"{url}: Status {response.status_code}, Final URL: {response.url}")
        if response.status_code == 200:
            print(f"  Content length: {len(response.text)}")
            # Look for WeChat-related info
            if 'weixin' in response.text.lower() or '微信' in response.text:
                print(f"  Found WeChat-related content!")
    except Exception as e:
        print(f"{url}: Error - {e}")

# Try to search for their WeChat public account ID
print("\n=== Trying Sogou WeChat search via API ===")

# Try using the Sogou WeChat search with different parameters
# The search requires JavaScript rendering, but let's try the API directly
api_url = 'https://weixin.sogou.com/weixin'
params = {
    'type': '1',
    'query': '新智元',
    'ie': 'utf8',
    's_from': 'input',
}

try:
    response = requests.get(api_url, params=params, headers=headers, timeout=15)
    print(f"Status: {response.status_code}")
    
    # Try to extract any useful data
    # Look for profile URLs
    profile_matches = re.findall(r'profile_ext\?action=home[^"\']+', response.text)
    print(f"Profile matches: {profile_matches[:3] if profile_matches else 'None'}")
    
    # Look for __biz values
    biz_matches = re.findall(r'__biz=([a-zA-Z0-9+=]+)', response.text)
    print(f"Biz matches: {biz_matches[:3] if biz_matches else 'None'}")
    
except Exception as e:
    print(f"Error: {e}")

# Try to find 新智元 via a known WeChat article
print("\n=== Trying to find 新智元 articles via search ===")

# Try using a simple search query
search_query = '新智元 微信公众号'
encoded = urllib.parse.quote_plus(search_query)

# Try with a different search engine
try:
    # Try using Baidu (might work better for Chinese content)
    baidu_url = f'https://www.baidu.com/s?wd={encoded}&rn=20'
    response = requests.get(baidu_url, headers=headers, timeout=15)
    print(f"Baidu Status: {response.status_code}")
    
    # Find WeChat article URLs
    wechat_urls = re.findall(r'https?://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+', response.text)
    print(f"Found WeChat URLs: {wechat_urls[:5] if wechat_urls else 'None'}")
    
except Exception as e:
    print(f"Baidu Error: {e}")
