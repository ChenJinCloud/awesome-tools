param(
  [string]$Root = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"

$patterns = @(
  'C:\\Users\\Dell',
  'D:\\chenjin-life-os',
  'F:\\wechat_full_export',
  'wxid_[A-Za-z0-9_\-]+',
  'gho_[A-Za-z0-9_]+',
  'github_pat_[A-Za-z0-9_]+',
  'CHATLOG_DATA_KEY',
  'vc-helper-.*\.json',
  'private__\d+__',
  'groups__\d+__'
)

$excludeDirs = @('.git')
$files = Get-ChildItem -LiteralPath $Root -Recurse -File -Force |
  Where-Object {
    $full = $_.FullName
    $isExcludedDir = [bool]($excludeDirs | Where-Object { $full -like "*\$_\*" })
    $isThisScript = $full -ieq $PSCommandPath
    -not $isExcludedDir -and -not $isThisScript
  }

$hits = foreach ($file in $files) {
  $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
  foreach ($pattern in $patterns) {
    if ($text -match $pattern) {
      [PSCustomObject]@{
        File = $file.FullName.Substring($Root.Length).TrimStart('\')
        Pattern = $pattern
      }
    }
  }
}

if ($hits) {
  $hits | Format-Table -AutoSize
  throw "Public safety scan failed."
}

Write-Output "Public safety scan passed."
