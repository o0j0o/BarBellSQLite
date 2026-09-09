from src.batch import build_batch_number


def test_build_batch_number_concatenates_with_no_separator():
    assert build_batch_number("122984", "233458") == "122984233458"


def test_build_batch_number_preserves_alphanumeric_job_numbers():
    """
    Ticket.Number is alphanumeric text coming out of Label Traxx, not a numeric
    string that happens to be stored as CLOB - job numbers can contain letters,
    so this must never cast to int, strip leading zeros, or reformat.
    """
    assert build_batch_number("A12984B", "233458") == "A12984B233458"
    assert build_batch_number("012984", "233458") == "012984233458"
