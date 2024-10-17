# Mongo Tweets API

## Local usage

### Install requirements
```bash
pip install -e .
```

### Start service
Go to `docker` directory and start a mongo server instance.
```bash
docker compose up
```
Now you can access the service using web-based MongoDB admin interface provided under `localhost:8081`.

### Upload data
Create or download `data/tweets.json` file with tweets data. You can see the data structure in the `data/example_tweet.json` file.

Go to `scripts` directory and run script for uploading tweets data to mongo database.
```bash
python upload_tweets_data.py
```

### Query data
Now you are ready to query the tweets data from mongo database. You can see example queries in the script.
```bash
python example_queries.py
```

### Stop service
Kill the containers and reset the volumes.
```bash
docker compose down -v
```