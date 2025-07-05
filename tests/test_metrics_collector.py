import pytest
import time
from src.metrics_collector import PerformanceMetricsCollector, MetricType

def test_metrics_collector_basic_recording():
    """Test basic metric recording functionality."""
    collector = PerformanceMetricsCollector()
    
    # Record a performance metric
    collector.record_metric("learning_rate", 0.01)
    
    # Verify metric was recorded
    history = collector.get_metric_history("learning_rate")
    assert len(history) == 1
    assert history[0].value == 0.01

def test_metrics_collector_max_history():
    """Test max history limitation."""
    collector = PerformanceMetricsCollector(max_history=3)
    
    # Record more than max history
    for i in range(5):
        collector.record_metric("test_metric", i)
    
    # Verify only last 3 records are kept
    history = collector.get_metric_history("test_metric")
    assert len(history) == 3
    assert [record.value for record in history] == [2, 3, 4]

def test_latest_metric_retrieval():
    """Test retrieving the latest metric."""
    collector = PerformanceMetricsCollector()
    
    collector.record_metric("accuracy", 0.75)
    collector.record_metric("accuracy", 0.80)
    
    latest = collector.get_latest_metric("accuracy")
    assert latest is not None
    assert latest.value == 0.80

def test_metric_average_calculation():
    """Test average calculation for metrics."""
    collector = PerformanceMetricsCollector()
    
    collector.record_metric("error_rate", 0.1)
    collector.record_metric("error_rate", 0.2)
    collector.record_metric("error_rate", 0.3)
    
    avg = collector.calculate_metric_average("error_rate")
    assert avg == 0.2  # (0.1 + 0.2 + 0.3) / 3

def test_metric_types():
    """Test recording different metric types."""
    collector = PerformanceMetricsCollector()
    
    collector.record_metric("cpu_usage", 50.0, MetricType.RESOURCE_USAGE)
    
    latest = collector.get_latest_metric("cpu_usage")
    assert latest is not None
    assert latest.type == MetricType.RESOURCE_USAGE

def test_non_existent_metric():
    """Test behavior with non-existent metrics."""
    collector = PerformanceMetricsCollector()
    
    history = collector.get_metric_history("non_existent")
    assert len(history) == 0
    
    latest = collector.get_latest_metric("non_existent")
    assert latest is None
    
    avg = collector.calculate_metric_average("non_existent")
    assert avg is None