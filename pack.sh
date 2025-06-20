find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
rm -rf hn.zip
zip -r hn.zip Dockerfile pyproject.toml system_prompt.txt src config.json