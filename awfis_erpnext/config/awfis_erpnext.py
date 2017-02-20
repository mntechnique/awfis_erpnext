from frappe import _

def get_data():
	return [
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
	]
