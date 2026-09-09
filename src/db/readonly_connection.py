"""
The ONLY sanctioned path to the Label Traxx (4D) database.

The supplied 4D account ("designer") has full write privileges and the
database does not enforce read-only access, so this wrapper enforces it
in code:

  - passes readonly=True to pyodbc.connect
  - additionally sets SQL_ATTR_ACCESS_MODE to read-only on the connection
  - inspects every statement before execution and raises unless it begins
    with SELECT after stripping whitespace and comments
  - refuses outright on any occurrence of INSERT, UPDATE, DELETE, DROP,
    ALTER, CREATE, TRUNCATE or EXECUTE as a statement keyword

Do not call pyodbc.connect() anywhere else in this project - go through
ReadOnlyConnection so the guard rails above always apply.
"""

import os
import re

import pyodbc
from dotenv import load_dotenv

# ODBC constants (avoids depending on pyodbc exposing them by name).
SQL_ATTR_ACCESS_MODE = 101
SQL_MODE_READ_ONLY = 1

_FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "EXECUTE",
}

_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_LINE_COMMENT_RE = re.compile(r"--[^\n]*")
_LEADING_KEYWORD_RE = re.compile(r"^\s*([A-Za-z]+)")
_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


class WriteAttemptError(RuntimeError):
    """Raised when a statement other than a plain SELECT is attempted."""


def _strip_comments(sql: str) -> str:
    sql = _BLOCK_COMMENT_RE.sub(" ", sql)
    sql = _LINE_COMMENT_RE.sub(" ", sql)
    return sql


def assert_select_only(sql: str) -> None:
    """Raise WriteAttemptError unless `sql` is a single SELECT statement."""
    cleaned = _strip_comments(sql).strip()
    if not cleaned:
        raise WriteAttemptError("Empty statement is not permitted.")

    match = _LEADING_KEYWORD_RE.match(cleaned)
    leading_keyword = match.group(1).upper() if match else ""
    if leading_keyword != "SELECT":
        raise WriteAttemptError(
            f"Only SELECT statements are permitted; statement begins with "
            f"{leading_keyword!r}."
        )

    tokens = {tok.upper() for tok in _WORD_RE.findall(cleaned)}
    forbidden_hit = tokens & _FORBIDDEN_KEYWORDS
    if forbidden_hit:
        raise WriteAttemptError(
            f"Statement contains forbidden keyword(s): "
            f"{', '.join(sorted(forbidden_hit))}."
        )


class ReadOnlyConnection:
    """Context-manager wrapper around a read-only pyodbc connection to LT64."""

    def __init__(self, dsn=None, user=None, password=None, timeout=30):
        load_dotenv()
        self._dsn = dsn or os.environ["LT_DSN"]
        self._user = user or os.environ["LT_USER"]
        self._password = password if password is not None else os.environ["LT_PASSWORD"]
        self._timeout = timeout
        self._conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def connect(self):
        if self._conn is not None:
            return
        self._conn = pyodbc.connect(
            dsn=self._dsn,
            uid=self._user,
            pwd=self._password,
            timeout=self._timeout,
            readonly=True,
            attrs_before={SQL_ATTR_ACCESS_MODE: SQL_MODE_READ_ONLY},
        )

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def execute(self, sql: str, params=None):
        """Validate `sql` as SELECT-only, then execute it and return the cursor."""
        assert_select_only(sql)
        if self._conn is None:
            self.connect()
        cursor = self._conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor

    def list_tables(self):
        """Catalog metadata only (SQLTables) - inherently read-only, no SQL text involved."""
        if self._conn is None:
            self.connect()
        return list(self._conn.cursor().tables())

    def list_columns(self, table=None):
        """Catalog metadata only (SQLColumns) - inherently read-only, no SQL text involved."""
        if self._conn is None:
            self.connect()
        return list(self._conn.cursor().columns(table=table))
