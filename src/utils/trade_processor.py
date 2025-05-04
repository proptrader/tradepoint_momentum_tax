"""
Trade processor module for handling trade execution.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Tuple, Any

from ..models.trade import Trade
from ..models.portfolio import Portfolio
from ..models.tax_calculator import TaxCalculator


class TradeProcessor:
    """
    Processes trades, manages the portfolio, and handles tax calculations.
    """

    def __init__(self, initial_capital: float, max_stocks: int):
        """
        Initialize the trade processor.

        Args:
            initial_capital: Initial capital (X) in rupees
            max_stocks: Maximum number of stocks (N) in the portfolio
        """
        self.portfolio = Portfolio(initial_capital, max_stocks)
        self.tax_calculator = TaxCalculator()
        self.corpus_history: Dict[datetime, Decimal] = {}
        self.processed_trades: List[Trade] = []
        self.current_trades: Dict[str, Trade] = {}

    def _get_trades_by_date(self, trades: List[Trade]) -> Dict[datetime, Dict[str, List[Trade]]]:
        """
        Group trades by date, separating entries and exits.

        Args:
            trades: List of trades to process

        Returns:
            Dictionary mapping dates to dictionaries of entries and exits
        """
        trades_by_date: Dict[datetime, Dict[str, List[Trade]]] = {}
        
        # First, organize trades by entry date
        for trade in trades:
            if trade.entry_date:
                date_key = trade.entry_date.date()
                if date_key not in trades_by_date:
                    trades_by_date[date_key] = {"entries": [], "exits": []}
                trades_by_date[date_key]["entries"].append(trade)
        
        # Then, organize trades by exit date
        for trade in trades:
            if trade.exit_date:
                date_key = trade.exit_date.date()
                if date_key not in trades_by_date:
                    trades_by_date[date_key] = {"entries": [], "exits": []}
                
                # Store a reference to this trade as an exit on this date
                exit_trade = Trade(
                    stock_name=trade.stock_name,
                    entry_price=float(trade.entry_price),
                    exit_price=float(trade.exit_price) if trade.exit_price else None,
                    entry_date=format_date(trade.entry_date) if trade.entry_date else None,
                    exit_date=format_date(trade.exit_date) if trade.exit_date else None
                )
                trades_by_date[date_key]["exits"].append(exit_trade)
        
        return trades_by_date

    def _process_exits(self, exit_trades: List[Trade], date: datetime) -> List[Trade]:
        """
        Process exit trades for a given date.

        Args:
            exit_trades: List of trades exiting on this date
            date: Date of the exits

        Returns:
            List of completed exit trades
        """
        completed_exits = []
        
        # Process each exit
        for exit_trade in exit_trades:
            stock_name = exit_trade.stock_name
            
            if stock_name in self.current_trades:
                # Get the actual trade from current holdings
                current_trade = self.current_trades[stock_name]
                
                # Set the exit price and date
                current_trade.exit_price = exit_trade.exit_price
                current_trade.exit_date = exit_trade.exit_date
                
                # Remove from portfolio and get the trade with exit details calculated
                try:
                    completed_trade, returned_amount = self.portfolio.remove_stock(stock_name)
                    completed_exits.append(completed_trade)
                    print(f"Exited {stock_name} at {exit_trade.exit_price}, returned {returned_amount} to corpus")
                except ValueError as e:
                    print(f"Error exiting {stock_name}: {e}")
                    
                # Remove from current trades
                del self.current_trades[stock_name]
            else:
                print(f"Warning: Attempted to exit {stock_name} but it's not in the current portfolio")
        
        # Calculate tax for this batch of exits
        if completed_exits:
            net_post_tax_pnl, tax_details = self.tax_calculator.calculate_tax(completed_exits)
            
            # Apply tax adjustments to corpus
            self.portfolio.apply_tax_adjustments(date, net_post_tax_pnl)
            
            # Debug output
            print(f"Tax details for {date}:")
            for key, value in tax_details.items():
                print(f"  {key}: {value}")
            
            # Add completed trades to the processed list
            self.processed_trades.extend(completed_exits)
        
        # Record corpus value after exits
        self.corpus_history[date.date()] = self.portfolio.get_corpus_available()
        
        return completed_exits

    def _process_entries(self, entry_trades: List[Trade], date: datetime) -> None:
        """
        Process entry trades for a given date.

        Args:
            entry_trades: List of trades entering on this date
            date: Date of the entries
        """
        # First, check if we have room in the portfolio
        available_slots = self.portfolio.max_stocks - self.portfolio.get_current_holdings_count()
        
        if available_slots <= 0:
            print(f"Warning: Portfolio is full, cannot add new entries on {date}")
            return
        
        # Limit entries to available slots
        entries_to_process = entry_trades[:available_slots]
        
        # Process each entry
        for entry_trade in entries_to_process:
            try:
                # Add to portfolio
                invested_amount = self.portfolio.add_stock(entry_trade)
                
                # Add to current trades
                self.current_trades[entry_trade.stock_name] = entry_trade
                
                print(f"Entered {entry_trade.stock_name} at {entry_trade.entry_price}, invested {invested_amount}")
            except ValueError as e:
                print(f"Error entering {entry_trade.stock_name}: {e}")
        
        # Record corpus value after entries
        self.corpus_history[date.date()] = self.portfolio.get_corpus_available()

    def process_trades(self, trades: List[Trade]) -> Dict[str, Any]:
        """
        Process all trades in chronological order.

        Args:
            trades: List of trades to process

        Returns:
            Dictionary with processing results
        """
        # Group trades by date
        trades_by_date = self._get_trades_by_date(trades)
        
        # Process dates in chronological order
        for date in sorted(trades_by_date.keys()):
            date_trades = trades_by_date[date]
            
            print(f"\nProcessing trades for {date}:")
            print(f"Corpus available: {self.portfolio.get_corpus_available()}")
            
            # Process exits first
            exits = date_trades.get("exits", [])
            if exits:
                print(f"Processing {len(exits)} exits...")
                self._process_exits(exits, datetime.combine(date, datetime.min.time()))
            
            # Then process entries
            entries = date_trades.get("entries", [])
            if entries:
                print(f"Processing {len(entries)} entries...")
                self._process_entries(entries, datetime.combine(date, datetime.min.time()))
            
            print(f"After processing - Corpus available: {self.portfolio.get_corpus_available()}")
            print(f"Current holdings: {self.portfolio.get_current_holdings_count()}/{self.portfolio.max_stocks}")
        
        return {
            "processed_trades": self.processed_trades,
            "corpus_history": self.corpus_history,
            "final_corpus": self.portfolio.get_corpus_available(),
            "holdings_count": self.portfolio.get_current_holdings_count()
        }


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