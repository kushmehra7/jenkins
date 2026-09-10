"""Core application logic demonstrating clean Python code."""

from typing import Any


def calculate_metrics(values: list[float]) -> dict[str, float]:
    """Calculate basic statistical metrics from a list of numerical values.

    Args:
        values: Non-empty list of float or int values.

    Returns:
        Dictionary containing sum, mean, min, and max.

    Raises:
        ValueError: If values list is empty.
    """
    if not values:
        raise ValueError("Values list must not be empty.")

    total = sum(values)
    count = len(values)
    mean = total / count

    return {
        "count": float(count),
        "sum": total,
        "mean": mean,
        "min": min(values),
        "max": max(values),
    }


def format_status_report(
    service_name: str,
    is_healthy: bool,
    details: dict[str, Any],
) -> str:
    """Format a human-readable service status report.

    Args:
        service_name: Name of the microservice.
        is_healthy: Health status flag.
        details: Additional status metadata.

    Returns:
        Formatted summary string.
    """
    status_label = "HEALTHY" if is_healthy else "DEGRADED"
    detail_str = ", ".join(f"{k}={v}" for k, v in sorted(details.items()))
    return f"[{status_label}] {service_name} | {detail_str}"


if __name__ == "__main__":
    sample_data = [10.5, 20.0, 30.5, 40.0]
    metrics = calculate_metrics(sample_data)
    print("Metrics:", metrics)
    report = format_status_report(
        "jenkins-ci-worker",
        True,
        {"version": "1.0.0", "active_jobs": 0},
    )
    print(report)
