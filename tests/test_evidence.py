from evidence.compare import compare_message_with_evidence
from evidence.models import Evidence

def test_mismatched_invoice():
    ev = Evidence(source="invoice.txt", text="Order ORD-1234 Amount ₹999", order_id="ORD-1234", amount="₹999", quality=1.0)
    conflicts, _ = compare_message_with_evidence("My order is ORD-9999 and amount is ₹999", [ev])
    assert conflicts

def test_blurred_image_requests_clarification():
    ev = Evidence(source="photo.jpg", text="", quality=0.1)
    _, clarification = compare_message_with_evidence("check this invoice", [ev])
    assert clarification

def test_missing_values_are_not_invented():
    ev = Evidence(source="invoice.txt", text="Product: Laptop", product="Laptop")
    _, clarification = compare_message_with_evidence("What is the order ID?", [ev])
    assert clarification
