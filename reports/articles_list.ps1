$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$data = Get-Content 'C:\Users\flyan\.openclaw\workspace\reports\v4_articles_extracted.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$out = @()
$out += "Total: $($data.Count)"
foreach ($a in $data) {
    $out += "$($a.num)|$($a.score)|$($a.march)|$($a.date)|$($a.source)|$($a.title)"
}
$out | Set-Content 'C:\Users\flyan\.openclaw\workspace\reports\articles_list.txt' -Encoding UTF8
Write-Host "Done. Written $($data.Count) articles."
