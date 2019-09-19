# PythonAnalyseService
Flask service for separating users by theirs interensts in AnoChatty project

## Installing
- create python `venv`
### Using pip-tools
- install pip-tools https://github.com/jazzband/pip-tools
- `pip-sync requirements.txt`
### Without pip-tools
- `pip install -r requirements.txt`

## Installing DB
- to create db schema: `python migrate.py` 

## Populating model with test rows (Optional)
- `python dataset_builder.py`

## Running
- `python run.py`
