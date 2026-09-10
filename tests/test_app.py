"""Unit tests for src.app."""

import pytest

from src.app import calculate_metrics, format_status_report


def test_calculate_metrics_success() -> None:
    """Validate statistics calculation with valid inputs."""
    data = [10.0, 20.0, 30.0]
    result = calculate_metrics(data)

    assert result["count"] == 3.0
    assert result["sum"] == 60.0
    assert result["mean"] == 20.0
    assert result["min"] == 10.0
    assert result["max"] == 30.0


def test_calculate_metrics_empty_list_raises() -> None:
    """Validate ValueError raised when input list is empty."""
    with pytest.raises(ValueError, match="Values list must not be empty"):
        calculate_metrics([])


def test_format_status_report_healthy() -> None:
    """Validate status report string when service is healthy."""
    output = format_status_report("auth-service", True, {"env": "prod", "replicas": 3})
    assert output == "[HEALTHY] auth-service | env=prod, replicas=3"


def test_format_status_report_degraded() -> None:
    """Validate status report string when service is degraded."""
    output = format_status_report("queue-worker", False, {"queue_depth": 500})
    assert output == "[DEGRADED] queue-worker | queue_depth=500"
