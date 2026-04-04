$data = Get-Content 'C:\Users\flyan\.openclaw\workspace\reports\v4_articles_extracted.json' -Raw -Encoding UTF8 | ConvertFrom-Json
Write-Host "Total articles: $($data.Count)"
foreach ($a in $data) {
    $title = if ($a.title.Length -gt 35) { $a.title.Substring(0, 35) } else { $a.title }
    Write-Host "$($a.num.ToString().PadLeft(3)) | score=$($a.score) | march=$($a.march) | $($a.date) | [$($a.source)] | $title"
}
