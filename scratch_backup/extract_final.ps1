
$path = "C:\Users\Yogesh E S\.gemini\antigravity\brain\b68d9ff8-2df1-4abc-84da-81e0a2c992d6\.system_generated\logs\overview.txt"
$text = [System.IO.File]::ReadAllText($path)
$idx = $text.IndexOf('"step_index":47')
if ($idx -ge 0) {
    $rest = $text.Substring($idx)
    $endIdx = $rest.IndexOf('}')
    $jsonStr = $rest.Substring(0, $endIdx + 1)
    $json = $jsonStr | ConvertFrom-Json
    $json.content | Out-File -Encoding utf8 "C:\Users\Yogesh E S\.gemini\antigravity\scratch\step47_really_full.txt"
}
