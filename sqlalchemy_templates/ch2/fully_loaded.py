from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Integer, Column, Table, MetaData, String, Numeric, delete, insert, cast, and_, or_, not_, update
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import CheckConstraint, ForeignKey, ForeignKeyConstraint, Index, UniqueConstraint

from sqlalchemy.sql import select

from sqlalchemy.sql.sqltypes import Boolean, DateTime
from datetime import datetime
metadata = MetaData()

events = Table("events", metadata,
    Column("event_id", Integer(), primary_key=True),
    Column("event_title", String(80)),
    Column("event_pic_url", String(255)),
    Column("date", DateTime()),
    Column("sold", Integer()),
    Column("price", Numeric(12, 2)),
    CheckConstraint("price>=0.00", name="price_positive_constraint"),
    Index("ix_event_title", "event_title")
)

users = Table('users', metadata,
    Column("user_id", Integer(), primary_key=True),
    Column("username", String(15), nullable=False),
    Column('customer_number', Integer(), autoincrement=True),
    Column("email_address", String(255), nullable=False),
    Column("phone", String(20), nullable=False),
    Column("password", String(25), nullable=False),
    Column("created_on", DateTime(), default=datetime.now),
    Column("updated_on", DateTime(), default=datetime.now, onupdate=datetime.now),
    UniqueConstraint("username", name="uix_username'")
)


orders = Table('orders', metadata,
    Column("order_id", Integer(), primary_key=True),
    Column("user_id", ForeignKey("users.user_id")),
    
)

tickets = Table("tickets", metadata,
    Column("ticket_id", Integer(), primary_key=True),
    Column("order_id", Integer()),
    Column('event_id', ForeignKey('events.event_id')),
    Column('ticket_title', String(50), nullable=False, default="standard"),
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
        'event_title': 'Flores',
        'event_pic_url': 'http://some.aweso.me/cookie/peanut.html',
        'date': datetime.now(),
        'sold': 2000,
        'price': 1028
    },
    {
        'event_title': 'Vintage Culture',
        'event_pic_url': 'http://some.aweso.me/cookie/peanut.html',
        'date': datetime.now(),
        'sold': 4000,
        'price': 1428
    },
]

order_list = [
    {
        
        "user_id": 1
    },
    
]

ticket_list = [
    {
        "order_id": 1,
        'event_id': 1,
        "used": False
    },
    {
        "order_id": 1,
        'event_id': 2,
        "used": True
    }

]

ins = events.insert()
connection = engine.connect()
result = connection.execute(ins, event_list)

ins = users.insert()
result = connection.execute(ins, user_list)


ins = orders.insert()
result = connection.execute(ins, order_list)

ins = tickets.insert()
result = connection.execute(ins, ticket_list)

columns = [orders.c.order_id, users.c.username, events.c.event_title, events.c.price, tickets.c.ticket_title]
johnnie_orders = select(columns)
johnnie_orders = johnnie_orders.select_from(orders.join(users).join(tickets).join(events)).where(users.c.username == "Johnnie")

result = connection.execute(johnnie_orders).fetchall()
for row in result:
    print(row)

columns = [users.c.username, func.count(tickets.c.ticket_id).label("ticket_count")]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders).outerjoin(tickets))
all_orders = all_orders.group_by(users.c.username)
result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)

event = events.alias("event")
stmt = select([tickets.c.ticket_id, event.c.event_title], and_(tickets.c.event_id == event.c.event_id, event.c.event_title == "Vintage Culture"))
print(str(stmt))
for item in connection.execute(stmt):
    print(item)

def get_orders_by_customer(cust_name):
    columns = [orders.c.order_id, users.c.username, events.c.event_title, tickets.c.ticket_title, tickets.c.used, events.c.price]
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(users.join(orders).join(tickets).join(events))
    cust_orders = cust_orders.where(users.c.username == cust_name)
    result = connection.execute(cust_orders).fetchall()
    return result

def get_orders_by_customer_not_shipped(cust_name):
    columns = [orders.c.order_id, users.c.username, events.c.event_title, tickets.c.ticket_title, tickets.c.used, events.c.price]
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(users.join(orders).join(tickets).join(events))
    cust_orders = cust_orders.where(and_(users.c.username == cust_name, tickets.c.used == False))
    result = connection.execute(cust_orders).fetchall()
    return result
print(get_orders_by_customer_not_shipped("Johnnie"))
print(connection.execute("select users.username, events.event_title, tickets.ticket_id, tickets.used from tickets  join orders on tickets.order_id = orders.order_id join events on tickets.event_id = events.event_id join users on orders.user_id = users.user_id where events.event_title = 'Flores'").fetchall())
connection.close()