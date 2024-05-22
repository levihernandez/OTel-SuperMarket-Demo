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
* Access the endpoints for testing:
  * http://192.168.86.37:8081/category/Seafood
  * http://192.168.86.37:8081/supplier/Meat%20Masters
* Review the OTel traces in the observability tool, for example in [Datadog](https://app.datadoghq.com/apm/home) APM.
