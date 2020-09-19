echo "Starting Docker Container for CORE!"
nohup python api/main.py > logs_flask.txt &
# python ./launcher.py analysis &
# python ./launcher.py report &
python ./launcher.py collection # the last command should not be parallel
