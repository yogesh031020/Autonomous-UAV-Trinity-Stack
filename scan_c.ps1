
Get-ChildItem -Path C:\ -Directory | ForEach-Object {
    try {
        $size = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        [PSCustomObject]@{
            Name = $_.Name
            SizeGB = [Math]::Round($size, 2)
        }
    } catch {}
} | Sort-Object SizeGB -Descending | Select-Object -First 10
