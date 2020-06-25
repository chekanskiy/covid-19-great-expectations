docker run -it -v ~/Documents/projects/:/projects --env-file .env schekan/great-expectations:latest /bin/bash -c "python /eval_scripts/eval_suite.py"
