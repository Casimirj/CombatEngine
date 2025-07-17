

# Get start time in nanoseconds (for higher precision)
start_time=$(date +%s.%N)


clear
cd venv/bin
. activate
cd ../../


export PYTHONPATH="./app"
python3 test.py


end_time=$(date +%s.%N)
duration=$(awk "BEGIN {printf \"%.6f\", $end_time - $start_time}")
echo ""
echo "---------------------------------------"
echo "Script execution time: $duration seconds"