import frappe
from frappe import _

import json, pdfkit, os
import calendar

@frappe.whitelist()
def add_pos_invoice(data):
    print (data)

    if not data:
        frappe.local.response = "POS Invoice data was not supplied."

    pos_invoice = None
    try:
        pos_invoice = json.loads(data)
    except Exception as e:
        return "POS Invoice could not be converted to JSON: {0}".format(e) 

    existing_invoice = frappe.db.get_value("Sales Invoice", 
        filters={"awfis_pos_invoice_no": pos_invoice.get("invoice_no")}, fieldname="name")

    for x in xrange(1,10):
        print existing_invoice

    if existing_invoice:
        return "POS Invoice {0} already saved as {1}.".format(pos_invoice.get("invoice_no"), existing_invoice)

    awfis_pos_invoice = frappe.new_doc("Sales Invoice")
    awfis_pos_invoice.posting_date = pos_invoice.get("posting_date")
    awfis_pos_invoice.customer = pos_invoice.get("customer")
    awfis_pos_invoice.is_pos = 1
    awfis_pos_invoice.awfis_pos_invoice_no = pos_invoice.get("invoice_no")

    for i in pos_invoice.get("items"):
        awfis_pos_invoice.append("items", {
            "item_code": i.get("item_code"),
            "warehouse": i.get("warehouse"),
            "qty":i.get("qty"),
            "rate":i.get("rate"),
        })
    try:
        awfis_pos_invoice.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        return "POS Invoice {0} was not saved. {1}".format(pos_invoice.get("invoice_no"), e.message)
    
    return "POS Invoice {0} saved as {1}.".format(pos_invoice.get("invoice_no"), awfis_pos_invoice.name)
