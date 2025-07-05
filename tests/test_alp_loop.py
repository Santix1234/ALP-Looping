import pytest
import logging
from src.alp_loop import AdaptiveLearningProcessLoop, LoopStatus, LoopMetrics

class ConcreteALPLoop(AdaptiveLearningProcessLoop):
    def __init__(self, max_iterations=5):
        super().__init__(max_iterations)
        self.initialization_called = False
        self.iteration_count = 0
    
    def _initialize(self):
        self.initialization_called = True
    
    def _iteration(self):
        self.iteration_count += 1
        return self.iteration_count < self._max_iterations

def test_alp_loop_initialization():
    loop = ConcreteALPLoop()
    assert loop._status == LoopStatus.INITIALIZED
    assert isinstance(loop._logger, logging.Logger)

def test_alp_loop_run():
    loop = ConcreteALPLoop()
    metrics = loop.run()
    
    assert loop._status == LoopStatus.FAILED
    assert metrics.iterations == 4  # 0-indexed iterations
    assert loop.initialization_called is True
    assert isinstance(metrics, LoopMetrics)

def test_alp_loop_pause_resume():
    loop = ConcreteALPLoop(max_iterations=10)
    assert loop._status == LoopStatus.INITIALIZED
    
    loop.pause()
    assert loop._status == LoopStatus.PAUSED

def test_alp_loop_max_iterations():
    loop = ConcreteALPLoop(max_iterations=3)
    metrics = loop.run()
    
    assert metrics.iterations == 3  # 0-indexed iterations
    assert loop._status == LoopStatus.FAILED

def test_alp_loop_logging():
    loop = ConcreteALPLoop()
    assert isinstance(loop._logger, logging.Logger)
    assert loop._logger.level == logging.INFO