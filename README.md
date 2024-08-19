# Simple Flask app for matching content

This is a simple flask app for matching content to users. 

# Data

For sample data see `./data`

# Setup

Set the Flask app environment variable
```bash
export FLASK_APP=run.py
```

Set db key and url environment variables
```bash
export SECRET_KEY='my-secret-key'
export DATABASE_URL='sqlite:////tmp/test.db'
```

Install necessary python packages
```bash
pip install -r requirements.txt
```

Run the app
```bash
flask run
```

or

```bash
python run.py
```


# Tests

First, install the necessary packages
```bash
pip install pytest flake8 black isort
```

Then run lint tests

```bash
make check
```

To run unittests

```bash
make test
```

# Considerations
