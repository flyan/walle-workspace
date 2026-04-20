# -*- coding: utf-8 -*-
from camoufox.sync_api import Camoufox
import time

print("=== Using Camoufox to scrape WeChat public account ===")

try:
    with Camoufox(headless=True) as browser:
        print("Browser started")
        
        # Navigate to Sogou WeChat search
        url = "https://weixin.sogou.com/weixin?type=1&query=%E6%96%B0%E6%99%8B%E5%85%83&ie=utf8"
        print(f"Navigating to {url}")
        
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=30000)
        print(f"Page title: {page.title()}")
        
        # Wait for content to load
        time.sleep(3)
        
        # Get the page content
        content = page.content()
        print(f"Content length: {len(content)}")
        
        # Look for WeChat public account info
        if 'profile_ext' in content:
            print("Found profile_ext in content!")
        
        # Get all text content
        try:
            text = page.inner_text('body')
            print(f"Body text length: {len(text)}")
            print(f"Body text preview:\n{text[:2000]}")
        except Exception as e:
            print(f"Error getting text: {e}")
        
        # Try to find account items
        try:
            accounts = page.query_selector_all('.wx-rb__item')
            print(f"Found {len(accounts)} account items")
            for i, account in enumerate(accounts[:5]):
                print(f"Account {i}: {account.inner_text()[:200]}")
        except Exception as e:
            print(f"Error finding accounts: {e}")
        
        page.close()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
