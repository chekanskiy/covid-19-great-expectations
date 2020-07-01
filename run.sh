COMMAND=$1 # "python /eval_scripts/eval_suite.py"
docker run -it -v ~/Documents/projects/:/projects --env-file .env -p 9999:8888 schekan/great-expectations:latest /bin/bash -c "$COMMAND"
