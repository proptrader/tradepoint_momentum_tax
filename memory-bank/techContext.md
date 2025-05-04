# TradePoint Momentum Tax - Technical Context

## Technologies Used

### Core Technology Stack
- **Python 3.9+**: Primary programming language
- **pandas**: For efficient data manipulation and CSV handling
- **datetime**: For date parsing and calculations
- **pathlib**: For cross-platform file path handling
- **decimal**: For precise financial calculations

### Development Tools
- **pytest**: For unit and integration testing
- **black**: For code formatting
- **flake8**: For linting
- **mypy**: For static type checking

## Development Setup

### Requirements
- Python 3.9 or higher
- pip for package management
- Virtual environment (recommended)

### Installation
```bash
# Clone the repository
git clone https://github.com/username/tradepoint_momentum_tax.git
cd tradepoint_momentum_tax

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Project Structure
```
tradepoint_momentum_tax/
├── input/                    # Directory for input CSV files
├── output/                   # Directory for generated output files
├── src/
│   ├── __init__.py
│   ├── main.py               # Entry point
│   ├── data_ingestion.py     # CSV reading and parsing
│   ├── portfolio.py          # Portfolio management
│   ├── tax_calculator.py     # Tax calculation logic
│   ├── trade_processor.py    # Trade processing
│   └── output_generator.py   # Output file generation
├── tests/
│   ├── __init__.py
│   ├── test_data_ingestion.py
│   ├── test_portfolio.py
│   ├── test_tax_calculator.py
│   └── test_trade_processor.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Technical Constraints

### Performance Considerations
- The system should be efficient enough to handle large CSV files (thousands of trades)
- Memory usage should be optimized for processing large datasets
- Performance is secondary to accuracy in financial calculations

### Financial Calculation Precision
- All monetary calculations must use decimal.Decimal to avoid floating-point errors
- Rounding must follow the specified rules (round to 2 decimal places)
- Quantity calculations must always round down to integers

### Error Handling Requirements
- The system must validate input data and report errors clearly
- Missing or malformed data should be handled gracefully
- Calculation errors should be logged with sufficient context for debugging

### Testing Requirements
- Unit tests must cover all critical calculation paths
- Integration tests must verify end-to-end functionality
- Test cases should include edge cases in tax calculation

## Dependencies

### Core Dependencies
```
pandas>=1.5.0
pytest>=7.0.0
black>=22.3.0
flake8>=5.0.0
mypy>=0.960
```

### Rationale for Key Dependencies
- **pandas**: Chosen for its powerful DataFrame capabilities, making CSV handling and data manipulation straightforward
- **pytest**: Selected for its simple syntax and powerful fixture system
- **decimal**: Used for precise financial calculations to avoid floating-point errors

## Deployment Considerations

### Environment Variables
- `INITIAL_CAPITAL`: The starting capital amount (X)
- `MAX_STOCKS`: Maximum number of stocks in the portfolio (N)

### Development vs. Production
- Development: Uses smaller test datasets and verbose logging
- Production: Optimized for larger datasets with minimal logging

### Logging
- Development: DEBUG level, showing all calculation steps
- Production: INFO level, showing only significant events and errors

## Testing Strategy
- Unit tests for individual components
- Integration tests for end-to-end flows
- Specific test cases for tax calculation edge cases
- Performance tests for large datasets 