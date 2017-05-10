//Ensure that only the newer space types are seen.
frappe.ui.form.on("Lead Awfis Space", {
    "awfis_spaces_add": function(doc, cdt, cdn) {
	     cur_frm.fields_dict["awfis_spaces"].grid.fields_map["space_type"].options = "Flexi Seat\nFixed Seat\nCabin Seat\nVirtual Office\nMeeting Room 4\nMeeting Room 6\nMeeting Room 8\nMeeting Room 10\nMobile Awfis";
       cur_frm.fields_dict["awfis_spaces"].grid.fields_map["tenure"].options = "Hours\nDays\nWeeks\nMonths\nYears";
    },
    "space_type": function(frm, cdt, cdn) {
      var space = locals[cdt][cdn];

      var space_capacity_map = {
        "Fixed Seat": 1, "Flexi Seat": 1, "Cabin Seat": 1, "Virtual Office": 1, "Mobile Awfis": 1,
        "Meeting Room 4": 4, "Meeting Room 6": 6, "Meeting Room 8": 8, "Meeting Room 10": 10}

      space.capacity = space_capacity_map[space.space_type];

      refresh_field("awfis_spaces");
    }
});

//Ensure that only newer tenures are seen.

frappe.ui.form.on("Lead Awfis Centre", "centre_city", function(frm, cdt, cdn){
  var child = locals[cdt][cdn];
  grid_row = cur_frm.fields_dict['lead_awfis_centres'].grid.grid_rows_by_docname[child.name];
  field = frappe.utils.filter_dict(grid_row.docfields, {fieldname: "centre"})[0]
  field.get_query = function(){
    return {
       filters: { city: child.centre_city }
    }
  }
});

frappe.ui.form.on("Lead", "validate", function(frm){
  if(!isMobileNoValid(frm.doc.mobileno||"")||!isMobileNoValid(frm.doc.alt_mobile_no_1||"")) {
        flashMessage();
        validated = false;
  }
});

function isMobileNoValid(mobno) {
    return (mobno.length <= 15);
}

function flashMessage() {
       msgprint(__("Please check the value for Mobile No.", "Invalid Mobile No"));
}

frappe.ui.form.on("Lead", "onload", function(frm) {
    frm.set_df_property("naming_series","read_only",1);
    frm.set_query("channel_partner", function() {
      return {
      "filters": {
                "partner_type": frm.doc.source
            }
        };
    });
    frm.set_query( "awfis_lead_territory", function() {
      return {
      "filters": {
                "is_group": "No"
            }
        };
    });

    if ((frappe.boot.user.roles != "Awfis Ops User") && (frm.doc.__islocal)) {
      var dialog = new frappe.ui.Dialog({
        title: __("Lookup Lead"),
        fields: [
          {"fieldtype": "Data", "label": __("Caller Number"), "fieldname": "caller_number",
            "reqd": 1 },
          {"fieldtype": "Button", "label": __("Search"), "fieldname": "search_lead"},
        ],

      });

      dialog.fields_dict.search_lead.$input.click(function() {
          args = dialog.get_values();

          frappe.call({
            method: "awfis_erpnext.awfis_erpnext.api.lookup_lead",
            args: {
                caller_number: args.caller_number
            },
            callback: function(r) {
              if (!r || !r.message) {
                  frappe.show_alert("No value returned.");
              } else if (r.message == "New Lead") {
                  frappe.show_alert("No existing Lead with that number.", 5);
                  cur_frm.set_value("awfis_mobile_no", args.caller_number)
                  dialog.hide();
              } else {
                  frappe.set_route("Form", "Lead", r.message);
                  dialog.hide();
                  cur_frm.refresh();
              }
            }
          })
        });
        dialog.show();
      }
});

//Set FirstName and LastName
frappe.ui.form.on("Lead", "first_name", function(frm){
    frm.set_value("lead_name", buildName(frm.doc.first_name, frm.doc.last_name));
});

frappe.ui.form.on("Lead", "last_name", function(frm){
    frm.set_value("lead_name", buildName(frm.doc.first_name, frm.doc.last_name));
});

//Lead Name cannot be hidden via Customize Form. Hide using script.
frappe.ui.form.on("Lead", "refresh", function(frm) {
    frm.toggle_display("lead_name", false);
    frm.toggle_display("lead_name", false);

    //Set sources by channel.
    var sources_by_channel = {
      "Sales Team" : ["Referral", "Marketing", "Broker", "Direct"],
      "Centre Walk-in": ["Outdoor", "Online", "Referral", "Marketing"],
      "Call Centre": ["Outdoor", "Online", "Referral", "Marketing", "Returning Customer", "NA"],
      "Inbound": ["Email", "SEM", "Online", "Instant Office", "Listings"]
    }

    var campaigns_by_sub_source = {
      "Events" : ["Internal", "External"],
      "Social Media": ["Facebook", "Twitter", "Instagram", "Youtube", "Google", "Linkedin"],
      "Online Listing": ["99Acres", "Magic Bricks", "CoWorkable", "Work Spot", "Space Hiring"],
      "Advertising": ["TV", "Radio", "Theatre", "Print", "3rd Party Websites"],
      "Friend/Colleague": ["Word of Mouth"]
    }

    cur_frm.set_query("source", function() {
      return {
        "filters": [
          ["Lead Source", "name", "in", sources_by_channel[cur_frm.doc.awfis_lead_channel]]
         ]
      }
    });

    cur_frm.set_query("awfis_lead_sub_source", function() {
      if ((cur_frm.doc.awfis_lead_channel == "Inbound") && (cur_frm.doc.source == "Online")) {
        return {
          "filters": [
            ["Lead Source", "name", "=", "Social Media"]
           ]
        }
      } else {
        return {
          "filters": [
            ["Lead Source", "awfis_lead_source_parent", "=", cur_frm.doc.source]
           ]
        }
      }
    });

    cur_frm.set_query("campaign_name", function() {
      if ((cur_frm.doc.awfis_lead_channel == "Sales Team") && (cur_frm.doc.source == "Marketing")) {
        return {
          "filters": [
            ["Campaign", "name", "in", ["Email", "Cold Calling"]]
           ]
        }
      } else {
        return {
          "filters": [
            ["Campaign", "name", "in", campaigns_by_sub_source[cur_frm.doc.awfis_lead_sub_source] || []]
           ]
        }
      }
    });
    set_field_visibility();

    //Hide mobile no in modify mode.
    frm.set_df_property("awfis_mobile_no", "read_only", frm.doc.__islocal ? 0 : 1);
    frm.set_df_property("lead_owner", "read_only", 1);

});

frappe.ui.form.on("Lead", "awfis_spaces_add", function(frm, cdt, cdn) {
console.log("Awfis Space Added");
})

//Set value of Mobile No when Awfis Mobile No is entered.
frappe.ui.form.on("Lead", "awfis_mobile_no", function(frm) {
    frm.set_value("mobile_no", frm.doc.awfis_mobile_no);
});

//Set value of Mobile No when Awfis Mobile No is entered.
frappe.ui.form.on("Lead", "awfis_company_website", function(frm) {
    frm.set_value("website", frm.doc.awfis_company_website);
});

//Set value of Mobile No when Awfis Mobile No is entered.
frappe.ui.form.on("Lead", "awfis_email_id", function(frm) {
    frm.set_value("email_id", frm.doc.awfis_email_id);
});

//Set value of Territory when Awfis Lead Territory is set.
frappe.ui.form.on("Lead", "awfis_lead_territory", function(frm) {
    frm.set_value("territory", frm.doc.awfis_lead_territory);
});

//Helpers
function buildName(fname, lname) {
  if (!lname) {
    return fname;
  } else if (!fname) {
    return lname;
  } else {
    return fname + ' ' + lname;
  }
}

// frappe.ui.form.on("Lead Awfis Space", "space_type", function(frm, cdt, cdn) {
//    var space = locals[cdt][cdn];
//    if (space.space_type == "Desk-Fixed" || space.space_type == "Desk-Flexi") {
//       space.capacity = 1;
//       set_capacity_property_readonly(1);
//    } else {
//       space.capacity = "";
//       set_capacity_property_readonly(0);
//    }
//    refresh_field("awfis_spaces");
// });

function set_capacity_property_readonly(state) {
    var df = frappe.meta.get_docfield("Lead Awfis Space","capacity", cur_frm.doc.name);
    df.read_only = state;
}

frappe.ui.form.on("Lead", "source", function(frm) {
  if (frm.doc.source === "IPC" || frm.doc.source === "Broker" ){
      frm.set_value("type", "Channel Partner");
  } else{
      frm.set_value("type", "");
  }
  cur_frm.set_value("awfis_lead_sub_source", "");
  cur_frm.set_value("campaign_name", "");
  set_field_visibility();
});

frappe.ui.form.on("Lead", "awfis_lead_channel", function(frm) {
    cur_frm.set_value("source", "");
    cur_frm.set_value("awfis_lead_sub_source", "");
    cur_frm.set_value("campaign_name", "");
    set_field_visibility();
});

frappe.ui.form.on("Lead", "awfis_lead_sub_source", function(frm) {
    cur_frm.set_value("campaign_name", "");
    set_field_visibility();
});

function set_field_visibility() {

  if (cur_frm.doc.awfis_lead_channel == "Sales Team") {
    cur_frm.set_df_property("awfis_lead_sub_source", "hidden", ["Referral", "Broker"].indexOf(cur_frm.doc.source) == -1);
  } else if (cur_frm.doc.awfis_lead_channel == "Call Centre") {
    cur_frm.set_df_property("awfis_lead_sub_source", "hidden", ["Returning Customer", "NA"].indexOf(cur_frm.doc.source) != -1);
  } else {
    cur_frm.set_df_property("awfis_lead_sub_source", "hidden", 0);
  }


  if (cur_frm.doc.awfis_lead_channel == "Sales Team") {
    cur_frm.set_df_property("campaign_name", "hidden", (cur_frm.doc.source != "Marketing"));
  } else if (["Events", "Social Media", "Online Listing", "Advertising", "Friend/Colleague"].indexOf(cur_frm.doc.awfis_lead_sub_source) == -1) {
    cur_frm.set_df_property("campaign_name", "hidden", 1);
  } else {
    cur_frm.set_df_property("campaign_name", "hidden", 0);
  }

  cur_frm.set_df_property("channel_partner", "hidden", cur_frm.doc.awfis_lead_channel == "Sales Team");
}