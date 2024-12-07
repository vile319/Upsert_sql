# SQL Upsert

A Python package for handling SQL upsert operations with pandas DataFrames.

## Installation

```bash
pip install sql_upsert
```

## Usage

```python
import sql_upsert as pdu
import pandas as pd
from sqlalchemy import create_engine

# Create engine
engine = create_engine('sqlite:///example.db')

# Create sample DataFrame
df = pd.DataFrame({'id': [1, 2], 'value': ['a', 'b']})

# Write with upsert functionality
pdu.to_sql_upsert(df, 'my_table', engine, unique_columns=['id'])
```

## Features

- Automatic handling of upsert operations
- Support for custom unique constraints
- Compatible with any SQLAlchemy supported database
- Preserves column types when creating tables

## Requirements

- Python >= 3.6
- SQLAlchemy >= 1.4.0
- pandas >= 1.0.0 