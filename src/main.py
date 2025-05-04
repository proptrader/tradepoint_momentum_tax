"""
Main application for TradePoint Momentum Tax.
"""

import os
import sys
import glob
import argparse
from pathlib import Path
from typing import Dict, List, Any
import logging

from .config.config import get_config
from .models.trade import Trade
from .utils.data_ingestion import load_trades, get_input_filename
from .utils.trade_processor import TradeProcessor
from .utils.output_generator import save_trade_history


def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.

    Args:
        verbose: Whether to use verbose (DEBUG) logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )


def find_input_files() -> List[str]:
    """
    Find CSV files in the input directory.

    Returns:
        List of paths to CSV files in the input directory
    """
    config = get_config()
    input_dir = config.get_input_dir()
    
    # Find all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    if not csv_files:
        # Try also with .txt extension as sometimes CSV files have .txt extension
        csv_files = glob.glob(os.path.join(input_dir, "*.txt"))
    
    return csv_files


def parse_arguments() -> Dict[str, Any]:
    """
    Parse command-line arguments.

    Returns:
        Dictionary of parsed arguments
    """
    parser = argparse.ArgumentParser(description='TradePoint Momentum Tax - Stock Portfolio Management')
    
    parser.add_argument('--input', '-i', type=str,
                        help='Path to the input CSV file (if not specified, will use files in the input directory)')
    
    parser.add_argument('--config', '-c', type=str, default='config.json',
                        help='Path to the configuration file (default: config.json)')
    
    parser.add_argument('--initial-capital', '-x', type=float,
                        help='Initial capital (X) in rupees (overrides config file)')
    
    parser.add_argument('--max-stocks', '-n', type=int,
                        help='Maximum number of stocks (N) (overrides config file)')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')
    
    args = vars(parser.parse_args())
    
    # If input is not specified, try to find input files
    if not args.get('input'):
        input_files = find_input_files()
        if input_files:
            args['input'] = input_files[0]  # Use the first file found
            if len(input_files) > 1:
                print(f"Multiple input files found. Using {args['input']}.")
                print("To use a specific file, specify with --input option.")
    
    return args


def validate_input_file(input_file: str) -> None:
    """
    Validate that the input file exists and is accessible.

    Args:
        input_file: Path to the input file

    Raises:
        FileNotFoundError: If the input file does not exist
    """
    if not input_file:
        raise ValueError("No input file specified and no CSV files found in the input directory.")
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    if not os.path.isfile(input_file):
        raise ValueError(f"Input path is not a file: {input_file}")


def process_portfolio(input_file: str, config_file: str = None, 
                     initial_capital: float = None, max_stocks: int = None) -> Dict[str, Any]:
    """
    Process the portfolio based on the input file and configuration.

    Args:
        input_file: Path to the input CSV file
        config_file: Path to the configuration file (optional)
        initial_capital: Override for initial capital (optional)
        max_stocks: Override for maximum stocks (optional)

    Returns:
        Dictionary with processing results
    """
    # Load configuration
    config = get_config(config_file)
    
    # Override configuration if specified
    if initial_capital is not None:
        config.config_data["initial_capital"] = initial_capital
    
    if max_stocks is not None:
        config.config_data["max_stocks"] = max_stocks
    
    # Get configuration values
    initial_capital = config.get_initial_capital()
    max_stocks = config.get_max_stocks()
    
    logging.info(f"Configuration: initial_capital={initial_capital}, max_stocks={max_stocks}")
    
    # Load trades from input file
    trades = load_trades(input_file)
    logging.info(f"Loaded {len(trades)} trades from {input_file}")
    
    # Initialize trade processor
    processor = TradeProcessor(initial_capital, max_stocks)
    
    # Process trades
    results = processor.process_trades(trades)
    
    # Generate output file
    output_file = save_trade_history(
        results["processed_trades"], 
        results["corpus_history"], 
        input_file
    )
    
    logging.info(f"Output written to {output_file}")
    
    # Return results
    return {
        "processed_trades_count": len(results["processed_trades"]),
        "final_corpus": float(results["final_corpus"]),
        "holdings_count": results["holdings_count"],
        "output_file": output_file
    }


def main() -> int:
    """
    Main entry point for the application.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Set up logging
        setup_logging(args.get('verbose', False))
        
        # Validate input file
        validate_input_file(args.get('input'))
        
        # Process portfolio
        results = process_portfolio(
            input_file=args['input'],
            config_file=args.get('config'),
            initial_capital=args.get('initial_capital'),
            max_stocks=args.get('max_stocks')
        )
        
        # Print summary
        print("\nProcessing complete!")
        print(f"Processed {results['processed_trades_count']} trades")
        print(f"Final corpus: {results['final_corpus']}")
        print(f"Final holdings: {results['holdings_count']}")
        print(f"Output file: {results['output_file']}")
        
        return 0
        
    except Exception as e:
        logging.error(f"Error: {e}")
        if args and args.get('verbose', False):
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 