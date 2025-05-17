from nikolasigmoid/py-mcp-proxy:latest

copy src src 
copy pyproject.toml pyproject.toml

run python -m pip install . && rm -rf pyproject.toml && rm -rf ~/.cache/pip

copy config.json config.json
copy system_prompt.txt system_prompt.txt