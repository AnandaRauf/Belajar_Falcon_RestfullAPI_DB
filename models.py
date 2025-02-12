from pony.orm import Database, Required, PrimaryKey

db = Database()

class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    price = Required(float)
    description = Required(str)


db.bind(provider='mysql', host='localhost', user='root', password='', db='falcon_restfulldb')
db.generate_mapping(create_tables=True)