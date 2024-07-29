from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

dbUser = os.getenv("DB_USER")
dbPass = os.getenv("DB_PASS")
dbHost = "dbportfolio.cvoieyqw6d46.us-east-2.rds.amazonaws.com"
dbPort = "3306"
dbName = "db_portfolio"

engine = create_engine(f"mysql+pymysql://{dbUser}:{dbPass}@{dbHost}:{dbPort}/{dbName}?charset=utf8mb4",pool_size=10, max_overflow=20)

try:
    connection = engine.connect()
    print("Connected to the database!")
    connection.close()
except Exception as e:
    print(f"U got an error: {e}")



try:
    def load_db_contacts():
        with engine.connect() as conx:
            result = conx.execute(text("select * from contacts2"))
            contacts = []
            for row in result.all():
                contacts.append(dict(row._mapping))
            return contacts    
    # with engine.connect() as conx:
    #     result = conx.execute(text("select * from contacts2"))
        
    #     result_dicts = []
    #     for row in result.all():
    #             result_dicts.append(dict(row._mapping))
        
    #     print(result_dicts)
        # print("type(result):",type(result))
        
        # first_result = result.fetchone()
        # if first_result:
        #     print('type(first_result)',type(first_result))
        #     first_resultDict = dict(first_result._mapping)
        #     print("first_resultDict:",first_resultDict)
        # else:
        #     print("no records found")
        
except Exception as e:
    print(f"U got an Error: {e}")
    
Session = sessionmaker(bind=engine)

Base = declarative_base()
   