import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
database_url = os.environ.get('DATABASE_URL')
database_pool_size = int(os.environ.get('DATABASE_POOL_SIZE'))
database_pool_overflow = int(os.environ.get('DATABASE_POOL_OVERFLOW'))
database_pool_timeout = int(os.environ.get('DATABASE_POOL_TIMEOUT'))
engine = create_engine(database_url,
                       echo=True,
                       pool_size=database_pool_size,
                       max_overflow=database_pool_overflow,
                       pool_timeout=database_pool_timeout)
Session = sessionmaker(bind=engine)

