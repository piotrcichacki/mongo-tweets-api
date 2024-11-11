from pydantic import BaseModel, Field


class Tweet(BaseModel):
    id: str = Field(description="Tweet identifier")
    lang: str = Field(description="Language code", max_length=3)
    text: str = Field(description="Tweet text", max_length=500)
    author_id: str = Field(description="Author identifier")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                  "id": "1",
                  "lang": "pl",
                  "text": "tweet text",
                  "author_id": "1"
                }
            ]
        }
    }


class TweetUpdate(BaseModel):
    text: str = Field(description="Tweet text", max_length=500)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "tweet updated text",
                }
            ]
        }
    }
