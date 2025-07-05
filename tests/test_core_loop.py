import pytest
from typing import Dict, Any
from src.alp.core_loop import CoreLoopExecutor, LoopStatus, LoopExecutionError

def simple_iteration_function(context: Dict[str, Any]) -> Dict[str, Any]:
    """A simple mock iteration function for testing."""
    current_count = context.get('count', 0)
    context['count'] = current_count + 1
    return context

def test_core_loop_basic_execution():
    """Test basic execution of the core loop."""
    executor = CoreLoopExecutor(
        iteration_function=simple_iteration_function, 
        max_iterations=5
    )
    
    result = executor.execute()
    
    assert result['count'] == 5
    assert executor.status == LoopStatus.COMPLETED
    assert executor.metrics.total_iterations == 5

def test_core_loop_max_iterations():
    """Test that the loop respects max iterations."""
    executor = CoreLoopExecutor(
        iteration_function=simple_iteration_function, 
        max_iterations=3
    )
    
    result = executor.execute()
    
    assert result['count'] == 3
    assert executor.metrics.total_iterations == 3

def test_core_loop_error_handling():
    """Test error handling in the core loop."""
    def error_function(context: Dict[str, Any]) -> Dict[str, Any]:
        """A function that raises an error after 2 iterations."""
        current_count = context.get('count', 0)
        if current_count >= 2:
            raise ValueError("Simulated error")
        context['count'] = current_count + 1
        return context
    
    with pytest.raises(LoopExecutionError):
        executor = CoreLoopExecutor(
            iteration_function=error_function, 
            max_iterations=5
        )
        executor.execute()

def test_core_loop_performance_metrics():
    """Test performance metrics tracking."""
    executor = CoreLoopExecutor(
        iteration_function=simple_iteration_function, 
        max_iterations=5
    )
    
    executor.execute()
    
    assert executor.metrics.total_iterations == 5
    assert executor.metrics.total_runtime > 0
    assert executor.metrics.average_iteration_time > 0
    assert executor.metrics.errors_encountered == 0

def test_core_loop_with_initial_context():
    """Test loop execution with an initial context."""
    def context_tracking_function(context: Dict[str, Any]) -> Dict[str, Any]:
        """Track context through iterations."""
        context['iterations'] = context.get('iterations', []) + [1]
        return context
    
    executor = CoreLoopExecutor(
        iteration_function=context_tracking_function, 
        max_iterations=3
    )
    
    result = executor.execute()
    
    assert len(result['iterations']) == 3
    assert result['iterations'] == [1, 1, 1]