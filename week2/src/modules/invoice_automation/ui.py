"""Streamlit UI for the Week 2 invoice automation module."""

from __future__ import annotations

from decimal import Decimal

import pandas as pd
import streamlit as st

from src.modules.invoice_automation.engine import Customer, InvoiceAutomationEngine, LineItem


SAMPLE_ORDER = """Website audit, 1, 25000
Monthly SEO retainer, 2, 18000
Support package, 3, 7500"""


def _build_line_items(rows: list[dict[str, object]]) -> list[LineItem]:
    """Convert editable table rows into validated invoice line items."""
    items: list[LineItem] = []
    for row in rows:
        description = str(row.get("description", "")).strip()
        if description:
            items.append(
                LineItem(
                    description=description,
                    quantity=Decimal(str(row.get("quantity", 0) or 0)),
                    unit_price=Decimal(str(row.get("unit_price", 0) or 0)),
                )
            )
    return items


def _items_frame(items: list[LineItem]) -> pd.DataFrame:
    return pd.DataFrame([item.to_dict() for item in items])


def render_ui() -> None:
    """Render Arsalan Qasim's submission-ready invoice workflow."""
    engine = InvoiceAutomationEngine()

    st.markdown('<div class="eyebrow">Week 2 · Business automation</div>', unsafe_allow_html=True)
    st.title("Invoice automation")
    st.caption("Create a customer invoice, review the calculated totals, and export a printable record.")

    with st.expander("Module details", expanded=False):
        st.write("Owner: Arsalan Qasim")
        st.write("Status: Submission ready")
        st.write("Local workflow: invoice calculation, export bundle, and delivery-message preparation.")

    st.subheader("Customer")
    left, right = st.columns(2)
    with left:
        customer_name = st.text_input("Customer name", value="NorthStar Retail")
        customer_email = st.text_input("Email", value="billing@northstar.example")
    with right:
        customer_phone = st.text_input("Phone", value="+92 300 0000000")
        customer_address = st.text_area("Billing address", value="Blue Area, Islamabad", height=94)

    st.subheader("Items")
    input_mode = st.radio("Item entry", ["Table", "Paste order"], horizontal=True, label_visibility="collapsed")
    if input_mode == "Table":
        default_items = pd.DataFrame(
            [
                {"description": "Website audit", "quantity": 1, "unit_price": 25000},
                {"description": "Monthly SEO retainer", "quantity": 2, "unit_price": 18000},
                {"description": "Support package", "quantity": 3, "unit_price": 7500},
            ]
        )
        edited_items = st.data_editor(
            default_items,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="invoice_line_items_editor",
            column_config={
                "description": st.column_config.TextColumn("Description", required=True),
                "quantity": st.column_config.NumberColumn("Quantity", min_value=0.01, step=1.0, required=True),
                "unit_price": st.column_config.NumberColumn("Unit price (PKR)", min_value=0.0, step=500.0, required=True),
            },
        )
        line_items = _build_line_items(edited_items.to_dict("records"))
    else:
        order_text = st.text_area("Order details", value=SAMPLE_ORDER, height=132, help="Use: Description, quantity, unit price")
        try:
            line_items = engine.parse_order_text(order_text)
            st.caption(f"{len(line_items)} items ready for invoicing")
        except ValueError as exc:
            line_items = []
            st.error(str(exc))

    st.subheader("Terms")
    term_one, term_two, term_three, term_four = st.columns(4)
    with term_one:
        tax_rate = st.number_input("Tax rate (%)", 0.0, 100.0, 16.0, 0.5)
    with term_two:
        discount_rate = st.number_input("Discount (%)", 0.0, 100.0, 0.0, 0.5)
    with term_three:
        payment_terms = st.number_input("Payment terms (days)", 0, 90, 7, 1)
    with term_four:
        channel = st.selectbox("Delivery channel", ["Email", "WhatsApp", "SMS"])
    notes = st.text_area("Notes", value="Payment is due by the listed date.", height=80)

    if st.button("Generate invoice", type="primary", key="generate_invoice_button"):
        try:
            invoice = engine.create_invoice(
                customer=Customer(customer_name, customer_email, customer_phone, customer_address),
                line_items=line_items,
                tax_rate=tax_rate,
                discount_rate=discount_rate,
                payment_terms_days=int(payment_terms),
                notes=notes,
                status="Ready for review",
            )
            delivery = engine.prepare_delivery(invoice, channel=channel)
            st.session_state.invoice_automation_result = {
                "invoice": invoice,
                "delivery": delivery,
                "saved_paths": engine.save_invoice_bundle(invoice, delivery),
            }
        except ValueError as exc:
            st.error(str(exc))

    result = st.session_state.get("invoice_automation_result")
    if not result:
        return

    invoice = result["invoice"]
    delivery = result["delivery"]
    st.divider()
    st.subheader("Invoice review")
    number, subtotal, tax, total = st.columns(4)
    number.metric("Invoice", invoice.invoice_number)
    subtotal.metric("Subtotal", f"PKR {invoice.subtotal:,.2f}")
    tax.metric("Tax", f"PKR {invoice.tax_amount:,.2f}")
    total.metric("Total due", f"PKR {invoice.total:,.2f}")
    st.dataframe(_items_frame(list(invoice.line_items)), use_container_width=True, hide_index=True)

    review_left, review_right = st.columns(2)
    with review_left:
        with st.expander("Delivery message", expanded=True):
            st.caption(f"{delivery.channel} · {delivery.recipient}")
            st.code(delivery.body, language="text")
    with review_right:
        with st.expander("Invoice data", expanded=False):
            st.json(invoice.to_dict())

    st.subheader("Exports")
    st.download_button(
        "Download printable invoice",
        data=engine.render_invoice_html(invoice),
        file_name=f"{invoice.invoice_number.lower()}.html",
        mime="text/html",
    )
    st.caption("Saved locally: " + " · ".join(result["saved_paths"].values()))
