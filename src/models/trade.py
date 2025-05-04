"""
Trade class for representing stock trades.
"""

import math
from datetime import datetime
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from typing import Optional
from dateutil.relativedelta import relativedelta


class Trade:
    """
    Represents a single stock trade with entry and exit information.
    """

    def __init__(
        self,
        stock_name: str,
        entry_price: float,
        exit_price: Optional[float] = None,
        entry_date: Optional[str] = None,
        exit_date: Optional[str] = None,
    ):
        """
        Initialize a Trade object.

        Args:
            stock_name: Name of the stock
            entry_price: Price at which the stock was bought
            exit_price: Price at which the stock was sold (if applicable)
            entry_date: Date when the stock was bought (format: DD-MMM-YY or DD Month YYYY)
            exit_date: Date when the stock was sold (format: DD-MMM-YY or DD Month YYYY)
        """
        self.stock_name = stock_name
        self.entry_price = Decimal(str(entry_price))
        self.exit_price = Decimal(str(exit_price)) if exit_price is not None else None
        
        # Parse dates if provided
        self.entry_date = self._parse_date(entry_date) if entry_date else None
        self.exit_date = self._parse_date(exit_date) if exit_date else None
        
        # Trade details to be calculated
        self.quantity = 0
        self.entry_amount = Decimal('0')
        self.exit_amount = Decimal('0')
        self.pnl = Decimal('0')
        self.is_long_term = False
        self.tax = Decimal('0')

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse a date string in various formats.

        Args:
            date_str: Date string in various formats (DD-MMM-YY, DD Month YYYY, etc.)

        Returns:
            Parsed datetime object
        """
        date_formats = [
            "%d-%b-%y",       # DD-MMM-YY (e.g., 01-Nov-01)
            "%d-%B-%y",       # DD-MONTH-YY (e.g., 01-November-01)
            "%d %B %Y",       # DD Month YYYY (e.g., 01 February 2001)
            "%d %b %Y",       # DD Mon YYYY (e.g., 01 Feb 2001)
            "%d-%b-%Y",       # DD-MMM-YYYY (e.g., 01-Nov-2001)
            "%d-%B-%Y",       # DD-MONTH-YYYY (e.g., 01-November-2001)
            "%Y-%m-%d",       # YYYY-MM-DD (e.g., 2001-11-01)
            "%d/%m/%Y",       # DD/MM/YYYY (e.g., 01/11/2001)
            "%m/%d/%Y",       # MM/DD/YYYY (e.g., 11/01/2001)
        ]
        
        # Try each format until one works
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
        
        # If none of the formats work, raise an error
        raise ValueError(f"Unable to parse date: {date_str}. Expected format: DD-MMM-YY (e.g., 01-Nov-01)")

    def calculate_entry_details(self, allocated_amount: Decimal) -> None:
        """
        Calculate quantity and entry amount based on allocated funds.

        Args:
            allocated_amount: Amount allocated for this stock
        """
        # Calculate the quantity (round down to integer)
        self.quantity = int(allocated_amount / self.entry_price)
        
        # Calculate the actual entry amount
        self.entry_amount = self.quantity * self.entry_price
        
        # Round to 2 decimal places
        self.entry_amount = self.entry_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def calculate_exit_details(self) -> None:
        """
        Calculate exit amount and PNL.
        Should be called only after exit price is set and quantity is known.
        """
        if self.exit_price is None:
            raise ValueError("Exit price must be set before calculating exit details")
        
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive to calculate exit details")
        
        # Calculate exit amount
        self.exit_amount = self.quantity * self.exit_price
        
        # Round to 2 decimal places
        self.exit_amount = self.exit_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Calculate PNL
        self.pnl = self.exit_amount - self.entry_amount
        
        # Round to 2 decimal places
        self.pnl = self.pnl.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Determine if this is a long-term trade
        if self.entry_date and self.exit_date:
            # Correctly compare using relativedelta
            one_year = self.entry_date + relativedelta(years=1)
            self.is_long_term = self.exit_date >= one_year

    def is_profitable(self) -> bool:
        """
        Check if the trade is profitable.

        Returns:
            True if the trade has a positive PNL, False otherwise
        """
        return self.pnl > 0
    
    def is_completed(self) -> bool:
        """
        Check if the trade is completed (has both entry and exit).

        Returns:
            True if the trade is completed, False otherwise
        """
        return (self.entry_price is not None and 
                self.exit_price is not None and 
                self.entry_date is not None and 
                self.exit_date is not None)
    
    def __str__(self) -> str:
        """String representation of the trade."""
        return (f"Trade({self.stock_name}, entry: {self.entry_price}, "
                f"exit: {self.exit_price}, pnl: {self.pnl}, "
                f"{'long-term' if self.is_long_term else 'short-term'})") 