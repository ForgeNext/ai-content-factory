$ErrorActionPreference = "Stop"

# Project root: directory containing this script
$root = $PSScriptRoot

# Output files
$outputDirectory = Join-Path $root "audit_snapshot"
$treeOutput = Join-Path $outputDirectory "00_project_tree.txt"
$snapshotOutput = Join-Path $outputDirectory "01_project_snapshot.txt"

# Excluded directories
$excludedDirectoryNames = @(
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    "logs",
    "audit_snapshot"
)

# Excluded files
$excludedFileNames = @(
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    "secrets.json",
    "credentials.json"
)

# Included extensions
$includedExtensions = @(
    ".md",
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
    ".ini",
    ".cfg",
    ".ps1",
    ".bat",
    ".cmd",
    ".csv",
    ".html",
    ".css",
    ".js",
    ".ts"
)

# Included names regardless of extension
$includedFileNames = @(
    "Dockerfile",
    "Makefile",
    ".gitignore",
    ".dockerignore",
    "requirements.txt",
    "pyproject.toml"
)

New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

function Get-ProjectRelativePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FullPath
    )

    $normalizedRoot = $root.TrimEnd("\")
    return $FullPath.Substring($normalizedRoot.Length).TrimStart("\")
}

function Test-ExcludedPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FullPath
    )

    $relativePath = Get-ProjectRelativePath -FullPath $FullPath
    $pathParts = $relativePath -split '[\\/]'

    foreach ($part in $pathParts) {
        if ($excludedDirectoryNames -contains $part) {
            return $true
        }
    }

    return $false
}

# ------------------------------------------------------------
# 1. Create project tree
# ------------------------------------------------------------

$treeLines = New-Object System.Collections.Generic.List[string]

$treeLines.Add("ForgeNext Project Tree")
$treeLines.Add("Root: $root")
$treeLines.Add("Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
$treeLines.Add("")

$allItems = Get-ChildItem -Path $root -Recurse -Force |
    Where-Object {
        -not (Test-ExcludedPath -FullPath $_.FullName)
    } |
    Sort-Object FullName

foreach ($item in $allItems) {
    $relativePath = Get-ProjectRelativePath -FullPath $item.FullName

    if ($item.PSIsContainer) {
        $treeLines.Add("[DIR]  $relativePath")
    }
    else {
        $treeLines.Add("[FILE] $relativePath")
    }
}

$treeLines | Out-File -FilePath $treeOutput -Encoding utf8

# ------------------------------------------------------------
# 2. Create full project snapshot
# ------------------------------------------------------------

$snapshotHeader = @"
ForgeNext Project Snapshot

Root: $root
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

Excluded:
- Secret files
- Git internal data
- Virtual environments
- External libraries
- Cache files
- Build outputs
- Logs
- Snapshot output directory

================================================================================

"@

$snapshotHeader | Out-File -FilePath $snapshotOutput -Encoding utf8

$targetFiles = Get-ChildItem -Path $root -Recurse -File -Force |
    Where-Object {
        $extension = $_.Extension.ToLowerInvariant()

        -not (Test-ExcludedPath -FullPath $_.FullName) -and
        $_.Name -notin $excludedFileNames -and
        (
            $extension -in $includedExtensions -or
            $_.Name -in $includedFileNames
        )
    } |
    Sort-Object FullName

foreach ($file in $targetFiles) {
    $relativePath = Get-ProjectRelativePath -FullPath $file.FullName

    $fileHeader = @"

================================================================================
FILE: $relativePath
SIZE: $($file.Length) bytes
LAST MODIFIED: $($file.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))
================================================================================

"@

    $fileHeader | Out-File -FilePath $snapshotOutput -Encoding utf8 -Append

    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8

        if ([string]::IsNullOrWhiteSpace($content)) {
            "[EMPTY FILE]" |
                Out-File -FilePath $snapshotOutput -Encoding utf8 -Append
        }
        else {
            $content |
                Out-File -FilePath $snapshotOutput -Encoding utf8 -Append
        }
    }
    catch {
        "[READ ERROR: $($_.Exception.Message)]" |
            Out-File -FilePath $snapshotOutput -Encoding utf8 -Append
    }
}

# ------------------------------------------------------------
# 3. Show result
# ------------------------------------------------------------

Write-Host ""
Write-Host "========================================"
Write-Host "ForgeNext snapshot completed"
Write-Host "========================================"
Write-Host ""
Write-Host "Project tree:"
Write-Host $treeOutput
Write-Host ""
Write-Host "Full snapshot:"
Write-Host $snapshotOutput
Write-Host ""
Write-Host "Collected files: $($targetFiles.Count)"
Write-Host ""
