# Copyright (c) 2013, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []

	columns = get_columns()
	data = get_data()	

	return columns, data

def get_columns():
	columns = [
		"ID:Link/Lead:75", 
		"Person Name::150", 
		"Mobile No::80",
		"Territory:Link/Lead:80",
		"Lead Channel::120",
		"Lead Source:Link/Lead Source:80", 
		"Created On:Datetime:80",
		"Created By::80",
		"Action Taken By::250"]

	return columns

def get_data():
	out = []
	leads = frappe.get_all("Lead", fields=["*"])

	for lead in leads:
		versions = frappe.get_all("Version", filters={"ref_doctype": "Lead", "docname": lead.name}, fields="owner", distinct=True)
		owners = [v.owner for v in versions]

		row = []
		row.append(lead.name)
		row.append(lead.lead_name)
		row.append(lead.mobile_no)
		row.append(lead.awfis_lead_territory)
		row.append(lead.awfis_lead_channel)
		row.append(lead.source)
		row.append(lead.awfis_lead_sub_source)
		row.append(lead.creation)
		row.append(lead.owner)
		row.append(".".join(owners))

		if len(owners > 0):
			out.append(row)

	return out
		# if len(owners) > 0:
		# 	lead.update({"edited_by": ",".join(owners)})
		# else:
		# 	lead.update({"edited_by": lead.modified_by })
		
		
