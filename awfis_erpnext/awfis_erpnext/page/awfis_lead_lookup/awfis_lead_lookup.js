frappe.pages['awfis_lead_lookup'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Lead Lookup',
		single_column: true
	});
}