# TradePoint Momentum Tax - Project Brief

## Overview
TradePoint Momentum Tax is a system that manages a portfolio of stocks with a focus on calculating taxes correctly based on Indian tax regulations for short-term and long-term capital gains. The system manages the corpus of available funds, allocates investments, tracks trades, and applies the appropriate tax calculations.

## Core Requirements

### Stock Portfolio Management
- The portfolio starts with an initial capital of 'X' rupees
- The capital is divided equally among a maximum of 'N' stocks
- Both X and N are configurable parameters
- Trades occur monthly, with stocks entering and exiting the portfolio
- For a given date, exits are processed before entries

### Data Processing
- Input data comes in CSV format with specified columns
- Only stock name, entry price, exit price, entry date, and exit date are relevant
- All calculations with decimals should be rounded to two decimal places

### Corpus Management
- A "Corpus available" field tracks the available capital
- Initial amount is divided equally among N stocks
- After each buy, the invested amount is subtracted from the corpus
- When stocks exit, their value (plus/minus profit/loss) returns to the corpus

### Trade Handling
- Quantity calculations must be integers (round down)
- Profit and Loss (PNL) is calculated for each trade
- Trades are categorized as short-term (< 1 year) or long-term (≥ 1 year)

### Tax Calculation
For each exit date:
1. Calculate total losses (`todays_loss`)
2. Calculate total short-term profits (`todays_st_profit`)
3. Calculate total long-term profits (`todays_lt_profit`)
4. Apply tax calculation formula based on relationship between profits and losses
5. Update corpus with post-tax values

### Output
- Generate CSV output with specified columns
- Follow naming convention of "tax-{input_filename}.csv"
- Place output files in the "output" directory

## Technical Constraints
- The system must handle various edge cases in the input data
- Calculations must be precise and follow Indian tax regulations
- The implementation should be maintainable and well-documented 