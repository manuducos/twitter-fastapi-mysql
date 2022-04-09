# Python
from datetime import datetime
from select import select
from typing import List

# Models
from tables.user import users
from tables.tweet import tweets
from models.tweet import TweetIn, TweetOut

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import status, HTTPException

# Database
from config.db import conn

tweet = APIRouter()

# Functions
def get_tweet_by_ID(id: int):
    tweet = conn.execute(tweets.select().where(tweets.c.id == id)).first()
    if tweet:
        return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tweet ID not found'
        )


def get_user_by_ID(id: int):
    user = conn.execute(users.select().where(users.c.id == id)).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User ID not found'
        )


def to_TweetOut(tweet):
    response_tweet = dict()
    response_user = get_user_by_ID(tweet.user_id)

    response_tweet['id'] = tweet.id
    response_tweet['content'] = tweet.content
    response_tweet['created_at'] = tweet.created_at
    response_tweet['updated_at'] = tweet.updated_at
    response_tweet['by'] = dict(response_user)

    return response_tweet

def check_existence_and_relation(user_id: int, tweet_id: int):
    user = get_user_by_ID(user_id)
    tweet = get_tweet_by_ID(tweet_id)

    if user.id != tweet.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The tweet does not belong to this user'
        )

# Path operations

## Post a tweet
@tweet.post(
    path='/users/{user_id}/post',
    response_model=TweetOut,
    status_code=status.HTTP_201_CREATED,
    summary='Post tweet',
    tags=['tweets']
)
def post_tweet(
    user_id: int = Path(...),
    tweet: TweetIn = Body(...)
):
    '''
    Post tweet

    This path operation posts a tweet on behalf of a user

    Parameters:
    - Path parameters:
        - user_id: int
    - Request body parameters:
        - tweet: Tweet

    Returns a json of the tweet with the following keys:
    - id: int
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: UserOut
    '''
    user = get_user_by_ID(user_id)

    new_tweet = dict(tweet)

    result = conn.execute(tweets.insert().values(
        content=new_tweet['content'],
        created_at=datetime.now(),
        updated_at=None,
        user_id=user.id
    ))

    db_tweet = get_tweet_by_ID(result.lastrowid)

    new_tweet['id'] = db_tweet.id
    new_tweet['by'] = dict(user)

    return new_tweet


## Show all tweets
@tweet.get(
    path='/tweets',
    response_model=List[TweetOut],
    status_code=status.HTTP_200_OK,
    summary='Show all tweets',
    tags=['tweets']
)
def show_all_tweets():
    '''
    Show all tweets

    This path operation shows all the tweets stored in the database

    Parameters:
    -

    Returns a json list of the tweets with the following keys:
    - id: int
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: UserOut
    '''
    all_tweets = conn.execute(tweets.select()).fetchall()

    response_list = [to_TweetOut(tweet) for tweet in all_tweets]

    return response_list
        
        
## Show all the tweets of a user
@tweet.get(
    path='/users/{user_id}/tweets',
    response_model=List[TweetOut],
    status_code=status.HTTP_200_OK,
    summary='Show all the tweets of a user',
    tags=['tweets']
)
def show_user_tweets(user_id: int = Path(...)):
    '''
    Show all the tweets of the user

    This path operation shows all the tweets stored of the user with the given ID. If it doesn't exist, it raises an httpexception

    Parameters:
    -

    Returns a json list of all the tweets of the user with the following keys:
    - id: int
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: UserOut
    '''
    get_user_by_ID(user_id)
    all_user_tweets = conn.execute(tweets.select().where(tweets.c.user_id == user_id)).fetchall()
    response_list = [to_TweetOut(tweet) for tweet in all_user_tweets]

    return response_list


## Show a tweet
@tweet.get(
    path='/tweets/{tweet_id}',
    response_model=TweetOut,
    status_code=status.HTTP_200_OK,
    summary='Show a tweet',
    tags=['tweets']
)
def show_a_tweet(tweet_id: int = Path(...)):
    '''
    Show a tweet

    This path operation shows the tweet with the given ID. If it doesn't exist, it raises an httpexception

    Parameters:
    - Path parameters:
        - tweet_id: int
    
    Returns a json of the tweet with the following keys:
    - id: int
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: UserOut
    '''
    return to_TweetOut(get_tweet_by_ID(tweet_id))


## Update a tweet
@tweet.put(
    path='/users/{user_id}/tweets/{tweet_id}/update',
    response_model=TweetOut,
    status_code=status.HTTP_202_ACCEPTED,
    summary='Update a tweet',
    tags=['tweets']
)
def update_tweet(
    user_id: int = Path(...),
    tweet_id: int = Path(...),
    updated_content: TweetIn = Body(...)
):
    '''
    Update a tweet

    This path operation updates an already existing tweet. If the tweet or user ID doesn't exist or the tweet doesn't belong to the user, an httpexception is raised according to the case

    Parameters:
    - Path parameters:
        - user_id: int
        - tweet_id: int
    - Request Body parameters:
        - updated_content: Tweet

    Returns a json of the updated tweet with the following keys:
    - id: int
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: UserOut
    '''
    check_existence_and_relation(user_id=user_id, tweet_id=tweet_id)

    updated_content = dict(updated_content)

    conn.execute(tweets.update().where(tweets.c.id == tweet_id).values(
        content=updated_content['content'],
        updated_at=datetime.now()
    ))
    
    return to_TweetOut(get_tweet_by_ID(tweet_id))


## Delete a tweet
@tweet.delete(
    path='/users/{user_id}/tweets/{tweet_id}',
    response_model=TweetOut,
    status_code=status.HTTP_200_OK,
    summary='Delete a tweet',
    tags=['tweets']
)
def delete_tweet(
    user_id: int = Path(...),
    tweet_id: int = Path(...)
):
    '''
    Delete tweet

    This path operation deletes an already existing tweet. If the tweet or user ID doesn't exist or the tweet doesn't belong to the user, an httpexception is raised according to the case

    Parameters:
    - Path parameters:
        - user_id: int
        - tweet_id: int

    Returns a json of the deleted tweet with the following keys:
    - id: int
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: UserOut
    '''
    check_existence_and_relation(user_id=user_id, tweet_id=tweet_id)

    deleted_tweet = to_TweetOut(get_tweet_by_ID(tweet_id))
    
    conn.execute(tweets.delete().where(tweets.c.id == tweet_id))
    
    return deleted_tweet