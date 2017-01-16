import frappe
from frappe import _
import os
import io


def get_filedata(file_name, options=None):
	fname = file_name #os.path.join("/tmp", file_name)

	try:
		with open(fname, "rb") as fileobj:
			filedata = fileobj.read()
	except IOError, e:
		if ("ContentNotFoundError" in e.message
			or "ContentOperationNotPermittedError" in e.message
			or "UnknownContentError" in e.message
			or "RemoteHostClosedError" in e.message):

			# allow pdfs with missing images if file got created
			if os.path.exists(fname):
				with open(fname, "rb") as fileobj:
					filedata = fileobj.read()

			else:
				frappe.throw(_("Could not open file."))
		else:
			raise
	finally:
		cleanup(fname)
	print filedata
	return filedata
	
def cleanup(fname):
	if os.path.exists(fname):
		os.remove(fname)
