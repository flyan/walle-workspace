// Report v5 generator
const fs = require('fs');
const path = require('path');

const whitelistSources = new Set([
  '机器之心','量子位','新智元','极客公园','硅星人','智东西',
  '馨金融','零壹财经','未央网','一本财经','十字财经','新金融洛书','独角金融','移动支付网','支付百科','消金界','第一消费金融','易鑫','金融数字化观察',
  '轻金融','中国银行保险报','银行家杂志','愉见财经','零售银行','信贷风险管理','行长要参','支行长','银行科技研究社','银行青年',
  '中国工商银行','中国建设银行','中国农业银行','中国银行','中国邮政储蓄银行','交通银行',
  '招商银行','招商银行信用卡','兴业银行','中信银行','上海浦东发展银行',
  '中原银行','宁波银行','盛京银行','蒙商银行',
  '国家金融监督管理总局','央行发布','中国银行业杂志','中国金融四十人论坛','星图金融研究院','麦肯锡','波士顿咨询','金融论坛',
  '第一财经','澎湃新闻','金融界','华尔街见闻','钛媒体','东方财富网','投资明见','商行新鲜事','思维纪要社','国际金融报','运营商财经',
  '中金公司','华泰证券','招商证券',
  // Exact matches from data
  '未央网weiyangx','银行家杂志','中国工商银行','交通银行','零壹财经','钛媒体','移动支付网','轻金融','银行科技研究社'
]);

const relatedSources = new Set([
  '兴业银行长沙分行','中国工商银行数据中心','招商银行信用卡','交通银行研究员'
]);

function isAcceptable(source) {
  return whitelistSources.has(source) || relatedSources.has(source);
}

const finalData = require('./v4_final.json');
const filteredData = require('./v4_filtered.json');
const finalUrls = new Set(finalData.map(a => a.url));

// March 2026 articles from v4_final
const marchArticles = finalData
  .filter(a => a._march2026 && a._score >= 70)
  .sort((a, b) => b._score - a._score);

// Non-March from v4_filtered that are in whitelist and not in final
const nonMarchWL = filteredData
  .filter(a => !a._march2026 && (a._score||0) >= 70 && isAcceptable(a.source) && !finalUrls.has(a.url))
  .sort((a, b) => b._score - a._score)
  .slice(0, 20);  // max 20 to complement

// Combine: all March + non-March supplement
const allArticles = [...marchArticles, ...nonMarchWL];

console.log('March articles:', marchArticles.length);
console.log('Non-March supplement:', nonMarchWL.length);
console.log('Total:', allArticles.length);
console.log('');
console.log('Non-March sources used:');
nonMarchWL.forEach(a => console.log('  ' + a._score + ' | ' + a.source + ' | ' + a.datetime));
