import pytest
from src.alp_loop import ALPLoopBase, LoopConfiguration

class TestALPLoop(ALPLoopBase):
    def initialize(self):
        self.test_data = [1, 2, 3, 4, 5]
    
    def learning_iteration(self):
        # Simulate a learning process that increases performance
        return self.current_iteration * 0.1

def test_alp_loop_initialization():
    default_config = LoopConfiguration()
    loop = TestALPLoop()
    
    assert loop.config.max_iterations == 100
    assert loop.config.learning_rate == 0.01
    assert loop.current_iteration == 0

def test_custom_configuration():
    custom_config = LoopConfiguration(
        max_iterations=50,
        learning_rate=0.05,
        convergence_threshold=1e-3
    )
    loop = TestALPLoop(custom_config)
    
    assert loop.config.max_iterations == 50
    assert loop.config.learning_rate == 0.05
    assert loop.config.convergence_threshold == 1e-3

def test_loop_run():
    loop = TestALPLoop()
    results = loop.run()
    
    assert 'total_iterations' in results
    assert 'best_performance' in results
    assert 'iteration_history' in results
    assert results['total_iterations'] <= 100
    assert len(results['iteration_history']) > 0

def test_loop_reset():
    loop = TestALPLoop()
    loop.run()
    loop.reset()
    
    assert loop.current_iteration == 0
    assert loop.best_performance == float('-inf')
    assert len(loop.iteration_history) == 0

def test_early_stopping_config():
    config = LoopConfiguration(early_stopping=False)
    loop = TestALPLoop(config)
    results = loop.run()
    
    assert results['total_iterations'] == 100