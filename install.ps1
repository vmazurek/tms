pip install -e .
[System.Environment]::SetEnvironmentVariable("FLASK_APP", "tasks_server", "User")
[System.Environment]::SetEnvironmentVariable("FLASK_ENV", "development", "User")
flask init-db
