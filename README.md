- [How to run](#how-to-run)
  - [Local](#local)
  - [Microservices](#microservices)
  - [URL parameters](#url-parameters)
- [Considerations](#considerations)
- [Improvements](#improvements)
- [TODO](#todo)


# How to run

## Local

Your microservices (PostgreSQL and Feddit API) **are already running apart**.

```
  $ pip install -r requirements.txt
  $ python app/main.py
```

## Microservices

SentimentMS is attached to your docker containers

```
  $ docker-compose build
  $ docker-compose up
```

## URL parameters

* limit
  * Indicates the number of records to return
  * Possible values: Integer
* sort
  * Sorts results by polarity_score
  * Possible values: asc/desc
* start_date
  * Filters the results by start date
  * Possible values: YYYY-MM-DD
  * Requires end_date to be informed
* end_date
  * Filters the results by end date
  * Possible values: YYYY-MM-DD
  * Requires start_date to be informed
* page
  * Returns pages of results depending on limit
  * Possible values: Integer


# Considerations

- As the Feddit API does not work with dates, I had to filter dates directly on the results. That means that we have 
  to extend the limit to reach a sensitive quantity of records, as it ever starts with the most recent records, making the system inefficient in order to query date ranges. A more efficient approach would be to direct query the Database, but I assumed that you want me to use the Feddit API and don't mess with the database. I have created a controller for the database, but in the end I'm not using it.
- The aprroach is a little bit confusing regarding dates, because limit is relative to the last created_at and it's relying on the Feddit API, which is inconsistent with the start_date and end_date parameters of our API, so I created the page parameter to allow the user browse through results using limits. Despite this, as limit is acting before the date filter, it could happen that we specify a date range outside our limit. For instance:
```
  ?limit=25&start_date=2020-07-8&end_date=2020-07-8
  
  The first 25 records will not match that criteria. We could fix that extending the Feddit API to filter dates through the database. It could be more efficient and accurate.
```
  
- Note that if we use sort and date filters at the same time, sorting is applied on date-filtered results and not the other way around. It means that first we get the comments between the dates and then we sort the results. Maybe we could sort the results first and then filter by date, but that's is a less efficient approach because we have to fetch all records firts (as the API doesn't support date filtering). As the desired behaviour is not specified, I've choosen to filter the dates before sorting. Another time, it could be fixed accessing directly to the database.
- I've used TextBlob.sentiment to simulate results from an actual ML model
- All tests asserts True (original commented) due we have to run the FedditAPI in a preproduction environment to run them


# Improvements

**How I would improve this?** 
  As the challenge asks for handling date filtering, sorting and pagination, I would extend the Feddit API to add these parameters to the endpoints. I would implement the necessary queries to the database in order to fit with the requirements, but I thought that it's not the goal of this challenge, as indicated in the documentation. In any case, it would be easy to implement.

# TODO

* envs