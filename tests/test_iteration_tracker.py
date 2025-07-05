import pytest
from src.iteration_tracker import IterationState, IterationStatus

def test_initialization():
    """Test initial state of IterationState."""
    tracker = IterationState()
    assert tracker.current_iteration == 0
    assert tracker.status == IterationStatus.INITIALIZED
    assert tracker.max_iterations is None

def test_start_iteration_without_max():
    """Test starting iterations without max limit."""
    tracker = IterationState()
    
    # First iteration
    assert tracker.start_iteration() is True
    assert tracker.current_iteration == 1
    assert tracker.status == IterationStatus.IN_PROGRESS

def test_start_iteration_with_max():
    """Test starting iterations with max limit."""
    tracker = IterationState(max_iterations=3)
    
    # First iteration
    assert tracker.start_iteration() is True
    assert tracker.current_iteration == 1
    
    # Second iteration
    assert tracker.start_iteration() is True
    assert tracker.current_iteration == 2
    
    # Third iteration
    assert tracker.start_iteration() is True
    assert tracker.current_iteration == 3
    
    # Fourth iteration (should terminate)
    assert tracker.start_iteration() is False
    assert tracker.status == IterationStatus.TERMINATED

def test_complete_iteration():
    """Test completing an iteration."""
    tracker = IterationState(max_iterations=2)
    
    # First iteration
    assert tracker.start_iteration() is True
    tracker.complete_iteration()
    
    # Second iteration
    assert tracker.start_iteration() is True
    tracker.complete_iteration()
    
    assert tracker.status == IterationStatus.COMPLETED

def test_terminate():
    """Test terminating the iteration process."""
    tracker = IterationState()
    tracker.terminate(reason="Test termination")
    
    assert tracker.status == IterationStatus.TERMINATED
    assert tracker.metadata.get('termination_reason') == "Test termination"

def test_reset():
    """Test resetting the iteration state."""
    tracker = IterationState(max_iterations=3)
    tracker.start_iteration()
    tracker.start_iteration()
    
    tracker.reset()
    
    assert tracker.current_iteration == 0
    assert tracker.status == IterationStatus.INITIALIZED
    assert len(tracker.metadata) == 0