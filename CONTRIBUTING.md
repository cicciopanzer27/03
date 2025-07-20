# 🤝 Contributing to M.I.A. Consciousness Research System

Thank you for your interest in contributing to M.I.A.! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Workflow](#contribution-workflow)
- [Code Guidelines](#code-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)
- [Code of Conduct](#code-of-conduct)

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.8+ (3.10+ recommended)
- **Git**: Latest version
- **Ollama**: For local AI model support
- **Node.js**: 16+ (for web interface development)

### Areas for Contribution

We welcome contributions in several areas:

#### 🧠 **Core Research**
- New consciousness research protocols
- Enhanced analysis algorithms
- Academic methodology improvements
- Citation and reference management

#### 🔌 **Integrations**
- MCP server implementations
- A2A agent development
- Database connectors
- External API integrations

#### 🌐 **Web Interface** (Priority for Jules)
- React/Vue.js frontend development
- FastAPI backend enhancement
- Real-time dashboard features
- User experience improvements

#### 📱 **Mobile & Desktop**
- Mobile companion app
- Desktop GUI applications
- Cross-platform compatibility
- Accessibility features

#### 🧪 **Testing & Quality**
- Test coverage improvements
- Performance optimization
- Bug fixes and stability
- Documentation updates

## 🛠 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/yourusername/mia-consciousness-system.git
cd mia-consciousness-system

# Add upstream remote
git remote add upstream https://github.com/original/mia-consciousness-system.git
```

### 2. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .
```

### 3. Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files (optional)
pre-commit run --all-files
```

### 4. Ollama Setup (for core development)

```bash
# Install Ollama (visit https://ollama.ai)
# Download recommended models
ollama pull llama3.2:3b
ollama pull llama3.2:1b
ollama pull mistral:7b
```

### 5. Verify Setup

```bash
# Run basic tests
python -m pytest tests/test_core_functionality.py -v

# Check system readiness
python test_everything_mia.py
```

## 🔄 Contribution Workflow

### 1. Create Feature Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Development Cycle

```bash
# Make changes
# Run tests frequently
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_your_feature.py -v

# Check code quality
flake8 src/
black src/
mypy src/
```

### 3. Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Feature additions
git commit -m "feat(mcp): add ArXiv server implementation"

# Bug fixes
git commit -m "fix(core): resolve timeout issues in research protocols"

# Documentation
git commit -m "docs(readme): update MCP integration examples"

# Tests
git commit -m "test(a2a): add workflow execution tests"

# Performance improvements
git commit -m "perf(vector): optimize ChromaDB queries"
```

#### Commit Types
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `test`: Test additions/modifications
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `style`: Code style changes
- `build`: Build system changes
- `ci`: CI/CD changes

### 4. Pull Request Process

```bash
# Push feature branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Include:
# - Clear description of changes
# - Link to related issues
# - Screenshots (for UI changes)
# - Test results
```

#### PR Template

Your PR should include:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly hard-to-understand areas
- [ ] Documentation updated
- [ ] Tests added for new functionality
```

## 📝 Code Guidelines

### Python Code Style

We follow **PEP 8** with these extensions:

```python
# Use type hints
def process_research_data(
    data: List[Dict[str, Any]], 
    config: ResearchConfig
) -> ResearchResult:
    """Process research data according to configuration."""
    pass

# Use docstrings
def analyze_consciousness_theory(theory: str) -> Dict[str, float]:
    """
    Analyze a consciousness theory using multi-agent approach.
    
    Args:
        theory: The consciousness theory to analyze
        
    Returns:
        Dictionary containing analysis results with confidence scores
        
    Raises:
        AnalysisError: If theory cannot be processed
    """
    pass

# Error handling
try:
    result = process_complex_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise ProcessingError(f"Failed to process: {e}") from e
```

### Code Organization

```
src/mia_consciousness/
├── __init__.py              # Main exports
├── core/                    # Core functionality
│   ├── research.py         # Main research engine
│   ├── protocols.py        # Research protocols
│   └── config.py          # Configuration management
├── integrations/           # External integrations
│   ├── mcp_integration.py  # MCP protocol
│   ├── a2a_integration.py  # A2A protocol
│   └── vector_database.py  # Vector databases
├── output/                 # Output generation
│   ├── formatters.py      # Output formatters
│   └── templates/         # Report templates
└── utils/                 # Utility functions
    ├── logging.py         # Logging configuration
    └── helpers.py         # Helper functions
```

### Async Code Guidelines

```python
# Use async/await consistently
async def fetch_research_papers(query: str) -> List[Paper]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/search?q={query}")
        return parse_papers(response.json())

# Context managers for resources
async def research_with_mcp():
    async with MCPManager() as (mcp, connections):
        results = await mcp.search_consciousness_papers("neural correlates")
        return results
```

### Error Handling

```python
# Custom exceptions
class MIAError(Exception):
    """Base exception for M.I.A. system."""
    pass

class ResearchProtocolError(MIAError):
    """Raised when research protocol execution fails."""
    pass

# Proper error handling
def execute_research_protocol(protocol: ResearchProtocol) -> ResearchResult:
    try:
        validate_protocol(protocol)
        return _execute_protocol_internal(protocol)
    except ValidationError as e:
        logger.error(f"Protocol validation failed: {e}")
        raise ResearchProtocolError(f"Invalid protocol: {e}") from e
    except Exception as e:
        logger.exception("Unexpected error in protocol execution")
        raise ResearchProtocolError(f"Execution failed: {e}") from e
```

## 🧪 Testing

### Test Structure

```
tests/
├── test_core/                    # Core functionality tests
│   ├── test_research_engine.py
│   └── test_protocols.py
├── test_integrations/           # Integration tests
│   ├── test_mcp_integration.py
│   └── test_a2a_integration.py
├── test_output/                # Output generation tests
├── fixtures/                   # Test data and fixtures
└── conftest.py                # Pytest configuration
```

### Test Categories

#### Unit Tests
```python
import pytest
from unittest.mock import Mock, patch
from mia_consciousness import ConsciousnessResearcher

def test_researcher_initialization():
    """Test that researcher initializes correctly."""
    config = Mock()
    researcher = ConsciousnessResearcher(config)
    assert researcher.config == config

@patch('mia_consciousness.ollama_client')
def test_research_protocol_execution(mock_ollama):
    """Test research protocol execution."""
    mock_ollama.chat.return_value = {"message": {"content": "test result"}}
    # Test implementation
    pass
```

#### Integration Tests
```python
@pytest.mark.integration
async def test_mcp_a2a_pipeline():
    """Test complete MCP + A2A pipeline."""
    async with MCPManager() as (mcp, _):
        papers = await mcp.search_consciousness_papers("test query")
        assert len(papers) >= 0  # Mock may return empty list
```

#### Performance Tests
```python
@pytest.mark.performance
def test_research_protocol_performance():
    """Test that research completes within acceptable time."""
    import time
    start = time.time()
    result = execute_research_protocol(simple_protocol)
    duration = time.time() - start
    assert duration < 300  # 5 minutes max
```

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific category
python -m pytest tests/ -m "not integration" -v  # Skip slow integration tests
python -m pytest tests/ -m "integration" -v      # Only integration tests

# With coverage
python -m pytest tests/ --cov=src/mia_consciousness --cov-report=html

# Parallel execution
python -m pytest tests/ -n auto
```

### Test Requirements

- **Coverage**: Aim for >90% code coverage
- **Speed**: Unit tests should run quickly (<1s each)
- **Isolation**: Tests should not depend on external services
- **Mocking**: Mock external dependencies appropriately
- **Documentation**: Test names should be descriptive

## 📚 Documentation

### Code Documentation

```python
def analyze_consciousness_data(
    data: List[ConsciousnessData],
    method: AnalysisMethod = AnalysisMethod.INTEGRATED,
    confidence_threshold: float = 0.7
) -> AnalysisResult:
    """
    Analyze consciousness research data using specified method.
    
    This function processes consciousness research data through multiple
    analysis pipelines and returns comprehensive results with confidence
    scores and methodological assessments.
    
    Args:
        data: List of consciousness data objects to analyze
        method: Analysis method to use (default: INTEGRATED)
        confidence_threshold: Minimum confidence for including results (0.0-1.0)
        
    Returns:
        AnalysisResult containing:
            - analysis_summary: Dict with key findings
            - confidence_scores: Dict mapping metrics to confidence values
            - methodology_assessment: Evaluation of methods used
            - recommendations: List of suggested next steps
            
    Raises:
        ValueError: If confidence_threshold is not between 0.0 and 1.0
        AnalysisError: If analysis cannot be completed
        
    Example:
        >>> data = load_consciousness_data("neural_correlates.json")
        >>> result = analyze_consciousness_data(data, confidence_threshold=0.8)
        >>> print(f"Analysis confidence: {result.confidence_scores['overall']}")
        
    Note:
        This function may take several minutes for large datasets.
        Consider using async version for better performance.
    """
    pass
```

### README Updates

When adding features, update the README:

```markdown
# Add to features list
- ✅ **Your New Feature**: Brief description of what it does

# Add to usage examples
### Your Feature Usage
```python
from mia_consciousness import YourNewFeature
feature = YourNewFeature(config)
result = feature.execute()
```

# Update installation if new dependencies
```bash
pip install new-dependency
```
```

### API Documentation

We use **Sphinx** for API documentation:

```bash
# Generate docs
cd docs/
make html

# View docs
open _build/html/index.html
```

## 🐛 Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Windows 11, macOS 14, Ubuntu 22.04]
- Python version: [e.g. 3.10.5]
- M.I.A version: [e.g. 2.0.0]
- Ollama version: [e.g. 0.9.3]

**Additional Context**
- Log files (if applicable)
- Screenshots (if applicable)
- Configuration files (sanitized)
```

### Performance Issues

```markdown
**Performance Issue Description**
What operation is slower than expected?

**Current Performance**
- Time taken: X minutes/seconds
- Memory usage: X GB
- CPU usage: X%

**Expected Performance**
- Expected time: X minutes/seconds
- System specs: RAM, CPU, etc.

**Environment**
- Hardware specs
- System resources available
- Concurrent operations
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How do you envision this working?

**Alternative Solutions**
Any alternative approaches considered?

**Additional Context**
- Priority level (High/Medium/Low)
- Willing to implement? (Yes/No)
- Related issues or features
```

### Research-Specific Features

For consciousness research features:

```markdown
**Research Context**
- Which consciousness theory does this support?
- Academic references or papers
- Methodological approach

**Scientific Validation**
- How can results be validated?
- What metrics should be used?
- Peer review considerations
```

## 🤝 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. Please read our full [Code of Conduct](CODE_OF_CONDUCT.md).

**In summary:**
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow academic and scientific ethics
- Respect privacy and confidentiality of research

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests, technical discussions
- **GitHub Discussions**: General questions, showcases, community chat
- **Discord** (Coming Soon): Real-time chat and collaboration
- **Email**: For security issues or private matters

### Recognition

Contributors are recognized in several ways:

- **README Contributors Section**: All contributors listed
- **Changelog**: Feature contributors mentioned in releases
- **Academic Papers**: Code contributors acknowledged in research publications
- **Conference Presentations**: Community contributions highlighted

## 🏆 Special Projects for Contributors

### Priority Projects (Great for Getting Started)

#### 🌐 Web Interface (Perfect for Jules)
- **Tech Stack**: React/Vue.js + FastAPI
- **Difficulty**: Intermediate
- **Impact**: High
- **Timeline**: 4-6 weeks
- **Skills Learned**: Full-stack development, WebSocket real-time updates

#### 📱 Mobile App
- **Tech Stack**: React Native or Flutter
- **Difficulty**: Intermediate-Advanced
- **Impact**: High
- **Timeline**: 6-8 weeks
- **Skills Learned**: Mobile development, offline capabilities

#### 🔧 DevOps & Deployment
- **Tech Stack**: Docker, Kubernetes, AWS/GCP/Azure
- **Difficulty**: Advanced
- **Impact**: Medium-High
- **Timeline**: 2-4 weeks
- **Skills Learned**: Container orchestration, cloud deployment

#### 🧠 Advanced Research Features
- **Tech Stack**: Python, NumPy, SciPy, NetworkX
- **Difficulty**: Advanced
- **Impact**: Very High
- **Timeline**: 4-8 weeks
- **Skills Learned**: Academic research methods, consciousness science

### Research Collaboration Opportunities

- **Academic Partnerships**: Collaborate with university research teams
- **Paper Publications**: Co-author academic papers using M.I.A. results
- **Conference Presentations**: Present M.I.A. features at consciousness research conferences
- **Grant Applications**: Contribute to research grant applications

## 📞 Getting Help

### For New Contributors

- **Start Here**: Check out `good-first-issue` labeled issues
- **Mentorship**: Experienced contributors available for guidance
- **Documentation**: Comprehensive guides and API reference
- **Pair Programming**: Available for complex features

### Technical Support

- **Setup Issues**: Detailed troubleshooting in documentation
- **API Questions**: Examples and tutorials available
- **Performance**: Optimization guides and benchmarking tools
- **Architecture**: System design documents and diagrams

### Research Support

- **Consciousness Science**: Academic advisors available for consultation
- **Methodology**: Guidance on scientific rigor and validation
- **Ethics**: Research ethics and privacy considerations
- **Publication**: Support for academic writing and publication

---

## 🚀 Ready to Contribute?

1. **Choose an Area**: Pick something that interests you
2. **Start Small**: Begin with documentation or small bug fixes
3. **Ask Questions**: Don't hesitate to ask for help
4. **Have Fun**: Enjoy contributing to cutting-edge consciousness research!

**Welcome to the M.I.A. development community!** 🧠✨

---

**Last Updated**: December 20, 2024  
**Maintainers**: M.I.A. Development Team  
**Community Manager**: [To be assigned]