from datetime import datetime, timezone
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, Boolean, create_engine,
                        CheckConstraint, Index, UniqueConstraint, ForeignKeyConstraint, select, CheckConstraint)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import insert

metadata = MetaData()

events = Table("events", metadata,
    Column("event_id", Integer(), primary_key=True),
    Column("event_title", String(80)),
    Column("event_pic_url", String(255)),
    Column("open_gates", DateTime()),
    Column("home", String(50)),
    
    Index("ix_event_title", "event_title")
)

ticket_boilerplates = Table("ticket_boilerplates", metadata,
    Column('ticket_boilerplate_id', Integer(), primary_key=True),
    Column('ticket_title', String(50), nullable=False, default="standard"),
    Column("event_id", ForeignKey('events.event_id'), nullable=False),
    Column("price", Numeric(12, 2)),
    Column("start_selling", DateTime()),
    Column("batch_size", Integer()),
    Column("out_date", DateTime(), nullable=True),
    Column("batch", String(12), nullable=False, default="lote 1"),
    CheckConstraint('batch_size >= 0', name='batch_size_positive'),
    CheckConstraint("price>=0.00", name="price_positive_constraint"),
    
)

users = Table('users', metadata,
    Column("user_id", Integer(), primary_key=True),
    Column("username", String(15), nullable=False),
    Column('customer_number', Integer(), autoincrement=True),
    Column("email_address", String(255), nullable=False, unique=True),
    Column("phone", String(20), nullable=False),
    Column("password", String(25), nullable=False),
    Column("created_on", DateTime(), default=datetime.now),
    Column("updated_on", DateTime(), default=datetime.now, onupdate=datetime.now),
    UniqueConstraint("username", name="uix_username'")
)


orders = Table('orders', metadata,
    Column("order_id", Integer(), primary_key=True),
    Column("user_id", ForeignKey("users.user_id")),
    #missing time, payments, cancelled, will be divided in orders and orders items
)

tickets = Table("tickets", metadata,
    Column("ticket_id", Integer(), primary_key=True),
    Column("order_id", Integer()),
    Column('ticket_boilerplate_id', ForeignKey('ticket_boilerplates.ticket_boilerplate_id')),
    Column("used", Boolean(), default=False),
    ForeignKeyConstraint(['order_id'], ['orders.order_id'])
)

engine = create_engine("sqlite:///:memory:")

metadata.create_all(engine)

user_list = [
    {
        "username": "Johnnie",
        'customer_number': "user-0001",
        "email_address": "johnnie.fujita@gmail.com",
        "phone": "5585988526803",
        "password": "fjisa84dfer",
        "created_on": datetime.now(),
        "updated_on": datetime.now(),
    },
    {
        "username": "Liz",
        'customer_number': "user-0002",
        "email_address": "lizandra.fujita@gmail.com",
        "phone": "5585988526806",
        "password": "lzia4090df",
        "created_on": datetime.now(),
        "updated_on": datetime.now(),
    }
]
event_list = [
    {
        "event_title": "Reveillon",
        "event_pic_url": "www.colosso.com.br",
        "open_gates": datetime(2021, 12, 31, 22, 30, tzinfo=timezone.utc),
        "home": "Colosso"
    }
]
ticket_boilerplates_list = [
    {
        
        'ticket_title': "pista",
        "event_id": 1,
        "price": 100,
        "start_selling": datetime.now(),
        "batch_size": 2000,
        "out_date": datetime(2021, 11, 30, 23,59 , tzinfo=timezone.utc),
        "batch": "lote 1"
    },
    {
        
        'ticket_title': "pista",
        "event_id": 1,
        "price": 180,
        "start_selling": datetime.now(),
        "batch_size": 5000,
        "out_date": datetime(2021, 12, 31, 12,0, tzinfo=timezone.utc),
        "batch": "lote 2"
    },
    {
        
        'ticket_title': "VIP",
        "event_id": 1,
        "price": 500,
        "start_selling": datetime.now(),
        "batch_size": 500,
        "out_date": datetime(2021, 11, 30, 12,0, tzinfo=timezone.utc),
        "batch": "lote 1"
    },
    {
        
        'ticket_title': "VIP",
        "event_id": 1,
        "price": 700,
        "start_selling": datetime.now(),
        "batch_size": 1000,
        "out_date": datetime(2021, 12, 31, 12,0, tzinfo=timezone.utc),
        "batch": "lote 2"
    }
]

## inserting users
ins = insert(users)
connection = engine.connect()
rp = connection.execute(ins,user_list)
### inserting events
ins = insert(events)
connection = engine.connect()
rp = connection.execute(ins, event_list)
##inserting tickets
ins = insert(ticket_boilerplates)
connection = engine.connect()
rp = connection.execute(ins, ticket_boilerplates_list)


s = select(users.c.username, users.c.user_id)
results = connection.execute(s)
for result in results:
    print(result.username, result.user_id)
  
s = select(events.c.event_title, ticket_boilerplates.c.ticket_title, ticket_boilerplates.c.batch, ticket_boilerplates.c.price, ticket_boilerplates.c.batch_size)
s = s.select_from(ticket_boilerplates.join(events))

results = connection.execute(s).fetchall()
for result in results:
    print(result.event_title, result.ticket_title, result.batch, result.price, result.batch_size)

s = select(users.c.username)
connection.execute(s).fetchall()

ins = insert(users).values(
    username = "Johnnie",
    customer_number = "user-0001",
    email_address = "johnnie.fujita@gmail.com",
    phone = "5585988526803",
    password ="fjisa84dfer",
    created_on = datetime.now(),
    updated_on = datetime.now(),
)

try:
    result = connection.execute(ins)
except IntegrityError as error:
    print(error.orig, error.detail)

#### Ticket and order insertions

order_list = [
    {
        
        "user_id": 1
    }
]


tickets = Table("tickets", metadata,
    Column("ticket_id", Integer(), primary_key=True),
    Column("order_id", Integer()),
    Column('ticket_boilerplate_id', ForeignKey('ticket_boilerplates.ticket_boilerplate_id')),
    Column("used", Boolean(), default=False),
    ForeignKeyConstraint(['order_id'], ['orders.order_id'])