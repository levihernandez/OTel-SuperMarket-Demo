from flask import Flask, jsonify
import otel.otel as config
import os

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

provider = config.TracerProvider(resource=config.inventory_resource)
provider.add_span_processor(config.processor)
config.trace.set_tracer_provider(provider)
tracer = config.trace.get_tracer(__name__)

# Database connection setup
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
config.SQLAlchemyInstrumentor().instrument(engine=engine, enable_commenter=True, commenter_options={"db_driver": True})
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()
items_table = Table('products', metadata, autoload_with=engine)


@app.route('/category/<string:category>')
def category(category):
    return web_handler(category)

def web_handler(category):
    with tracer.start_as_current_span("category") as span:
        span.set_attribute("span.type", "web")

        items, stock_level = db_handler(category)

        if stock_level < 1:
            return jsonify({'error': f'Item category {category} is out of stock!'}), 404

        return jsonify({'count': stock_level, 'products': items})

def db_handler(category):
    with tracer.start_as_current_span("category-db") as span:
        span.set_attribute("span.type", "db")

        session = SessionLocal()
        result = session.execute(items_table.select().where(items_table.c.category == category)).fetchall()

        if not result:
            return [], 0

        items = []
        for row in result:
            item = {"id": row[0], "category": row[2], "supplier": row[5], "quantity": row[3], "price": row[4]}
            items.append(item)

        session.close()

        span.set_attribute("stock_level", len(items))
        return items, len(items)


@app.route('/supplier/<string:supplier>')
def supplier(supplier):
    with tracer.start_as_current_span("supplier") as span:
        span.set_attribute("span.type", "web")
        # span.set_attribute("sql.query", f"SELECT * FROM products WHERE category = :category;")

        session = SessionLocal()
        result = session.execute(items_table.select().where(items_table.c.supplier == supplier)).fetchall()

        if not result:
            return jsonify({'error': f'Supplier {supplier} not found in inventory!'}), 404

        items = []
        for row in result:
            item = {"id": row[0], "category": row[2], "supplier": row[5], "quantity": row[3], "price": row[4]}
            items.append(item)

        session.close()

        stock_level = len(items)

        span.set_attribute("stock_level", stock_level)

        # Your inventory management logic here
        if stock_level < 1:
            return jsonify({'error': f'Supplier {supplier} is out of stock!'}), 404

        return jsonify({'count': stock_level, 'supplier': items})


if __name__ == '__main__':
    app.run(debug=True)
