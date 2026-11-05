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

## Local PostgreSQL database

The project uses Docker Compose to run PostgreSQL locally. Copy the example environment file and set your local database values in `.env`:

```bash
cp .env.example .env
```

Start the database:

```bash
docker compose up -d db
docker compose ps
```

The database is available on localhost at the host port set by POSTGRES_PORT in .env (for example, 5433). Containers in the Compose network connect to the database service at db:5432.

Stop the database without deleting its data:

```bash
docker compose down
```

To delete the database volume and all data stored in it:

```bash
docker compose down -v
```

## Database schema

The PostgreSQL schema stores the synthetic retail data in related tables:

- `stores` contains store records.
- `categories` contains product categories.
- `products` references a category.
- `transactions` references a store and product.

Foreign keys connect these records, and constraints enforce rules such as unique transaction IDs, positive quantities and prices, valid discounts, and allowed transaction types.

To create the tables, start the database with Docker Compose and run:

```bash
docker compose up -d db
docker compose exec -T db sh -c 'psql -v ON\_ERROR\_STOP=1 -U "\$POSTGRES\_USER" -d "\$POSTGRES\_DB"' < db/001\_create\_transactions.sql
```
This creates the schema; CSV validation and importing are planned.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.