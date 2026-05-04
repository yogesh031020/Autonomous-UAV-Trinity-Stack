
Get-ChildItem -Path C:\ -Recurse -File -ErrorAction SilentlyContinue | 
    Where-Object { $_.Length -gt 500MB } | 
    Sort-Object Length -Descending | 
    Select-Object FullName, @{Name='SizeGB'; Expression={[Math]::Round($_.Length / 1GB, 2)}} |
    Format-Table -AutoSize
