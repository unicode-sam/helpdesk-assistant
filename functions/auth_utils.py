import uuid
import random
import datetime 

def create_session():
    session_id=uuid.uuid4()
    create_ts=datetime.datetime.now()
    print(session_id)
    print(create_ts)
    return session_id,create_ts

#Create a function for storing session details in BQ


