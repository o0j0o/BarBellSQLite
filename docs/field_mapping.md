# Field Mapping (Label Traxx -> BarBell)

Grounded in the real rows pulled for job **122984** / item **233458** (the sample-label
ground truth). All ID-like columns below are `CLOB` (text) even where the values look
numeric - always quote them as strings in `WHERE` clauses (see
[label_traxx_schema.md](label_traxx_schema.md)).

Three tables are involved, joined in Python (the 4D SQL server doesn't do joins):

- **`Ticket`** - the job itself. Primary key `Number`.
- **`Product`** - the item master. Primary key `ProdNum` (Label Traxx's own internal item
  number - this is `'47388'`, NOT `233458`; see the "Item number" note below).
- **`TicketItem`** - the line linking a `Ticket` to a `Product`, one row per job/item pair.
  Join: `TicketItem.TicketNumber = Ticket.Number` and
  `TicketItem.ProductNumber = Product.ProdNum`.

## Job number

- **Column: `Ticket.Number`** - the primary key of `Ticket`.
- Sample value: `'122984'` - exact match to the job number given.
- Also echoed on `TicketItem.TicketNumber` for the join.
- **Confirmed by the user: this is genuinely alphanumeric text coming out of Label Traxx**,
  not just a numeric string that happens to be stored as CLOB. `'122984'` only looks
  numeric because that's this particular job - other jobs may contain letters. Don't cast
  it to an int, strip leading zeros, or apply numeric padding/formatting anywhere
  downstream; treat it as an opaque string end to end.

## Item number and ProductNo ("P/N") - two distinct fields, confirmed by the user

Both are kept on every label row; they feed different things:

- **`Product.ProdNum`** (e.g. `'47388'`) - Label Traxx's own internal number. **The user
  confirmed this is what "ProductNo" / "P/N" means** - this is what feeds the batch
  number (see below), NOT the item number.
- **`Product.Name4`** (e.g. `'233458'`) - "item number", a separate field kept on the
  label for its own sake (it also appears as the leading token of
  `Product.Description`, e.g. `'233458 - JWN White O/P Rum B 750Ml USA - PS'`).
  `Name4` is a generic user-defined field slot (4D's `CDF_Definition` table, which
  normally names these custom fields, is empty on this server), so there's no system
  label confirming this beyond the value match - but it's no longer in question for the
  batch, since the user clarified batch uses ProductNo instead.

This **supersedes the earlier "is item number the same as customer part number"
question** (old QUESTIONS.md #2) - they're just two different fields, full stop, and
"P/N" specifically means `ProdNum`.

## Item description

- **Column: `Product.Description`** (also duplicated per-line on `TicketItem.Description`
  and `PackSlipItem.ProdDescr`, same text).
- Sample value: `'233458 - JWN White O/P Rum B 750Ml USA - PS'`.

## Customer

- **Columns: `Ticket.CustomerNum` / `Ticket.CustomerName`** (also `Product.CustNum` /
  `Product.CustName`, same values).
- Sample values: `CustomerNum = 'J00005'`, `CustomerName = 'J. Wray & Nephew Ltd.'`.
- Note: `Ticket.CustPONum` (`'4500912350'`) is the customer's PO number for the job - a
  different thing from the customer part number above; don't confuse the two.

## Quantity ordered

- **Column: `TicketItem.OrderQuantity`** (per job/item line).
- Sample value: `550000`.
- Also echoed at the ticket level as `Ticket.TicQuantity` (same value, `550000`, for this
  single-item job) and `Ticket.ActQuantity` (`547000`, the actual/produced quantity - not
  the ordered quantity, don't use this one).

## Production date - SUPERSEDED, no longer sourced from Label Traxx

BarBell now asks the user for the production date directly (see QUESTIONS.md #3) rather
than trusting a guessed column - kept below for historical context only.

- **Decided (for now): `Ticket.PressStat`.** No single column is unambiguously "the"
  production date - this was the best candidate and the user confirmed going with it while
  more jobs get checked. Candidates considered
  on `Ticket` (all real values for job 122984):
  - `OrderDate` = `2026-02-26` (when the job was entered/ordered)
  - `EntryDate` = `2026-02-26` (same as OrderDate here)
  - `PressStat` = `'3/23/2026'` (text field - the date the press step was marked done; this
    is the closest thing to "the date it was actually manufactured")
  - `FinishStat` = `'3/24/2026'` (text field - date the finishing step was marked done)
  - `DateDone` = `2026-08-14`, `DateShipped` = `2026-08-14` (these two match each other but
    are ~5 months after PressStat/FinishStat for this job, so "done"/"shipped" here likely
    reflects a later batch/reprint or backlog clearance, not the original press date)
  - `Ship_by_Date` = `2026-05-01`, `Due_on_Site_Date` = `None` (both are target dates, not
    actuals)
  - `Product.ProdDate` = `2024-07-10` - this is when the *item master* was created, not
    specific to this job run; not a candidate for a per-job production date.
- Stored as text (`'3/23/2026'`), not a real date type - parsing not yet implemented.

## Batch number

- **Corrected 2026-09-09: `Ticket.Number` + `Product.ProdNum` (ProductNo / "P/N"),
  concatenated with no separator - NOT `Product.Name4` (item number).** The user
  explicitly corrected this: "the Batch number is the job number and the product
  number not the itemNumber."
- Example: job `'122984'` + ProductNo `'47388'` -> batch `'12298447388'` (previously,
  incorrectly, computed as `'122984233458'` using the item number - fixed).
- `build_batch_number()` in [`src/batch.py`](../src/batch.py) is unchanged (still just
  concatenates two strings) - what changed is which value `src/labels.py::assemble_label_rows`
  passes as the second argument (`product.prod_num`, not `product.item_number`).
