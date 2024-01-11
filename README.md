# Senior Living Community Rating Evaluator

## Overview

This project evaluates senior living communities using a rating system based on specific criteria. Each criterion is assigned a weight based on a perceived importance for a senior living community. Here's the breakdown of the criteria along with their respective weights:

* Location: 20%
* Cost: 15%
* Amenities: 25%
* Staffing: 15%
* Safety and Security: 10%
* Reviews and Ratings: 10%

## How does the project work?

First, you need to start the Celery workers to calculate the scores for a given list of senior living communities.

Two scripts have been created for:
* One script evaluates a list of communities that will be randomly generated based on a number you provide.
* The other script loads the results obtained from the Celery tasks.

Once you start the Celery workers, you can proceed to run the evaluate_communities script as follows: `poetry run python scripts/evaluate_communities.py`

The scores will be evaluated asynchronously, allowing you to run multiple tasks concurrently.

To retrieve the results, execute the load_communities_result script as follows: `poetry run python scripts/load_communities_result.py`

You'll need to provide an ID obtained from running the evaluate_communities script to fetch the results.

## Prerequisites

- Python 3.10.3
- Poetry 1.6.1
- Ensure local Redis is running

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/senior-living-rating-loader.git
   ```
2. Run `make start-worker`
3. Run the scripts.