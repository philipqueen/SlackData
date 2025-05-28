## Backend

### Installation

1. Create and activate a new python environment:
- uv: 
    1. `uv venv`
    2. `source venv/bin/activate`

- python
    1. `python3 -m venv venv`
    2. `source venv/bin/activate`

2. Install dependencies
- uv:
    1. `uv sync`
- python:
    1. `pip install '-e.[dev]'`

### Running

1. Activate environment (if not already activated)
    - `source venv/bin/activate`
2. Navigate to backend folder
    - `cd slack_data`
3. Run server
    - `fastapi dev main.py`
4. Open browser and go to URL printed in terminal