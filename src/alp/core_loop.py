from typing import Any, Callable, Dict, Optional
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from time import time

class LoopStatus(Enum):
    """Represents the status of the learning loop."""
    INITIALIZED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    TERMINATED = auto()

@dataclass
class PerformanceMetrics:
    """Track performance metrics for the learning loop."""
    total_iterations: int = 0
    total_runtime: float = 0.0
    average_iteration_time: float = 0.0
    errors_encountered: int = 0

class AdaptiveLearningLoopException(Exception):
    """Base exception for Adaptive Learning Loop errors."""
    pass

class LoopExecutionError(AdaptiveLearningLoopException):
    """Raised when a critical error occurs during loop execution."""
    pass

class CoreLoopExecutor:
    """
    Core execution strategy for Adaptive Learning Process (ALP) learning cycles.
    
    Manages iteration flow control, performance tracking, and error handling.
    """
    
    def __init__(
        self, 
        iteration_function: Callable[[Dict[str, Any]], Dict[str, Any]], 
        config: Optional[Dict[str, Any]] = None,
        max_iterations: Optional[int] = None,
        max_runtime: Optional[float] = None
    ):
        """
        Initialize the core loop executor.
        
        Args:
            iteration_function: Callable that performs a single learning iteration
            config: Configuration dictionary for the learning process
            max_iterations: Maximum number of iterations to run
            max_runtime: Maximum runtime in seconds
        """
        self.iteration_function = iteration_function
        self.config = config or {}
        self.max_iterations = max_iterations or float('inf')
        self.max_runtime = max_runtime or float('inf')
        
        self.status = LoopStatus.INITIALIZED
        self.metrics = PerformanceMetrics()
        self.current_context: Dict[str, Any] = {}
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    
    def _validate_config(self) -> None:
        """
        Validate the configuration parameters.
        
        Raises:
            LoopExecutionError: If configuration is invalid
        """
        if not callable(self.iteration_function):
            raise LoopExecutionError("Invalid iteration function")
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the learning loop with comprehensive tracking and error handling.
        
        Returns:
            Final context/result of the learning process
        
        Raises:
            LoopExecutionError: If a critical error occurs during execution
        """
        try:
            self._validate_config()
            
            start_time = time()
            self.status = LoopStatus.RUNNING
            
            while (
                self.metrics.total_iterations < self.max_iterations and 
                time() - start_time < self.max_runtime
            ):
                iteration_start = time()
                
                try:
                    # Perform a single learning iteration
                    self.current_context = self.iteration_function(self.current_context)
                    
                    # Update performance metrics
                    iteration_time = time() - iteration_start
                    self.metrics.total_iterations += 1
                    self.metrics.total_runtime += iteration_time
                    self.metrics.average_iteration_time = (
                        self.metrics.total_runtime / self.metrics.total_iterations
                    )
                    
                    # Optional: Add termination condition check
                    if self._should_terminate():
                        break
                
                except Exception as e:
                    self.metrics.errors_encountered += 1
                    self.logger.error(f"Iteration error: {e}")
                    
                    # Optionally handle or re-raise based on error strategy
                    if self.metrics.errors_encountered > 10:
                        raise LoopExecutionError("Too many errors") from e
            
            # Determine final status
            self.status = (
                LoopStatus.COMPLETED 
                if self.metrics.total_iterations > 0 
                else LoopStatus.TERMINATED
            )
            
            return self.current_context
        
        except Exception as e:
            self.status = LoopStatus.FAILED
            self.logger.critical(f"Loop execution failed: {e}")
            raise LoopExecutionError(f"Learning loop execution failed: {e}") from e
        
        finally:
            self._log_metrics()
    
    def _should_terminate(self) -> bool:
        """
        Optional method to implement custom termination conditions.
        
        Returns:
            bool: Whether the loop should terminate
        """
        # Override this method in subclasses to add custom termination logic
        return False
    
    def _log_metrics(self) -> None:
        """Log performance metrics after loop execution."""
        self.logger.info(f"Loop Metrics: {self.metrics}")
        return {
            "total_iterations": self.metrics.total_iterations,
            "total_runtime": self.metrics.total_runtime,
            "average_iteration_time": self.metrics.average_iteration_time,
            "errors_encountered": self.metrics.errors_encountered
        }