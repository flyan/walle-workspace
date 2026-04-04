$slides = Get-ChildItem "C:\Users\flyan\.openclaw\workspace\agents-workspaces\secretary\pptx_extract_temp\ppt\slides\*.xml"
foreach ($slide in $slides) {
    $content = Get-Content $slide.FullName -Raw
    $text = [regex]::Replace($content, '<[^>]+>', ' ')
    $text = [regex]::Replace($text, '\s+', ' ')
    Write-Output "=== $($slide.Name) ==="
    Write-Output $text
    Write-Output ""
}
