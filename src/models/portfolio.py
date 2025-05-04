"""
Portfolio class for managing stocks and corpus.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from .trade import Trade


class Portfolio:
    """
    Represents a portfolio of stocks and manages the available corpus.
    """

    def __init__(self, initial_capital: float, max_stocks: int):
        """
        Initialize a Portfolio object.

        Args:
            initial_capital: Initial capital (X) in rupees
            max_stocks: Maximum number of stocks (N) in the portfolio
        """
        self.initial_capital = Decimal(str(initial_capital))
        self.max_stocks = max_stocks
        self.corpus_available = self.initial_capital
        self.current_holdings: Dict[str, Trade] = {}  # Stock name -> Trade
        self.completed_trades: List[Trade] = []
        
    def get_allocation_per_stock(self) -> Decimal:
        """
        Calculate the amount to be allocated per stock.

        Returns:
            Amount to be allocated per stock
        """
        if not self.current_holdings and self.max_stocks <= 0:
            return Decimal('0')
        
        # If we already have stocks, calculate based on remaining slots
        remaining_slots = max(0, self.max_stocks - len(self.current_holdings))
        
        if remaining_slots <= 0:
            return Decimal('0')
        
        allocation = self.corpus_available / Decimal(str(remaining_slots))
        return allocation.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
    def add_stock(self, trade: Trade) -> Decimal:
        """
        Add a stock to the portfolio.

        Args:
            trade: Trade object representing the stock entry

        Returns:
            Amount actually invested in the stock

        Raises:
            ValueError: If the portfolio is already at maximum capacity
        """
        if len(self.current_holdings) >= self.max_stocks:
            raise ValueError(f"Portfolio already at maximum capacity ({self.max_stocks} stocks)")
        
        # Calculate allocation for this stock
        allocation = self.get_allocation_per_stock()
        
        # Calculate entry details (quantity and actual entry amount)
        trade.calculate_entry_details(allocation)
        
        # Add to current holdings
        self.current_holdings[trade.stock_name] = trade
        
        # Update corpus
        self.corpus_available -= trade.entry_amount
        self.corpus_available = self.corpus_available.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        return trade.entry_amount
        
    def remove_stock(self, stock_name: str) -> Tuple[Trade, Decimal]:
        """
        Remove a stock from the portfolio (exit position).

        Args:
            stock_name: Name of the stock to remove

        Returns:
            Tuple of (Trade object, Amount returned to corpus)

        Raises:
            ValueError: If the stock is not in the portfolio
        """
        if stock_name not in self.current_holdings:
            raise ValueError(f"Stock {stock_name} not in portfolio")
        
        trade = self.current_holdings.pop(stock_name)
        
        # Calculate exit details
        trade.calculate_exit_details()
        
        # Add to completed trades
        self.completed_trades.append(trade)
        
        # Return entry amount to corpus (PNL is handled separately via tax calculations)
        self.corpus_available += trade.entry_amount
        self.corpus_available = self.corpus_available.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        return trade, trade.entry_amount
        
    def apply_tax_adjustments(self, date: datetime, net_post_tax_pnl: Decimal) -> None:
        """
        Apply tax adjustments to the corpus.

        Args:
            date: Date of the tax adjustment
            net_post_tax_pnl: Net post-tax PNL to add to the corpus
        """
        self.corpus_available += net_post_tax_pnl
        self.corpus_available = self.corpus_available.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
    def get_trades_exiting_on_date(self, date: datetime) -> List[Trade]:
        """
        Get all trades that exit on a specific date.

        Args:
            date: Exit date to filter by

        Returns:
            List of trades exiting on the given date
        """
        return [trade for trade in self.completed_trades if trade.exit_date and trade.exit_date.date() == date.date()]
        
    def get_corpus_available(self) -> Decimal:
        """
        Get the available corpus.

        Returns:
            Available corpus in rupees
        """
        return self.corpus_available
        
    def get_current_holdings_count(self) -> int:
        """
        Get the number of stocks currently in the portfolio.

        Returns:
            Number of stocks
        """
        return len(self.current_holdings)
        
    def is_full(self) -> bool:
        """
        Check if the portfolio is at maximum capacity.

        Returns:
            True if the portfolio has reached maximum capacity, False otherwise
        """
        return len(self.current_holdings) >= self.max_stocks
        
    def __str__(self) -> str:
        """String representation of the portfolio."""
        return (f"Portfolio(corpus: {self.corpus_available}, "
                f"holdings: {len(self.current_holdings)}/{self.max_stocks})") 