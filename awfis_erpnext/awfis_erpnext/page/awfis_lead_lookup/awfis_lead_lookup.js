frappe.pages['awfis_lead_lookup'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Lead Lookup',
		single_column: true
	});

	//Append search textbox and button
	var content = null;
	content = page.wrapper.find(".page-content");
	//console.log(content);
	var input_html= '<div class="input-group"><input id="txt-lookup" type="text" class="form-control" placeholder="Search for caller number..."> <span class="input-group-btn"> <button id="btn-lookup" class="btn btn-primary" type="button">Search!</button> </span> </div> <div class="clearfix"></div>'
	content.append(input_html);

	//Wireup events to search textbox and button
	var btn = content.find('#btn-lookup');
	var txt = content.find('#txt-lookup');
	

	btn.click(function() {
		on_search($(txt).val());
	});

	//Handle enter.
	$(document).keypress(function(e) {
		if (e.which == 13) {
			btn.click();			
		}
	});
}


function on_search(caller_number) {
	frappe.call({
		method: "awfis_erpnext.awfis_erpnext.api.lookup_lead",
		args: {
			caller_number: caller_number
		},
		freeze: true,
		freeze_message: __("Looking up caller number..."),
		callback: function(r) {
			//console.log(r.message); 
			if (!r || !r.message) {
				frappe.show_alert("No value returned.");
				return
			} else if (r.message == "New Lead") {
				var l = frappe.model.make_new_doc_and_get_name("Lead");
				l = locals["Lead"][l];
				l.awfis_mobile_no = caller_number;
				l.owner = frappe.user.name;
				frappe.set_route("Form", "Lead", l.name);
			} else {
				frappe.set_route("Form", "Lead", r.message);	
			}
		}
	});
}