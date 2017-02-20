import frappe
from frappe import _
import os
import io


def get_filedata(file_name, options=None):
	fname = file_name #os.path.join("/tmp", file_name)

	try:
		with open(fname, "rb") as fileobj:
			filedata = fileobj.read()
	except IOError, e:
		if ("ContentNotFoundError" in e.message
			or "ContentOperationNotPermittedError" in e.message
			or "UnknownContentError" in e.message
			or "RemoteHostClosedError" in e.message):

			# allow pdfs with missing images if file got created
			if os.path.exists(fname):
				with open(fname, "rb") as fileobj:
					filedata = fileobj.read()

			else:
				frappe.throw(_("Could not open file."))
		else:
			raise
	finally:
		cleanup(fname)
	print filedata
	return filedata
	
def cleanup(fname):
	if os.path.exists(fname):
		os.remove(fname)

@frappe.whitelist()
def get_lead_list_data(limit=20):
	leads_assigned_to_user = frappe.get_all("ToDo", filters={"owner": frappe.session.user, "reference_type": "Lead"}, fields=["reference_name"])

	out = frappe._dict({
		"follow_up_today": frappe.db.sql("SELECT * FROM tabLead WHERE date(contact_date) = curdate() ORDER BY name DESC LIMIT {limit}".format(limit=limit), as_dict=True),
		"assigned_to_me_open": frappe.get_all("Lead", filters=[["name", "in", leads_assigned_to_user], ["status", "=", "Open"]], fields=["*"], limit=limit),
		"other": frappe.get_all("Lead", fields=["*"], order_by="lead_state, contact_date DESC", limit=limit),
	})

	return out
