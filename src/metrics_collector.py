from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
import time
import logging

class MetricType(Enum):
    """Enum representing different types of metrics."""
    PERFORMANCE = auto()
    RESOURCE_USAGE = auto()
    ERROR_RATE = auto()
    LEARNING_PROGRESS = auto()

@dataclass
class MetricRecord:
    """Represents a single metric record with timestamp and value."""
    value: Any
    timestamp: float = field(default_factory=time.time)
    type: MetricType = MetricType.PERFORMANCE

class PerformanceMetricsCollector:
    """
    A lightweight, thread-safe metrics collection system for tracking 
    performance characteristics of the Adaptive Learning Process.
    
    Supports multiple metric types, basic statistical tracking, 
    and configurable logging.
    """
    
    def __init__(self, max_history: int = 100, logger: Optional[logging.Logger] = None):
        """
        Initialize the metrics collector.
        
        Args:
            max_history (int): Maximum number of historical records to keep per metric.
            logger (Optional[logging.Logger]): Optional logger for recording metrics.
        """
        self._metrics: Dict[str, list[MetricRecord]] = {}
        self._max_history = max_history
        self._logger = logger or logging.getLogger(__name__)
    
    def record_metric(self, name: str, value: Any, metric_type: MetricType = MetricType.PERFORMANCE):
        """
        Record a new metric value.
        
        Args:
            name (str): Name of the metric.
            value (Any): Value of the metric.
            metric_type (MetricType): Type of metric being recorded.
        """
        metric_record = MetricRecord(value=value, type=metric_type)
        
        if name not in self._metrics:
            self._metrics[name] = []
        
        # Maintain max history
        if len(self._metrics[name]) >= self._max_history:
            self._metrics[name].pop(0)
        
        self._metrics[name].append(metric_record)
        
        # Optional logging
        self._logger.debug(f"Metric recorded: {name} = {value}")
    
    def get_metric_history(self, name: str) -> list[MetricRecord]:
        """
        Retrieve the historical records for a specific metric.
        
        Args:
            name (str): Name of the metric.
        
        Returns:
            list[MetricRecord]: Historical records for the metric.
        """
        return self._metrics.get(name, [])
    
    def get_latest_metric(self, name: str) -> Optional[MetricRecord]:
        """
        Get the most recent record for a specific metric.
        
        Args:
            name (str): Name of the metric.
        
        Returns:
            Optional[MetricRecord]: Most recent metric record, or None if not found.
        """
        history = self.get_metric_history(name)
        return history[-1] if history else None
    
    def calculate_metric_average(self, name: str) -> Optional[float]:
        """
        Calculate the average value for a given metric.
        
        Args:
            name (str): Name of the metric.
        
        Returns:
            Optional[float]: Average value of the metric, or None if no records.
        """
        history = self.get_metric_history(name)
        
        if not history:
            return None
        
        # Try to calculate average, handling potential type mismatches
        try:
            return sum(record.value for record in history) / len(history)
        except (TypeError, ValueError):
            self._logger.warning(f"Cannot calculate average for metric {name}")
            return None