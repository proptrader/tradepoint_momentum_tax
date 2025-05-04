# TradePoint Momentum Tax - Active Context

## Current Work Focus

The current focus is on requirements documentation and architecture definition. We are in the planning phase, establishing the overall structure of the application and defining the key components based on user clarifications.

### Primary Goals
1. Create a comprehensive requirements document
2. Define the overall architecture and component interactions
3. Set up the project structure
4. Implement the core data models

## Recent Changes

No implementation has been done yet. We have established the following:

1. Created the memory bank infrastructure
2. Defined the project requirements and architecture
3. Planned the system components and their interactions
4. Outlined the data flow and processing approach
5. Received clarifications from the user:
   - Sample data format has been provided and is sufficient
   - Configuration values should be read from a config file:
     - Initial capital (X) default: 2,000,000 rupees
     - Maximum stocks (N) default: 20
   - The system should flag errors for cases where there are more than N stocks
   - No need to adjust for stock splits or dividends
   - Input file processing should stop at the first blank line, ignoring any content after it

## Next Steps

1. Create a comprehensive requirements document

2. Set up the basic project structure
   - Create input and output directories
   - Set up the src directory with initial Python files
   - Create configuration file handling

3. Implement core data models
   - Define Trade class
   - Implement Portfolio class
   - Create Corpus management class

4. Develop data ingestion
   - CSV parsing
   - Implement logic to stop reading at the first blank line
   - Date handling (DD-MMM-YY format)
   - Data validation

5. Implement trade processing logic
   - Exit handling
   - Entry handling
   - Portfolio rebalancing

6. Create tax calculation logic
   - Short-term vs long-term classification
   - Loss and profit aggregation
   - Tax formula implementation

7. Build output generation
   - CSV formatting
   - File naming convention

## Active Decisions and Considerations

### Architecture Decisions
- Using a modular approach with clear separation of concerns
- Focusing on maintainability and readability over performance optimization
- Using pandas for data manipulation to simplify CSV handling
- Configuration values to be stored in a config file
- Input file parsing should stop at the first blank line

### Tax Calculation Clarifications
- Short-term trades: Exit date < Entry date + 1 year
- Long-term trades: Exit date ≥ Entry date + 1 year
- Tax rates: 20% for short-term profits, 10% for long-term profits

### Implementation Strategy
- Develop and test each component separately
- Use test-driven development
- Create comprehensive unit tests for tax calculation logic
- Implement detailed logging for debugging

### Open Questions
- Format of the configuration file (JSON, YAML, INI, etc.)
- Specific error handling and reporting mechanisms
- Logging requirements and level of detail 