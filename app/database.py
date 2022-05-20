from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

#Import psycopg2 components to start Postgres session
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time


#SQLAlchemy does not do mirations (updation of rows and addition deletion)
#of columns so we would need to use alembic for that. 

#Format of connection string for postgresql databases is
#"postgresql://<username>:<password>@<ip-address/hostname>/<database name>"
SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependency. This will be used to create an instance
#of SessionLocal class inorder to interact with our
#database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This code is not required when using SQL Alchemy
# while True:
#     try:
#         """
#         Establish Postgres connection using Psycopg2. We
#         need to pass in RealDictCursor in order to get column
#         names with the data that we are retrieving
#         """
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='postgres',
#                                 cursor_factory=RealDictCursor)

#         cursor = conn.cursor()

#         print('Database connection was successful')
#         break

#     except Exception as e:
#         print("Connection to database failed!")
#         print("Error was: ", e)
#         time.sleep(3)