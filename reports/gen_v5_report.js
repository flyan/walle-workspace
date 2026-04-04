// gen_v5_report.js - Generate the v5 report
const fs = require('fs');

const whitelistSources = new Set([
  '机器之心','量子位','新智元','极客公园','硅星人','智东西',
  '馨金融','零壹财经','未央网','一本财经','十字财经','新金融洛书','独角金融','移动支付网','支付百科','消金界','第一消费金融','易鑫','金融数字化观察',
  '轻金融','中国银行保险报','银行家杂志','愉见财经','零售银行','信贷风险管理','行长要参','支行长','银行科技研究社','银行青年',
  '中国工商银行','中国建设银行','中国农业银行','中国银行','中国邮政储蓄银行','交通银行',
  '招商银行','招商银行信用卡','兴业银行','中信银行','上海浦东发展银行',
  '中原银行','宁波银行','盛京银行','蒙商银行',
  '国家金融监督管理总局','央行发布','中国银行业杂志','中国金融四十人论坛','星图金融研究院','麦肯锡','波士顿咨询','金融论坛',
  '第一财经','澎湃新闻','金融界','华尔��见闻','钛媒体','东方财富网','投资明见','商行新鲜事','思维纪要社','国际金融报','运营商财经',
  '中金公司','华泰证券','招商证券',
  '未央网weiyangx','银行家杂志','中国工商银行','交通银行','零壹财经','钛媒体','移动支付网','轻金融','银行科技研究社'
]);

const finalData = require('./v4_final.json');
const filteredData = require('./v4_filtered.json');
const finalUrls = new Set(finalData.map(a => a.url));

// March 2026 articles from v4_final (all score>=70)
const marchArticles = finalData
  .filter(a => a._march2026 && a._score >= 70)
  .sort((a, b) => b._score - a._score);

// Non-March from v4_filtered: whitelist, score>=70, not in final
const nonMarchSupp = filteredData
  .filter(a => !a._march2026 && (a._score||0) >= 70 && whitelistSources.has(a.source) && !finalUrls.has(a.url))
  .sort((a, b) => b._score - a._score)
  .slice(0, 11);

const allArticles = [...marchArticles, ...nonMarchSupp];

// Categories
const aiBanking = [];       // AI大模型+银行应用
const consumerFinance = []; // 消费金融AI
const digitalCNY = [];      // 数字人民币+跨境支付
const greenFinance = [];    // 绿色金融
const bankTech = [];        // 银行信创+IT
const industryTrends = [];  // 行业趋势+综合

const aiKW = ['大模型','AI','智能体','人工智能','生成式AI','ChatGPT'];
const cfKW = ['消费金融','消金','催收','贷款','信贷'];
const dcnKW = ['数字人民币','数字货币','e-CNY','跨境支付','货币桥','CIPS','稳定币'];
const gfKW = ['绿色金融','绿色信贷','双碳','ESG','气候'];
const btKW = ['信创','中标','IT','系统','数据库','存储','科技'];

function classify(article) {
  const t = article.title + ' ' + (article.summary||'');
  const scores = {
    ai: aiKW.reduce((s,k) => s + (t.includes(k)?1:0), 0),
    cf: cfKW.reduce((s,k) => s + (t.includes(k)?1:0), 0),
    dcn: dcnKW.reduce((s,k) => s + (t.includes(k)?1:0), 0),
    gf: gfKW.reduce((s,k) => s + (t.includes(k)?1:0), 0),
    bt: btKW.reduce((s,k) => s + (t.includes(k)?1:0), 0),
  };
  // Priority: specific > general
  if (scores.dcn >= 1) return 'dcn';
  if (scores.gf >= 1) return 'gf';
  if (scores.bt >= 1) return 'bt';
  if (scores.cf >= 1 && scores.ai >= 1) return 'cf';
  if (scores.ai >= 1) return 'ai';
  return 'industry';
}

marchArticles.forEach(a => {
  const cat = classify(a);
  if (cat === 'ai') aiBanking.push(a);
  else if (cat === 'cf') consumerFinance.push(a);
  else if (cat === 'dcn') digitalCNY.push(a);
  else if (cat === 'gf') greenFinance.push(a);
  else if (cat === 'bt') bankTech.push(a);
  else industryTrends.push(a);
});

nonMarchSupp.forEach(a => industryTrends.push(a));

console.log('Categories:');
console.log('AI Banking:', aiBanking.length);
console.log('Consumer Finance:', consumerFinance.length);
console.log('Digital CNY:', digitalCNY.length);
console.log('Green Finance:', greenFinance.length);
console.log('Bank Tech:', bankTech.length);
console.log('Industry:', industryTrends.length);
console.log('Total:', allArticles.length);

// Summaries for each article (generated inline - these are template summaries based on titles)
// The actual summaries will be written in the report

// Export for use
module.exports = { allArticles, marchArticles, nonMarchSupp, aiBanking, consumerFinance, digitalCNY, greenFinance, bankTech, industryTrends };
