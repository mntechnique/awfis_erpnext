var is_mobno_valid = false;

frappe.ui.form.on("Contact", "mobile_no", function(frm){
	var mobno = frm.doc.mobile_no;
	var rx = new RegExp("^[789]\\d{9}$"); 
	var isvalid = rx.test(mobno);

	if (isvalid == true) {
          is_mobno_valid = true;
	} else {
          is_mobno_valid = false;
	  msgprint("Entered Mobile No. is either incomplete or invalid. <br /> Tip: Add it without the +0 or +91 at the beginning.", "Invalid Mobile No");
	}
});

frappe.ui.form.on("Contact", "validate", function(frm) {
   if (!is_mobno_valid) {
       msgprint("Entered Mobile No. is either incomplete or invalid. <br /> Tip: Add it without the +0 or +91 at the beginning.", "Invalid Mobile No");
      validated = false;
   }

});
