# CreditAPI

Endpoints for Blog Post api

## Requirement and Installation

### Via Cloning The Repository

``` txt
# Setup Env
Follow the format specified in the .env.template file and after rename .env

# Setup postgres
Create a PostgreSQL database called "CreditAPI"
```

1. `git clone https://github.com/Daquiver1/blogpost_api.git`
2. Install python dependencies
   - `pip install -r requirements.txt`
3. `alembic upgrade head`
4. `uvicorn src.api.main:app --reload`
5. The app is now running on <http://127.0.0.1:8000>
