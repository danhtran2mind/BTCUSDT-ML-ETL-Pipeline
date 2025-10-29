#!/usr/bin/env python3
"""
Extract DuckDB schema + sample data from a given .db file.
Usage:
    python tools/get_duckdb_info.py duckdb_databases/financial_data.db
    python tools/get_duckdb_info.py ./abc.db
"""

import sys
import pathlib
import json
import argparse
import duckdb
from typing import Dict, Any


def extract_schema(con: duckdb.DuckDBPyConnection, db_path: str) -> Dict[str, Any]:
    """Extract full schema: tables → columns → types → PK → sample rows."""
    schema: Dict[str, Any] = {
        "database": str(db_path),
        "tables": {}
    }

    # Get all tables in 'main' schema
    tables = con.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'main' 
        ORDER BY table_name;
    """).fetchall()

    if not tables:
        return schema

    for (table_name,) in tables:
        # --- Columns ---
        cols = con.execute(
            """
            SELECT 
                column_name,
                data_type,
                CASE WHEN is_nullable = 'YES' THEN true ELSE false END AS nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'main' AND table_name = ?
            ORDER BY ordinal_position;
            """,
            [table_name]
        ).fetchall()

        columns = [
            {"name": name, "type": dtype, "nullable": nullable, "default": default}
            for name, dtype, nullable, default in cols
        ]

        # --- Primary Key ---
        pk = con.execute(
            """
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
              AND tc.table_schema = 'main'
              AND tc.table_name = ?
            ORDER BY kcu.ordinal_position;
            """,
            [table_name]
        ).fetchall()
        primary_key = [row[0] for row in pk] or None

        # --- Sample Data (≤3 rows) ---
        try:
            sample_rows = con.execute(f"SELECT * FROM {duckdb.string_escape(table_name)} LIMIT 3;").fetchall()
            headers = [col[0] for col in con.description] if con.description else []
            sample_data = [dict(zip(headers, row)) for row in sample_rows]
            sample_error = None
        except Exception as e:
            sample_data = []
            sample_error = str(e)

        schema["tables"][table_name] = {
            "columns": columns,
            "primary_key": primary_key,
            "sample_rows": sample_data,
            "sample_error": sample_error
        }

    return schema


def print_schema_markdown(schema: Dict[str, Any]):
    print(f"# DuckDB Schema: `{schema['database']}`\n")

    if not schema["tables"]:
        print("**No tables found.** The database is empty or has no tables in the `main` schema.\n")
        return

    for table_name, info in schema["tables"].items():
        print(f"## Table: `{table_name}`\n")

        # Columns
        print("### Columns\n")
        print("| Column | Type | Nullable | Default |")
        print("|--------|------|----------|---------|")
        for col in info["columns"]:
            default = f"`{col['default']}`" if col['default'] is not None else "—"
            nullable = "YES" if col['nullable'] else "NO"
            print(f"| `{col['name']}` | `{col['type']}` | {nullable} | {default} |")
        print()

        # Primary Key
        if info["primary_key"]:
            print(f"**Primary Key:** `{'`, `'.join(info['primary_key'])}`\n")

        # Sample Data
        if info["sample_rows"]:
            print("### Sample Data (≤3 rows)\n")
            headers = info["sample_rows"][0].keys()
            print("| " + " | ".join(f"`{h}`" for h in headers) + " |")
            print("| " + " | ".join("---" for _ in headers) + " |")
            for row in info["sample_rows"]:
                values = [
                    "NULL" if v is None
                    else f"<binary:{len(v)}B>" if isinstance(v, (bytes, bytearray))
                    else str(v)[:100]
                    for v in row.values()
                ]
                print("| " + " | ".join(values) + " |")
            print()
        elif info.get("sample_error"):
            print(f"**Warning: Sample query failed:** `{info['sample_error']}`\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extract schema and sample data from a DuckDB database file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--db_path",
        default="duckdb_databases/financial_data.db",
        type=str,
        help="Path to the DuckDB database file (e.g., duckdb_databases/financial_data.db)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Also output full schema as JSON to stdout (after markdown)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Save markdown output to a file (e.g., schema.md)"
    )

    args = parser.parse_args()
    db_path = pathlib.Path(args.db_path).resolve()

    if not db_path.exists():
        print(f"Error: File not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to: {db_path}", file=sys.stderr)

    con = duckdb.connect(database=str(db_path), read_only=True)
    try:
        schema = extract_schema(con, db_path)

        # Markdown output
        markdown_output = []
        import io
        f = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = f
        print_schema_markdown(schema)
        sys.stdout = sys_stdout
        markdown_content = f.getvalue()

        if args.output:
            with open(args.output, "w", encoding="utf-8") as out_file:
                out_file.write(markdown_content)
            print(f"Markdown saved to: {args.output}", file=sys.stderr)
        else:
            print(markdown_content)

        # Optional JSON
        if args.json:
            print("\n--- JSON SCHEMA ---\n")
            print(json.dumps(schema, indent=2, default=str))

    finally:
        con.close()


if __name__ == "__main__":
    main()