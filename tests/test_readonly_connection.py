import pytest

from src.db.readonly_connection import (
    SQL_ATTR_ACCESS_MODE,
    SQL_MODE_READ_ONLY,
    ReadOnlyConnection,
    WriteAttemptError,
    assert_select_only,
)


# --- assert_select_only: the statement guard used before every execute() ---

@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO Ticket (JobNumber) VALUES (1)",
        "UPDATE Ticket SET Quantity = 0",
        "DELETE FROM Ticket WHERE JobNumber = 1",
        "DROP TABLE Ticket",
        "ALTER TABLE Ticket ADD COLUMN Foo INT",
        "CREATE TABLE Foo (id INT)",
        "TRUNCATE TABLE Ticket",
        "EXECUTE some_procedure()",
        "  \n  insert into Ticket values (1)",
        "-- comment\nINSERT INTO Ticket VALUES (1)",
        "/* block comment */ DELETE FROM Ticket",
        "SELECT * FROM Ticket; DROP TABLE Ticket",
        "",
        "   ",
    ],
)
def test_write_and_invalid_statements_are_rejected(sql):
    with pytest.raises(WriteAttemptError):
        assert_select_only(sql)


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT * FROM Ticket WHERE JobNumber = 122984",
        "select JobNumber, Quantity from Ticket",
        "  SELECT TOP 1 * FROM Product WHERE ItemNumber = 233458",
        "-- fetch one ticket\nSELECT * FROM Ticket WHERE JobNumber = 122984",
        "/* header */\nSELECT * FROM Ticket LIMIT 1",
    ],
)
def test_select_statements_are_accepted(sql):
    assert_select_only(sql)  # should not raise


def test_execute_rejects_write_before_touching_the_connection(monkeypatch):
    """
    A write attempt must be rejected before pyodbc.connect is ever called -
    this is what makes ReadOnlyConnection the only path to the database
    even though the underlying account has full write privileges.
    """
    def _fail_if_called(*args, **kwargs):
        raise AssertionError("pyodbc.connect must not be called for a rejected statement")

    monkeypatch.setattr("src.db.readonly_connection.pyodbc.connect", _fail_if_called)

    conn = ReadOnlyConnection(dsn="LT64", user="designer", password="unused")
    with pytest.raises(WriteAttemptError):
        conn.execute("DELETE FROM Ticket WHERE JobNumber = 122984")


def test_connect_requests_readonly_access(monkeypatch):
    """pyodbc.connect must be asked for readonly=True and SQL_ATTR_ACCESS_MODE."""
    captured = {}

    class _FakeConn:
        def close(self):
            pass

    def _fake_connect(**kwargs):
        captured.update(kwargs)
        return _FakeConn()

    monkeypatch.setattr("src.db.readonly_connection.pyodbc.connect", _fake_connect)

    conn = ReadOnlyConnection(dsn="LT64", user="designer", password="unused")
    conn.connect()

    assert captured["readonly"] is True
    assert captured["attrs_before"] == {SQL_ATTR_ACCESS_MODE: SQL_MODE_READ_ONLY}
    conn.close()


def test_list_tables_and_list_columns_use_catalog_calls_not_raw_sql(monkeypatch):
    """
    list_tables/list_columns must go through SQLTables/SQLColumns (catalog
    metadata), never through cursor.execute with a hand-built SQL string -
    that's what lets them stay read-only by construction.
    """
    calls = {"tables": 0, "columns": 0}

    class _FakeCursor:
        def tables(self):
            calls["tables"] += 1
            return iter([("cat", "schema", "Ticket", "TABLE", None)])

        def columns(self, table=None):
            calls["columns"] += 1
            assert table == "Ticket"
            return iter([("cat", "schema", "Ticket", "JobNumber", 4, "INTEGER")])

        def execute(self, *a, **kw):
            raise AssertionError("execute() must not be used for catalog metadata")

    class _FakeConn:
        def cursor(self):
            return _FakeCursor()

        def close(self):
            pass

    monkeypatch.setattr(
        "src.db.readonly_connection.pyodbc.connect", lambda **kw: _FakeConn()
    )

    conn = ReadOnlyConnection(dsn="LT64", user="designer", password="unused")
    tables = conn.list_tables()
    columns = conn.list_columns(table="Ticket")

    assert calls == {"tables": 1, "columns": 1}
    assert tables[0][2] == "Ticket"
    assert columns[0][3] == "JobNumber"
