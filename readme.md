# Jira Organizer

This simple script helps to organize and manage tasks in Jira.

## Installation

### Prerequisites

This app was should work with `Python 3` interpreters. If you run into compatibility issues, try to use exact
version `Python 3.9`.

You can check your Python version using command:

```
$ python -v
```

### Creating virtualenv and installing dependencies

Use `virtualenv` to create isolated Python environment for this app.

1. Install `virtualenv` if you don't have it:

```
$ pip install virtualenv
```

2. Clone this repository and create a virtual environment:

```
$ git clone https://github.com/w13rny/jiraorganizer.git
$ cd jiraorganizer
$ virtualenv venv
```

3. Activate virtual environment and install the Python dependencies with `pip`:

```
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Configuration

Create `.env` file in main directory and fill it with following data:

```
# JIRA URL - e.g. 'https://company.atlassian.net/'
JIRA_URL=''

# JIRA_USERNAME - e.g. 'john.smith@company.com'
JIRA_USERNAME=''

# JIRA_API_TOKEN - get it from https://id.atlassian.com/manage-profile/security/api-tokens
JIRA_API_TOKEN=''
```

## Run script

Run script using command with arguments:

* `--project` - Jira project name,
* `--delta` - script processes only tasks with limit since the last update (pass value in hours, default=24).

Example:

```
$ python main.py --project ABC --delta 48
```

When you finish using the app on virtual environment, remember to deactivate it in console:

```
$ deactivate
```