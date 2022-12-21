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
    Column("quantity", Integer()),
    Column('ticket_title', String(50), nullable=False, default="standard"),
    Column("upgrade_value", Numeric(12, 2)),
     Column("used", Boolean(), default=False),

    ForeignKeyConstraint(['order_id'], ['orders.order_id'])
)

engine = create_engine("sqlite:///:memory:")

metadata.create_all(engine)


# Insert as a method of the table object
# insertion = events.insert().values(
   
#     event_title="Fortal",
#     event_pic_url="www.pic.com.braba",
#     date=datetime.now(),
#     sold=2000,
#     price=1000
# )

insertion = insert(events).values(
    event_title="Fortal",
    event_pic_url="www.pic.com.braba",
    date=datetime.now(),
    sold=2000,
    price=1000
)

## Multiple insertions
inventory_list = [
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
ins = events.insert()
connection = engine.connect()
result = connection.execute(ins, inventory_list)
print(insertion.compile().params)


print("connected")
result = connection.execute(insertion)
print(result.inserted_primary_key)



## query
s = select([events])
print(str(s))
query_result = connection.execute(s)
query_result_2 = connection.execute(s)
results = query_result.fetchall()
print(results)

first_row = results[0]
#access the first result
print("first row ", first_row)
# access the first collumn of the first result
print('first row[1]', first_row[1])
# access the first collumn by collumn name
print("first_row.event_title", first_row.event_title)
print("first_row[events.c.event_title]", first_row[events.c.event_title])

# using the result proxy as an iterable
for event in query_result_2:
    print(event.event_title)

# select specific columns
s2 = select([events.c.event_title, events.c.price])

# ordering
s2 = s2.order_by(desc(events.c.price))
# limiting the query results

s2 = s2.limit(2)
rp = connection.execute(s2)
rp2 = connection.execute(s2)
# get the keys from the fetched items
print(rp.keys())

#get only the first result
result_3 = rp.first()
print(result_3)

## print the ordered version with the iterable
for event in rp2:
    print(event.event_title, event.price)

s4 = select(func.sum(events.c.price))
rp5 = connection.execute(s4)
print(rp5.scalar())

#Count the number of events, also relabel it

s5 = select(func.count(events.c.event_title).label("event_count"))
rp6 = connection.execute(s5)
record_count = rp6.first()
print(record_count.event_count)

## select filtering
s_filter = select(events).where(events.c.event_title=="Flores")
rp_filter = connection.execute(s_filter)
record = rp_filter.first()
print(record.items())


selection = select([events.c.event_title, cast((events.c.price * events.c.sold), Numeric(12,2)).label("total_sold")])
for row in connection.execute(selection):
    print(row.event_title, row.total_sold)


s9 = select(events).where(or_(and_(events.c.price > 1000, events.c.sold > 1300), events.c.event_title == "Fortal"))
for row in connection.execute(s9):
    print(row.event_title)

updated = update(events).where(events.c.event_title == "Fortal")
updated = updated.values(sold=(events.c.sold + 200))
result = connection.execute(updated)
print(result.rowcount)
s = select(events).where(events.c.event_title == "Fortal")
result = connection.execute(s).first()
for key in result.keys():
    print(f"{key}: {result[key]}")


deleted = delete(events).where(events.c.event_title == "Fortal")
result = connection.execute(deleted)
print(result.rowcount)

s = select(events).where(events.c.event_title == "Fortal")
result = connection.execute(s).fetchall()
print(len(result))

connection.close()
print("closed")
