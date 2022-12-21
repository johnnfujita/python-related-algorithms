from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/sqlalchemy_essentials")
connection = engine.connect()
print("connected")
connection.close()
print("disconnected")