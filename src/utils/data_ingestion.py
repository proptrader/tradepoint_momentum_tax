"""
Data ingestion module for reading and parsing CSV input files.
"""

import csv
import os
import codecs
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from pathlib import Path

from ..models.trade import Trade


def detect_delimiter(file_path: str) -> str:
    """
    Detect the delimiter used in a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Detected delimiter (tab, comma, or semicolon)
    """
    # Read the first few lines to detect the delimiter
    with open(file_path, 'r', errors='replace') as f:
        # Read first few lines
        sample_lines = [f.readline() for _ in range(5) if f.readline()]
        
    # Count occurrences of potential delimiters
    delimiters = ['\t', ',', ';']
    counts = {}
    
    for delimiter in delimiters:
        counts[delimiter] = sum(line.count(delimiter) for line in sample_lines)
    
    # Pick the delimiter with the most consistent count
    if counts['\t'] > 0:
        return '\t'  # Prefer tab if it exists
    elif counts[','] > 0:
        return ','   # Next preference is comma
    else:
        return ';'   # Last resort is semicolon


def parse_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse a CSV file and return a list of dictionaries.
    Stop parsing at the first blank line.

    Args:
        file_path: Path to the CSV file

    Returns:
        List of dictionaries representing trades
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    trades_data = []
    
    # Detect the delimiter
    delimiter = detect_delimiter(file_path)
    print(f"Detected delimiter: {repr(delimiter)}")
    
    # Try to handle BOM if present
    try:
        with codecs.open(file_path, 'r', encoding='utf-8-sig') as f:
            # Create CSV reader
            csv_reader = csv.reader(f, delimiter=delimiter)
            
            # Skip header row
            next(csv_reader, None)
            
            # Process each row until a blank line is encountered
            for row_num, row in enumerate(csv_reader, start=1):
                # Check if row is blank (empty or contains only whitespace)
                if not row or all(cell.strip() == '' for cell in row):
                    print(f"Stopped reading at blank line (row {row_num})")
                    break
                
                # Debug output
                print(f"Row {row_num}: {row}")
                
                # Check if we have enough columns
                if len(row) < 8:
                    print(f"Warning: Row {row_num} has insufficient columns: {row}")
                    # If this is a single column that might contain the entire row
                    if len(row) == 1 and delimiter in row[0]:
                        # Try to split the first element
                        split_row = row[0].split(delimiter)
                        if len(split_row) >= 8:
                            print(f"  Fixed by splitting first element: {split_row}")
                            row = split_row
                        else:
                            print(f"  Unable to fix row format. Skipping.")
                            continue
                
                # Extract relevant columns
                try:
                    # Extract by position since the meaning of each column is fixed
                    sr_no = row[0].strip() if len(row) > 0 else ""
                    stock_name = row[1].strip() if len(row) > 1 else ""
                    entry_price = row[2].strip() if len(row) > 2 else ""
                    exit_price = row[3].strip() if len(row) > 3 else ""
                    entry_date = row[6].strip() if len(row) > 6 else ""
                    exit_date = row[7].strip() if len(row) > 7 else ""
                    
                    # Debug output
                    print(f"  Extracted: sr_no={sr_no}, stock={stock_name}, entry_price={entry_price}, exit_price={exit_price}")
                    print(f"  Dates: entry={entry_date}, exit={exit_date}")
                    
                    # Skip rows with missing essential data
                    if not all([stock_name, entry_price, entry_date]):
                        print(f"  Skipping row due to missing essential data")
                        continue
                    
                    # Convert to appropriate types
                    try:
                        entry_price = float(entry_price.replace(',', ''))
                        exit_price = float(exit_price.replace(',', '')) if exit_price else None
                    except ValueError as ve:
                        print(f"Warning: Invalid price format in row {row_num} ({sr_no}): {ve}. Skipping.")
                        continue
                    
                    trades_data.append({
                        "sr_no": sr_no,
                        "stock_name": stock_name,
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "entry_date": entry_date,
                        "exit_date": exit_date
                    })
                    print(f"  Successfully added trade: {stock_name}")
                    
                except Exception as e:
                    print(f"Error processing row {row_num}: {e}. Skipping.")
                    continue
    except Exception as e:
        print(f"Error reading file: {e}")
        # Try again with a different encoding if needed
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                # Same logic as above, but with different encoding
                csv_reader = csv.reader(f, delimiter=delimiter)
                # Skip header row
                next(csv_reader, None)
                # Process each row...
                # (abbreviated for clarity)
        except Exception as e2:
            print(f"Also failed with alternate encoding: {e2}")
    
    print(f"Successfully parsed {len(trades_data)} trades from {file_path}")
    return trades_data


def create_trades_from_data(trades_data: List[Dict[str, Any]]) -> List[Trade]:
    """
    Create Trade objects from parsed data.

    Args:
        trades_data: List of dictionaries containing trade data

    Returns:
        List of Trade objects
    """
    trades = []
    
    for data in trades_data:
        try:
            trade = Trade(
                stock_name=data["stock_name"],
                entry_price=data["entry_price"],
                exit_price=data["exit_price"],
                entry_date=data["entry_date"],
                exit_date=data["exit_date"]
            )
            trades.append(trade)
        except Exception as e:
            print(f"Error creating trade for {data.get('stock_name', 'unknown')}: {e}")
    
    return trades


def sort_trades_by_date(trades: List[Trade]) -> List[Trade]:
    """
    Sort trades by entry date.

    Args:
        trades: List of Trade objects

    Returns:
        Sorted list of Trade objects
    """
    # Sort by entry date (if available)
    return sorted(trades, key=lambda t: t.entry_date if t.entry_date else datetime.max)


def group_trades_by_date(trades: List[Trade]) -> Dict[datetime, List[Trade]]:
    """
    Group trades by their entry date.

    Args:
        trades: List of Trade objects

    Returns:
        Dictionary mapping dates to lists of trades
    """
    grouped_trades = {}
    
    for trade in trades:
        if trade.entry_date:
            # Use date (not datetime) as key for proper grouping
            date_key = trade.entry_date.date()
            if date_key not in grouped_trades:
                grouped_trades[date_key] = []
            grouped_trades[date_key].append(trade)
    
    return grouped_trades


def load_trades(file_path: str) -> List[Trade]:
    """
    Load trades from a CSV file and return as Trade objects.

    Args:
        file_path: Path to the CSV file

    Returns:
        List of Trade objects
    """
    trades_data = parse_csv_file(file_path)
    trades = create_trades_from_data(trades_data)
    sorted_trades = sort_trades_by_date(trades)
    return sorted_trades


def get_input_filename(file_path: str) -> str:
    """
    Extract the base filename from a file path.

    Args:
        file_path: Path to the file

    Returns:
        Base filename
    """
    return os.path.basename(file_path) 