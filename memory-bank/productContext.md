# TradePoint Momentum Tax - Product Context

## Why This Project Exists

The TradePoint Momentum Tax system exists to solve a critical challenge faced by investors in the Indian stock market: accurately calculating tax obligations while following a momentum-based trading strategy.

Momentum trading involves regularly entering and exiting positions based on market trends. This creates a complex tax situation due to:

1. **Different Tax Rates** - Short-term capital gains (holdings < 1 year) are taxed at a higher rate than long-term capital gains
2. **Loss Offsetting** - Losses can be offset against profits to reduce tax liability, but with specific rules
3. **Portfolio Rebalancing** - Monthly rebalancing requires precise tracking of corpus changes and reinvestment amounts

## Problems It Solves

### 1. Accurate Tax Calculation
The system applies the complex Indian tax rules correctly, handling:
- Short-term vs. long-term gains differentiation
- Loss offset against profits
- Tax rate application (20% for short-term, 10% for long-term as per requirements)

### 2. Portfolio Management
- Tracks available corpus throughout the investment period
- Handles monthly portfolio changes
- Ensures optimal allocation of capital across the portfolio

### 3. Record Keeping
- Maintains detailed records of all transactions
- Provides clear documentation for tax filing purposes
- Enables analysis of trading performance

## How It Should Work

The system follows a clear workflow:

1. **Initial Setup**:
   - User configures initial capital (X) and maximum number of stocks (N)
   - System divides capital equally among initial stock selections

2. **Monthly Trade Processing**:
   - Process all exits for the date first
   - Calculate PNL and tax implications
   - Update available corpus
   - Process all entries for the date
   - Allocate available corpus among new entries

3. **Tax Calculation**:
   - Apply the specified tax calculation rules based on:
     - Whether trades are short-term or long-term
     - The relationship between profits and losses
     - The priority of offsetting losses against short-term gains

4. **Output Generation**:
   - Create detailed records for each transaction
   - Include all required information for tax and analysis purposes

## User Experience Goals

Users of this system should be able to:

1. **Easily Input Trade Data**: Submit CSV files with their trading history
2. **Get Clear Tax Calculations**: Receive precise tax calculations for each trading period
3. **Track Performance**: Understand how their portfolio performs over time
4. **Plan Future Trades**: Have visibility into their available corpus for future investments
5. **Meet Compliance Requirements**: Generate documentation that satisfies tax authorities

This system aims to eliminate the manual effort and potential errors in tax calculation, allowing traders to focus on their momentum strategy rather than tax compliance complexities. 