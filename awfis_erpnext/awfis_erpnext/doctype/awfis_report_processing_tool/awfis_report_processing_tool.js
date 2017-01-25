// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Awfis Report Processing Tool', {
	refresh: function(frm) {

	},
	btn_process_comments: function(frm) {
		var w = window.open("/api/method/awfis_erpnext.awfis_erpnext.doctype.awfis_report_processing_tool.awfis_report_processing_tool.get_processed_lead_report?"
						+"lead_report="+encodeURIComponent(frm.doc.lead_report));

		if(!w) {
			frappe.msgprint(__("Please enable pop-ups")); return;
		}

		frm.fields_dict.lead_report.clear_attachment();
	}
});
