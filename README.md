# TradePoint Momentum Tax

A system for stock portfolio management with tax calculations, specifically designed for momentum trading strategies.

## Overview

TradePoint Momentum Tax manages a portfolio of stocks, tracks trades, calculates profit and loss, and applies tax calculations based on whether trades are short-term or long-term. The system maintains a corpus of available funds, which gets distributed among stocks as they enter the portfolio. When stocks exit, their value (plus or minus profit/loss) returns to the corpus, with appropriate tax considerations.

## Features

- Manages a portfolio with configurable initial capital and maximum number of stocks
- Processes trades chronologically, handling exits before entries on the same date
- Calculates precise quantities based on allocated funds (always rounded down to integers)
- Tracks corpus updates after each trade
- Categorizes trades as short-term (<1 year) or long-term (≥1 year)
- Applies complex tax calculations based on Indian tax regulations
- Generates detailed CSV reports

## Requirements

- Python 3.9 or higher
- pandas
- python-dateutil

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/username/tradepoint_momentum_tax.git
   cd tradepoint_momentum_tax
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Simply place your input CSV file in the `input` directory and run:

```
python run.py
```

The system will automatically find the input file, process it, and generate an output file in the `output` directory.

### Command-line Options

You can customize the behavior with command-line options:

```
python run.py --input path/to/input.csv --config path/to/config.json --initial-capital 1000000 --max-stocks 15 --verbose
```

Available options:
- `--input`, `-i`: Path to the input CSV file (if not specified, will use files in the input directory)
- `--config`, `-c`: Path to the configuration file (default: config.json)
- `--initial-capital`, `-x`: Initial capital (X) in rupees (overrides config file)
- `--max-stocks`, `-n`: Maximum number of stocks (N) (overrides config file)
- `--verbose`, `-v`: Enable verbose output

## Input Format

The input file should be a CSV file with tab-separated values (TSV) containing the following columns:

```
Sr no., Stock Name, Entry Price, Exit Price, Qty, P&L, Entry Date, Exit Date, Exit Reason
```

The system only uses the following columns:
- Stock Name
- Entry Price
- Exit Price
- Entry Date (format: DD-MMM-YY, e.g., 01-Nov-01)
- Exit Date (format: DD-MMM-YY, e.g., 01-Nov-01)

The system will stop reading at the first blank line in the input file.

## Configuration

The configuration is stored in `config.json` with the following defaults:

```json
{
    "initial_capital": 2000000,
    "max_stocks": 20,
    "input_dir": "input",
    "output_dir": "output"
}
```

- `initial_capital`: Initial capital (X) in rupees
- `max_stocks`: Maximum number of stocks (N) in the portfolio
- `input_dir`: Directory for input files
- `output_dir`: Directory for output files

## Output Format

The output is a CSV file with the following columns:

```
Stock Name, Entry date, Entry price, Entry Amount, Quantity, Exit date, Exit price, Exit amount, PNL, ST/LT, Tax, Corpus available
```

The output file is saved in the `output` directory with the naming pattern `tax-{input_filename}.csv`.

## Tax Calculation Rules

The system applies the following tax calculation rules:

1. For each exit date:
   - Calculate total losses (todays_loss)
   - Calculate total short-term profits (todays_st_profit)
   - Calculate total long-term profits (todays_lt_profit)

2. Apply tax calculations:
   - If todays_st_profit - todays_loss > 0:
     net_post_tax_pnl = (todays_st_profit - todays_loss) * 0.8 + todays_lt_profit * 0.9
   - If todays_st_profit - todays_loss = 0:
     net_post_tax_pnl = todays_lt_profit * 0.9
   - If todays_st_profit - todays_loss < 0:
     - If todays_loss > todays_st_profit + todays_lt_profit:
       net_post_tax_pnl = todays_loss - todays_lt_profit - todays_st_profit
     - Else:
       net_post_tax_pnl = (todays_lt_profit - (todays_loss - todays_st_profit)) * 0.9

3. Update corpus: Corpus available = Corpus available + sum(amount invested in exited stocks) + net_post_tax_pnl 