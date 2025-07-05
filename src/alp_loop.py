from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import logging
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class LoopConfiguration:
    """Configuration class for ALP Loop parameters."""
    max_iterations: int = 100
    learning_rate: float = 0.01
    convergence_threshold: float = 1e-5
    logging_level: int = logging.INFO
    early_stopping: bool = True
    additional_params: Dict[str, Any] = field(default_factory=dict)

class ALPLoopBase(ABC):
    """
    Abstract Base Class for Adaptive Learning Process (ALP) Loop Mechanism.
    
    Provides a standardized template for implementing iterative learning cycles
    with robust configuration, tracking, and error handling.
    
    Key Features:
    - Configurable learning parameters
    - Iteration tracking and management
    - Comprehensive logging
    - Flexible error handling
    - Performance metrics collection
    """
    
    def __init__(self, config: Optional[LoopConfiguration] = None):
        """
        Initialize the ALP Loop with configuration.
        
        Args:
            config (Optional[LoopConfiguration]): Configuration for the learning loop.
        """
        self.config = config or LoopConfiguration()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(self.config.logging_level)
        
        # Iteration tracking
        self.current_iteration = 0
        self.best_performance = float('-inf')
        self.iteration_history: List[Dict[str, Any]] = []
        
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize learning process, models, or data structures.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def learning_iteration(self) -> float:
        """
        Perform a single learning iteration.
        
        Returns:
            float: Performance metric for the current iteration.
        
        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        pass
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the main learning loop with comprehensive error handling.
        
        Returns:
            Dict[str, Any]: Final learning results and metadata.
        """
        try:
            self.initialize()
            
            while not self._should_terminate():
                performance = self.learning_iteration()
                
                # Track iteration history
                iteration_data = {
                    'iteration': self.current_iteration,
                    'performance': performance
                }
                self.iteration_history.append(iteration_data)
                
                # Update best performance
                if performance > self.best_performance:
                    self.best_performance = performance
                
                self.current_iteration += 1
                
                self.logger.info(
                    f"Iteration {self.current_iteration}: "
                    f"Performance = {performance}"
                )
            
            return self._finalize()
        
        except Exception as e:
            self.logger.error(f"Learning process failed: {e}")
            raise
    
    def _should_terminate(self) -> bool:
        """
        Determine if the learning loop should terminate.
        
        Returns:
            bool: Whether to stop the learning process.
        """
        conditions = [
            self.current_iteration >= self.config.max_iterations,
            (self.config.early_stopping and 
             len(self.iteration_history) > 1 and 
             abs(self.iteration_history[-1]['performance'] - 
                 self.iteration_history[-2]['performance']) < 
                 self.config.convergence_threshold)
        ]
        
        return any(conditions)
    
    def _finalize(self) -> Dict[str, Any]:
        """
        Finalize the learning process and collect results.
        
        Returns:
            Dict[str, Any]: Comprehensive learning results.
        """
        results = {
            'total_iterations': self.current_iteration,
            'best_performance': self.best_performance,
            'iteration_history': self.iteration_history
        }
        
        self.logger.info(f"Learning process completed. Results: {results}")
        return results
    
    def reset(self) -> None:
        """
        Reset the learning loop to its initial state.
        """
        self.current_iteration = 0
        self.best_performance = float('-inf')
        self.iteration_history.clear()