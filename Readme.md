# Github Navigator

A simple repository search and detail display.

## Installation

This application requires `python` 2 or 3 and `pip`.
`pip` is used to install the additional required python libraries, namely `flask`, `flask-restful`, `python-dateutil` and `requests`.
To set it up in a virtual environment also `virtualenv` is required.

### Setting up requirements

Run these commands in a terminal from the extracted archives root directory:

```shell
    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt
```

To set up the application without a virtual environment only the last line is needed.

## Running the application

Once the requirements are installed, the application can be run using:

```shell
    $ ./application.py
```

or

```shell
    $ python -m application
```

## Using the application

When the application is running in a terminal, it can be accessed through browser at `localhost:9876`.
This will bring up a search form, where you can type in a search term, and click `Submit Query` to get to the search results.
To instantly get to the search results for a search term `<term>` navigate your browser to `localhost:9876/navigator?search_term=<term>` and the results will be fetched and served by the application.

## Optional Setup (relax github rate limiting)

Github limits the request rate of IPs to 60 API requests per hour.
One search query requires 6 requests (1 search + 5 commit details).
To get a better experience, you can create an OAUTH-Token in your github profile settings, which will allow the app to authenticate as your github profile and this will raise the rate limit to 5000 requests per hour.
In your profile settings choose "Developer settings" -> "OAuth applications" in the menu on the left.
Then click "Register a new application" and fill in some details (the "Authorization callback URL" will not be used).
Once the token is created, create a file named `oauth.json` in the folder from where you run the application and fill it as follows:
```
{
 "client_id": "<client-id>",
 "client_secret": "<client-secret>"
}
```
Of course you have to replace `<client-id>` and `<client-secret>` with the values of your newly created application token from github.

If you then restart the application, you should see a message in it's output like this:
```
--------------------------------------------------------------------------------
INFO in application [application.py:128]:
Successfully loaded OAUTH credentials from 'oauth.json'.
--------------------------------------------------------------------------------
```

If loading the file was not successful you will see something like this:

```
--------------------------------------------------------------------------------
INFO in application [application.py:130]:
Failed to load OAUTH credentials from 'oauth.json'.
Exception was: [Errno 2] No such file or directory: 'oauth.json'
--------------------------------------------------------------------------------
```

### How this works

The client-id and client-secret loaded from the file `oauth.json` will be added to all API-requests as GET-Parameters.
To check if it is functioning correctly you can run
```shell
    $ curl -i 'https://api.github.com/users/whatever?client_id=xxxx&client_secret=yyyy'
```

after a few search requests, and see if some of your contingent is used.
More information on this can be found here: https://developer.github.com/v3/#rate-limiting
