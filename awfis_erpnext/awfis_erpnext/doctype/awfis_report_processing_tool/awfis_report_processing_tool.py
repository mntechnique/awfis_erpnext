# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import csv, ast, json
from bs4 import BeautifulSoup
from awfis_erpnext.awfis_erpnext.api import get_filedata

class AwfisReportProcessingTool(Document):
	pass
	# def process_comments(self):

	# 	file_rows = []
	# 	out_rows = []

	# 	csv_path = frappe.utils.get_site_path() + self.lead_report

	# 	with open(csv_path, 'rb') as csvfile:
	# 		rdr = csv.reader(csvfile, delimiter=str(','), quotechar=str('|'))

	# 		for row in rdr:
	# 			file_rows.append(row)

	# 		columns_row = file_rows[0]
	# 		comments_index = columns_row.index("_Comments")

	# 		for row in rdr:
				
			



	# 	return file_rows			
				
			# column_headings_row = file_rows[0]

			# for i in xrange(1, len(file_rows) - 1):
			# 	record_core = ""

			# 	if len(file_rows[i]) == len(column_headings_row):
			# 		for j in range(0, len(column_headings_row) - 1):
			# 			record_core += '"' +  column_headings_row[j] + '" : "' + file_rows[i][j] + '", '

			# 		record_json_string = "{" + record_core[:-2] + "}"
			# 		json_data.append(json.loads(record_json_string))

			# return final_json

@frappe.whitelist()
def get_processed_lead_report(lead_report):
	csv_path = frappe.utils.get_site_path() + lead_report
	
	outfile_name = "/tmp/Processed_Leads.csv"
	with open(csv_path,'r') as csvinput:
		with open(outfile_name, 'w') as csvoutput:
			writer = csv.writer(csvoutput, lineterminator='\n')
			reader = csv.reader(csvinput)

			all = []
			row = next(reader)
			row.append('Processed Comments')
			all.append(row)

			comment_idx = row.index("_Comments")
			for row in reader:
				#row.append(self.process_comment(row[comment_idx], row))
				row[comment_idx] = process_comment(row[comment_idx], row)
				all.append(row)

			writer.writerows(all)

	frappe.local.response.filename = outfile_name.split("/")[-1]
	frappe.local.response.filecontent = get_filedata(outfile_name)
	frappe.local.response.type = "download"

def process_comment(row_comments, row):
	if row_comments:
		comments_json = json.loads(row_comments)

		out = []
		
		for comment_json_row in comments_json:
			try:
				comment = frappe.db.get_value("Communication", comment_json_row.get("name"), "content")
				clean_comment = BeautifulSoup(comment).text
				out.append(clean_comment + '\n')
			except Exception as e:
				pass
			
		return "".join(out)
	else:
		return ""

	
	#//Diagnostic//
	# def process_comment(self, row_comments, row):
	# 	if row_comments:
	# 		comments_json = json.loads(row_comments)

	# 		out = []
			
	# 		for comment_json_row in comments_json:
	# 			try:
	# 				comment = frappe.db.get_value("Communication", comment_json_row.get("name"), "content")
	# 				print "COMMENT", comment
	# 				clean_comment = BeautifulSoup(comment).text
	# 				out.append(clean_comment + '\n')
	# 			except Exception as e:
	# 				print "BSERROR", row[0], row[1]
				
	# 		return "".join(out)
	# 	else:
	# 		return ""

			







