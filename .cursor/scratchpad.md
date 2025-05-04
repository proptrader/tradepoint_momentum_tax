# Stock Portfolio Management System with Tax Calculations

## Background and Motivation
We need to build a system that manages a portfolio of stocks, tracks trades, calculates profit and loss, and applies tax calculations based on whether trades are short-term or long-term. The system needs to maintain a corpus of available funds, which gets distributed among stocks as they enter the portfolio. When stocks exit, their value (plus or minus profit/loss) returns to the corpus, with appropriate tax considerations.

## Key Challenges and Analysis
1. **Data Processing**: Read and parse CSV input files containing trade data, stopping at the first blank line.
2. **Date-based Trade Ordering**: Process trades chronologically, handling exits before entries on the same date.
3. **Fund Allocation**: Manage the available corpus, tracking investments in each stock.
4. **Tax Calculation**: Implement a complex tax calculation logic based on short-term vs long-term trades, losses, and profits.
5. **Portfolio Tracking**: Track the portfolio composition over time.
6. **Configuration Management**: Read X (initial capital) and N (max stocks) from a configuration file with defaults.
7. **Error Handling**: Flag errors for invalid scenarios like having more than N stocks.

## High-level Task Breakdown

1. **Project Setup**
   - Create a basic directory structure (input, output folders)
   - Set up the main application file
   - Create configuration file structure with defaults (X=2,000,000, N=20)
   - Define data models and classes
   - Success criteria: Directory structure created and basic application skeleton in place

2. **Input Data Processing**
   - Implement CSV parsing
   - Extract relevant columns (stock name, entry price, exit price, entry date, exit date)
   - Implement logic to stop reading at the first blank line
   - Sort trades by date for proper processing
   - Handle date format (DD-MMM-YY)
   - Success criteria: Ability to correctly parse input files and organize trade data chronologically

3. **Portfolio Management Logic**
   - Implement logic to track available corpus
   - Calculate stock quantities based on allocated funds
   - Track investment amount per stock
   - Success criteria: Correctly calculate portfolio allocation and track investments

4. **Trade Processing Logic**
   - Implement exit processing logic
   - Implement entry processing logic
   - Ensure exits are processed before entries on the same date
   - Success criteria: Trades are processed in the correct order with appropriate corpus updates

5. **Profit/Loss and Tax Calculation**
   - Identify short-term vs long-term trades
   - Calculate raw profit/loss for each trade
   - Implement the tax calculation logic based on specifications
   - Success criteria: Correct tax calculations as per the formula provided

6. **Output Generation**
   - Create formatted CSV output with required columns
   - Ensure proper naming convention (tax-{input_filename})
   - Success criteria: Properly formatted output files with all required columns

7. **Testing and Validation**
   - Test with sample data
   - Verify calculations match expected outcomes
   - Success criteria: System produces correct results for test cases

## Project Status Board
- [x] Requirements Documentation
- [ ] Project Setup
- [ ] Input Data Processing
- [ ] Portfolio Management Logic
- [ ] Trade Processing Logic
- [ ] Profit/Loss and Tax Calculation
- [ ] Output Generation
- [ ] Testing and Validation

## Executor's Feedback or Assistance Requests
We have completed the comprehensive requirements documentation as requested. The document includes:
- Detailed functional requirements
- Non-functional requirements
- System constraints
- Assumptions and dependencies
- Acceptance criteria

We've updated the requirements to include handling of blank lines in the input file - the system should stop reading upon encountering the first blank line and ignore any content after it.

We are waiting for approval to begin implementation.

## Lessons
- Include corpus calculations and tax logic in debug output for easier verification
- Round decimal calculations to two places as specified in the requirements
- Ensure quantity calculations always round down to integers
- Configuration values (X=2,000,000, N=20) should be read from a config file with defaults
- Flag errors for invalid scenarios like having more than N stocks
- Stop reading the input file at the first blank line 