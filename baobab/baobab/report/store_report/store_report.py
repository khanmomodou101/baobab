# Copyright (c) 2024, Jokoor and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, today, now
import erpnext
from erpnext.stock.doctype.stock_reconciliation.stock_reconciliation import get_items



def execute(filters=None):
	columns, data = get_columns(filters), get_item_stock_entry_details(filters)
	return columns, data

# Additional Columns for the Report

def get_columns(filters=None):
    return [
        {
            "fieldname": "item_code",
            "label": "Item Code",
            "fieldtype": "Data",
            "width": 150
        },
        # item grou
        {
            "fieldname": "item_group",
            "label": "Item Group",
            "fieldtype": "Data",
            "width": 150

        },
		# uom
        {
            "fieldname": "uom",
            "label": "UOM",
            "fieldtype": "Data",
            "width": 100
		},
        
        
        {
            "fieldname": "valuation_rate",
            "label": "Valuation Rate",
            "fieldtype": "Currency",
            'precision': 0,
            "width": 150
        },
        {
            "fieldname": "store_balance",
            "label": "Store Balance",
            "fieldtype": "Float",
            "width": 150,
            'precision': 1,
        },
        {
            "fieldname": "store_value",
            "label": "Store Value",
            "fieldtype": "Currency",
            'precision': 0,
            "width": 150
        },

        # otulet qty 
        {
            "fieldname": "supplied_qty",
            "label": "Suplied Qty",
            "fieldtype": "Data",
            "width": 150

        },
        # outlet value
        {
            "fieldname": "supplied_value",
            "label": "Supplied Value",
            "fieldtype": "Currency",
            'precision': 0,
            "width": 200

        },
        
        
       
    ]


def get_item_stock_entry_details(filters):
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
            
    # return list values 
    return list(data.values())