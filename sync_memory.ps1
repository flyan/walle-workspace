$env:SUPERMEMORY_OPENCLAW_API_KEY='sm_6sTckwukqeCyo93TEaPHCE_odFwNxliCawXSCjMbHjwxwjJljUeRiltUBlAiuFfkAVllkVuRsQStBbNttoVmLNU'
$env:PYTHONIOENCODING='utf-8'
$script='C:\Users\flyan\.agents\skills\supermemory-free\store.py'

$files = @(
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-07.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-08.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-09.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-10.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-12.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-13.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-14.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-15.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\2026-03-16.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\reminders.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents\main\memory\team-management.md'; tag='main'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents-workspaces\writer\MEMORY.md'; tag='writer'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents-workspaces\writer\memory\2026-03-15.md'; tag='writer'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents-workspaces\writer\memory\HANDOFF-2026-03-25.md'; tag='writer'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents-workspaces\secretary\MEMORY.md'; tag='secretary'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents-workspaces\secretary\memory\2026-03-26.md'; tag='secretary'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents-workspaces\secretary\memory\SYSTEM_HANDOFF.md'; tag='secretary'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents-workspaces\coder\memory\HANDOFF-2026-03-25.md'; tag='coder'},
    @{path='C:\Users\flyan\.openclaw\workspace\agents-workspaces\stock\memory\2026-03-26.md'; tag='stock'}
)

foreach ($item in $files) {
    $p = $item.path
    $t = $item.tag
    if (Test-Path $p) {
        $content = Get-Content $p -Raw -Encoding UTF8
        $result = $content | python $script - --tag $t --json 2>&1
        $name = Split-Path $p -Leaf
        Write-Host "[$t] $name : $result"
        Start-Sleep -Milliseconds 300
    } else {
        Write-Host "SKIP: $p"
    }
}
Write-Host "Done!"
