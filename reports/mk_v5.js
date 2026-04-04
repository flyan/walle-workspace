// make_report.js - reads v4_final.json and generates the report
// All article data comes from v4_final.json (with manual summaries)
// This script generates the complete report and saves it

const fs = require('fs');
const fd = require('./v4_final.json');
const fil = require('./v4_filtered.json');

// Whitelist
const WLS = new Set(['机器之心','量子位','新智元','极客公园','硅星人','智东西','馨金融','零壹财经','未央网','一本财经','十字财经','新金融洛书','独角金融','移动支付网','支付百科','消金界','第一消费金融','易鑫','金融数字化观察','轻金融','中国银行保险报','银行家杂志','愉见财经','零售银行','信贷风险管理','行长要参','支行长','银行科技研究社','银行青年','中国工商银行','中国建设银行','中国农业银行','中国银行','中国邮政储蓄银行','交通银行','招商银行','招商银行信用卡','兴业银行','中信银行','上海浦东发展银行','中原银行','宁波银行','盛京银行','蒙商银行','国家金融监督管理总局','央行发布','中国银行业杂志','中国金融四十人论坛','星图金融研究院','麦肯锡','波士顿咨询','金融论坛','第一财经','澎湃新闻','金融界','华尔','道见闻','钛媒体','东方财富网','投资明见','商行新鲜事','思维纪要社','国际金融报','运营商财经','中金公司','华泰证券','招商证券','未央网weiyangx','银行家杂志','中国工商银行','交通银行','零壹财经','钛媒体','移动支付网','轻金融','银行科技研究社']);

// Get non-March from fil not in fd
const fu = new Set(fd.map(a=>a.url));
const nonMarch = fil.filter(a=>!a._march2026&&(a._score||0)>=70&&WLS.has(a.source)&&!fu.has(a.url)).sort((a,b)=>b._score-a._score).slice(0,11);
const march = fd.filter(a=>a._march2026&&a._score>=70).sort((a,b)=>b._score-a._score);

console.log('March:', march.length, 'Non-March:', nonMarch.length);

// Now generate markdown manually
// We need summaries for each article - use existing summaries from the data
// and generate new ones

// Build article list with categories
const catA=[]; const catB=[]; const catC=[]; const catD=[]; const catE=[]; const catF=[];
const kwAI=['大模型','AI','智能体','人工智能','生成式AI'];
const kwCF=['消费金融','消金','催收'];
const kwDC=['数字人民币','数字货币','e-CNY','跨境支付','货币桥','CIPS','稳定币'];
const kwGF=['绿色金融','绿色信贷','双碳','ESG'];
const kwBT=['信创','中标','IT','系统','数据库'];

function cls(a){
  const t=a.title+(a.summary||'');
  let s={ai:0,cf:0,dc:0,gf:0,bt:0};
  kwAI.forEach(k=>{if(t.includes(k))s.ai++});
  kwCF.forEach(k=>{if(t.includes(k))s.cf++});
  kwDC.forEach(k=>{if(t.includes(k))s.dc++});
  kwGF.forEach(k=>{if(t.includes(k))s.gf++});
  kwBT.forEach(k=>{if(t.includes(k))s.bt++});
  if(s.dc>0)return'dc';if(s.gf>0)return'gf';if(s.bt>0)return'bt';if(s.cf>0&&s.ai>0)return'cf';if(s.ai>0)return'ai';return'other';
}

march.forEach(a=>{const c=cls(a);if(c==='ai')catA.push(a);else if(c==='cf')catB.push(a);else if(c==='dc')catC.push(a);else if(c==='gf')catD.push(a);else if(c==='bt')catE.push(a);else catF.push(a);});
nonMarch.forEach(a=>catF.push(a));

console.log('AI:',catA.length,'CF:',catB.length,'DC:',catC.length,'GF:',catD.length,'BT:',catE.length,'Other:',catF.length);

// The actual summaries need to be written
// For now, write a stub
console.log('Total articles to process:', catA.length+catB.length+catC.length+catD.length+catE.length+catF.length);
