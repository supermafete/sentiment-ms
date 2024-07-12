# main.py

from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from datetime import datetime
from controllers.fakeredditapi import FakeRedditAPI
from textblob import TextBlob
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
fake_reddit_api = FakeRedditAPI()


@app.get("/subfeddit/{subfeddit_name}/comments")
def get_recent_comments(
        subfeddit_name: str,
        start_date: Optional[str] = Query(None),
        end_date: Optional[str] = Query(None),
        sort: Optional[str] = Query(None),
        page: Optional[int] = 0,
        limit: Optional[int] = Query(25)
    ):
   
    subfeddits_response = fake_reddit_api.get_subfeddits(limit=25)
    df = pd.DataFrame(subfeddits_response['subfeddits'])
    subfeddit = df[df['title'] == subfeddit_name]
    
    comments_response = fake_reddit_api.get_comments(
        subfeddit_id=subfeddit['id'],
        limit=limit,
        page=page
    )

    comments = comments_response.get("comments", [])

    # Check if the user has specified date filters as first step
    # Raise an error if we don't have both dates
    if (start_date is None) + (end_date is None) == 1:
        raise HTTPException(status_code=400, detail="Bad request: Both start_date and end_date must be specified") 
    
    # Have dates, we must filter the results
    elif (start_date):
        # Convert date strings to datetime objects
        start_date_ts = datetime.strptime(start_date, "%Y-%m-%d").timestamp() if start_date else None
        end_date_ts = datetime.strptime(end_date, "%Y-%m-%d").timestamp() + 86400 if end_date else None  # add 24h (86400s) so end_date is the end of the date

        # # Filter by dates
        df = pd.DataFrame(comments)           
        comments_df = df[(df['created_at'] >= start_date_ts) & (df['created_at'] <= end_date_ts)]
        comments = comments_df.to_dict('records')

    # Once date filter are processed, add polarity
    comments_with_polarity = []
    for comment in comments:
        text = comment["text"]
        polarity = TextBlob(text).sentiment.polarity
        comments_with_polarity.append({
            "comment_id": comment["id"],
            "text": text,
            "polarity_score": polarity,
            "created_at": datetime.fromtimestamp(comment["created_at"]).strftime('%Y-%m-%d %H:%M:%S'),
            "classification": "Positive" if polarity >= 0.0 else "Negative"
        })

    # Then apply sorting on date-filtered results. Note that sorting happens AFTER date filter
    # So sorted results already are between date ranges and not the other way around.
    if ((sort == "asc" or sort == "desc") and len(comments_with_polarity) > 0):
        df = pd.DataFrame(comments_with_polarity)
        ascending = True if sort == "asc" else (False if sort == "desc" else None)
        comments_with_polarity = df.sort_values(by="polarity_score", ascending=ascending).to_dict('records')

    return comments_with_polarity


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("BIND_HOST"), port=8081)