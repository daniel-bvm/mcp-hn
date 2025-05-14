from nikolasigmoid/py-mcp-proxy:latest

copy src src 
copy pyproject.toml pyproject.toml

run --mount=type=cache,target=/root/.cache/pip python -m pip install . && rm -rf pyproject.toml

copy config.json config.json
copy system_prompt.txt system_prompt.txt