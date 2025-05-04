# TradePoint Momentum Tax - Requirements Document

## 1. Introduction

### 1.1 Purpose
This document outlines the requirements for the TradePoint Momentum Tax system, a portfolio management application that tracks stock trades, calculates profits and losses, and applies appropriate tax calculations based on Indian tax regulations.

### 1.2 Scope
The system will manage a stock portfolio, process monthly trades, track investments, calculate taxes, and generate detailed reports. It is designed specifically for momentum trading strategies with monthly rebalancing.

### 1.3 Definitions and Acronyms
- **ST**: Short-term (trades held for less than 1 year)
- **LT**: Long-term (trades held for 1 year or more)
- **PNL**: Profit and Loss
- **Corpus**: Total available capital for investment

## 2. System Overview

### 2.1 System Description
TradePoint Momentum Tax is a portfolio management system that processes stock trades from a CSV input file, tracks investments, calculates profits and losses, and applies tax calculations based on whether trades are short-term or long-term. The system maintains an available corpus, which gets redistributed among stocks as they enter and exit the portfolio.

### 2.2 Target Users
- Individual investors following momentum trading strategies
- Financial advisors managing client portfolios
- Tax professionals calculating capital gains taxes

### 2.3 System Context
The system operates independently, reading input data from CSV files and generating output files with detailed trade and tax information.

## 3. Functional Requirements

### 3.1 Portfolio Initialization
- **FR-1.1**: The system shall initialize with a configurable initial capital (X) rupees.
- **FR-1.2**: The initial capital shall be divided equally among a maximum of N stocks.
- **FR-1.3**: Both X and N shall be configurable via a configuration file.
- **FR-1.4**: Default value for X shall be 2,000,000 rupees if not specified.
- **FR-1.5**: Default value for N shall be 20 stocks if not specified.

### 3.2 Data Input
- **FR-2.1**: The system shall read trade data from CSV files.
- **FR-2.2**: Input CSV files shall contain columns for stock name, entry price, exit price, entry date, exit date, and other information.
- **FR-2.3**: The system shall only use stock name, entry price, exit price, entry date, and exit date columns from the input files.
- **FR-2.4**: The system shall parse date values in DD-MMM-YY format (e.g., "01-Nov-01").
- **FR-2.5**: The system shall stop reading the input file upon encountering a blank line.
- **FR-2.6**: The system shall ignore any content in the input file that appears after the first blank line.

### 3.3 Trade Processing
- **FR-3.1**: The system shall process trades chronologically.
- **FR-3.2**: For a given date, the system shall process all exits before entries.
- **FR-3.3**: The system shall maintain a "Corpus available" value starting with the initial capital X.
- **FR-3.4**: After each buy, the system shall subtract the amount invested from the corpus available.
- **FR-3.5**: The system shall track the amount invested in each stock.
- **FR-3.6**: The system shall compute the quantity bought for each stock using the entry price.
- **FR-3.7**: Stock quantities shall always be integers, rounded down.
- **FR-3.8**: The system shall compute the PNL for each stock using the exit price.
- **FR-3.9**: The system shall categorize trades as long-term if the exit date is at least one year after the entry date.
- **FR-3.10**: The system shall categorize trades as short-term if the exit date is less than one year after the entry date.

### 3.4 Tax Calculation
- **FR-4.1**: For each exit date, the system shall compute:
  - The sum of all losses (todays_loss)
  - The sum of all short-term profits (todays_st_profit)
  - The sum of all long-term profits (todays_lt_profit)
- **FR-4.2**: The system shall apply tax calculations as follows:
  - If todays_st_profit - todays_loss > 0, then:
    net_post_tax_pnl = (todays_st_profit - todays_loss) * 0.8 + todays_lt_profit * 0.9
  - If todays_st_profit - todays_loss = 0, then:
    net_post_tax_pnl = todays_lt_profit * 0.9
  - If todays_st_profit - todays_loss < 0, then:
    - If todays_loss > todays_st_profit + todays_lt_profit:
      net_post_tax_pnl = todays_loss - todays_lt_profit - todays_st_profit
    - Else:
      net_post_tax_pnl = (todays_lt_profit - (todays_loss - todays_st_profit)) * 0.9
- **FR-4.3**: After exits, the system shall update the corpus as:
  Corpus available = Corpus available + sum(amount invested in exited stocks) + net_post_tax_pnl

### 3.5 Portfolio Rebalancing
- **FR-5.1**: After processing exits and updating the corpus, the system shall calculate the new amount to be invested in each stock as: Corpus available / N
- **FR-5.2**: The system shall allocate this amount to each new stock entry.

### 3.6 Output Generation
- **FR-6.1**: The system shall create output files in CSV format.
- **FR-6.2**: Output files shall be placed in the "output" directory.
- **FR-6.3**: Output filenames shall be prefixed with "tax-" followed by the input filename.
- **FR-6.4**: Output files shall contain the following columns:
  - Stock Name
  - Entry date
  - Entry price
  - Entry Amount
  - Quantity
  - Exit date
  - Exit price
  - Exit amount
  - PNL
  - ST/LT (indicating whether the trade was short-term or long-term)
  - Tax
  - Corpus available

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-1.1**: The system shall handle input files containing thousands of trades efficiently.
- **NFR-1.2**: Processing time should be reasonable for large datasets.

### 4.2 Accuracy
- **NFR-2.1**: All monetary calculations shall use appropriate decimal precision to avoid floating-point errors.
- **NFR-2.2**: All decimal calculations shall be rounded to two decimal places.
- **NFR-2.3**: Quantity calculations shall always round down to integers.

### 4.3 Usability
- **NFR-3.1**: The system shall provide clear error messages for invalid input data.
- **NFR-3.2**: The system shall create well-formatted output files that are easy to analyze.

### 4.4 Reliability
- **NFR-4.1**: The system shall validate input data and report any inconsistencies.
- **NFR-4.2**: The system shall handle edge cases gracefully.
- **NFR-4.3**: The system shall detect and report if there are more than N stocks in the initial dataset.

### 4.5 Maintainability
- **NFR-5.1**: The code shall be well-structured and documented.
- **NFR-5.2**: The system shall use a modular architecture for easy maintenance.
- **NFR-5.3**: The system shall include comprehensive tests.

## 5. System Constraints

### 5.1 Technical Constraints
- **SC-1.1**: The system shall be implemented in Python 3.9 or higher.
- **SC-1.2**: The system shall use pandas for data manipulation.
- **SC-1.3**: The system shall use decimal.Decimal for financial calculations.

### 5.2 Business Constraints
- **SC-2.1**: The tax calculations shall comply with the specified rules for short-term and long-term capital gains.
- **SC-2.2**: The system shall not need to account for stock splits or dividends.

## 6. Assumptions and Dependencies

### 6.1 Assumptions
- **AS-1.1**: Input CSV files will be properly formatted with the required columns.
- **AS-1.2**: The date format in input files will be DD-MMM-YY.
- **AS-1.3**: All trades will have both entry and exit information.
- **AS-1.4**: Input files may contain additional information after a blank line, which should be ignored.

### 6.2 Dependencies
- **DP-1.1**: Availability of pandas library for CSV processing.
- **DP-1.2**: Access to input and output directories for file operations.

## 7. Acceptance Criteria

The system will be considered complete when:

1. It correctly reads trade data from CSV input files and stops at the first blank line.
2. It accurately processes trades, tracking corpus and investments.
3. It correctly categorizes trades as short-term or long-term.
4. It applies the tax calculation rules correctly.
5. It generates properly formatted output files with all required information.
6. It handles configuration parameters correctly.
7. It provides appropriate error handling and reporting.
8. It passes all tests with sample data provided. 