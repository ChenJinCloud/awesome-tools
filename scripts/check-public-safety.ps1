param(
  [string]$Root = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"

$script = Join-Path $PSScriptRoot "check_public_safety.py"
python $script --root $Root
