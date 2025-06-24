// Copyright (c) 2025, royalsmb and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Cash Transaction"] = {
	"filters": [
		{
			"fieldname":"report_type",
			"label": __("Report Type"),
			"fieldtype": "Select",
			"options": ["Report Per Shift", "Report Per Income/Expense"],
			"default": "Report Per Shift",
		},
		// froom date 
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		// to date
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"shift",
			"label": __("Shift"),
			"fieldtype": "Link",
			"options": "Front Desk Shift",
			"get_query": function() {
				return {
					query: "baobab.baobab.report.daily_cash_transaction.daily_cash_transaction.get_shift",
					
			}

		}
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": ["Income", "Expense"],
		
		}
	]
};
