# Copyright (c) 2025, royalsmb and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    report_per_shift = [
        # Top Section - Sales
        {"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 200},
        {"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 200},
        {"label": _("Shift Time"), "fieldname": "shift_time", "fieldtype": "Data", "width": 200},
        {"label": _("Opening Balance"), "fieldname": "opening_balance", "fieldtype": "Currency", "width": 200},
        {"label": _("Income"), "fieldname": "income", "fieldtype": "Currency", "width": 200},
        {"label": _("Expenditure"), "fieldname": "expenditure", "fieldtype": "Currency", "width": 200},
        {"label": _("Bank Deposit"), "fieldname": "bank_deposit", "fieldtype": "Currency", "width": 200},
        {"label": _("Closing Balance"), "fieldname": "closing_balance", "fieldtype": "Currency", "width": 200}
    ]

    report_per_type = [
        {"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 200},
        {"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 200},
        {"label": _("Type"), "fieldname": "type", "fieldtype": "Data", "width": 200},
        {"label": _("Reference"), "fieldname": "reference", "fieldtype": "Data", "width": 200},
        {"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 200},
        {"label": _("Remark"), "fieldname": "remark", "fieldtype": "Data", "width": 200}
    ]

    if filters.get("report_type") and  filters.get("report_type") == "Report Per Shift":
        return report_per_shift
    return report_per_type

def get_data(filters):
    if filters.get("report_type") and filters.get("report_type") == "Report Per Shift":
        return report_per_shift(filters)
    return report_per_type(filters)

def report_per_type(filters):
    data = []
    
    # Get all shifts for the given date range
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    shift_filters = {
        "date": ["between", [from_date, to_date]]
    }

    if filters.get("shift"):
        shift_filters["name"] = filters.get("shift")

    

    
    
    
    shifts = frappe.get_all(
        "Front Desk Shift",
        filters=shift_filters,
        fields=["name", "opening_cash", "remaining_balance", "user", "date", "shift_type"],
        order_by="date DESC"
    )

    for shift in shifts:
        petty_cash_filters = {"shift": shift.name}
        if filters.get("type"):
            petty_cash_filters["type"] = filters.get("type")
        entries = frappe.get_all(
            "Petty Cash Entry",
            filters=petty_cash_filters,
            fields=["name", "amount", "remark", "type", "expense_type", "income_type"]
        )

        for entry in entries:
            reference = entry.income_type if entry.type == "Income" else entry.expense_type

            data.append({
                "date": shift.date,
                "shift": shift.user,
                "type": entry.type,
                "reference": reference,
                "amount": entry.amount,
                "remark": entry.remark,
                "shift_time": shift.shift_type,
            })

    return data

def report_per_shift(filters):
    data = []

    # Get all shifts for the given date range
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    shift_filters = {
        "date": ["between", [from_date, to_date]]
    }

    if filters.get("shift"):
        shift_filters["name"] = filters.get("shift")

    shifts = frappe.get_all(
        "Front Desk Shift",
        filters=shift_filters,
        fields=["name", "opening_cash", "remaining_balance", "user", "date"],
        order_by="date DESC"
    )

    for shift in shifts:
        row = get_shift_summary(shift.name)
        data.append(row)

    return data

# Report per shift calculation
def get_shift_summary(shift_name):
    shift = frappe.get_doc("Front Desk Shift", shift_name)

    income = frappe.db.sql("""
        SELECT SUM(amount) 
        FROM `tabPetty Cash Entry` 
        WHERE shift = %s AND type = 'Income'
    """, shift_name)[0][0] or 0

    expenditure = frappe.db.sql("""
        SELECT SUM(amount) 
        FROM `tabPetty Cash Entry` 
        WHERE shift = %s AND type = 'Expense'
    """, shift_name)[0][0] or 0

    bank_deposit = frappe.db.sql("""
        SELECT SUM(amount) 
        FROM `tabPetty Cash Entry` 
        WHERE shift = %s AND type = 'Bank Deposit'
    """, shift_name)[0][0] or 0

    return {
        "opening_balance": shift.opening_cash,
        "income": income,
        "expenditure": expenditure,
        "closing_balance": shift.remaining_balance,
        "bank_deposit": bank_deposit,
        "shift": shift.user,
        "date": shift.date
    }

# Search function for shifts
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_shift(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT name, date, user
        FROM `tabFront Desk Shift`
        ORDER BY date DESC
        LIMIT %s OFFSET %s
    """, (page_len, start))
