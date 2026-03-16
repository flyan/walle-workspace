const fs = require('fs');
const path = require('path');
const marked = require('marked');

// 读取markdown文件
const mdFile = 'C:\\Users\\flyan\\.openclaw\\workspace\\reports\\intelligence_monthly_20260315.md';
const markdown = fs.readFileSync(mdFile, 'utf-8');

// 转换为HTML
const html = marked.parse(markdown);

// 创建完整的HTML文档
const fullHtml = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>金融科技情报-2026年3月15日</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }
        h1, h2, h3 { color: #1a5490; margin-top: 1.5em; }
        h1 { border-bottom: 3px solid #1a5490; padding-bottom: 10px; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 12px; border-radius: 5px; overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f0f0f0; }
        @media print {
            body { margin: 0; padding: 10mm; }
            h1 { page-break-after: avoid; }
            h2 { page-break-after: avoid; }
        }
    </style>
</head>
<body>
    ${html}
</body>
</html>`;

// 保存HTML文件
const htmlFile = 'C:\\Users\\flyan\\.openclaw\\workspace\\reports\\temp.html';
fs.writeFileSync(htmlFile, fullHtml);
console.log('HTML file created:', htmlFile);
