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
5. Implemented the core system functionality for processing trades and generating tax outputs
6. Added a new feature to generate monthly profit summary reports showing profit after tax by month and year
7. Received clarifications from the user:
   - Sample data format has been provided and is sufficient
   - Configuration values should be read from a config file:
     - Initial capital (X) default: 2,000,000 rupees
     - Maximum stocks (N) default: 20
   - The system should flag errors for cases where there are more than N stocks
   - No need to adjust for stock splits or dividends
   - Input file processing should stop at the first blank line, ignoring any content after it
   - Monthly profit summary should aggregate profit after tax (PNL - Tax) by month and year

## Next Steps

1. Test the new monthly profit summary feature
2. Implement additional error handling for the summary report generation
3. Add unit tests for the new functionality
4. Explore potential visualizations of the monthly profit data
5. Expand the documentation with examples of the new summary reports
6. Enhance the system with additional reporting capabilities
7. Improve performance for large datasets

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