
$path = "C:\Users\Yogesh E S\.gemini\antigravity\brain\b68d9ff8-2df1-4abc-84da-81e0a2c992d6\.system_generated\logs\overview.txt"
$lines = Get-Content $path
$line47 = $lines[20]
$json = $line47 | ConvertFrom-Json
$json.content | Out-File -Encoding utf8 "C:\Users\Yogesh E S\.gemini\antigravity\scratch\step47_full.txt"
