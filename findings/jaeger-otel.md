# OTel Traces Shipped to Jaeger

## Outcomes Performed by OpenTelemetry Manual Instrumentation

* APM OpenTelemetry Trace + Discovery of SQL transaction with SQLAlchemy shipped to Jaeger
  * `SQLAlchemyInstrumentor().instrument(engine=engine, enable_commenter=True, commenter_options={"db_driver": True})`

![](../img/jaeger-01.png)

* Proper mapping of the manually instrumented functions

![](../img/jaeger-02.png)

* Flamegraph stats for execution time

![](../img/jaeger-03.png)
