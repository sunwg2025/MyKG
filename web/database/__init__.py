import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine(os.environ.get('DATABASE_URL'), echo=True)
Session = sessionmaker(bind=engine)
session = Session()