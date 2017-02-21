from frappe import _

def get_data():
	return [
		{
			"label": _("CRM"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Lead",
					"label": "Leads",
					"description": _("Lead."),
				},
				{
					"type": "page",
					"name": "awfis_lead_list",
					"label": "Lead Dashboard",
					"description": _("Dashboard with actionable grids for Lead."),
				},
				{
					"type": "doctype",
					"name": "Awfis Centre",
					"label": "Awfis Centre",
					"description": _("Awfis Centre"),
				},
				{
					"type": "doctype",
					"name": "Awfis Guest",
					"label": "Awfis Guest",
					"description": _("Awfis Guest"),
				},
				{
					"type": "page",
					"name": "awfis_lead_lookup",
					"label": "Lead Lookup",
					"description": _("Look up record for Lead by caller number and navigate to it."),
				},	
			]
		},
		{
			"label": _("Settings"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Awfis Settings",
					"label": "Awfis Settings",
					"description": _("General settings for Awfis ERPNext"),
				},
			]
		},
		{
			"label": _("Tools"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Awfis Report Processing Tool",
					"label": "Awfis Report Processing Tool",
					"description": _("Awfis Report Processing Tool"),
				},
			]
		},
		{		
			"label": _("MMS Reports (Awfis Material Management System)"),
			"icon": "icon-star",
			"items": [
				{
					"type": "report",
					"name": "Item Batch Expiry Status",
					"label": "Item Batch Expiry Status",
					"description": _("Report indicating expiry date for Item Batches"),
					"route": "query-report/Item Batch Expiry Status",
					"doctype": "DocType"
				},
			]
		},
	]
