from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import ConsoleLogExporter, SimpleLogRecordProcessor

from opentelemetry.sdk.resources import Resource


## SimpleLogRecordProcessor processes the logs as soon as they are created
## BatchLogRecordProcessor collects multiple LogRecords and processes them in a batch


logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": "example-app"
        }
    ),
)

logger_provider.add_log_record_processor(SimpleLogRecordProcessor(ConsoleLogExporter()))
handler = LoggingHandler(logger_provider=logger_provider)


## Logs offer a view of what's happening inside your application at any given point
## OpenTelemetry offers a single set of APIs, libraries, agents and collectors to capture logs from your application
## Logs Bridge API is used to integrate existing logging solutions with OpenTelemetry's tracing and metrics collection