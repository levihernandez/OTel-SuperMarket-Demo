# FastInventory with Datadog

FastInventory is only a template using OpenTelemetry traces.

* Example hosts: 
  * App host: `192.168.86.37` or `127.0.0.1`
  * Database host: `192.168.86.53`
  * Datadog:
    * agent: `192.168.86.37`
    * OTel Port: `4317`
  * Jaeger UI: `http://192.168.86.62:16686/` (optional)
* Clone the project: `git clone`
* Install Python dependencies
```commandline
# Install dependencies
pip install Flask
pip install opentelemetry-sdk
pip install opentelemetry-exporter-otlp
pip install opentelemetry-exporter-datadog
pip install opentelemetry-instrumentation-flask
pip install opentelemetry.instrumentation.sqlalchemy
pip install SQLAlchemy
pip install psycopg2-binary

# Set the DB
export DATABASE_URL="postgresql://postgres:postgres@192.168.86.53:5432/marketdb"

# Set the OTel OTLP endpoint
export OTLP_ENDPOINT="http://192.168.86.62:4317"
```
* Configure Datadog agent to enable OTel integration
```commandline
# configuration in datadog.yaml
## Enable OpenTelemetry Collector
otlp_config:
  receiver:
    protocols:
      grpc:
        endpoint: 192.168.86.37:4317
```
* Restart the Datadog agent
* Run each micro-service as `python run.py inventory`
* Access the endpoints for testing:
  * http://127.0.0.1:8081/category/Seafood
  * http://127.0.0.1:8081/supplier/Meat%20Masters
* Review the OTel traces in the observability tool, for example in [Datadog](https://app.datadoghq.com/apm/home) APM.