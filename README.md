# Retail Insight Studio

Retail Insight Studio is a portfolio project for exploring synthetic U.S. retail transaction data. The planned application will import CSV data into PostgreSQL, display sales trends in a dashboard, and let users ask questions about the data through an AI-powered analyst.

All included retail data is synthetic and is not associated with a real retailer.

## Project status

**Early development.** The project structure and synthetic data generator are being prepared. The database, backend, frontend dashboard, and AI analyst are planned but may not be implemented yet.

## Planned features

- Generate reproducible synthetic retail transaction data.
- Validate CSV data and report invalid records.
- Import valid records into PostgreSQL.
- Explore sales over time, by state, and by product category.
- Filter dashboard results.
- Ask an AI analyst questions grounded in database query results.
- Document the setup, data definitions, and application architecture.

## Project structure

```text
.
├── backend/   # API and server-side application code
├── data/      # Synthetic data generator and CSV files
├── db/        # Database schema, migrations, and database scripts
└── frontend/  # React user interface
```

## Synthetic data

The data generator creates:
- data/retail_demo_clean.csv -- valid synthetic transactions for development.
- data/retail_demo_with_quality_issues.csv -- test data containing intentional validation errors.

Generate the files from the project root:
```bash
python data/generate_retail_data.py
```

## Data and metric conventions
- ```quantity``` and ```unit_price``` are positive values.
- ```transaction_type``` identifies whether a row is a ```sale``` or a ```return```.
- Net revenue is calculated as:
```text
quantity × unit\_price × (1 − discount\_pct / 100)
```
- Returns should be subtracted from sales when calculating net revenue.
- The data-quality test file intentionally includes invalid records; it should not be treated as clean production data.
