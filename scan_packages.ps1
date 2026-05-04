
Get-ChildItem -Path C:\Users\Yogesh` E` S\AppData\Local\Packages -Recurse -File -ErrorAction SilentlyContinue | 
    Where-Object { $_.Length -gt 1GB } | 
    Select-Object FullName, @{Name='SizeGB'; Expression={[Math]::Round($_.Length / 1GB, 2)}}
