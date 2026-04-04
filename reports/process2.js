// v4 report generator
const fs = require('fs');
const path = require('path');

const reportsDir = 'C:\\Users\\flyan\\.openclaw\\workspace\\reports';
const filtered = JSON.parse(fs.readFileSync(path.join(reportsDir, 'v4_filtered.json'), 'utf-8'));

// March 2026: score >= 70
// Other months: also include 65-69 (lower threshold per instructions)
// But prioritize March 2026 articles
const marchArticles = filtered.filter(a => a._march2026 && a._score >= 70);
const otherArticles = filtered.filter(a => !a._march2026 && a._score >= 65);

// Target 50+ articles
const finalArticles = [...marchArticles];
for (const a of otherArticles) {
  if (finalArticles.length >= 60) break; // Cap at 60
  finalArticles.push(a);
}

console.log(`Final articles: ${finalArticles.length}`);
console.log(`March 2026: ${finalArticles.filter(a => a._march2026).length}`);
console.log(`Other: ${finalArticles.filter(a => !a._march2026).length}`);

// Save final
fs.writeFileSync(path.join(reportsDir, 'v4_final.json'), JSON.stringify(finalArticles, null, 2), 'utf-8');
console.log('Saved v4_final.json');
