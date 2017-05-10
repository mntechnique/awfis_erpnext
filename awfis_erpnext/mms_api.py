import frappe
from frappe import _

import json, pdfkit, os
import calendar

@frappe.whitelist(allow_guest=True)
def add_pos_invoice(pos_invoice=None):
    awfis_pos_invoice = None
    if validate_request_header() != 1:
        return "You are not authorized to make this request."

    if pos_invoice:
        pos_invoice = json.loads(pos_invoice)
        if pos_invoice.get("customer"):
            pos_invoice_name = frappe.db.get_value("Sales Invoice",{"customer":pos_invoice.get("customer")},"name")

            if pos_inovie_name:
                awfis_pos_invoice = frappe.get_doc("Sales Invoice", pos_invoice_name)
            else:
                awfis_pos_invoice = frappe.new_doc("Sales Invoice")

            if awfis_pos_invoice:
                awfis_pos_invoice.posting_date = pos_invoice.get("posting_date")
                awfis_pos_invoice.customer = pos_invoice.get("customer")
                awfis_pos_invoice.is_pos = pos_invoice.get("is_pos")

                for i in pos_invoice.get("items"):
                    awfis_pos_invoice.item_code = i.get("item_code")
                    awfis_pos_invoice.qty = i.get("qty")
                     awfis_pos_invoice.warehuse = i.get("warehouse")


        awfis_pos_invoice.save(ignore_permissions=True)
        frappe.db.commit()
    else:
        return "Please specify Sales Invoice"

    return awfis_pos_invoice

def validate_request_header():
    key_header = frappe.get_request_header("awfis-api-key")
    key_local = frappe.get_single("Awfis Settings").api_key_knowlarity

    if key_header == "":
        return -1 #"Key header is blank"
    elif key_header != key_local:
        return 0 #"{0} != {1} : Key header does not match local key".format(key_header, key_local)
    else:
        return 1 #""
