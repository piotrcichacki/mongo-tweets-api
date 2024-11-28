# Mongo Tweets API

## Services

### Start services

Go to `docker` directory and start services.
```bash
docker compose up
```

1. MongoDB is running and accessible at `localhost:27017`.
You can access the database using web-based MongoDB admin interface provided under `localhost:8081`.

2. Tweets API is running and accessible at `localhost:8000`. 
You can check how to communicate with the API in the documentation available at `localhost:8000/docs`.
Or you can see the raw OpenAPI schema with the descriptions of all API available at `localhost:8000/openapi.json`.

3. Redis is running at `localhost:6379` and is used to cache responses from the API.

### Stop service

Kill the containers and reset the volumes.
```bash
docker compose down -v
```


## Data

### Upload data
Create or download `data/tweets.json` file with tweets data.

Go to `scripts` directory and run script for uploading tweets data to mongo database.
```bash
python upload_tweets_data.py
```

### Query data
You can query the tweets data directly from mongo database. You can see example queries in the script.
```bash
python example_queries.py
```