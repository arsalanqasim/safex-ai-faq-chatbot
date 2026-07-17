"""Streamlit UI for the Week 2 invoice automation module."""

from __future__ import annotations

from decimal import Decimal

import pandas as pd
import streamlit as st

from src.modules.invoice_automation.engine import Customer, InvoiceAutomationEngine, LineItem
from src.modules.registry import MODULE_REGISTRY


SAMPLE_ORDER = """Website audit, 1, 25000
Monthly SEO retainer, 2, 18000
Support package, 3, 7500"""


def _build_line_items_from_editor(rows: list[dict[str, object]]) -> list[LineItem]:
    items: list[LineItem] = []
    for row in rows:
        description = str(row.get("description", "")).strip()
        if not description:
            continue
        quantity = Decimal(str(row.get("quantity", 0) or 0))
        unit_price = Decimal(str(row.get("unit_price", 0) or 0))
        items.append(LineItem(description=description, quantity=quantity, unit_price=unit_price))
    return items


def _line_items_dataframe(items: list[LineItem]) -> pd.DataFrame:
    return pd.DataFrame([item.to_dict() for item in items])


def render_ui() -> None:
    """Render the invoice automation workflow."""
    metadata = MODULE_REGISTRY["week2"]["invoice_automation"]

    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">Business Automation Research</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Assigned to: <strong>{metadata["developer"]}</strong> ({metadata["role"]})
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        f"**Status:** {metadata['status']}  \n"
        f"**Difficulty Level:** {metadata['difficulty']}  \n"
        f"**Stack:** {', '.join(metadata['tech'])}"
    )
    st.write(metadata["description"])

    engine = InvoiceAutomationEngine()

    st.markdown("### 1. Customer Details")
    customer_col_1, customer_col_2 = st.columns(2)
    with customer_col_1:
        customer_name = st.text_input("Customer name", value="NorthStar Retail")
        customer_email = st.text_input("Customer email", value="billing@northstar.example")
    with customer_col_2:
        customer_phone = st.text_input("Customer phone", value="+92 300 0000000")
        customer_address = st.text_area("Billing address", value="Blue Area, Islamabad", height=88)

    st.markdown("### 2. Line Items")
    input_mode = st.radio(
        "Input mode",
        ["Editable table", "Paste order text"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if input_mode == "Editable table":
        starting_rows = pd.DataFrame(
            [
                {"description": "Website audit", "quantity": 1, "unit_price": 25000},
                {"description": "Monthly SEO retainer", "quantity": 2, "unit_price": 18000},
                {"description": "Support package", "quantity": 3, "unit_price": 7500},
            ]
        )
        edited_rows = st.data_editor(
            starting_rows,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "description": st.column_config.TextColumn("Description", required=True),
                "quantity": st.column_config.NumberColumn("Quantity", min_value=0.01, step=1.0, required=True),
                "unit_price": st.column_config.NumberColumn("Unit price (PKR)", min_value=0.0, step=500.0, required=True),
            },
            key="invoice_line_items_editor",
        )
        line_items = _build_line_items_from_editor(edited_rows.to_dict("records"))
    else:
        order_text = st.text_area(
            "Order text",
            value=SAMPLE_ORDER,
            height=150,
            help="Supported: 'Description, quantity, unit price' or '2 x Service @ 10000'.",
        )
        try:
            line_items = engine.parse_order_text(order_text)
            st.success(f"Parsed {len(line_items)} line item(s).")
        except ValueError as exc:
            line_items = []
            st.error(str(exc))

    if line_items:
        st.dataframe(_line_items_dataframe(line_items), use_container_width=True, hide_index=True)

    st.markdown("### 3. Terms and Delivery")
    terms_col_1, terms_col_2, terms_col_3, terms_col_4 = st.columns(4)
    with terms_col_1:
        tax_rate = st.number_input("Tax rate %", min_value=0.0, max_value=100.0, value=16.0, step=0.5)
    with terms_col_2:
        discount_rate = st.number_input("Discount %", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
    with terms_col_3:
        payment_terms = st.number_input("Payment terms (days)", min_value=0, max_value=90, value=7, step=1)
    with terms_col_4:
        channel = st.selectbox("Delivery channel", ["Email", "WhatsApp", "SMS"])

    notes = st.text_area(
        "Invoice notes",
        value="Payment is due by the listed date. This invoice was generated through the SafeX invoice automation module.",
        height=90,
    )

    if st.button("Generate invoice", type="primary", key="generate_invoice_button"):
        try:
            customer = Customer(
                name=customer_name,
                email=customer_email,
                phone=customer_phone,
                address=customer_address,
            )
            invoice = engine.create_invoice(
                customer=customer,
                line_items=line_items,
                tax_rate=tax_rate,
                discount_rate=discount_rate,
                payment_terms_days=int(payment_terms),
                notes=notes,
                status="Ready for review",
            )
            delivery = engine.prepare_delivery(invoice, channel=channel)
            saved_paths = engine.save_invoice_bundle(invoice, delivery)
            st.session_state["invoice_automation_result"] = {
                "invoice": invoice,
                "delivery": delivery,
                "saved_paths": saved_paths,
            }
        except ValueError as exc:
            st.error(str(exc))

    result = st.session_state.get("invoice_automation_result")
    if result:
        invoice = result["invoice"]
        delivery = result["delivery"]
        saved_paths = result["saved_paths"]

        st.markdown("### 4. Invoice Review")
        metric_1, metric_2, metric_3, metric_4 = st.columns(4)
        metric_1.metric("Invoice No.", invoice.invoice_number)
        metric_2.metric("Subtotal", f"PKR {invoice.subtotal:.2f}")
        metric_3.metric("Tax", f"PKR {invoice.tax_amount:.2f}")
        metric_4.metric("Total Due", f"PKR {invoice.total:.2f}")

        st.dataframe(_line_items_dataframe(list(invoice.line_items)), use_container_width=True, hide_index=True)

        with st.expander("Invoice JSON", expanded=False):
            st.json(invoice.to_dict())

        with st.expander("Prepared delivery message", expanded=True):
            st.write(f"**Channel:** {delivery.channel}")
            st.write(f"**Recipient:** {delivery.recipient}")
            st.write(f"**Subject:** {delivery.subject}")
            st.code(delivery.body, language="text")

        st.markdown("### 5. Exported Files")
        for label, path in saved_paths.items():
            st.write(f"- **{label.replace('_', ' ').title()}:** `{path}`")

        printable_html = engine.render_invoice_html(invoice)
        st.download_button(
            "Download printable invoice HTML",
            data=printable_html,
            file_name=f"{invoice.invoice_number.lower()}.html",
            mime="text/html",
        )
