from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum, auto
import logging

class IterationStatus(Enum):
    """Enumeration of possible iteration statuses."""
    INITIALIZED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    TERMINATED = auto()

@dataclass
class IterationState:
    """
    Manages the state and tracking of iterations in an adaptive learning process.
    
    Attributes:
        current_iteration (int): Current iteration number, starts at 0
        max_iterations (Optional[int]): Maximum number of iterations allowed
        status (IterationStatus): Current status of the iteration process
        metadata (Dict[str, Any]): Additional metadata about the iteration
    """
    current_iteration: int = 0
    max_iterations: Optional[int] = None
    status: IterationStatus = IterationStatus.INITIALIZED
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def start_iteration(self) -> bool:
        """
        Starts a new iteration if conditions are met.
        
        Returns:
            bool: True if iteration can proceed, False otherwise
        """
        # Check if max iterations is reached
        if (self.max_iterations is not None and 
            self.current_iteration >= self.max_iterations):
            self.status = IterationStatus.TERMINATED
            logging.warning(f"Maximum iterations ({self.max_iterations}) reached.")
            return False
        
        # Increment iteration count
        self.current_iteration += 1
        self.status = IterationStatus.IN_PROGRESS
        logging.info(f"Starting iteration {self.current_iteration}")
        
        return True
    
    def complete_iteration(self) -> None:
        """
        Marks the current iteration as complete.
        """
        if self.status == IterationStatus.IN_PROGRESS:
            logging.info(f"Completed iteration {self.current_iteration}")
            
            # Check if all iterations are complete
            if (self.max_iterations is not None and 
                self.current_iteration >= self.max_iterations):
                self.status = IterationStatus.COMPLETED
    
    def terminate(self, reason: Optional[str] = None) -> None:
        """
        Forcibly terminates the iteration process.
        
        Args:
            reason (Optional[str]): Optional reason for termination
        """
        self.status = IterationStatus.TERMINATED
        logging.warning(f"Iteration process terminated. Reason: {reason or 'Unspecified'}")
        
        # Store termination reason in metadata
        if reason:
            self.metadata['termination_reason'] = reason
    
    def reset(self) -> None:
        """
        Resets the iteration state to its initial configuration.
        """
        self.current_iteration = 0
        self.status = IterationStatus.INITIALIZED
        self.metadata.clear()
        logging.info("Iteration state reset")