from app.utils.hash_utils import calculate_content_hash


def test_hash_is_deterministic():
    text = "VPN; reset hasla; kategoria: network"

    first = calculate_content_hash(text)
    second = calculate_content_hash(text)

    assert first == second


def test_hash_changes_when_content_changes():
    baseline = calculate_content_hash("Tytul A\nTresc A\nTagi: vpn")
    changed = calculate_content_hash("Tytul A\nTresc B\nTagi: vpn")

    assert baseline != changed