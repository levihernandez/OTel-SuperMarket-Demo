from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

import os
import sys
import argparse


span_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTLP_ENDPOINT"),
    insecure=True
)
    # Your configuration code here


# Instrument Flask apps for inventory management and order processing
# export OTLP_ENDPOINT="http://192.168.86.62:4317" # for Jaeger collector
# export OTLP_ENDPOINT="http://192.168.86.37:4317" # for Datadog agent OTel collector

# Initialize OpenTelemetry exporters
inventory_resource = Resource(attributes={
    "service.name": "inventory-management",
    "env":"test",
    "service.instance.id": "instance-1"
})
order_resource = Resource(attributes={
    "service.name": "order-processing",
    "env":"test",
    "service.instance.id": "instance-2"
})

processor = BatchSpanProcessor(span_exporter)

FlaskInstrumentor().instrument()
