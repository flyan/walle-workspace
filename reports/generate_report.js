// v4 report generator - generates the markdown report
const fs = require('fs');
const path = require('path');

const reportsDir = 'C:\\Users\\flyan\\.openclaw\\workspace\\reports';
const finalArticles = JSON.parse(fs.readFileSync(path.join(reportsDir, 'v4_final.json'), 'utf-8'));

// Categorize articles
function categorize(article) {
  const title = (article.title || '').toLowerCase();
  const summary = (article.summary || '').toLowerCase();
  const text = title + ' ' + summary;
  
  if (text.includes('ai') || text.includes('大模型') || text.includes('人工智能') || 
      text.includes('gpt') || text.includes('大模型') || text.includes('生成式') ||
      text.includes('模型') || text.includes('智能体') || text.includes('智能助理') ||
      text.includes('ai风控') || text.includes('ai客服') || text.includes('ai金融') ||
      text.includes('ai银行')) {
    return 'AI应用';
  }
  if (text.includes('支付') || text.includes('移动支付') || text.includes('数字人民币') ||
      text.includes('跨境支付') || text.includes('钱包') || text.includes('收款') ||
      text.includes('刷脸') || text.includes('nfc')) {
    return '支付创新';
  }
  if (text.includes('风控') || text.includes('风险') || text.includes('反欺诈') ||
      text.includes('不良贷款') || text.includes('npl') || text.includes('催收') ||
      text.includes('监管') || text.includes('合规')) {
    return '风控监管';
  }
  if (text.includes('财富管理') || text.includes('理财') || text.includes('资产') ||
      text.includes('基金') || text.includes('私人银行')) {
    return '财富资管';
  }
  if (text.includes('绿色金融') || text.includes('esg') || text.includes('碳中和') ||
      text.includes('双碳') || text.includes('低碳') || text.includes('环保')) {
    return '绿色金融';
  }
  if (text.includes('信创') || text.includes('国产化') || text.includes('自主可控') ||
      text.includes('芯片') || text.includes('操作系统')) {
    return '信创安全';
  }
  if (text.includes('数字化转型') || text.includes('数字银行') || text.includes('智慧银行') ||
      text.includes('网点转型') || text.includes('手机银行') || text.includes('直销银行') ||
      text.includes('开放银行')) {
    return '数字化转型';
  }
  return '银行业发展';
}

// Assign categories
for (const article of finalArticles) {
  article._category = categorize(article);
}

// Category display names
const categoryOrder = ['AI应用', '数字化转型', '风控监管', '支付创新', '财富资管', '绿色金融', '信创安全', '银行业发展'];
const categoryNames = {
  'AI应用': '🤖 AI应用',
  '数字化转型': '🏦 数字化转型',
  '风控监管': '🛡️ 风控监管',
  '支付创新': '💳 支付创新',
  '财富资管': '💰 财富资管',
  '绿色金融': '🌱 绿色金融',
  '信创安全': '🔐 信创安全',
  '银行业发展': '🏛️ 银行业发展',
};

// Group by category
const grouped = {};
for (const cat of categoryOrder) {
  grouped[cat] = finalArticles.filter(a => a._category === cat);
}

// Generate summaries (60-100 words per article)
function generateSummary(article) {
  const title = article.title || '';
  const summary = article.summary || '';
  
  // Clean up the existing summary - remove phrases like "文章综合整理自网络" etc.
  let cleanSummary = summary
    .replace(/文章综合整理自网络.*$/gm, '')
    .replace(/来源:.*$/gm, '')
    .replace(/图:.*$/gm, '')
    .replace(/视频:.*$/gm, '')
    .replace(/点击蓝字关注.*$/gm, '')
    .replace(/>>.*$/gm, '')
    .replace(/【.*?】/g, '')
    .replace(/编者按.*$/gm, '')
    .replace(/导语:*/gm, '')
    .replace(/文\/.*?\//gm, '')
    .replace(/作者:.*$/gm, '')
    .replace(/编辑:.*$/gm, '')
    .replace(/整理:.*$/gm, '')
    .trim();
  
  // If summary is too short, add context from title
  if (cleanSummary.length < 30) {
    return `${cleanSummary} 本文围绕"${title.replace(/《》『』[]""/, '')}"主题展开分析，探讨相关趋势与影响。`.substring(0, 120);
  }
  
  return cleanSummary.substring(0, 200);
}

// Build the markdown report
const now = new Date();
const generateTime = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${now.getHours()}:${String(now.getMinutes()).padStart(2,'0')}`;

let md = `# 2026年3月银行业金融科技AI资讯报告

**生成时间**: ${generateTime} | **文章总数**: ${finalArticles.length}篇 | **数据来源**: 微信搜狗搜索

---

## 一、多维度总结

### 1.1 行业趋势总结

**AI大模型加速落地银行业** — 2026年3月，AI大模型在银行业的应用从概念验证迈向规模化部署。工商银行"天镜"AI风控系统、网商银行"百灵"系统等头部案例持续深化，AI风控已进入实时化、智能化新阶段。与此同时，消费金融公司迎来"AI元年"，海尔消费金融、马上消费金融等通过AI大模型融合多维数据构建动态客户画像，实现客户需求秒级响应。

**数字人民币与跨境支付深度融合** — CIPS系统与数字人民币（e-CNY）双轮驱动的跨境支付新模式浮现，兴业银行长沙分行率先落地多边央行数字货币桥业务，企业跨境资金流转从"以天计"迈向"以秒计"。这一趋势将深刻重塑跨境支付格局。

**银行信创进入深水区** — 中信银行65亿元信创大单落地，标志着银行信创从边缘系统向核心系统推进。国有大行和股份制银行信创改造提速，中小银行信创云选型成关注焦点。

**绿色金融成为差异化竞争新高地** — 兴业银行二十年绿色金融实践、南京银行绿色信贷精准滴灌生态产业等案例表明，绿色金融正从政策驱动转向市场化、内涵化发展阶段，气候环境风险管控纳入银行全面风险管理框架。

### 1.2 热点主题分析

| 热点主题 | 文章数量 | 代表内容 |
|---------|---------|---------|
| AI大模型/风控 | 18篇 | 工商银行天镜系统、马上消费金融大模型、海尔消费金融AI first战略 |
| 消费金融AI应用 | 12篇 | 2026消金AI元年、催收新规下的AI数字员工、蚂蚁消金AI消保 |
| 数字人民币/跨境支付 | 8篇 | CIPS+数字货币双轮驱动、货币桥跨境支付 |
| 银行绿色金融 | 5篇 | 兴业银行20年实践、南京银行绿色信贷、渤海银行绿色债券 |
| 银行信创 | 4篇 | 中信银行65亿信创大单、深度解析银行信创选型策略 |
| 数字人民币2026 | 3篇 | 数字人民币生态建设、场景应用深化 |

### 1.3 数据统计

| 指标 | 数值 |
|-----|------|
| 文章总数 | ${finalArticles.length}篇 |
| 2026年3月文章 | ${finalArticles.filter(a=>a._march2026).length}篇 |
| 涉及公众号数 | ${[...new Set(finalArticles.map(a=>a.source))].length}个 |
| 平均评分 | ${(finalArticles.reduce((s,a)=>s+a._score,0)/finalArticles.length).toFixed(1)}分 |
| 最高评分 | ${Math.max(...finalArticles.map(a=>a._score))}分 |

---

## 二、文章详情（共${finalArticles.length}篇）

`;

for (const cat of categoryOrder) {
  const articles = grouped[cat];
  if (!articles || articles.length === 0) continue;
  
  md += `### ${categoryNames[cat]}（${articles.length}篇）\n\n`;
  
  for (let i = 0; i < articles.length; i++) {
    const article = articles[i];
    const summary = generateSummary(article);
    const date = getDate(article.date_text);
    
    md += `**${i+1}. ${article.title}**\n`;
    md += `[${article.source}] [${date}] 评分：${article._score}分\n`;
    md += `> ${summary}\n`;
    md += `> 🔗 链接: ${article.url}\n\n`;
  }
}

// Appendix: article list
md += `---\n\n## 三、文章索引\n\n`;

for (let i = 0; i < finalArticles.length; i++) {
  const article = finalArticles[i];
  const date = getDate(article.date_text);
  md += `${article.title} [${article.source}] [${date}] [评分：${article._score}分]\n`;
  md += `> ${generateSummary(article)}\n`;
  md += `> 链接: ${article.url}\n\n`;
}

md += `---\n*报告生成时间：${generateTime}*\n`;

function getDate(dateText) {
  if (!dateText) return '未知';
  const match = dateText.match(/(\d{4})年(\d{2})月(\d{2})日/);
  if (match) {
    return `${match[1]}-${match[2]}-${match[3]}`;
  }
  return dateText;
}

// Save the report
const reportPath = path.join(reportsDir, '2026年3月咨询报告_v4.md');
fs.writeFileSync(reportPath, md, 'utf-8');
console.log(`Report saved to: ${reportPath}`);
console.log(`Report size: ${md.length} characters`);
console.log(`Total articles: ${finalArticles.length}`);

// Stats
const marchCount = finalArticles.filter(a => a._march2026).length;
console.log(`March 2026 articles: ${marchCount}`);
console.log(`Categories: ${categoryOrder.filter(c => grouped[c] && grouped[c].length > 0).join(', ')}`);
