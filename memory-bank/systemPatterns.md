# TradePoint Momentum Tax - System Patterns

## System Architecture

The TradePoint Momentum Tax system follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Data Ingestion │────▶│ Trade Processor │────▶│ Output Generator│
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               ▲
                               │
                        ┌──────┴──────┐
                        │ Tax Calculator │
                        └──────────────┘
```

### Components:

1. **Data Ingestion Module**
   - Reads and parses input CSV files
   - Validates input data
   - Organizes trades chronologically

2. **Trade Processor**
   - Manages portfolio state
   - Processes entries and exits
   - Tracks corpus and investments
   - Calculates raw P&L

3. **Tax Calculator**
   - Categorizes trades as short-term or long-term
   - Applies tax calculation rules
   - Determines post-tax P&L

4. **Output Generator**
   - Creates formatted output files
   - Ensures all required information is included

## Key Technical Decisions

### 1. Data Model

The system uses several key data structures:

- **Trade** - Represents a single trade with entry and exit information
- **Portfolio** - Tracks the current state of all holdings
- **Corpus** - Manages the available funds
- **TaxReport** - Stores the calculated tax information

### 2. Processing Approach

The system follows a sequential processing approach:

1. Load all trades from input file
2. Sort trades by date
3. Process chronologically, handling each date as follows:
   - Process all exits for the date first
   - Apply tax calculations
   - Update available corpus
   - Process all entries for the date
   - Rebalance portfolio

### 3. Tax Calculation Strategy

Tax calculations follow a specific algorithm:
1. Categorize each trade as short-term or long-term
2. For each exit date:
   - Calculate total losses
   - Calculate total short-term profits
   - Calculate total long-term profits
   - Apply tax calculation formula based on the relationship between these values

## Design Patterns in Use

1. **Repository Pattern** - For data access and storage
2. **Strategy Pattern** - For different tax calculation scenarios
3. **Factory Pattern** - For creating trade objects
4. **Command Pattern** - For processing trades

## Component Relationships

- **Data Flow**: Input file → Parsed trades → Processed trades → Tax calculations → Output file
- **Dependency Direction**: Output depends on Tax Calculator, which depends on Trade Processor, which depends on Data Ingestion
- **Configuration**: System parameters (X, N) are set at initialization

## Error Handling Strategy

The system includes robust error handling:
- Input validation to ensure data integrity
- Exception handling for calculation errors
- Logging for debugging and audit purposes
- Graceful degradation when encountering partial data issues 