//Allow only material transfers when user has just Stock User in roles.
//Length == 3: user_roles=["Stock User", "All", "Guest"]
frappe.ui.form.on('Material Request', 'validate', function(frm){
	if ((roles.length == 3) && (roles[0] == "Stock User")) {
		if (cur_frm.doc.material_request_type != "Material Transfer") {
			validated=false;
			frappe.msgprint('Not allowed.');
		}
	}
});