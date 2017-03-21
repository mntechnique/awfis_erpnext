# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe

def execute():
	frappe.db.set_value("DocType", {"name": "Lead Awfis Space"}, "editable_grid", 1)
	frappe.db.commit()