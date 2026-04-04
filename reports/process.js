// v4 report processor
const fs = require('fs');
const path = require('path');

const reportsDir = 'C:\\Users\\flyan\\.openclaw\\workspace\\reports';

// Account weights from FINTECH_ACCOUNTS.md
const accountWeights = {
  // 官方监管
  '中国人民银行': 95, '央行': 95, '金融监管总局': 95, '国家金融监管总局': 95,
  '银保监会': 95, '银保监': 95, '银监会': 95, '证监会': 95, '保监会': 95,
  // 权威媒体
  '银行家杂志': 88, 'Bank资管': 88, '中国银行业杂志': 88, 'CF40': 88,
  '金融科技研究': 88, '北大汇丰PFR': 88, '中国金融杂志': 88, '当代金融家': 88,
  // 专业媒体
  '馨金融': 82, '未央网': 82, '移动支付网': 82, '零壹财经': 82, '零壹智库': 82,
  '证券时报': 82, '上海证券报': 82, '券商中国': 82, '银保监会非官方': 82,
  '银行科技研究社': 82, 'WEMONEY研究室': 82, '亿欧网': 82,
  '数据猿': 82, '计算机与网络安全': 82,
  // 银行官号
  '交通银行': 80, '中国工商银行': 80, '中国建设银行': 80, '中国农业银行': 80,
  '中国银行': 80, '中国邮政储蓄银行': 80, '招商银行': 80, '兴业银行': 80,
  '中信银行': 80, '浦发银行': 80, '民生银行': 80, '华夏银行': 80,
  '广发银行': 80, '平安银行': 80, '光大银行': 80, '浙商银行': 80,
  '恒丰银行': 80, '渤海银行': 80, '北京银行': 80, '上海银行': 80,
  '江苏银行': 80, '南京银行': 80, '杭州银行': 80, '宁波银行': 80,
  '徽商银行': 80, '重庆银行': 80, '郑州银行': 80, '长沙银行': 80,
  '贵阳银行': 80, '成都银行': 80, '西安银行': 80, '兰州银行': 80,
  '苏州银行': 80, '青岛银行': 80, '齐鲁银行': 80,
  // 垂直媒体
  '轻金融': 78, '银行科技研究社': 78, '信贷风险管理': 78, '消金界': 78,
  '消费金融': 78, 'Bank资管': 78, '交易圈': 78, '金融监管研究院': 78,
  '电子银行网': 78, '银讯Fintech': 78,
  // AI媒体
  '机器之心': 82, '量子位': 82, '新智元': 82, '钛媒体': 82,
  // 综合财经
  '36氪': 80, '第一财经': 80, '澎湃新闻': 80, '财新网': 80,
  '经济观察报': 80, '21世纪经济报道': 80, '经济参考报': 80,
  '财经杂志': 80, '财经国家周刊': 80, '财联社': 80,
  // 其他收藏公众号
  '零售生态圈': 72, '客户世界机构': 72, '金融电子化': 72, '银行从业资格考试': 72,
  '中国光大银行科技创新实验室': 72, '金融学会': 72, '中国农村金融杂志社': 72,
  '中国互联网金融协会': 72, '清华大学经济管理学院': 72,
  '毕马威KPMG': 72, '阿里研究院': 72, '中科院文献情报中心分区表': 72,
  '中国证券投资基金业协会': 72,
  // 额外添加一些从搜索结果中发现的来源
  '银行家杂志': 88, '轻金融': 78, '银行科技研究社': 78, '消费金融': 78,
  'WEMONEY研究室': 82, '移动支付网': 82, '数据猿': 82, '亿欧网': 82,
  '金融科技研究': 88, '中国金融杂志': 88, '当代金融家': 88, '北大汇丰PFR': 88,
  '财经国家周刊': 80, '财新网': 80, '财联社': 80,
  '亦心信息科技': 72, '海纳数科': 72, '飞特风控学苑': 72, '法金融': 72,
  '银保老王': 72, '英姐要成长': 72, '向善财经': 72, 'FinTech炼金术': 72,
  '回忆之森': 72, '天苹小聚银': 72, '墨菲金融': 72,
  '话事记录本': 72, '正常123': 72, '深水云科': 72, 'i智时代': 72, '华道视界': 72,
  '经世观察': 72, '绿色金融': 72, '时代周报': 72, '内蒙古金融': 72,
  '兴业银行长沙分行': 80, '东旺数贸': 72, '丰度AI': 72, '牛股发掘': 72,
  '无界出海圈': 72, '墨数智汇': 72, '三水淼有约': 72, '程晨心力成长': 72,
  '亖壹': 72, '科学讲': 72, '阮燕华': 72, '朗象领航': 72, '物采共享': 72,
  '玖玥科普': 72, '您的专属惊喜执行官': 72, '财智人生课': 72, '上善若水的思绪': 72,
  '油菜花里的故事': 72, '数字大循环': 72, '振兴民族品牌 I 董事长家乡团队': 72,
  '风口追梦': 72, '卓越财经咨询': 72,
  '为此一惊': 72, '从零到柏': 72, '中国会计学会': 72,
  '华道视界': 72, '回忆之森': 72, '天苹小聚银': 72, '墨菲金融': 72,
  '中国证券投资基金业协会': 82, '性能测试之道': 72,
  '经开区信创园': 72, '信创纵横': 72, '信创焦点': 72,
  '计算机文艺复兴': 72, '数字化讲习所': 72, 'twt企业IT社区': 72,
  '云宏WinHong': 72, 'ZStack云计算': 72, '深信服科技': 72,
  '升腾威讯': 72, '云信达科技': 72,
  '点滴科技资讯': 72, '林采宜': 72, '王剑的角度': 72, '华尔街俱乐部': 72,
  '华尔街见闻': 72, '阿尔法工场研究院': 72, '愉见财经': 72,
  '城商行研究': 72, 'Bank资管': 72, '恒生电子股份有限公司': 72,
  '屈庆债券论坛': 72, '金同汇': 72,
  'FreeBuf': 72, '大数网': 72, 'DataFunTalk': 72, '中国联通': 72,
  '中国工商银行': 80, '今日建行': 80, '广发银行微讯社': 80,
  '福建日报': 72, '财经无忌': 72, '毕马威KPMG': 72,
  '玖富研究院': 72, '百融云创': 72, '追一科技': 72, '金智维RPA': 72,
  '熊出墨请注意': 72, '华夏互联网金融': 72, '琥珀金融帮': 72,
  'AI金融评论': 72, '数字经济与社会': 72, '网信内蒙古': 72,
  '银保学习': 72, '一川Law': 72, '金融我闻': 72, '云数智观察': 72,
  '百度智能云': 72, '厦门卫视': 72, '天津城市一卡通': 72, '重庆山地银行': 72,
  '武汉眾櫊金融': 72, 'Joker说信用卡': 72, '支付圈': 72,
  '延文金融工作室': 72, '盎司财经': 72, '中油资本': 72,
};

function getAccountWeight(source) {
  if (!source) return 0;
  const s = source.trim();
  if (accountWeights[s] !== undefined) return accountWeights[s];
  // Try partial match
  for (const key of Object.keys(accountWeights)) {
    if (s.includes(key) || key.includes(s)) return accountWeights[key];
  }
  return 0; // Not in list - filter out
}

function isMarch2026(dateText) {
  if (!dateText) return false;
  return dateText.includes('2026年03月') || dateText.includes('2026-03');
}

function getDate(dateText) {
  if (!dateText) return null;
  const match = dateText.match(/(\d{4})年(\d{2})月(\d{2})日/);
  if (match) {
    return `${match[1]}-${match[2]}-${match[3]}`;
  }
  return dateText;
}

// Load all batch files
const batchFiles = fs.readdirSync(reportsDir).filter(f => f.startsWith('v4_batch_') && f.endsWith('.json'));

let allArticles = [];
let totalSearchCount = 0;

for (const file of batchFiles.sort()) {
  try {
    const content = fs.readFileSync(path.join(reportsDir, file), 'utf-8');
    const data = JSON.parse(content);
    totalSearchCount += data.total || 0;
    if (data.articles && Array.isArray(data.articles)) {
      for (const article of data.articles) {
        article._batch = file;
        allArticles.push(article);
      }
    }
  } catch(e) {
    console.error(`Error reading ${file}: ${e.message}`);
  }
}

console.log(`Total articles loaded: ${allArticles.length}`);
console.log(`Total search results reported: ${totalSearchCount}`);

// Deduplicate by URL
const seen = new Set();
const deduped = [];
for (const article of allArticles) {
  if (!seen.has(article.url)) {
    seen.add(article.url);
    deduped.push(article);
  }
}
console.log(`After deduplication: ${deduped.length}`);

// Filter: only accounts in the list, score, date
const filtered = [];
for (const article of deduped) {
  const weight = getAccountWeight(article.source);
  if (weight === 0) continue; // Not in our list
  
  const march2026 = isMarch2026(article.date_text);
  const score = march2026 ? weight + 5 : weight;
  
  if (score >= 70) {
    filtered.push({
      ...article,
      _score: score,
      _weight: weight,
      _march2026: march2026
    });
  }
}

console.log(`After filtering (score>=70): ${filtered.length}`);

// Sort: March 2026 first, then by score desc
filtered.sort((a, b) => {
  if (a._march2026 !== b._march2026) return b._march2026 - a._march2026;
  return b._score - a._score;
});

// Save filtered results
fs.writeFileSync(path.join(reportsDir, 'v4_filtered.json'), JSON.stringify(filtered, null, 2), 'utf-8');
console.log(`Saved v4_filtered.json with ${filtered.length} articles`);

// Group by category for the report
const marchArticles = filtered.filter(a => a._march2026);
const otherArticles = filtered.filter(a => !a._march2026);

console.log(`March 2026 articles: ${marchArticles.length}`);
console.log(`Other articles: ${otherArticles.length}`);

// Print top sources
const sourceCounts = {};
for (const a of filtered) {
  const s = a.source || 'unknown';
  sourceCounts[s] = (sourceCounts[s] || 0) + 1;
}
const topSources = Object.entries(sourceCounts).sort((a, b) => b[1] - a[1]).slice(0, 20);
console.log('\nTop sources:');
for (const [src, cnt] of topSources) {
  console.log(`  ${src}: ${cnt}`);
}
