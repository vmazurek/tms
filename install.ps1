pip install -e .
$env:FLASK_APP="tasks_server"
$env:FLASK_ENV="development"
flask init-db