frappe.pages['awfis_lead_list'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Lead Dashboard',
		single_column: true
	});

	var content = page.wrapper.find('.page-content');

	frappe.call({
		method: "awfis_erpnext.awfis_erpnext.api.get_lead_list_data",
		callback: function(r) {
			if (r) {
				console.log("Return", r.message);
				var leads_html = frappe.render_template("awfis_lead_list", {"lead_data": r.message});
				content.html(leads_html);
			}
		}
	})
}