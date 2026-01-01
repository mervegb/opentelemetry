# OTel SDK
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
    MetricReader,
)

from opentelemetry.metrics import Counter, Histogram, ObservableGauge
from opentelemetry.sdk.metrics import MeterProvider


# OTel API
from opentelemetry import metrics as metric_api

import psutil


def create_meter (name: str, version:str) -> metric_api.Meter:
    metric_reader = create_metrics_pipeline(5000)
    provider = MeterProvider(
        metric_readers=[metric_reader]
    )
    metric_api.set_meter_provider(provider)
    meter = metric_api.get_meter(name, version)
    return meter

def create_metrics_pipeline(export_interval: int) -> MetricReader:
    console_exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader( # collects metrics at regular intervals and passes them to the exporter
        exporter=console_exporter,
        export_interval_millis=export_interval
    )
    return reader


# def create_request_instruments(meter: metric_api.Meter) -> dict[str, metric_api.Instrument]:
#     index_counter = meter.create_counter(
#         name="index_called",
#         unit="request",
#         description="Total amount of requests to /"
#     )

#     instruments = {
#         "index_counter": index_counter,
#     }
#     return instruments


# you can create multiple instruments from the same meter
# traffic volume counter -> how much traffic do we get
# error rate counter -> how many requests fail
def create_request_instruments(meter: metric_api.Meter) -> dict:
    traffic_volume = meter.create_counter(
        name="traffic_volume",
        unit="request",
        description="total volume of requests to an endpoint",
    )
    error_rate = meter.create_counter(
        name="error_rate",
        unit="request",
        description="rate of failed requests"
    )
    request_latency = meter.create_histogram(
        name="http.server.request.duration",
        unit="s",
        description="latency for a request to be served"
    )
    
    instruments = {
        "traffic_volume": traffic_volume,
        "error_rate": error_rate,
        "request_latency": request_latency,
    }
    return instruments


def get_cpu_utilization(opt: metric_api.CallbackOptions) -> metric_api.Observation:
    cpu_util = psutil.cpu_percent(interval=None) / 100
    yield metric_api.Observation(cpu_util)
    

def create_resource_instruments(meter: metric_api.Meter) -> dict:
    cpu_util_gauage = meter.create_observable_gauge(
        name="process.cpu.utilization",
        callbacks=[get_cpu_utilization],
        unit="1",
        description="CPU utilization since last call",
    )
    
    instruments = {
        "cpu_utilization": cpu_util_gauage
    }
    return instruments

