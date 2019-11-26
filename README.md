# Activity Logger Microservice Validator

## Overview

This repository contains a simple set of [pytest](https://docs.pytest.org/en/latest/) tests designed to validate a running instance of the activity logger microservice for the CS 465 project.

## What it checks for

The best way to learn what these tests are looking for is to read the tests. A brief summary is as follows:

* The service returns a list of at least one entry at `/api/activities` (note there is **no** trailing slash)
    * The top-level item is a dictionary with a single `activities` entry
    * This dictionary contains an array of individual items
* A single item returned from the list will have the following elements:
    * `id`: a string that uniquely identifies the item
    * `user_id`: an integer that uniquely identifies the user generating the activity
    * `username`: a string that identifies the username of the user generating the activity
    * `details`: a string with the details of the activity
    * `timestamp`: a standardized string representation (UTC) of when the event happened
    * `location`: a resource identifier that points back to this item, e.g., /api/activities/67ab45f
* A new entry can be posted to the logger then subsequently retrieved to learn its `id` and `location`


## How to run it

By default it will run against http://localhost:5001. See `runtests.sh` for an example of how to use an environment variable to point it elsewhere.