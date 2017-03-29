import frappe
from frappe import _
import os
import io
import ast

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
def get_lead_list_data():
	all_leads = frappe.get_all("Lead", fields=["*"])

	user = frappe.get_doc("User", frappe.session.user)
	user_roles = [u.role for u in user.user_roles]

	follow_up_today, open_leads, other_leads = [], [], []

	user_territories = frappe.get_all("DefaultValue", 
				fields=["defvalue"],
				filters={"defkey": "Territory", "parenttype": "User Permission", "parent":frappe.session.user}
				)
	user_territories = [ut.defvalue for ut in user_territories]
	
	if "Sales Manager" in user_roles or "Awfis Ops Manager" in user_roles or "System Manager" in user_roles:
		team = frappe.get_all("DefaultValue", 
					fields=["parent"], 
					filters=[["defkey", "=", "Territory"],["defvalue", "in", user_territories], ["parenttype", "=", "User Permission"]],
					distinct=True)
		team = [tm.parent for tm in team]

		#print "TEAM", team
		
		follow_up_today = [l for l in all_leads if
							(l.contact_date and frappe.utils.getdate(l.contact_date) == frappe.utils.getdate()) and
							(
								(l.owner in team) or 
								(l._assign and 
									(len([assignee for assignee in ast.literal_eval(l._assign) if assignee in team]) > 0) or
									(frappe.session.user in ast.literal_eval(l._assign))
								)
							)
						]

		open_leads = [l for l in all_leads if 
							(l.owner in team) or 
							(	
								(l.contact_by == "") and  
								(
									(l._assign and len(ast.literal_eval(l._assign)) == 1) and 
									("Sales Manager" in [ur.role for ur in frappe.get_doc("User", ast.literal_eval(l._assign)[0]).user_roles])
								)
							)
					]
		other_leads = [l for l in all_leads if 
							not (l.contact_date and frappe.utils.getdate(l.contact_date) == frappe.utils.getdate()) and
							not (	
								(l.contact_by == "") and  
								(
									(l._assign and len(ast.literal_eval(l._assign)) == 1) and 
									("Sales Manager" in [ur.role for ur in frappe.get_doc("User", ast.literal_eval(l._assign)[0]).user_roles])
								)
							) and
							(
								(l.owner in team) or 
								(l._assign and len([assignee for assignee in ast.literal_eval(l._assign) if assignee in team]) > 0)
							)
						]
		# other_leads.sort(key=lambda l: -(l.contact_date or None))

	elif "Sales User" in user_roles or "Awfis Ops User" in user_roles:
		follow_up_today = [l for l in all_leads if
							(l.contact_date and frappe.utils.getdate(l.contact_date) == frappe.utils.getdate()) and
							(
								(l.owner == frappe.session.user) or 
								(frappe.session.user in ast.literal_eval(l._assign))
							)
						]

		open_leads = [l for l in all_leads if 
							(l.owner == frappe.session.user) or 
							(	
								(l.contact_by == "") and  
								(
									(l._assign and len(ast.literal_eval(l._assign)) == 1) and 
									("Sales Manager" in [ur.role for ur in frappe.get_doc("User", ast.literal_eval(l._assign)[0]).user_roles])
								)
							)
					]
		other_leads = [l for l in all_leads if 
							(
								(l.contact_date == "")
								or 
								(l.contact_date and (frappe.utils.getdate(l.contact_date) != frappe.utils.getdate()))
							) and
							(
								(l.contact_by == "")
								or 
								(l.contact_by and not ((
									(l._assign and len(ast.literal_eval(l._assign)) == 1) and 
									("Sales Manager" in [ur.role for ur in frappe.get_doc("User", ast.literal_eval(l._assign)[0]).user_roles])
								)))
							)
							and
							(
								(l.owner == "") or 
								(l._assign and len([assignee for assignee in ast.literal_eval(l._assign) if assignee in team]) > 0)
							)
						]

		# other_leads.sort(key=lambda l: (l.contact_date))



	return {"follow_up_today": follow_up_today, "open_leads":open_leads, "other_leads": other_leads}
	

#ORIGINAL
# @frappe.whitelist()
# def get_lead_list_data(limit=20):
# 	user = frappe.get_doc("User", frappe.session.user)
	
# 	assigned_to_user = frappe.get_all("ToDo", filters={"owner": frappe.session.user, "reference_type": "Lead"}, fields=["reference_name"])

# 	assigned_to_user = [l.get("reference_name") for l in assigned_to_user]	

# 	roles_by_user = [u.role for u in user.user_roles]
	
# 	follow_up_today, assigned_to_me_open, other = [], [], []
	
# 	if "Administrator" in roles_by_user or "System Manager" in roles_by_user:
# 		follow_up_today = frappe.db.sql("SELECT * FROM tabLead WHERE date(contact_date) = curdate() ORDER BY name DESC LIMIT {limit}".format(limit=limit), as_dict=True)

# 		assigned_to_me_open = frappe.get_all("Lead", 
# 								filters=[["name", "in", assigned_to_user], ["status", "=", "Open"], ["_comments", "=", None]], fields=["*"], limit=limit)
	
# 		other = frappe.get_all("Lead", filters=[["name", "in", assigned_to_user]], order_by="lead_state, contact_date DESC", limit=limit)

# 	elif "Sales Manager" in roles_by_user or "Sales User" in roles_by_user or "Awfis Ops User" in roles_by_user or "Awfis Ops Manager" in roles_by_user:
# 		allowed_territories = frappe.get_all("DefaultValue", fields=["defvalue"], filters={"defkey": "Territory", "parenttype": "User Permission", "parent":frappe.session.user})
# 		allowed_territories_list = [at["defvalue"] for at in allowed_territories]

# 		territories_clause = ""
# 		if len(allowed_territories_list):
# 			territories_string = ",".join(["'" + at + "'" for at in allowed_territories_list])
# 			territories_clause = " AND awfis_lead_territory in ({0}) ".format(territories_string)

		
# 		follow_up_today = frappe.db.sql("""SELECT * FROM tabLead WHERE date(contact_date) = curdate()
# 											{territories_clause} ORDER BY name DESC LIMIT {limit}"""
# 											.format(
# 												limit=limit,
# 												territories_clause= territories_clause
# 											), as_dict=True)
		
# 		assigned_to_me_open = frappe.get_all("Lead", filters=[["name", "in", assigned_to_user], ["status", "=", "Open"], ["_comments", "=", None]], fields=["*"], limit=limit)
# 		other = frappe.get_all("Lead", filters=[["awfis_lead_territory", "in", allowed_territories_list], ["name", "in", assigned_to_user]], fields=["*"], order_by="lead_state, contact_date DESC", limit=limit)

# 	out = frappe._dict({
# 		"follow_up_today": follow_up_today,
# 		"assigned_to_me_open": assigned_to_me_open,
# 		"other": other
# 	})

# 	return out

#VIABLE
# @frappe.whitelist()
# def get_lead_list_data(limit=100):
# 	user = frappe.get_doc("User", frappe.session.user)
	
# 	leads_assigned_to_user = frappe.get_all("ToDo", filters={"owner": frappe.session.user, "reference_type": "Lead"}, fields=["reference_name"])
# 	leads_assigned_to_user = [l.get("reference_name") for l in leads_assigned_to_user]	

# 	roles_by_user = [u.role for u in user.user_roles]
	
# 	follow_up_today, assigned_to_me_open, other = [], [], []

# 	if "Administrator" in roles_by_user or "System Manager" in roles_by_user:
# 		follow_up_today = frappe.db.sql("SELECT * FROM tabLead WHERE date(contact_date) = curdate() ORDER BY name DESC LIMIT {limit}".format(limit=limit), as_dict=True)

# 		assigned_to_me_open = frappe.get_all("Lead", 
# 								filters=[["name", "in", leads_assigned_to_user], ["status", "=", "Open"], ["_comments", "=", None]], fields=["*"], limit=limit)
	
# 		#other = frappe.get_all("Lead", filters=[["name", "in", leads_assigned_to_user]], order_by="lead_state, contact_date DESC", limit=limit)
# 		other = frappe.get_all("Lead", fields=["*"], order_by="lead_state, contact_date DESC", limit=limit)

# 	else:
# 		allowed_territories = frappe.get_all("DefaultValue", fields=["defvalue"], filters={"defkey": "Territory", "parenttype": "User Permission", "parent":frappe.session.user})
# 		allowed_territories_list = [at["defvalue"] for at in allowed_territories]

# 		territories_clause = ""
# 		if len(allowed_territories_list):
# 			territories_string = ",".join(["'" + at + "'" for at in allowed_territories_list])
# 			territories_clause = " AND awfis_lead_territory in ({0}) ".format(territories_string)

# 		if "Sales Manager" in roles_by_user or "Awfis Ops Manager" in roles_by_user:
# 			#Will fetch Leads for all people in territories.
# 			follow_up_today = frappe.db.sql("""SELECT * FROM tabLead WHERE date(contact_date) = curdate()
# 												{territories_clause} ORDER BY name DESC LIMIT {limit}"""
# 												.format(
# 													limit=limit,
# 													territories_clause= territories_clause
# 												), as_dict=True)
			
# 			assigned_to_me_open = frappe.get_all("Lead", filters=[["name", "in", leads_assigned_to_user], ["status", "=", "Open"]], fields=["*"], limit=limit)
# 			other = frappe.get_all("Lead", filters=[["awfis_lead_territory", "in", allowed_territories_list], ["name", "in", leads_assigned_to_user]], fields=["*"], order_by="lead_state, contact_date DESC", limit=limit)
		
# 		elif "Sales User" in roles_by_user or "Awfis Ops User" in roles_by_user:
# 			follow_up_today = frappe.db.sql("""SELECT * FROM tabLead WHERE date(contact_date) = curdate() and owner = '{owner}'
# 												 {territories_clause} ORDER BY name DESC LIMIT {limit}"""
# 												.format(
# 													limit=limit,
# 													owner=frappe.session.user,
# 													territories_clause= territories_clause
# 												), as_dict=True)
			
# 			assigned_to_me_open = frappe.get_all("Lead", filters=[["name", "in", leads_assigned_to_user], ["status", "=", "Open"]], fields=["*"], limit=limit)
# 			other = frappe.get_all("Lead", filters=[["awfis_lead_territory", "in", allowed_territories_list], ["name", "in", leads_assigned_to_user]], fields=["*"], order_by="lead_state, contact_date DESC", limit=limit)

# 	out = frappe._dict({
# 		"follow_up_today": follow_up_today,
# 		"assigned_to_me_open": assigned_to_me_open,
# 		"other": other
# 	})

# 	return out


#INVIABLE
# @frappe.whitelist()
# def get_lead_list_data(limit=0):
# 	import ast


# 	#Preload essentials
# 	user = frappe.get_doc("User", frappe.session.user)
# 	roles_by_user = [u.role for u in user.user_roles]

# 	follow_up_today, open_general, other = [], [], []

# 	#Administrators and system managers get unrestricted view of leads across territories. 
# 	if "Administrator" in roles_by_user or "System Manager" in roles_by_user:
# 		open_leads_prelim = frappe.get_all("Lead", filters=[["contact_by", "=", ""]], fields=["*"])
# 		open_leads = [ol for ol in open_leads_prelim if not(ol._assign) or len(ast.literal_eval(ol._assign)) == 1]
			
# 		follow_up_today = frappe.db.sql("SELECT * FROM tabLead WHERE date(contact_date) = curdate() ORDER BY name DESC LIMIT {limit}".format(limit=limit), as_dict=True)
# 		open_general = open_leads
# 		other = frappe.get_all("Lead", filters=[["contact_by", "!=", ""]], fields=["*"], order_by="lead_state, contact_date DESC", limit=limit)
	
# 	else:
# 		allowed_territories_list = frappe.get_all("DefaultValue", fields=["defvalue"], filters={"defkey": "Territory", "parenttype": "User Permission", "parent":frappe.session.user})
# 		allowed_territories = [at["defvalue"] for at in allowed_territories_list]

# 		territories_clause, territories_string = "", ""
		
# 		if len(allowed_territories_list) > 0:
# 			territories_string = ",".join(["'" + at + "'" for at in allowed_territories])
# 			territories_clause = " AND awfis_lead_territory in ({0}) ".format(territories_string)


# 		if "Sales Manager" in roles_by_user or "Awfis Ops Manager" in roles_by_user:
# 			follow_up_today = frappe.db.sql("""SELECT * FROM tabLead WHERE date(contact_date) = curdate() 
# 					{territories_clause} ORDER BY name DESC LIMIT {limit}"""
# 					.format(limit=limit,territories_clause= territories_clause), as_dict=True)

# 			#Get Open Leads from allowed territories						
# 			open_leads_prelim = frappe.get_all("Lead", filters=[
# 					["contact_by", "=", ""], 
# 					["awfis_lead_territory", "in", allowed_territories]
# 					], fields=["*"])
# 			open_leads = [ol for ol in open_leads_prelim if not(ol._assign) or len(ast.literal_eval(ol._assign)) == 1]
# 			open_general = open_leads

# 			other = frappe.get_all("Lead", filters=[
# 						["awfis_lead_territory", "in", allowed_territories]
# 						["contact_by", "!=", ""]
# 					], fields=["*"], order_by="lead_state, contact_date DESC", limit=limit)

# 		elif "Sales User" in roles_by_user or "Awfis Ops User" in roles_by_user:
# 			# leads_assigned_to_user = frappe.get_all("ToDo", filters={"owner": frappe.session.user, "reference_type": "Lead"}, fields=["reference_name"])
# 			# leads_assigned_to_user = [l.get("reference_name") for l in leads_assigned_to_user]	
# 			follow_up_today = frappe.db.sql("""SELECT * FROM tabLead WHERE date(contact_date) = curdate() and owner = '{owner}'
# 												 {territories_clause} ORDER BY name DESC LIMIT {limit}"""
# 												.format(
# 													limit=limit,
# 													owner=frappe.session.user,
# 													territories_clause= territories_clause
# 												), as_dict=True)
			
# 			#Get Open Leads owned by 
# 			open_leads_prelim = frappe.get_all("Lead", filters=[
# 					["contact_by", "=", ""], 
# 					["awfis_lead_territory", "in", allowed_territories],
# 					["owner", "=", frappe.session.user]
# 					], fields=["*"])
# 			open_leads = [ol for ol in open_leads_prelim if not(ol._assign) or len(ast.literal_eval(ol._assign)) == 1]
# 			open_general = open_leads

# 			other = frappe.get_all("Lead", filters=[["awfis_lead_territory", "in", allowed_territories], ["owner", "=", frappe.session.user]], fields=["*"], order_by="lead_state, contact_date DESC", limit=limit)	
# 		else:
# 			pass



	
	
# 	# else:

		
# 	# 	# rsms_for_territories = frappe.get_all("DefaultValue", fields=["parent"], filters={"defkey": "Territory", "defvalue": lead.awfis_lead_territory, "parenttype": "User Permission"})

		
# 	# 		#Will fetch Leads for all people in territories.
# 	# 		sql = """SELECT * FROM tabLead WHERE date(contact_date) = curdate() 
# 	# 				{territories_clause} ORDER BY name DESC LIMIT {limit}"""
# 	# 				.format(limit=limit,territories_clause= territories_clause)

			
# 	out = frappe._dict({
# 		"follow_up_today": follow_up_today,
# 		"open_general": open_general,
# 		"other": other
# 	})

# 	return out


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
