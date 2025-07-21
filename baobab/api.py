import frappe
from erpnext.stock.doctype.stock_reconciliation.stock_reconciliation import get_items
from frappe.utils import today, now, getdate, flt
import erpnext

@frappe.whitelist()
def get_items_list():
    
    warehouse = "Stores - BHR"
    posting_date = today()
    posting_time = now()
    company = erpnext.get_default_company()

    return get_items(warehouse, posting_date, posting_time, company)

@frappe.whitelist()
def get_item_stock_entry_details():
    filters = {
        "outlet": "Afra - BHR",
        "from_date": "2025-01-05",
        "to_date": "2025-01-05",
    }
    data = {}
    
    stock_entries = frappe.get_list("Stock Entry", {"posting_date":['between', [getdate(filters.get('from_date')), getdate(filters.get('to_date'))]], "purpose": "Material Transfer"})
    for se in stock_entries:
        se_doc = frappe.get_doc("Stock Entry", se.name)
        for item in se_doc.items:
            if filters.get("item_code") and item.item_code != filters.get("item_code"):
                continue
            if filters.get("item_group") and item.item_group != filters.get("item_group"):
                continue
            if filters.get("outlet") and item.t_warehouse != filters.get("outlet"):
                continue

            if item.item_code not in data:
                store_qty = frappe.db.get_value("Bin", {"item_code": item.item_code, "warehouse": "Stores - BHR"}, "actual_qty")
                store_value = flt(store_qty) * flt(item.valuation_rate)
                data[item.item_code] = {
                    "item_code": item.item_code,
                    "item_group": item.item_group,
                    "uom": item.uom,
                    "valuation_rate": item.valuation_rate,
                    "supplied_qty": 0,
                    "supplied_value": 0,
                    "store_balance": store_qty,
                    "store_value": store_value
                }
            data[item.item_code]["supplied_qty"] += item.qty
            data[item.item_code]["supplied_value"] += flt(item.qty) * flt(item.valuation_rate)
            
    return data.values()


@frappe.whitelist()
def edit_items():
    items = frappe.
    
@frappe.whitelist()
def update_maintenan_stock(item_group):
    items = frappe.get_list("Item", {"item_group": item_group})
    for item in items:
        frappe.db.set_value("Item", item.name, "maintenance_schedule", "Maintenance Schedule-00001")
        frappe.db.commit()

@frappe.whitelist()
def remove_duplicate_sales_invoice(doc, method=None):
    if doc.payments:
        payment_methods = set()
        unique_payments = []
        
        for payment in doc.payments:
            if payment.mode_of_payment not in payment_methods:
                payment_methods.add(payment.mode_of_payment)
                unique_payments.append(payment)
        
        doc.payments = unique_payments
