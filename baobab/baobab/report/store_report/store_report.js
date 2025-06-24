// Copyright (c) 2024, Jokoor and contributors
// For license information, please see license.txt

frappe.query_reports["Store Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		
		// item gorup
		{
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
		},
		// item and fileter base on item group and if item grou is emty then show all item
		{
			"fieldname": "item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"get_query": function() {
				if (frappe.query_report.get_filter_value('item_group')) {
				return {
					
					"filters": {
						"item_group": frappe.query_report.get_filter_value('item_group')
					}
				}
			}
		}
			
			

			
		},

		
		{
			"fieldname": "outlet",
			"label": __("Outlet"),
			"fieldtype": "Link",
			"options": "Warehouse",
		},
		
	]
};
