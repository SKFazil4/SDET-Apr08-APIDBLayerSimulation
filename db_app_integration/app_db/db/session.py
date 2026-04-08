from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mssql+pyodbc://ATMECSINLT-1507\\SQLEXPRESS/TestDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes")

SessionLocal = sessionmaker(bind=engine)