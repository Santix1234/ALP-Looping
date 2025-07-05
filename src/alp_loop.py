from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
from dataclasses import dataclass, field
from enum import Enum, auto

class LoopStatus(Enum):
    """Enum representing the status of the learning loop."""
    INITIALIZED = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()

@dataclass
class LoopMetrics:
    """Dataclass to track loop performance and metrics."""
    iterations: int = 0
    total_runtime: float = 0.0
    current_performance: float = 0.0
    additional_metrics: Dict[str, Any] = field(default_factory=dict)

class AdaptiveLearningProcessLoop(ABC):
    """
    Abstract Base Class for Adaptive Learning Process Loop Mechanism.
    
    This class defines the core structure and interface for implementing
    iterative, self-improving learning cycles with robust error handling
    and performance tracking.
    
    Key Responsibilities:
    - Define the core learning loop structure
    - Provide hooks for configuration and initialization
    - Manage loop status and lifecycle
    - Track and report performance metrics
    - Support error handling and logging
    """
    
    def __init__(
        self, 
        max_iterations: Optional[int] = None, 
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the Adaptive Learning Process Loop.
        
        Args:
            max_iterations (Optional[int]): Maximum number of iterations allowed.
            logger (Optional[logging.Logger]): Custom logger for tracking events.
        """
        self._max_iterations = max_iterations or float('inf')
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        
        # Core loop state tracking
        self._status = LoopStatus.INITIALIZED
        self._metrics = LoopMetrics()
        
        # Initialize logging
        self._configure_logging()
    
    def _configure_logging(self):
        """Configure logging with standard formatting."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
    
    @abstractmethod
    def _initialize(self) -> None:
        """
        Abstract method to perform initialization before the loop starts.
        
        Implementations must set up any required resources, load configurations,
        and prepare the learning environment.
        
        Raises:
            RuntimeError: If initialization fails
        """
        pass
    
    @abstractmethod
    def _iteration(self) -> bool:
        """
        Abstract method representing a single learning iteration.
        
        Performs one complete learning cycle and returns whether 
        the loop should continue.
        
        Returns:
            bool: True if the loop should continue, False to terminate
        
        Raises:
            Exception: For any critical errors during iteration
        """
        pass
    
    def run(self) -> LoopMetrics:
        """
        Execute the main learning loop with robust error handling.
        
        Returns:
            LoopMetrics: Performance metrics from the completed loop
        
        Raises:
            RuntimeError: If loop encounters unrecoverable errors
        """
        try:
            # Initialize loop
            self._status = LoopStatus.RUNNING
            self._initialize()
            
            # Main learning loop
            should_continue = True
            while (
                self._metrics.iterations < self._max_iterations and 
                should_continue
            ):
                should_continue = self._iteration()
                
                # Update metrics
                self._metrics.iterations += 1
                
                # Check termination conditions
                if not should_continue:
                    break
            
            # Mark loop completion
            self._status = (
                LoopStatus.COMPLETED 
                if should_continue 
                else LoopStatus.FAILED
            )
            
            return self._metrics
        
        except Exception as e:
            self._status = LoopStatus.FAILED
            self._logger.error(f"Learning loop failed: {e}")
            raise RuntimeError(f"Unrecoverable error in learning loop: {e}") from e
    
    def pause(self):
        """
        Pause the current learning loop if supported.
        
        Implementations may override for specific pause behavior.
        """
        if self._status == LoopStatus.RUNNING:
            self._status = LoopStatus.PAUSED
            self._logger.info("Learning loop paused")
        elif self._status == LoopStatus.INITIALIZED:
            # Allow pause from initialized state
            self._status = LoopStatus.PAUSED
            self._logger.info("Learning loop paused before running")
    
    def resume(self):
        """
        Resume a paused learning loop.
        
        Implementations may override for specific resume behavior.
        """
        if self._status == LoopStatus.PAUSED:
            self._status = LoopStatus.RUNNING
            self._logger.info("Learning loop resumed")