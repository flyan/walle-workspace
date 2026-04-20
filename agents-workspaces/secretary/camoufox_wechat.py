# -*- coding: utf-8 -*-
import camoufox
import json

print("=== Using camoufox to scrape WeChat public account ===")

# Try to access Sogou WeChat search with camoufox
with camoufox.Client() as client:
    print("Browser started")
    
    # Navigate to Sogou WeChat search
    url = "https://weixin.sogou.com/weixin?type=1&query=%E6%96%B0%E6%99%8B%E5%85%83&ie=utf8"
    print(f"Navigating to {url}")
    
    page = client.get(url)
    print(f"Page title: {page.title}")
    
    # Wait for content to load
    page.wait_for_timeout(3000)
    
    # Get the page content
    content = page.content
    print(f"Content length: {len(content)}")
    
    # Look for WeChat public account info
    if 'profile_ext' in content:
        print("Found profile_ext in content!")
    
    # Try to find account info
    accounts = page.query_selector_all('.wx-rb__item')
    print(f"Found {len(accounts)} account items")
    
    # Get all text content
    text = page.inner_text('body')
    print(f"Body text length: {len(text)}")
    print(f"Body text preview: {text[:1000]}")
