from flask_jsontools import JsonSerializableBase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, String, BigInteger

engine = create_engine('mysql://root:root@127.0.0.1:3306/users?charset=utf8', pool_recycle=3600)
#using scoped_session for thread safety
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


# declarative_base maps the tables to classes. JsonSerializableBase adds __json__ method to the instance
# so we can serialize SqlAlchemy models to JSON (the use is in DynamicJSONEncoder) when we respond
Base = declarative_base(cls=JsonSerializableBase)
# adds the ability to query with class.query
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    #validate email
    email = Column(String(50), unique=True)
    password = Column(String(15))

    def __repr__(self):
        return '<%s %s>' % (self.first_name, self.last_name)

# Run when initializing the db for the first time
def init_db():
    Base.metadata.create_all(bind=engine)
