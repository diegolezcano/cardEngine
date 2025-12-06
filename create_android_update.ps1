# PowerShell script to create android_updateFiles.zip
# Contains files from: deck, config, expansions, pics, script

# Load required .NET assemblies for zip file operations
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$directories = @('deck', 'config', 'expansions', 'pics', 'script')
$zipFileName = 'android_updateFiles.zip'
$projectRoot = $PSScriptRoot

# Remove existing zip file if it exists
if (Test-Path $zipFileName) {
    Write-Host "Removing existing $zipFileName..." -ForegroundColor Yellow
    Remove-Item $zipFileName -Force
}

Write-Host "Creating $zipFileName..." -ForegroundColor Green

# Create zip file
$zipPath = Join-Path $projectRoot $zipFileName
$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)

$filesAdded = 0

try {
    foreach ($directory in $directories) {
        $dirPath = Join-Path $projectRoot $directory
        
        if (-not (Test-Path $dirPath)) {
            Write-Host "Warning: Directory '$directory' does not exist. Skipping..." -ForegroundColor Yellow
            continue
        }
        
        Write-Host "Adding files from '$directory'..." -ForegroundColor Cyan
        
        # Get all files recursively
        $files = Get-ChildItem -Path $dirPath -Recurse -File
        
        foreach ($file in $files) {
            # Calculate relative path from project root
            $relativePath = $file.FullName.Substring($projectRoot.Length + 1)
            
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
$sizeMessage = "  File size: $zipSizeRounded MB"
Write-Host $sizeMessage -ForegroundColor Green

