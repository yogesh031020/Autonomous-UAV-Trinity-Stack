
$path = "C:\Users\Yogesh E S\.gemini\antigravity\brain\b68d9ff8-2df1-4abc-84da-81e0a2c992d6\.system_generated\logs\overview.txt"
$content = Get-Content -Raw $path
$matches = [regex]::Matches($content, 'Project [23]: .*?(\n|\\n)')
foreach ($m in $matches) {
    Write-Output $m.Value
}
