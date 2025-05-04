"""
Output generator module for creating CSV output files.
"""

import csv
import os
import calendar
from typing import List, Dict, Any, Set
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import pandas as pd

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


def generate_summary_filename(input_filename: str) -> str:
    """
    Generate the summary filename based on the input filename.

    Args:
        input_filename: Name of the input file

    Returns:
        Summary filename
    """
    # Get just the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    return f"summary-{base_name}.csv"


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


def create_summary_file(tax_output_path: str) -> str:
    """
    Create a summary CSV file showing profit after tax by month and year.
    
    Args:
        tax_output_path: Path to the tax output file
        
    Returns:
        Path to the created summary file
    """
    # Read the tax output file using pandas
    df = pd.read_csv(tax_output_path)
    
    # Convert Exit date to datetime
    df['Exit date'] = pd.to_datetime(df['Exit date'], format='%d-%b-%y')
    
    # Extract year and month from Exit date
    df['Year'] = df['Exit date'].dt.year
    df['Month'] = df['Exit date'].dt.month
    
    # Calculate profit after tax (PNL - Tax)
    df['Profit After Tax'] = df['PNL'] - df['Tax']
    
    # Group by year and month and sum the profit after tax
    monthly_profit = df.groupby(['Year', 'Month'])['Profit After Tax'].sum().reset_index()
    
    # Create a pivot table with years as rows and months as columns
    pivot_table = monthly_profit.pivot_table(
        index='Year', 
        columns='Month', 
        values='Profit After Tax',
        fill_value=0
    )
    
    # Rename month columns to month names
    month_names = {
        i: name[:3] for i, name in enumerate(calendar.month_name) if i > 0
    }
    pivot_table = pivot_table.rename(columns=month_names)
    
    # Make sure all months are present, even if there's no data
    for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        if month not in pivot_table.columns:
            pivot_table[month] = 0
    
    # Reorder columns by month
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    pivot_table = pivot_table[month_order]
    
    # Calculate row totals
    pivot_table['Total'] = pivot_table.sum(axis=1)
    
    # Reset index to make Year a column
    pivot_table = pivot_table.reset_index()
    
    # Generate the summary output path
    output_dir = os.path.dirname(tax_output_path)
    input_filename = os.path.basename(tax_output_path).replace('tax-', '')
    summary_filename = generate_summary_filename(input_filename)
    summary_path = os.path.join(output_dir, summary_filename)
    
    # Save the pivot table to CSV
    pivot_table.to_csv(summary_path, index=False, float_format='%.2f')
    
    return summary_path


def save_trade_history(trades: List[Trade], corpus_history: Dict[datetime, Decimal], input_file_path: str) -> Dict[str, str]:
    """
    Save the complete trade history with corpus information.

    Args:
        trades: List of completed trades
        corpus_history: History of corpus values by date
        input_file_path: Path to the input file

    Returns:
        Dictionary with paths to the created output files
    """
    # First, ensure each trade has the corpus available at its exit
    for trade in trades:
        if trade.exit_date and trade.exit_date.date() in corpus_history:
            trade.corpus_available = corpus_history[trade.exit_date.date()]
    
    # Generate the tax output file
    tax_output_path = create_output_file(trades, input_file_path)
    
    # Generate the summary file
    summary_output_path = create_summary_file(tax_output_path)
    
    return {
        "tax_output": tax_output_path,
        "summary_output": summary_output_path
    } 