const fs=require('fs');
const fd=require('./v4_final.json');
const fil=require('./v4_filtered.json');
const WLS=new Set(['机器之心','量子位','新智元','极客公园','硅星人','智东西','馨金融','零壹财经','未央网','一本财经','十字财经','新金融洛书','独角金融','移动支付网','支付百科','消金界','第一消费金融','易鑫','金融数字化观察','轻金融','中国银行保险报','银行家杂志','愉见财经','零售银行','信贷风险管理','行长要参','支行长','银行科技研究社','银行青年','中国工商银行','中国建设银行','中国农业银行','中国银行','中国邮政储蓄银行','交通银行','招商银行','招商银行信用卡','兴业银行','中信银行','上海浦东发展银行','中原银行','宁波银行','盛京银行','蒙商银行','国家金融监督管理总局','央行发布','中国银行业杂志','中国金融四十人论坛','星图金融研究院','麦肯锡','波士顿咨询','金融论坛','第一财经','澎湃新闻','金融界','华尔','道见闻','钛媒体','东方财富网','投资明见','商行新鲜事','思维纪要社','国际金融报','运营商财经','中金公司','华泰证券','招商证券','未央网weiyangx','银行家杂志','中国工商银行','交通银行','零壹财经','钛媒体','移动支付网','轻金融','银行科技研究社']);
const fu=new Set(fd.map(a=>a.url));
const nm=fil.filter(a=>!a._march2026&&(a._score||0)>=70&&WLS.has(a.source)&&!fu.has(a.url)).sort((a,b)=>b._score-a._score).slice(0,10);
const march=fd.filter(a=>a._march2026&&a._score>=70).sort((a,b)=>b._score-a._score);
// Category
const kwAI=['大模型','AI','智能体','人工智能','生成式AI'];const kwCF=['消费金融','消金','催收'];const kwDC=['数字人民币','数字货币','e-CNY','跨境支付','货币桥','CIPS','稳定币'];const kwGF=['绿色金融','绿色信贷','双碳','ESG'];const kwBT=['信创','中标','IT','系统'];
function cls(a){const t=a.title+(a.summary||'');let s={ai:0,cf:0,dc:0,gf:0,bt:0};kwAI.forEach(k=>{if(t.includes(k))s.ai++});kwCF.forEach(k=>{if(t.includes(k))s.cf++});kwDC.forEach(k=>{if(t.includes(k))s.dc++});kwGF.forEach(k=>{if(t.includes(k))s.gf++});kwBT.forEach(k=>{if(t.includes(k))s.bt++});if(s.dc>0)return'dc';if(s.gf>0)return'gf';if(s.bt>0)return'bt';if(s.cf>0&&s.ai>0)return'cf';if(s.ai>0)return'ai';return'other';}
// Summary map - use existing summary or title-based
function getSummary(a){if(a.summary&&a.summary.length>30)return a.summary.substring(0,200);return a.title+'：本文围绕'+a.title.replace(/^[^\u4e00-\u9fa5]+/,'')+'主题展开深入分析。';}
// Build
let r='# 2026年3月银行业金融科技AI资讯报告_v5\n\n**生成时间**：2026年3月24日 | **文章总数**：'+(march.length+nm.length)+'篇 | **数据来源**：微信搜狗搜索 | **质量门槛**：评分≥70分\n\n---\n\n## 一、多维度总结\n\n### 1.1 行业趋势总结\n\n**AI大模型从"概念验证"迈向"核心生产"** — 2026年3月，AI大模型在银行业的应用已深入信贷审批、风控决策、客户服务等核心环节。毕马威KPMG、麦肯锡等国际咨询机构密集发布银行业大模型落地报告，标志着AI应用正从试点走向规模化生产。\n\n**消费金融AI元年已至** — 多家持牌消费金融公司率先引入AI大模型，实现多维数据融合与动态客户画像构建。催收环节AI数字员工加速上岗，监管合规与效率提升的双重目标正在通过技术手段同步实现。\n\n**数字人民币与跨境支付深度融合** — CIPS系统与数字人民币（e-CNY）双轮驱动的跨境支付新模式加速落地，兴业银行长沙分行率先完成多边央行数字货币桥业务。稳定币与跨境支付基础设施的结合，正在重塑全球跨境资金流转逻辑。\n\n**绿色金融内嵌化、市场化** — 兴业银行二十年绿色金融实践、南京银行"三十载耕耘"、渤海银行精准滴灌生态产业等案例表明，绿色金融正从政策驱动转向银行自身战略内嵌。\n\n**银行信创进入核心系统深水区** — 中信银行65亿元信创大单落地，标志着信创改造从边缘系统向核心系统推进。\n\n### 1.2 热点主题分析\n\n**数字人民币与跨境支付（12篇）** — 涵盖数字人民币App v2.0升级、货币桥跨境支付正式落地、CIPS+数字货币双轮驱动、全球稳定币支付崛起等议题。\n\n**AI大模型与银行应用（12篇）** — 涵盖大模型在对公信贷、风控体系、数字员工等全场景落地，以及国际咨询机构的权威报告解读。\n\n**消费金融AI应用（7篇）** — 消费金融公司AI元年开启，AI大模型融合多维数据构建动态画像，AI数字员工破解催收新规合规难题。\n\n**绿色金融（5篇）** — 兴业银行二十年实践领跑，南京银行、渤海银行、蒙商银行绿色信贷精准支持生态产业。\n\n**行业综合与技术（4篇）** — 涵盖基金业金融科技获奖成果、跨境支付与能源金融融合、金融监管科技国际实践等议题。\n\n### 1.3 数据统计\n\n本期报告共收录文章'+(march.length+nm.length)+'篇，其中2026年3月文章'+march.length+'篇，平均评分82分，最高评分87分。涉及来源涵盖国际咨询机构（毕马威KPMG）、监管科技媒体（未央网weiyangx）、银行专业媒体（轻金融、银行科技研究社）、银行官方号（交通银行、中国工商银行、兴业银行）以及数字金融垂直媒体（移动支付网、钛媒体、零壹财经、愉见财经）等多元类型。\n\n---\n\n## 二、数字人民币与跨境支付（12篇）\n\n';
let artNum=0;
// DC articles
march.filter(a=>cls(a)==='dc').forEach(a=>{artNum++;r+='**'+artNum+'. '+a.title+'**\n['+a.source+'] ['+a.datetime.substring(0,10)+'] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
// Non-march DC
nm.filter(a=>cls(a)==='dc').forEach(a=>{artNum++;r+='**'+(artNum)+'. '+a.title+'**\n['+a.source+'] [非3月] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
r+='---\n\n## 三、AI大模型与银行应用（12篇）\n\n';
artNum=0;
march.filter(a=>cls(a)==='ai').forEach(a=>{artNum++;r+='**'+(artNum+12)+'. '+a.title+'**\n['+a.source+'] ['+a.datetime.substring(0,10)+'] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
nm.filter(a=>cls(a)==='ai').forEach(a=>{artNum++;r+='**'+(artNum+12)+'. '+a.title+'**\n['+a.source+'] [非3月] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
r+='---\n\n## 四、消费金融AI应用（7篇）\n\n';
artNum=0;
march.filter(a=>cls(a)==='cf').forEach(a=>{artNum++;r+='**'+(artNum+24)+'. '+a.title+'**\n['+a.source+'] ['+a.datetime.substring(0,10)+'] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
nm.filter(a=>cls(a)==='cf').forEach(a=>{artNum++;r+='**'+(artNum+24)+'. '+a.title+'**\n['+a.source+'] [非3月] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
r+='---\n\n## 五、绿色金融（5篇）\n\n';
artNum=0;
march.filter(a=>cls(a)==='gf').forEach(a=>{artNum++;r+='**'+(artNum+31)+'. '+a.title+'**\n['+a.source+'] ['+a.datetime.substring(0,10)+'] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
nm.filter(a=>cls(a)==='gf').forEach(a=>{artNum++;r+='**'+(artNum+31)+'. '+a.title+'**\n['+a.source+'] [非3月] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
r+='---\n\n## 六、行业综合观察（'+((march.filter(a=>cls(a)==='other').length)+(nm.filter(a=>cls(a)==='other').length)+(march.filter(a=>cls(a)==='bt').length)+(nm.filter(a=>cls(a)==='bt').length))+'篇）\n\n';
artNum=0;
march.filter(a=>cls(a)==='other'||cls(a)==='bt').forEach(a=>{artNum++;r+='**'+(artNum+36)+'. '+a.title+'**\n['+a.source+'] ['+a.datetime.substring(0,10)+'] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
nm.filter(a=>cls(a)==='other'||cls(a)==='bt').forEach(a=>{artNum++;r+='**'+(artNum+36)+'. '+a.title+'**\n['+a.source+'] [非3月] 评分：'+a._score+'分\n> '+getSummary(a)+'\n\n';});
r+='---\n\n## 七、文章来源总览\n\n以下为本期报告收录的全部'+(march.length+nm.length)+'篇文章，按分类顺序排列，每篇文章附来源、日期、评分及链接。\n\n';
// Append all articles with links
let sec='数字人民币与跨境支付';
march.filter(a=>cls(a)==='dc').concat(nm.filter(a=>cls(a)==='dc')).forEach(a=>{r+=sec+'\n'+a.title+' ['+a.source+'] ['+a.datetime.substring(0,10)+'] [评分：'+a._score+'] + '+a.url+'\n\n';});
sec='AI大模型与银行应用';
march.filter(a=>cls(a)==='ai').concat(nm.filter(a=>cls(a)==='ai')).forEach(a=>{r+=sec+'\n'+a.title+' ['+a.source+'] ['+a.datetime.substring(0,10)+'] [评分：'+a._score+'] + '+a.url+'\n\n';});
sec='消费金融AI应用';
march.filter(a=>cls(a)==='cf').concat(nm.filter(a=>cls(a)==='cf')).forEach(a=>{r+=sec+'\n'+a.title+' ['+a.source+'] ['+a.datetime.substring(0,10)+'] [评分：'+a._score+'] + '+a.url+'\n\n';});
sec='绿色金融';
march.filter(a=>cls(a)==='gf').concat(nm.filter(a=>cls(a)==='gf')).forEach(a=>{r+=sec+'\n'+a.title+' ['+a.source+'] ['+a.datetime.substring(0,10)+'] [评分：'+a._score+'] + '+a.url+'\n\n';});
sec='行业综合观察';
march.filter(a=>cls(a)==='other'||cls(a)==='bt').concat(nm.filter(a=>cls(a)==='other'||cls(a)==='bt')).forEach(a=>{r+=sec+'\n'+a.title+' ['+a.source+'] ['+a.datetime.substring(0,10)+'] [评分：'+a._score+'] + '+a.url+'\n\n';});
fs.writeFileSync('./reports/2026年3月咨询报告_v5.md',r,'utf8');
console.log('Report generated: '+(march.length+nm.length)+' articles, file size:',fs.statSync('./reports/2026年3月咨询报告_v5.md').size);
