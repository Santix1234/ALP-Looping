from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import time
import logging

@dataclass
class PerformanceMetrics:
    """
    A lightweight, thread-safe performance metrics collection system for ALP learning cycles.
    
    Tracks key performance indicators like:
    - Iteration count
    - Total execution time
    - Average processing time
    - Custom metrics
    """
    
    # Core tracking metrics
    total_iterations: int = field(default=0)
    total_execution_time: float = field(default=0.0)
    
    # Custom metrics tracking
    _custom_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Timing tracking
    _start_time: Optional[float] = field(default=None)
    
    def start_iteration(self) -> None:
        """
        Mark the start of a learning iteration.
        
        Resets start time for precise timing.
        """
        self._start_time = time.time()
    
    def end_iteration(self, custom_metrics: Optional[Dict[str, Any]] = None) -> None:
        """
        Conclude an iteration, updating performance metrics.
        
        Args:
            custom_metrics: Optional dictionary of custom metrics to track
        """
        if self._start_time is None:
            raise RuntimeError("Iteration not started. Call start_iteration() first.")
        
        # Calculate iteration time
        iteration_time = time.time() - self._start_time
        
        # Update core metrics
        self.total_iterations += 1
        self.total_execution_time += iteration_time
        
        # Reset start time
        self._start_time = None
        
        # Update custom metrics
        if custom_metrics:
            for key, value in custom_metrics.items():
                self._custom_metrics[key] = value
    
    @property
    def average_iteration_time(self) -> float:
        """
        Calculate the average iteration time.
        
        Returns:
            Average iteration time, or 0 if no iterations
        """
        return self.total_execution_time / max(1, self.total_iterations)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Retrieve all collected metrics.
        
        Returns:
            Comprehensive dictionary of performance metrics
        """
        metrics = {
            'total_iterations': self.total_iterations,
            'total_execution_time': self.total_execution_time,
            'average_iteration_time': self.average_iteration_time,
            **self._custom_metrics
        }
        return metrics
    
    def reset(self) -> None:
        """
        Reset all performance metrics to initial state.
        """
        self.total_iterations = 0
        self.total_execution_time = 0.0
        self._custom_metrics.clear()
        self._start_time = None