"""Invoice automation workflow for Arsalan Qasim's Week 2 module."""

from __future__ import annotations

import csv
import html
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable
from uuid import uuid4


MONEY = Decimal("0.01")


def _money(value: Decimal | float | int | str) -> Decimal:
    """Return a Decimal rounded to two places for invoice calculations."""
    return Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class LineItem:
    """Single invoice line item."""

    description: str
    quantity: Decimal
    unit_price: Decimal

    @property
    def subtotal(self) -> Decimal:
        """Line subtotal before invoice-level tax or discount."""
        return _money(self.quantity * self.unit_price)

    def to_dict(self) -> dict[str, str]:
        """Serialize the line item using display-safe string values."""
        return {
            "description": self.description,
            "quantity": str(self.quantity.normalize()),
            "unit_price": f"{self.unit_price:.2f}",
            "subtotal": f"{self.subtotal:.2f}",
        }


@dataclass(frozen=True)
class Customer:
    """Customer billing details."""

    name: str
    email: str = ""
    phone: str = ""
    address: str = ""


@dataclass(frozen=True)
class Invoice:
    """Calculated invoice document."""

    invoice_number: str
    issue_date: date
    due_date: date
    customer: Customer
    line_items: tuple[LineItem, ...]
    tax_rate: Decimal = Decimal("0")
    discount_rate: Decimal = Decimal("0")
    notes: str = ""
    status: str = "Draft"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def subtotal(self) -> Decimal:
        return _money(sum((item.subtotal for item in self.line_items), Decimal("0")))

    @property
    def discount_amount(self) -> Decimal:
        return _money(self.subtotal * self.discount_rate / Decimal("100"))

    @property
    def taxable_amount(self) -> Decimal:
        return _money(self.subtotal - self.discount_amount)

    @property
    def tax_amount(self) -> Decimal:
        return _money(self.taxable_amount * self.tax_rate / Decimal("100"))

    @property
    def total(self) -> Decimal:
        return _money(self.taxable_amount + self.tax_amount)

    def to_dict(self) -> dict[str, object]:
        """Serialize the invoice for JSON export or UI display."""
        return {
            "invoice_number": self.invoice_number,
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "customer": asdict(self.customer),
            "line_items": [item.to_dict() for item in self.line_items],
            "subtotal": f"{self.subtotal:.2f}",
            "discount_rate": f"{self.discount_rate:.2f}",
            "discount_amount": f"{self.discount_amount:.2f}",
            "tax_rate": f"{self.tax_rate:.2f}",
            "tax_amount": f"{self.tax_amount:.2f}",
            "total": f"{self.total:.2f}",
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(timespec="seconds"),
        }


@dataclass(frozen=True)
class DeliveryMessage:
    """Prepared delivery message for an invoice."""

    channel: str
    recipient: str
    subject: str
    body: str
    status: str
    reference: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, str]:
        return {
            "channel": self.channel,
            "recipient": self.recipient,
            "subject": self.subject,
            "body": self.body,
            "status": self.status,
            "reference": self.reference,
            "created_at": self.created_at.isoformat(timespec="seconds"),
        }


class InvoiceAutomationEngine:
    """Create, calculate, export, and prepare delivery for invoices."""

    def __init__(self, output_dir: str | Path | None = None) -> None:
        self.output_dir = Path(output_dir or Path.cwd() / "outputs" / "invoice_automation")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def parse_order_text(self, order_text: str) -> list[LineItem]:
        """Parse simple order text into line items."""
        items: list[LineItem] = []
        for raw_line in order_text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            item = self._parse_order_line(line)
            if item is None:
                raise ValueError(
                    "Could not parse line item. Use 'Description, quantity, unit price' "
                    f"or '2 x Description @ price'. Problem line: {line}"
                )
            items.append(item)

        self.validate_line_items(items)
        return items

    def create_invoice(
        self,
        customer: Customer,
        line_items: Iterable[LineItem],
        tax_rate: Decimal | float | int | str = Decimal("0"),
        discount_rate: Decimal | float | int | str = Decimal("0"),
        payment_terms_days: int = 7,
        issue_date: date | None = None,
        notes: str = "",
        status: str = "Draft",
    ) -> Invoice:
        """Create a calculated invoice from customer and line-item details."""
        clean_items = tuple(line_items)
        self.validate_customer(customer)
        self.validate_line_items(clean_items)

        clean_tax = self._validate_rate(tax_rate, "tax_rate")
        clean_discount = self._validate_rate(discount_rate, "discount_rate")
        if payment_terms_days < 0:
            raise ValueError("payment_terms_days cannot be negative.")

        invoice_date = issue_date or date.today()
        return Invoice(
            invoice_number=self.generate_invoice_number(invoice_date),
            issue_date=invoice_date,
            due_date=invoice_date + timedelta(days=payment_terms_days),
            customer=customer,
            line_items=clean_items,
            tax_rate=clean_tax,
            discount_rate=clean_discount,
            notes=notes.strip(),
            status=status,
        )

    def prepare_delivery(self, invoice: Invoice, channel: str = "Email") -> DeliveryMessage:
        """Prepare a delivery message without calling external APIs."""
        normalized_channel = channel.strip().title()
        if normalized_channel not in {"Email", "Whatsapp", "Sms"}:
            raise ValueError("channel must be Email, WhatsApp, or SMS.")

        recipient = invoice.customer.email if normalized_channel == "Email" else invoice.customer.phone
        if not recipient:
            recipient = "recipient-not-provided"

        subject = f"Invoice {invoice.invoice_number} from SafeX Solutions"
        body = (
            f"Dear {invoice.customer.name},\n\n"
            f"Your invoice {invoice.invoice_number} has been prepared.\n"
            f"Amount due: PKR {invoice.total:.2f}\n"
            f"Due date: {invoice.due_date.isoformat()}\n\n"
            "Thank you,\nSafeX Solutions"
        )
        return DeliveryMessage(
            channel=normalized_channel,
            recipient=recipient,
            subject=subject,
            body=body,
            status="Prepared for delivery",
            reference=f"MSG-{uuid4().hex[:10].upper()}",
        )

    def save_invoice_bundle(self, invoice: Invoice, delivery: DeliveryMessage | None = None) -> dict[str, str]:
        """Save invoice JSON, CSV line items, printable HTML, and delivery JSON."""
        slug = invoice.invoice_number.lower()
        json_path = self.output_dir / f"{slug}.json"
        csv_path = self.output_dir / f"{slug}_items.csv"
        html_path = self.output_dir / f"{slug}.html"

        json_path.write_text(json.dumps(invoice.to_dict(), indent=2), encoding="utf-8")
        self._write_line_items_csv(csv_path, invoice)
        html_path.write_text(self.render_invoice_html(invoice), encoding="utf-8")

        paths = {
            "invoice_json": str(json_path),
            "line_items_csv": str(csv_path),
            "printable_html": str(html_path),
        }

        if delivery is not None:
            delivery_path = self.output_dir / f"{slug}_delivery.json"
            delivery_path.write_text(json.dumps(delivery.to_dict(), indent=2), encoding="utf-8")
            paths["delivery_json"] = str(delivery_path)

        return paths

    def render_invoice_html(self, invoice: Invoice) -> str:
        """Render a printable invoice as standalone HTML."""
        rows = "\n".join(
            "<tr>"
            f"<td>{html.escape(item.description)}</td>"
            f"<td>{item.quantity}</td>"
            f"<td>PKR {item.unit_price:.2f}</td>"
            f"<td>PKR {item.subtotal:.2f}</td>"
            "</tr>"
            for item in invoice.line_items
        )
        notes = html.escape(invoice.notes) if invoice.notes else "Thank you for your business."
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(invoice.invoice_number)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; color: #172033; margin: 40px; }}
    .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #1f6feb; padding-bottom: 18px; }}
    .brand {{ font-size: 24px; font-weight: 700; }}
    .muted {{ color: #5f6b7a; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 28px; }}
    th, td {{ border-bottom: 1px solid #d7dde6; padding: 10px; text-align: left; }}
    th {{ background: #f3f6fb; }}
    .totals {{ width: 340px; margin-left: auto; margin-top: 24px; }}
    .totals div {{ display: flex; justify-content: space-between; padding: 7px 0; }}
    .total {{ font-size: 20px; font-weight: 700; color: #1f6feb; border-top: 2px solid #1f6feb; }}
  </style>
</head>
<body>
  <section class="header">
    <div>
      <div class="brand">SafeX Solutions</div>
      <div class="muted">Business Automation Research - Invoice Module</div>
    </div>
    <div>
      <strong>Invoice:</strong> {html.escape(invoice.invoice_number)}<br>
      <strong>Issue date:</strong> {invoice.issue_date.isoformat()}<br>
      <strong>Due date:</strong> {invoice.due_date.isoformat()}<br>
      <strong>Status:</strong> {html.escape(invoice.status)}
    </div>
  </section>
  <section>
    <h3>Bill To</h3>
    <p>
      <strong>{html.escape(invoice.customer.name)}</strong><br>
      {html.escape(invoice.customer.email)}<br>
      {html.escape(invoice.customer.phone)}<br>
      {html.escape(invoice.customer.address)}
    </p>
  </section>
  <table>
    <thead>
      <tr><th>Description</th><th>Qty</th><th>Unit Price</th><th>Subtotal</th></tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
  <section class="totals">
    <div><span>Subtotal</span><span>PKR {invoice.subtotal:.2f}</span></div>
    <div><span>Discount ({invoice.discount_rate:.2f}%)</span><span>PKR {invoice.discount_amount:.2f}</span></div>
    <div><span>Tax ({invoice.tax_rate:.2f}%)</span><span>PKR {invoice.tax_amount:.2f}</span></div>
    <div class="total"><span>Total</span><span>PKR {invoice.total:.2f}</span></div>
  </section>
  <section>
    <h3>Notes</h3>
    <p>{notes}</p>
  </section>
</body>
</html>
"""

    def generate_invoice_number(self, invoice_date: date | None = None) -> str:
        """Generate a short unique invoice number."""
        invoice_date = invoice_date or date.today()
        return f"INV-{invoice_date:%Y%m%d}-{uuid4().hex[:6].upper()}"

    def validate_customer(self, customer: Customer) -> None:
        if not customer.name.strip():
            raise ValueError("Customer name is required.")
        if customer.email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", customer.email):
            raise ValueError("Customer email is not valid.")

    def validate_line_items(self, line_items: Iterable[LineItem]) -> None:
        items = list(line_items)
        if not items:
            raise ValueError("At least one line item is required.")
        for item in items:
            if not item.description.strip():
                raise ValueError("Line item description is required.")
            if item.quantity <= 0:
                raise ValueError("Line item quantity must be greater than zero.")
            if item.unit_price < 0:
                raise ValueError("Line item unit price cannot be negative.")

    def _parse_order_line(self, line: str) -> LineItem | None:
        comma_match = re.match(r"^\s*(?P<desc>.+?)\s*,\s*(?P<qty>\d+(?:\.\d+)?)\s*,\s*(?P<price>\d+(?:\.\d+)?)\s*$", line)
        if comma_match:
            return LineItem(comma_match.group("desc").strip(), _money(comma_match.group("qty")), _money(comma_match.group("price")))

        x_match = re.match(r"^\s*(?P<qty>\d+(?:\.\d+)?)\s*x\s*(?P<desc>.+?)\s*@\s*(?P<price>\d+(?:\.\d+)?)\s*$", line, re.IGNORECASE)
        if x_match:
            return LineItem(x_match.group("desc").strip(), _money(x_match.group("qty")), _money(x_match.group("price")))

        labeled_match = re.match(r"^\s*(?P<desc>.+?)\s*-\s*qty\s*(?P<qty>\d+(?:\.\d+)?)\s*-\s*price\s*(?P<price>\d+(?:\.\d+)?)\s*$", line, re.IGNORECASE)
        if labeled_match:
            return LineItem(labeled_match.group("desc").strip(), _money(labeled_match.group("qty")), _money(labeled_match.group("price")))

        return None

    def _validate_rate(self, value: Decimal | float | int | str, name: str) -> Decimal:
        rate = _money(value)
        if rate < 0 or rate > 100:
            raise ValueError(f"{name} must be between 0 and 100.")
        return rate

    def _write_line_items_csv(self, path: Path, invoice: Invoice) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["invoice_number", "description", "quantity", "unit_price", "subtotal"])
            writer.writeheader()
            for item in invoice.line_items:
                row = item.to_dict()
                row["invoice_number"] = invoice.invoice_number
                writer.writerow(row)
