# Get start time with high precision
$start_time = Get-Date

Clear-Host
cd venv\Scripts
.\activate
cd ..\..

# Set PYTHONPATH and run the test script
$env:PYTHONPATH = "./app"
python test-bloat.py

deactivate

# Calculate and display duration
$end_time = Get-Date
$duration = $end_time - $start_time
Write-Output ""
Write-Output "---------------------------------------"
Write-Output ("Script execution time: {0:N6} seconds" -f $duration.TotalSeconds)
