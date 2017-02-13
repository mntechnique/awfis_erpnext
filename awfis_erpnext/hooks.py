# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "awfis_erpnext"
app_title = "Awfis Erpnext"
app_publisher = "MN Technique"
app_description = "ERPNext extensions for Awfis"
app_icon = "octicon octicon-file-directory"
app_color = "#DA251D"
app_email = "support@castlecraft.in"
app_license = "GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/awfis_erpnext/css/awfis_erpnext.css"
app_include_js = "/assets/js/awfis.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/awfis_erpnext/css/awfis_erpnext.css"
# web_include_js = "/assets/awfis_erpnext/js/awfis_erpnext.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "awfis_erpnext.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "awfis_erpnext.install.before_install"
# after_install = "awfis_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "awfis_erpnext.awfis_erpnext.awf.awfis_notification_filter"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
has_permission = {
	"Lead": "awfis_erpnext.awfis_erpnext.awf.awf_lead_has_permission",
	"Awfis Centre": "awfis_erpnext.awfis_erpnext.awf.awf_lead_has_permission"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Stock Entry": {
		"validate": "awfis_erpnext.awfis_erpnext.awf.validate_stock_entry"
	},
	"Purchase Receipt": {
		"on_submit": "awfis_erpnext.awfis_erpnext.awf.validate_stock_entry"
	},
	"Lead": {
		"after_insert":"awfis_erpnext.awfis_erpnext.awf.awf_lead_after_insert",
		"on_update":"awfis_erpnext.awfis_erpnext.awf.awf_lead_after_insert",
		"validate":"awfis_erpnext.awfis_erpnext.awf.awf_lead_validate"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"awfis_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"awfis_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"awfis_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"awfis_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"awfis_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "awfis_erpnext.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
override_whitelisted_methods = {
 	"erpnext.selling.page.sales_funnel.sales_funnel.get_funnel_data": "awfis_erpnext.awfis_erpnext.awf.awf_get_funnel_data"
 }

fixtures = ["Custom Script",
			 {"dt": "Role", "filters":[["name","in", ["Awfis Ops User", "Awfis Ops Manager"]]] },
			 {"dt": "Custom Field", "filters":[["name", "in", ['Purchase Order-awfis_warehouse',
					'Lead-awfis_spaces', 'Lead-sb_spaces', 'Lead-lead_awfis_centres',
					'Lead-section_break_centres', 'Lead-awfis_lead_channel', 'Lead-channel_partner',
					'Lead-online_listing', 'Lead-social_media', 'Lead-reason_lost_or_on_hold',
					'Lead-lead_state', 'Lead-site_visited', 'Lead-awfis_company_website',
					'Lead-awfis_email_id', 'Lead-awfis_lead_territory', 'Lead-awfis_mobile_no',
					'Lead-last_name', 'Lead-first_name', 'Opportunity-priority', 'Opportunity-complaint_issue',
					'Opportunity-opportunity_awfis_centres', 'Opportunity-reason_lost_or_on_hold',
					'Opportunity-awfis_lead_territory', 'Opportunity-awfis_lead_channel', 'Sales Order-awfis_booking_id',
					'Sales Order-mode_of_payment', 'Sales Order-discount_coupon', 'Sales Order-centre',
					'Sales Order-column_break_city_centre', 'Sales Order-awfis_city', 'Sales Order-section_city_centre',
					'Sales Order-awfis_channel_partner', 'Sales Order-awfis_lead',
					'Contact-joining_date', 'Contact-pan_card_no', 'Contact-date_of_anniversary', 'Contact-date_of_birth',
					'Contact-col_break_custom_1', 'Contact-contact_type', 'Customer-number_of_employees', 'Customer-industry',
					'Customer-company_website', 'Item Attribute Value-awfis_centre', 'Item Attribute Value-col_break_1',
					'Issue-awfis_channel', 'Communication-awfis_channel', 'Warehouse-awfis_warehouse_territory',
					'Item Group-sb1_expiry_warning_period', 'Item Group-expiry_warning_period',
					'Employee-awfis_employee_territory', "Lead-lead_owner_centre", "Lead-awfis_space_requirements_sem", "Lead-awfis_location_sem",
					'Lead-awfis_lead_sub_source', 'Lead Source-awfis_lead_source_parent']]]},
			 "Property Setter",
			 {"dt":"Print Format", "filters": [["name", "in", ["Awfis Purchase Order"]]]},
			 {"dt":"Lead Source", "filters":[["name", "in", ["IPC", 
			 		"Outdoor hoardings/ Banners/ signage outside Awfis centres", "Customer", 
			 		"Outdoor", "Online", "Marketing", "Referral", "Signage", "Hoarding", "Events", "Cold Calling", 
			 		"Website", "Friend/Colleague", "Advertising", "Client", "Google Search", 
			 		"Employee", "E-mail marketing", "Returning Customer", "NA", "Instant Office",
			 		"International Property Consultant", "Domestic Property Consultant", "Email", "info@awfis.com", 
			 		"info@awfis.com", "contact@awfis.com"]]]}]
