import pytest

def test_project_setup():
    """Basic test to verify project setup."""
    assert True, "Project setup test passed"

def test_readme_exists():
    """Verify README.md exists and has content."""
    try:
        with open('README.md', 'r') as readme:
            content = readme.read().strip()
            assert len(content) > 0, "README.md should not be empty"
    except FileNotFoundError:
        pytest.fail("README.md file is missing")

def test_gitignore_exists():
    """Verify .gitignore exists and has content."""
    try:
        with open('.gitignore', 'r') as gitignore:
            content = gitignore.read().strip()
            assert len(content) > 0, ".gitignore should not be empty"
    except FileNotFoundError:
        pytest.fail(".gitignore file is missing")