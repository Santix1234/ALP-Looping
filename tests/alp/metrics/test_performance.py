import time
import pytest
from src.alp.metrics.performance import PerformanceMetrics


def test_performance_metrics_basic_flow():
    """
    Test the basic flow of performance metrics tracking.
    """
    metrics = PerformanceMetrics()
    
    # Simulate multiple iterations
    for _ in range(5):
        metrics.start_iteration()
        time.sleep(0.1)  # Simulate some work
        metrics.end_iteration()
    
    summary = metrics.get_performance_summary()
    
    assert summary['total_iterations'] == 5
    assert 0.6 > summary['total_execution_time'] > 0.4  # Allow for some variance
    assert 0.12 > summary['avg_iteration_time'] > 0.08  # Relaxed time check
    assert 0.12 > summary['max_iteration_time'] > 0.08
    assert 0.12 > summary['min_iteration_time'] > 0.08


def test_performance_metrics_reset():
    """
    Test the reset functionality of performance metrics.
    """
    metrics = PerformanceMetrics()
    
    # Simulate multiple iterations
    for _ in range(3):
        metrics.start_iteration()
        time.sleep(0.1)
        metrics.end_iteration()
    
    metrics.reset()
    
    summary = metrics.get_performance_summary()
    
    assert summary['total_iterations'] == 0
    assert summary['total_execution_time'] == 0.0


def test_performance_metrics_no_iterations():
    """
    Test performance summary when no iterations have occurred.
    """
    metrics = PerformanceMetrics()
    
    summary = metrics.get_performance_summary()
    
    assert summary['total_iterations'] == 0
    assert summary['total_execution_time'] == 0.0
    assert summary['avg_iteration_time'] == 0.0
    assert summary['min_iteration_time'] == 0.0
    assert summary['max_iteration_time'] == 0.0


def test_performance_metrics_error_handling():
    """
    Test error handling for incorrect method calls.
    """
    metrics = PerformanceMetrics()
    
    with pytest.raises(RuntimeError):
        metrics.end_iteration()


def test_performance_metrics_single_iteration():
    """
    Test performance metrics for a single iteration.
    """
    metrics = PerformanceMetrics()
    
    metrics.start_iteration()
    time.sleep(0.05)
    iteration_time = metrics.end_iteration()
    
    summary = metrics.get_performance_summary()
    
    assert summary['total_iterations'] == 1
    assert 0.07 > iteration_time > 0.03  # Wider time window
    assert summary['iteration_time_std_dev'] == 0.0