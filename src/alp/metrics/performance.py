from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import time
import statistics


@dataclass
class PerformanceMetrics:
    """
    A comprehensive performance metrics collection class for ALP learning cycles.
    
    Tracks various performance characteristics including:
    - Execution times
    - Iteration statistics
    - Resource utilization
    """
    
    # Timing metrics
    total_iterations: int = 0
    total_execution_time: float = 0.0
    
    # Per-iteration tracking
    iteration_times: list[float] = field(default_factory=list)
    
    # Performance statistics
    _start_time: Optional[float] = None
    
    def start_iteration(self) -> None:
        """
        Mark the start of a learning iteration.
        """
        self._start_time = time.perf_counter()
        self.total_iterations += 1
    
    def end_iteration(self) -> float:
        """
        Mark the end of a learning iteration and calculate iteration time.
        
        Returns:
            float: Duration of the iteration in seconds
        """
        if self._start_time is None:
            raise RuntimeError("Iteration not started. Call start_iteration() first.")
        
        iteration_time = time.perf_counter() - self._start_time
        self.iteration_times.append(iteration_time)
        self.total_execution_time += iteration_time
        
        self._start_time = None
        return iteration_time
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive performance summary.
        
        Returns:
            Dict containing performance metrics
        """
        if not self.iteration_times:
            return {
                "total_iterations": self.total_iterations,
                "total_execution_time": self.total_execution_time,
                "avg_iteration_time": 0.0,
                "min_iteration_time": 0.0,
                "max_iteration_time": 0.0,
                "iteration_time_std_dev": 0.0
            }
        
        return {
            "total_iterations": self.total_iterations,
            "total_execution_time": self.total_execution_time,
            "avg_iteration_time": statistics.mean(self.iteration_times),
            "min_iteration_time": min(self.iteration_times),
            "max_iteration_time": max(self.iteration_times),
            "iteration_time_std_dev": statistics.stdev(self.iteration_times) if len(self.iteration_times) > 1 else 0.0
        }
    
    def reset(self) -> None:
        """
        Reset all performance metrics to their initial state.
        """
        self.total_iterations = 0
        self.total_execution_time = 0.0
        self.iteration_times.clear()
        self._start_time = None