# counttracker

CountTracker  keeps track of the counts of events that have happened over the past 5 minutes.
Precision is to the current second.
So for example, if an event happens at 5:50 and 12.34 seconds,
it will be considered to have happened at 5:50 and 12 seconds, truncating the milliseconds associated.

## Setup
Clone the repo:
`git clone https://github.com/jm2az/counttracker.git`

Install dependencies:
`pip install -r requirements.txt`

## Testing
Run tests:
`pytest`

For a more comprehensive report of code coverage:
`pytest --cov=counttracker --cov-report html`

* To view coverage, open `htmlcov/index.html` in a browser

## Documentation
To view documentation, open `_build/html/index.html` in a browser:
