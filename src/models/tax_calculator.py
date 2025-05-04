"""
Tax calculator for trade profits and losses.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Tuple
from datetime import datetime
from .trade import Trade


class TaxCalculator:
    """
    Handles tax calculations for trades based on whether they are short-term or long-term.
    """

    def __init__(self):
        """Initialize the tax calculator."""
        # Tax rates as per requirements
        self.short_term_tax_rate = Decimal('0.2')  # 20% tax for short-term gains
        self.long_term_tax_rate = Decimal('0.1')   # 10% tax for long-term gains

    def categorize_trades(self, trades: List[Trade]) -> Tuple[Decimal, Decimal, Decimal]:
        """
        Categorize trades into losses, short-term profits, and long-term profits.

        Args:
            trades: List of trades to categorize

        Returns:
            Tuple of (total_loss, short_term_profit, long_term_profit)
        """
        total_loss = Decimal('0')
        short_term_profit = Decimal('0')
        long_term_profit = Decimal('0')

        for trade in trades:
            if trade.pnl < 0:
                # This is a loss
                total_loss += abs(trade.pnl)
            elif trade.is_long_term:
                # This is a long-term profit
                long_term_profit += trade.pnl
            else:
                # This is a short-term profit
                short_term_profit += trade.pnl

        # Round to 2 decimal places
        total_loss = total_loss.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        short_term_profit = short_term_profit.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        long_term_profit = long_term_profit.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return total_loss, short_term_profit, long_term_profit

    def calculate_tax(self, trades: List[Trade]) -> Tuple[Decimal, Dict[str, Decimal]]:
        """
        Calculate the tax for the given trades.

        Args:
            trades: List of trades to calculate tax for

        Returns:
            Tuple of (net_post_tax_pnl, tax_details)
        """
        # Categorize trades
        todays_loss, todays_st_profit, todays_lt_profit = self.categorize_trades(trades)

        # Calculate net short-term profit after offsetting losses
        net_st_profit = todays_st_profit - todays_loss

        # Calculate post-tax PNL based on the rules
        if net_st_profit > 0:
            # If short-term profit exceeds loss
            net_post_tax_pnl = (net_st_profit * (1 - self.short_term_tax_rate) + 
                              todays_lt_profit * (1 - self.long_term_tax_rate))
            st_tax = net_st_profit * self.short_term_tax_rate
            lt_tax = todays_lt_profit * self.long_term_tax_rate
            total_tax = st_tax + lt_tax
        elif net_st_profit == 0:
            # If short-term profit equals loss
            net_post_tax_pnl = todays_lt_profit * (1 - self.long_term_tax_rate)
            st_tax = Decimal('0')
            lt_tax = todays_lt_profit * self.long_term_tax_rate
            total_tax = lt_tax
        else:
            # If loss exceeds short-term profit
            remaining_loss = abs(net_st_profit)
            
            if remaining_loss > todays_lt_profit:
                # If the remaining loss exceeds long-term profits
                net_post_tax_pnl = -(remaining_loss - todays_lt_profit)
                st_tax = Decimal('0')
                lt_tax = Decimal('0')
                total_tax = Decimal('0')
            else:
                # If long-term profits can absorb the remaining loss
                net_lt_profit = todays_lt_profit - remaining_loss
                net_post_tax_pnl = net_lt_profit * (1 - self.long_term_tax_rate)
                st_tax = Decimal('0')
                lt_tax = net_lt_profit * self.long_term_tax_rate
                total_tax = lt_tax

        # Round to 2 decimal places
        net_post_tax_pnl = net_post_tax_pnl.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Create tax details dictionary
        tax_details = {
            'todays_loss': todays_loss,
            'todays_st_profit': todays_st_profit,
            'todays_lt_profit': todays_lt_profit,
            'net_st_profit': net_st_profit,
            'st_tax': st_tax if 'st_tax' in locals() else Decimal('0'),
            'lt_tax': lt_tax if 'lt_tax' in locals() else Decimal('0'),
            'total_tax': total_tax if 'total_tax' in locals() else Decimal('0'),
            'net_post_tax_pnl': net_post_tax_pnl
        }

        # Assign tax to individual trades
        for trade in trades:
            if trade.pnl > 0:
                if trade.is_long_term:
                    # Apply long-term tax rate only to what's taxable
                    if todays_lt_profit > 0 and 'lt_tax' in locals():
                        trade.tax = (trade.pnl / todays_lt_profit) * lt_tax
                    else:
                        trade.tax = Decimal('0')
                else:
                    # Apply short-term tax rate only to what's taxable
                    if todays_st_profit > 0 and 'st_tax' in locals() and net_st_profit > 0:
                        trade.tax = (trade.pnl / todays_st_profit) * st_tax
                    else:
                        trade.tax = Decimal('0')
            else:
                trade.tax = Decimal('0')
            
            # Round to 2 decimal places
            trade.tax = trade.tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return net_post_tax_pnl, tax_details 