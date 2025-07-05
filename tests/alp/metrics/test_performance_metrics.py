import time
import pytest
from src.alp.metrics import PerformanceMetrics

def test_performance_metrics_initialization():
    """Test the initialization of PerformanceMetrics."""
    metrics = PerformanceMetrics()
    assert metrics.total_iterations == 0
    assert metrics.total_execution_time == 0.0

def test_start_and_end_iteration():
    """Test basic iteration tracking."""
    metrics = PerformanceMetrics()
    metrics.start_iteration()
    time.sleep(0.1)  # Simulate some processing time
    metrics.end_iteration()
    
    assert metrics.total_iterations == 1
    assert metrics.total_execution_time > 0.1
    assert metrics.total_execution_time < 0.2  # Accounting for slight overhead

def test_custom_metrics():
    """Test tracking custom metrics."""
    metrics = PerformanceMetrics()
    metrics.start_iteration()
    metrics.end_iteration({
        'loss': 0.5,
        'accuracy': 0.95
    })
    
    metric_results = metrics.get_metrics()
    assert metric_results['loss'] == 0.5
    assert metric_results['accuracy'] == 0.95

def test_multiple_iterations():
    """Test metrics tracking across multiple iterations."""
    metrics = PerformanceMetrics()
    
    for _ in range(3):
        metrics.start_iteration()
        time.sleep(0.1)
        metrics.end_iteration()
    
    assert metrics.total_iterations == 3
    assert metrics.total_execution_time > 0.3
    assert metrics.total_execution_time < 0.4

def test_average_iteration_time():
    """Test average iteration time calculation."""
    metrics = PerformanceMetrics()
    
    metrics.start_iteration()
    time.sleep(0.1)
    metrics.end_iteration()
    
    metrics.start_iteration()
    time.sleep(0.2)
    metrics.end_iteration()
    
    assert round(metrics.average_iteration_time, 1) == 0.2

def test_reset_metrics():
    """Test metrics reset functionality."""
    metrics = PerformanceMetrics()
    
    metrics.start_iteration()
    metrics.end_iteration({'test_metric': 42})
    
    metrics.reset()
    
    assert metrics.total_iterations == 0
    assert metrics.total_execution_time == 0.0
    assert metrics.get_metrics() == {}

def test_start_iteration_error():
    """Test error handling for ending an iteration without starting."""
    metrics = PerformanceMetrics()
    
    with pytest.raises(RuntimeError, match="Iteration not started"):
        metrics.end_iteration()