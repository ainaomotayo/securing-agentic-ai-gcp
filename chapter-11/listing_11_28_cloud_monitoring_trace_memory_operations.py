# Securing Agentic AI on Google Cloud
# Chapter 11 — Session State, Memory, and Data Governance
# Listing: Cloud Monitoring custom metrics + Cloud Trace for memory anomaly detection
# Repo: https://github.com/ainaomotayo/securing-agentic-ai-gcp
#
# IAM required: roles/monitoring.metricWriter, roles/cloudtrace.agent
# Run register_memory_metric_descriptor() once at deployment time before first data point.

import os
import time
import logging
from google.cloud import monitoring_v3
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logger = logging.getLogger(__name__)

_monitoring_client = monitoring_v3.MetricServiceClient()

_tracer_provider = TracerProvider()
_tracer_provider.add_span_processor(
    BatchSpanProcessor(CloudTraceSpanExporter())
)
trace.set_tracer_provider(_tracer_provider)
_tracer = trace.get_tracer(__name__)


def _write_memory_metric(
    project_id: str,
    operation: str,
    session_id: str,
    invocation_id: str,
) -> None:
    """
    Publish a custom metric for a memory read or write operation.
    operation must be 'write' or 'read'.
    """
    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/adk/memory_operation_count"
    series.metric.labels["operation"] = operation
    series.metric.labels["session_id"] = session_id[:32]
    series.metric.labels["invocation_id"] = invocation_id[:32]
    series.resource.type = "global"
    series.resource.labels["project_id"] = project_id
    now = time.time()
    series.points = [
        monitoring_v3.Point(
            interval=monitoring_v3.TimeInterval(
                end_time={"seconds": int(now), "nanos": int((now % 1) * 1e9)}
            ),
            value=monitoring_v3.TypedValue(int64_value=1),
        )
    ]
    try:
        _monitoring_client.create_time_series(
            name=f"projects/{project_id}",
            time_series=[series],
        )
    except Exception as exc:
        logger.warning("Failed to write memory operation metric: %s", exc)


def traced_memory_write(
    project_id: str,
    session_id: str,
    invocation_id: str,
    corpus_name: str,
) -> None:
    """Wrap a memory write call with a Cloud Trace span and publish the metric."""
    with _tracer.start_as_current_span("memory.write") as span:
        span.set_attribute("session.id", session_id)
        span.set_attribute("invocation.id", invocation_id)
        span.set_attribute("memory.corpus", corpus_name)
        _write_memory_metric(project_id, "write", session_id, invocation_id)


def traced_memory_read(
    project_id: str,
    session_id: str,
    invocation_id: str,
    query: str,
) -> None:
    """Wrap a memory read (search_memory) with a Cloud Trace span and metric."""
    with _tracer.start_as_current_span("memory.read") as span:
        span.set_attribute("session.id", session_id)
        span.set_attribute("invocation.id", invocation_id)
        span.set_attribute("memory.query.length", len(query))
        _write_memory_metric(project_id, "read", session_id, invocation_id)


def register_memory_metric_descriptor(project_id: str) -> None:
    """
    Register the custom metric descriptor for memory operation counts.
    Call once at deployment time, not on every agent startup.
    IAM required: roles/monitoring.metricWriter.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    descriptor = monitoring_v3.MetricDescriptor()
    descriptor.type = "custom.googleapis.com/adk/memory_operation_count"
    descriptor.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64
    descriptor.display_name = "ADK Memory Operation Count"
    descriptor.description = (
        "Count of ADK memory read and write operations per invocation. "
        "Use to detect memory poisoning attempts via write-frequency spikes."
    )

    label_operation = monitoring_v3.LabelDescriptor()
    label_operation.key = "operation"
    label_operation.value_type = monitoring_v3.LabelDescriptor.ValueType.STRING
    label_operation.description = "read or write"

    label_session = monitoring_v3.LabelDescriptor()
    label_session.key = "session_id"
    label_session.value_type = monitoring_v3.LabelDescriptor.ValueType.STRING

    label_invocation = monitoring_v3.LabelDescriptor()
    label_invocation.key = "invocation_id"
    label_invocation.value_type = monitoring_v3.LabelDescriptor.ValueType.STRING

    descriptor.labels.extend([label_operation, label_session, label_invocation])
    client.create_metric_descriptor(name=project_name, metric_descriptor=descriptor)


def create_memory_write_spike_alert(
    project_id: str,
    notification_channel_id: str,
) -> None:
    """
    Create a Cloud Monitoring alert policy that fires when more than 50 memory
    writes occur in a 5-minute window.
    IAM required: roles/monitoring.alertPolicyEditor.
    """
    client = monitoring_v3.AlertPolicyServiceClient()
    project_name = f"projects/{project_id}"

    condition = monitoring_v3.AlertPolicy.Condition(
        display_name="ADK memory write spike",
        condition_threshold=monitoring_v3.AlertPolicy.Condition.MetricThreshold(
            filter=(
                'metric.type="custom.googleapis.com/adk/memory_operation_count" '
                'AND metric.labels.operation="write"'
            ),
            comparison=monitoring_v3.ComparisonType.COMPARISON_GT,
            threshold_value=50,
            duration={"seconds": 300},
            aggregations=[
                monitoring_v3.Aggregation(
                    alignment_period={"seconds": 300},
                    per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_RATE,
                )
            ],
        ),
    )

    policy = monitoring_v3.AlertPolicy(
        display_name="ADK Memory Write Spike",
        conditions=[condition],
        notification_channels=[notification_channel_id],
        combiner=monitoring_v3.AlertPolicy.ConditionCombinerType.AND,
    )

    client.create_alert_policy(name=project_name, alert_policy=policy)
