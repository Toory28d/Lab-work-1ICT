param([int]$Count = 30)
$hosts = @{}
1..$Count | ForEach-Object {
  $result = Invoke-RestMethod -Uri 'http://localhost:8080/'
  $hostName = $result.hostname
  if (-not $hosts.ContainsKey($hostName)) { $hosts[$hostName] = 0 }
  $hosts[$hostName]++
  Write-Output "Request $_ : $hostName"
}
Write-Output 'Distribution:'
$hosts.GetEnumerator() | Sort-Object Name | Format-Table
