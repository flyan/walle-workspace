import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re

# 读取markdown文件
with open(r'C:\Users\flyan\.openclaw\workspace\reports\intelligence_monthly_20260315.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 转换markdown为HTML
html_content = markdown.markdown(md_content)

# 创建PDF
pdf_file = r'C:\Users\flyan\.openclaw\workspace\reports\金融科技情报-20260315.pdf'
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)

# 样式
styles = getSampleStyleSheet()
story = []

# 简单处理：将HTML转为文本并添加到PDF
lines = md_content.split('\n')
for line in lines:
    if line.startswith('# '):
        title = line.replace('# ', '')
        p = Paragraph(title, styles['Heading1'])
        story.append(p)
    elif line.startswith('## '):
        title = line.replace('## ', '')
        p = Paragraph(title, styles['Heading2'])
        story.append(p)
    elif line.startswith('### '):
        title = line.replace('### ', '')
        p = Paragraph(title, styles['Heading3'])
        story.append(p)
    elif line.strip():
        p = Paragraph(line, styles['Normal'])
        story.append(p)
    else:
        story.append(Spacer(1, 0.1*inch))

# 生成PDF
doc.build(story)
print(f"PDF created: {pdf_file}")
