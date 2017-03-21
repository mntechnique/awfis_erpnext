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
	user = frappe.get_doc("User", frappe.session.user)
	
	assigned_to_user = frappe.get_all("ToDo", filters={"owner": frappe.session.user, "reference_type": "Lead"}, fields=["reference_name"])

	assigned_to_user = [l.get("reference_name") for l in assigned_to_user]	

	roles_by_user = [u.role for u in user.user_roles]
	
	follow_up_today, assigned_to_me_open, other = [], [], []
	
	if "Administrator" in roles_by_user or "System Manager" in roles_by_user:
		follow_up_today = frappe.db.sql("SELECT * FROM tabLead WHERE date(contact_date) = curdate() ORDER BY name DESC LIMIT {limit}".format(limit=limit), as_dict=True)

		assigned_to_me_open = frappe.get_all("Lead", 
								filters=[["name", "in", assigned_to_user], ["status", "=", "Open"], ["_comments", "=", None]], fields=["*"], limit=limit)
	
		other = frappe.get_all("Lead", filters=[["name", "in", assigned_to_user]], order_by="lead_state, contact_date DESC", limit=limit)

	elif "Sales Manager" in roles_by_user or "Sales User" in roles_by_user or "Awfis Ops User" in roles_by_user or "Awfis Ops Manager" in roles_by_user:
		allowed_territories = frappe.get_all("DefaultValue", fields=["defvalue"], filters={"defkey": "Territory", "parenttype": "User Permission", "parent":frappe.session.user})
		allowed_territories_list = [at["defvalue"] for at in allowed_territories]

		territories_clause = ""
		if len(allowed_territories_list):
			territories_string = ",".join(["'" + at + "'" for at in allowed_territories_list])
			territories_clause = " AND awfis_lead_territory in ({0}) ".format(territories_string)

		
		follow_up_today = frappe.db.sql("""SELECT * FROM tabLead WHERE date(contact_date) = curdate()
											{territories_clause} ORDER BY name DESC LIMIT {limit}"""
											.format(
												limit=limit,
												territories_clause= territories_clause
											), as_dict=True)
		
		assigned_to_me_open = frappe.get_all("Lead", filters=[["name", "in", assigned_to_user], ["status", "=", "Open"], ["_comments", "=", None]], fields=["*"], limit=limit)
		other = frappe.get_all("Lead", filters=[["awfis_lead_territory", "in", allowed_territories_list], ["name", "in", assigned_to_user]], fields=["*"], order_by="lead_state, contact_date DESC", limit=limit)

	out = frappe._dict({
		"follow_up_today": follow_up_today,
		"assigned_to_me_open": assigned_to_me_open,
		"other": other
	})

	return out


@frappe.whitelist()
def lookup_lead(caller_number=None):
	#return caller_number
	print "Caller Number", caller_number

	lead_by_phone_no = frappe.get_all("Lead", filters={"phone":caller_number}, fields=["*"])
	if len(lead_by_phone_no) > 0:
		return lead_by_phone_no[0].name

	lead_by_mobile_no = frappe.get_all("Lead", filters={"awfis_mobile_no":caller_number}, fields=["*"])
	if len(lead_by_mobile_no) > 0:
		return lead_by_mobile_no[0].name

	return "New Lead"
