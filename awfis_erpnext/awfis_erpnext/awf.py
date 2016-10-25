import frappe
from frappe import async
from frappe import _

import re #regular expressions
from frappe.utils import flt, getdate, add_days, formatdate
from  datetime import  timedelta
from frappe.async import get_redis_server, get_user_room

@frappe.whitelist()
def check_duplicate_centres(docname):
	d = frappe.get_doc("Lead", docname)
	c = (d.lead_awfis_centres[0])

	return c

@frappe.whitelist(allow_guest=True)
def notify_incoming_call(caller_number, agent_number, call_id):
	#url = urllib.unquote(caller_number).decode('utf8')

	is_request_valid = validate_request_header()
	caller_no = process_mobile_no(caller_number)
	agent_no = process_mobile_no(agent_number)
	agent_id = validate_agent(agent_number)

	if is_request_valid != 1:
		return "You are not authorized to make this request."
	elif caller_no == "":
		return "Caller number is invalid."
	elif agent_no == "":
		return "Agent number is invalid."
	elif agent_id == "":
		return "No agent with this number."
	else:
		create_popup(caller_number, agent_id, frappe.db.escape(call_id))

	# # if possible then minues days from datetime
	# def minues_to_date(date, years=0, months=0, days=0):
	# 	"""Adds `days` to the given date"""
	# 	from dateutil.relativedelta import relativedelta

	# 	as_string, as_datetime = False, False
	# 	if date==None:
	# 		date = now_datetime()

	# 	if isinstance(date, basestring):
	# 		as_string = True
	# 		if " " in date:
	# 			as_datetime = True
	# 		date = parser.parse(date)

	# 	date = date - relativedelta(years=years, months=months, days=days)

	# 	if as_string:
	# 		if as_datetime:
	# 			return date.strftime(DATETIME_FORMAT)
	# 		else:
	# 			return date.strftime(DATE_FORMAT)
	# 	else:
	# 		return date


@frappe.whitelist()
def validate_stock_entry(self, method):
	for item in self.items:
		#If batch item, batch no must be specified.
		if frappe.db.get_value("Item", item.item_code, "has_batch_no"):
			item_group = frappe.db.get_value("Item", item.item_code, "item_group")
			# if (not item.batch_no):
			# 	frappe.throw(_("Row {0}: Batch number is mandatory for {1}".format(item.idx, item.item_name)))
			expiry_warning_period = int(frappe.db.get_value('Item Group', item_group, 'expiry_warning_period') or 0)

			if expiry_warning_period and item.batch_no: #Without batch no, validation goes through.
				expiry_date = frappe.db.get_value('Batch', item.batch_no, 'expiry_date')
				
				if (getdate(expiry_date) - frappe.utils.datetime.date.today()).days <= expiry_warning_period:
					frappe.throw(_("Row {0}: Item {1} cannot be issued. Batch {2} for selected item is about to expire.".format(item.idx, item.item_name, item.batch_no)))

	# if expiry_warning:
	# 	expiry_date = frappe.db.get_value('Batch', self.batch_no, 'expiry_date')
	# 	x_day_before = (add_days(getdate(self.expiry_date), expiry_warning) <= date.today())
	# 	# x_day_before = (expiry_date-expiry_warning) <= date.today())
	# 	if x_day_before:
	# 		frappe.throw(_("Material Can not be transfered. because of expiry warning period of {0}").format(expiry_warning))




# ===============
# 		self.pst_respond_by = str(frappe.utils.data.getdate(self.pst_posted_on) + frappe.utils.datetime.timedelta(days=2))
# ===========
#  my data start work here.......................................
# // additional validation on dates
# cur_frm.add_fetch("Awfis Settings", "expiry_warning_period", "expiry_warning_period");
# cur_frm.add_fetch("Batch", "expiry_date", "expiry_date");

# frappe.ui.form.on("batch_no", "validate", function(frm) {

#     if (frm.doc.expiry_date - frm.doc.expiray_warning_period < get_today()) {
#         msgprint("You can not Transfer material ");
#         validated = false;
#     }
# });
# =========
def create_popup(caller_number, agent_id, call_id):
	#return caller_number

	caller_number_processed = process_mobile_no(caller_number)

	ld = None

	ld_name = frappe.db.get_value("Lead", {"mobile_no": caller_number_processed}, "name") # frappe.get_all("Lead", fields=["*"], filters={"mobile_no": caller_number_processed})

	if not ld_name:
		#Create stub lead if lead is not found.
		ld = frappe.new_doc("Lead")
		ld.mobile_no = caller_number_processed
		ld.lead_name = "New Lead ({m})".format(m=caller_number)

		#Set mandatory custom fields.
		ld.first_name = "New Lead ({m})".format(m=caller_number)
		ld.awfis_mobile_no = caller_number_processed
		ld.source = "Other"
		ld.awfis_lead_territory = "All Territories"

		ld.insert(ignore_permissions=True)
		frappe.db.commit()
	else:
		ld = frappe.get_doc("Lead", ld_name)


	#Make popup content.
	lead_fields = {"mobile_no": caller_number,
			"lead_name": ld.lead_name,
			"company_name": ld.company_name,
			"name": ld.name,
			"call_timestamp": frappe.utils.datetime.datetime.strftime(frappe.utils.datetime.datetime.today(), '%d/%m/%Y %H:%M:%S'),
			"call_id": call_id}

	popup_content = frappe.render_template("awfis_erpnext/templates/lead_info.html", lead_fields)

	#Create a notification.
	notif = frappe.new_doc("Communication")
	notif.subject = "Incoming Call {m}".format(m=caller_number)
	notif.communication_type = "Communication"
	notif.content = popup_content #, {"communication_type": "Notification", "content": popup_content})
	notif.status = "Linked"
	notif.sent_or_received = "Sent"
	notif.reference_doctype = "Lead"
	notif.reference_name = ld.name

	notif.insert(ignore_permissions=True)
	frappe.db.commit()

	#Display the actual popup to all sales users.
	#Display popup to agent
	# for u in frappe.get_all("User", fields=['name'], filters={"role": "Sales User"}):
	# 	frappe.async.publish_realtime(event="msgprint", message=popup_content, user=u.name)

	frappe.async.publish_realtime(event="msgprint", message=popup_content, user=agent_id)


#Uses regex to match and extract a 10 digit mobile no from the caller_number parameter.
#'+' must be encoded if received from URL.
def process_mobile_no(caller_number):
	# matched_extracted_mobno = re.search(r"^\+?(91|0)\d{10}$", caller_number)

	# if matched_extracted_mobno:
	# 	mobno = matched_extracted_mobno.group(0)
	# 	return mobno[-10:]
	# else:
	# 	return ""
	return caller_number[-10:]


def validate_request_header():
	key_header = frappe.get_request_header("awfis-api-key")
	key_local = frappe.get_single("Awfis Settings").api_key_knowlarity

	if key_header == "":
		return -1 #"Key header is blank"
	elif key_header != key_local:
		return 0 #"{0} != {1} : Key header does not match local key".format(key_header, key_local)
	else:
		return 1 #""


def validate_agent(agent_number):
	agent_number_processed = process_mobile_no(agent_number)

	#If None, all agents are returned. Validation fails.
	if not agent_number_processed:
		return ""

	agents = frappe.get_all("User", fields=['name'], filters={"role": "Sales User", "phone": agent_number_processed})

	if len(agents) > 0:
		return agents[0]["name"] #Return the name of the first agent.
	else:
		return ""

#from frappe.core.notifications import get_notification_config

def awfis_notification_filter():
	return {
		"for_doctype": {
			"Communication": {"status": ["in", ('Linked', 'Open')], "communication_type": "Communication"}
		}
	}

@frappe.whitelist()
def generate_key_knowlarity():
	apikey = frappe.generate_hash()
	return apikey #{ "key" : apikey }

@frappe.whitelist(allow_guest=True)
def popuptest(caller_number, agent_number, call_id):

	is_request_valid = validate_request_header()
	caller_no = process_mobile_no(caller_number)
	agent_no = process_mobile_no(agent_number)
	agent_id = validate_agent(agent_number)

	if is_request_valid != 1:
		return "You are not authorized to make this request."
	elif caller_no == "":
		return "Caller number is invalid."
	elif agent_no == "":
		return "Agent number is invalid."
	elif agent_id == "":
		return "No agent with this number."
	else:
		return "Popup created {c}, {a}, {aid}, {cl}".format(c=caller_no, a=agent_number, aid=agent_id, cl=call_id)
		#create_popup(caller_number, agent_id, frappe.db.escape(call_id))

	# is_request_valid = validate_request_header()
	# caller_no = process_mobile_no(caller_number)
	# agent_id = validate_agent(agent_number)

	# if is_request_valid != 1:
	# 	return "You are not authorized to make this request. [0]"
	# elif agent_id == "":
	# 	return "No agent with this number."
	# else:
	# 	return "Popup created {c}, {a}, {cl}".format(c=caller_no, a=agent_number, cl=call_id)
	# 	#create_popup(caller_number, agent_id, frappe.db.escape(call_id))


# @frappe.whitelist(allow_guest=True)
# def regextest(caller_number):
# 	cano = process_mobile_no(caller_number)
# 	return "Raw: {r}, Processed: {p}".format(r=caller_number, p=cano)

from erpnext.selling.page.sales_funnel.sales_funnel import get_funnel_data
@frappe.whitelist()
def awf_get_funnel_data(from_date, to_date):
	guests = frappe.db.sql("""select count(*) from `tabAwfis Guest` 
		where (date(`creation`) between %s and %s)
		""", (from_date, to_date))[0][0]
	ret = get_funnel_data(from_date, to_date)
	ret_with_guests = [{ "title": _("Awfis Guest"), "value": guests, "color": "#FFFF15" }]
	ret_with_guests += ret
	
	return ret_with_guests