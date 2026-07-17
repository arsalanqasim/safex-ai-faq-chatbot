from decimal import Decimal

import pytest

from src.modules.invoice_automation.engine import Customer, InvoiceAutomationEngine, LineItem


def test_invoice_totals_include_discount_and_tax(tmp_path):
    engine = InvoiceAutomationEngine(output_dir=tmp_path)
    invoice = engine.create_invoice(
        customer=Customer(name="SafeX Client", email="client@example.com"),
        line_items=[
            LineItem("Automation setup", Decimal("2"), Decimal("10000")),
            LineItem("Support", Decimal("1"), Decimal("5000")),
        ],
        tax_rate=Decimal("10"),
        discount_rate=Decimal("20"),
        payment_terms_days=5,
    )

    assert invoice.subtotal == Decimal("25000.00")
    assert invoice.discount_amount == Decimal("5000.00")
    assert invoice.tax_amount == Decimal("2000.00")
    assert invoice.total == Decimal("22000.00")


def test_parse_order_text_supports_multiple_formats(tmp_path):
    engine = InvoiceAutomationEngine(output_dir=tmp_path)
    items = engine.parse_order_text(
        "Website audit, 1, 25000\n"
        "2 x SEO setup @ 12000\n"
        "Logo design - qty 1 - price 8000"
    )

    assert len(items) == 3
    assert items[0].description == "Website audit"
    assert items[1].quantity == Decimal("2.00")
    assert items[2].unit_price == Decimal("8000.00")


def test_save_invoice_bundle_writes_expected_files(tmp_path):
    engine = InvoiceAutomationEngine(output_dir=tmp_path)
    invoice = engine.create_invoice(
        customer=Customer(name="SafeX Client", email="client@example.com"),
        line_items=[LineItem("Automation setup", Decimal("1"), Decimal("10000"))],
    )
    delivery = engine.prepare_delivery(invoice, channel="Email")

    paths = engine.save_invoice_bundle(invoice, delivery)

    assert set(paths) == {"invoice_json", "line_items_csv", "printable_html", "delivery_json"}
    for path in paths.values():
        assert tmp_path.joinpath(path.split(str(tmp_path))[-1].lstrip("\\/")).exists()


def test_customer_validation_rejects_bad_email(tmp_path):
    engine = InvoiceAutomationEngine(output_dir=tmp_path)

    with pytest.raises(ValueError, match="email"):
        engine.create_invoice(
            customer=Customer(name="SafeX Client", email="not-valid"),
            line_items=[LineItem("Automation setup", Decimal("1"), Decimal("10000"))],
        )
