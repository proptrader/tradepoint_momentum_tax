"""
Output generator module for creating CSV output files.
"""

import csv
import os
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
from decimal import Decimal

from ..models.trade import Trade
from ..config.config import get_config


def format_date(date: datetime) -> str:
    """
    Format a datetime object as a string in the DD-MMM-YY format.

    Args:
        date: Datetime object to format

    Returns:
        Formatted date string
    """
    if date is None:
        return ""
    return date.strftime("%d-%b-%y")


def generate_output_filename(input_filename: str) -> str:
    """
    Generate the output filename based on the input filename.

    Args:
        input_filename: Name of the input file

    Returns:
        Output filename
    """
    # Get just the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    return f"tax-{base_name}.csv"


def create_output_file(trades: List[Trade], input_file_path: str) -> str:
    """
    Create an output CSV file with trade information.

    Args:
        trades: List of completed trades
        input_file_path: Path to the input file

    Returns:
        Path to the created output file
    """
    config = get_config()
    output_dir = config.get_output_dir()
    
    # Ensure output directory exists
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generate output filename
    input_filename = os.path.basename(input_file_path)
    output_filename = generate_output_filename(input_filename)
    output_file_path = os.path.join(output_dir, output_filename)
    
    # Define headers
    headers = [
        "Stock Name", 
        "Entry date", 
        "Entry price", 
        "Entry Amount", 
        "Quantity", 
        "Exit date", 
        "Exit price", 
        "Exit amount", 
        "PNL", 
        "ST/LT", 
        "Tax",
        "Corpus available"
    ]
    
    # Write data to the output file
    with open(output_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write headers
        writer.writerow(headers)
        
        # Write trade data
        for trade in trades:
            if not trade.is_completed():
                continue
                
            # Format the ST/LT field
            trade_type = "LT" if trade.is_long_term else "ST"
            
            # Format the dates
            entry_date = format_date(trade.entry_date)
            exit_date = format_date(trade.exit_date)
            
            # Write the row
            writer.writerow([
                trade.stock_name,
                entry_date,
                float(trade.entry_price),
                float(trade.entry_amount),
                trade.quantity,
                exit_date,
                float(trade.exit_price) if trade.exit_price else "",
                float(trade.exit_amount),
                float(trade.pnl),
                trade_type,
                float(trade.tax),
                float(trade.corpus_available) if hasattr(trade, 'corpus_available') else ""
            ])
    
    return output_file_path


def save_trade_history(trades: List[Trade], corpus_history: Dict[datetime, Decimal], input_file_path: str) -> str:
    """
    Save the complete trade history with corpus information.

    Args:
        trades: List of completed trades
        corpus_history: History of corpus values by date
        input_file_path: Path to the input file

    Returns:
        Path to the created output file
    """
    # First, ensure each trade has the corpus available at its exit
    for trade in trades:
        if trade.exit_date and trade.exit_date.date() in corpus_history:
            trade.corpus_available = corpus_history[trade.exit_date.date()]
    
    # Generate the output file
    return create_output_file(trades, input_file_path) 