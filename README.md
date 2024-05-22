# OTel-SuperMarket-Demo with Datadog

OTel-SuperMarket-Demo is only a sample code for OpenTelemetry traces with Datadog.

* Example hosts: 
  * App host: `192.168.86.37` or `127.0.0.1`
  * Database host: `192.168.86.53`
  * Datadog:
    * agent: `192.168.86.37`
    * OTel Port: `4317`
  * Jaeger UI: `http://192.168.86.62:16686/` (optionally deploy the [Jaeger docker compose](/jaeger/docker-compose.yaml))
* Clone the project: `git clone https://github.com/levihernandez/OTel-SuperMarket-Demo.git`
* Set venv and install Python dependencies
```commandline
# Setup venv
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install Flask
pip install opentelemetry-sdk
pip install opentelemetry-exporter-otlp
pip install opentelemetry-instrumentation-flask
pip install opentelemetry.instrumentation.sqlalchemy
pip install SQLAlchemy
pip install psycopg2-binary

# Set the DB
export DATABASE_URL="postgresql://postgres:postgres@192.168.86.53:5432/marketdb"

# Choose the OTLP Endpoint
## Set the OTel OTLP endpoint for Jaeger (can be deployed via docker compose separately)
export OTLP_ENDPOINT="http://192.168.86.62:4317"

## Set the OTel OTLP endpoint for Datadog Agent
export OTLP_ENDPOINT="http://192.168.86.37:4317"
```
* Configure Datadog agent to enable OTel integration
```commandline
# configuration in datadog.yaml
#...
# other Datadog configs, including API Key
#...

## Enable OpenTelemetry Collector
otlp_config:
  receiver:
    protocols:
      grpc:
        endpoint: 192.168.86.37:4317
```
* Restart the Datadog agent
* Create the database `marketdb` in Postgres
* Seed the DB with Faker data `python inventory_management/seed_db.py`
* Run each micro-service as `python run.py inventory`
* Access the endpoints for testing ([Jaeger](jaeger.md) & [Datadog](datadog.md) sample results):
  * http://192.168.86.37:8081/category/Seafood
  * http://192.168.86.37:8081/supplier/Meat%20Masters
  * ![](img/json-payload.png)
* Review the OTel traces in the observability tool, for example in [Datadog](https://app.datadoghq.com/apm/home) APM.

## Auto Instrumentation of Python Flask with Datadog `ddtrace`

* Install the Datadog library
* Auto Instrument with Datadog `ddtrace`
 * `DD_SERVICE="order-processing" DD_ENV="test" DD_LOGS_INJECTION=true DD_PROFILING_ENABLED=true DD_APPSEC_ENABLED=true ddtrace-run python run.py order`
* [Datadog Results](datadog-ddtrace.md)


## Auto Instrumentation of Python Flask with OTel

* Install OTel libraries
```commandline
pip install opentelemetry-distro
pip install opentelemetry-exporter-otlp

opentelemetry-bootstrap -a install

OTEL_RESOURCE_ATTRIBUTES=service.name=order-processing,environment=test-01,env=test \
OTEL_EXPORTER_OTLP_INSECURE=true \
OTEL_SERVICE_NAME=order-processing \
OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=192.168.86.37:4317 \
opentelemetry-instrument \
python run.py order

```
* OTel Auto Instrumentation might need additional configs as the transaction query was missing, see [OTel Auto Instrumentation Results](otel-auto-instrumentation.md)
