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
				//content.find(".").prettyDate(this.attr('data-date'))
			}
		}
	})
}

// frappe.views.AwfisLeadDocListView = frappe.views.DocListView.extend({
// 	init_list: function(auto_run) {
// 		var me = this;
// 		// init list
// 		this.make({
// 			method: 'frappe.desk.reportview.get',
// 			save_list_settings: true,
// 			get_args: this.get_args,
// 			parent: this.wrapper,
// 			freeze: true,
// 			start: 0,
// 			page_length: this.page_length,
// 			show_filters: true,
// 			show_grid: true,
// 			new_doctype: this.doctype,
// 			allow_delete: this.allow_delete,
// 			no_result_message: this.make_no_result(),
// 			custom_new_doc: me.listview.make_new_doc || undefined,
// 		});

// 		// make_new_doc can be overridden so that default values can be prefilled
// 		// for example - communication list in customer
// 		if(this.listview.settings.list_view_doc) {
// 			this.listview.settings.list_view_doc(this);
// 		}
// 		else{
// 			$(this.wrapper).on("click", 'button[list_view_doc="'+me.doctype+'"]', function(){
// 				(me.listview.make_new_doc || me.make_new_doc).apply(me, [me.doctype]);
// 			});
// 		}

// 		if((auto_run !== false) && (auto_run !== 0))
// 			this.refresh();
// 	}
// })