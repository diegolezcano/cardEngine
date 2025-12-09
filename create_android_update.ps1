# PowerShell script to create android_updateFiles.zip
# Contains files from: deck, config, expansions, pics, script

# Load required .NET assemblies for zip file operations
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$directories = @('deck', 'config', 'expansions', 'pics', 'script', 'AndroidBuild\StaticFiles')
$zipFileName = 'android_updateFiles.zip'
$projectRoot = $PSScriptRoot

# Remove existing zip file if it exists
$zipPath = Join-Path $projectRoot "AndroidBuild\$zipFileName"
if (Test-Path $zipPath) {
    Write-Host "Removing existing $zipFileName..." -ForegroundColor Yellow
    Remove-Item $zipPath -Force
}

Write-Host "Creating $zipFileName..." -ForegroundColor Green

# Create zip file
$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)

$filesAdded = 0
$dirsAdded = 0

try {
    foreach ($directory in $directories) {
        $dirPath = Join-Path $projectRoot $directory
        
        if (-not (Test-Path $dirPath)) {
            Write-Host "Warning: Directory '$directory' does not exist. Skipping..." -ForegroundColor Yellow
            continue
        }
        
        Write-Host "Adding files from '$directory'..." -ForegroundColor Cyan
        
        # Check if this is the StaticFiles directory (should be placed at root of zip)
        $isStaticFiles = $directory -eq 'AndroidBuild\StaticFiles'
        
        # Get all subdirectories recursively
        $allDirs = Get-ChildItem -Path $dirPath -Recurse -Directory
        
        # Get all files recursively
        $files = Get-ChildItem -Path $dirPath -Recurse -File
        
        # Add all subdirectories (including empty ones)
        foreach ($dir in $allDirs) {
            if ($isStaticFiles) {
                # For StaticFiles, calculate path relative to StaticFiles directory
                $relativePath = $dir.FullName.Substring($dirPath.Length + 1)
            }
            else {
                # Calculate relative path from project root
                $relativePath = $dir.FullName.Substring($projectRoot.Length + 1)
            }
            
            # Normalize path separators for zip (use forward slashes)
            $relativePath = $relativePath -replace '\\', '/'
            
            # Add trailing slash to indicate directory
            $relativePath = $relativePath + '/'
            
            # Create directory entry in zip
            $zip.CreateEntry($relativePath) | Out-Null
            $dirsAdded++
        }
        
        foreach ($file in $files) {
            if ($isStaticFiles) {
                # For StaticFiles, calculate path relative to StaticFiles directory
                $relativePath = $file.FullName.Substring($dirPath.Length + 1)
            }
            else {
                # Calculate relative path from project root
                $relativePath = $file.FullName.Substring($projectRoot.Length + 1)
            }
            
            # Normalize path separators for zip (use forward slashes)
            $relativePath = $relativePath -replace '\\', '/'
            
            # Add file to zip
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $file.FullName, $relativePath) | Out-Null
            $filesAdded++
            
            if ($filesAdded % 100 -eq 0) {
                Write-Host "  Added $filesAdded files..." -ForegroundColor Gray
            }
        }
    }
}
finally {
    $zip.Dispose()
}

$zipSize = (Get-Item $zipPath).Length / 1MB
$zipSizeRounded = [math]::Round($zipSize, 2)

Write-Host ""
Write-Host "Successfully created $zipFileName" -ForegroundColor Green
Write-Host "  Total files added: $filesAdded" -ForegroundColor Green
Write-Host "  Total directories added: $dirsAdded" -ForegroundColor Green
$sizeMessage = "  File size: $zipSizeRounded MB"
Write-Host $sizeMessage -ForegroundColor Green

