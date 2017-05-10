import frappe
from frappe import _

import json, pdfkit, os
import calendar

@frappe.whitelist(allow_guest=True)
def add_pos_invoice(pos_invoice=None):
    awfis_pos_invoice = None
    if validate_request_header() != 1:
        return "You are not authorized to make this request."

    if not pos_invoice:
        return "POS Invoice data was not supplied."

    try:
        pos_invoice = json.loads(pos_invoice)
    except Exception as e:
        return "POS Invoice could not be converted to JSON: {0}".format(e) 

    pos_invoice_name = frappe.db.get_value("Sales Invoice",{"customer":pos_invoice.get("customer")},"name")

    awfis_pos_invoice = frappe.new_doc("Sales Invoice")
    
    awfis_pos_invoice = frappe.get_doc("Sales Invoice", pos_invoice_name)
    awfis_pos_invoice.posting_date = pos_invoice.get("posting_date")
    awfis_pos_invoice.customer = pos_invoice.get("customer")
    awfis_pos_invoice.is_pos = 1
    awfis_pos_invoice.append("items": {
        "item_code": i.get("item_code"),
        "warehouse": i.get("warehouse"),
        "qty":i.get("qty")
    })
    
    try:
        awfis_pos_invoice.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        raise
    
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
