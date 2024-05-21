from flask import Flask, jsonify
import otel.otel as config

app = Flask(__name__)

provider = config.TracerProvider(resource=config.order_resource)
provider.add_span_processor(config.processor)
config.trace.set_tracer_provider(provider)
tracer = config.trace.get_tracer(__name__)


@app.route('/order')
def inventory():
    with tracer.start_as_current_span("order") as span:
        span.set_attribute("sql.query", "SELECT * FROM DUAL;")
        # Your inventory management logic here
        return jsonify({'message': 'Order processed successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
