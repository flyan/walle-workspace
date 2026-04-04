#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import markdown
from weasyprint import HTML
import os

# 读取markdown文件
with open(r'C:\Users\flyan\.openclaw\workspace\reports\金融科技资讯速递-2026-03-22.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 转换markdown为HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# 创建完整的HTML文档
full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>金融科技资讯速递 - 2026-03-22</title>
    <style>
        body {{
            font-family: 'SimHei', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        .keyword {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        .section {{
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    {html_content}
    <div class="footer">
        <p>报告生成时间: 2026年3月22日 20:10 GMT+8</p>
        <p>数据覆盖周期: 2026年3月3日-22日</p>
        <p>报告格式: PDF (使用WeasyPrint生成)</p>
    </div>
</body>
</html>"""

# 保存HTML文件（可选）
html_file = r'C:\Users\flyan\.openclaw\workspace\reports\金融科技资讯速递-2026-03-22.html'
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

# 生成PDF
pdf_file = r'C:\Users\flyan\.openclaw\workspace\reports\金融科技资讯速递-2026-03-22_weasyprint.pdf'
HTML(string=full_html).write_pdf(pdf_file)

print(f"HTML文件已保存: {html_file}")
print(f"PDF文件已生成: {pdf_file}")
print("注意: 如果weasyprint安装有问题，可以尝试安装: pip install weasyprint")