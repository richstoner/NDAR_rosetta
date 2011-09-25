#!/usr/bin/env python
# NDAR -> Redcap conversion
# Rich Stoner
# UCSD Autism Center of Excellence

import os, pprint, sys, json, csv, urllib2
from urllib2 import Request, urlopen, URLError, HTTPError


# read in file from csv, build database
# convert to dictionary format
# write redcap form
# "Variable / Field Name", 							-> ndar::ElementName
# "Form Name", 										-> ndar::filename (ados_input)
# "Section Header",									-> undefined, custom
# "Field Type",										-> ndar::DataType
# "Field Label",									-> ndar::ElementDescription
# "Choices, Calculations, OR Slider Labels",		-> ndar::Size, ndar::ValueRange
# "Field Note",										-> ndar::ValueRange, placeholder text
# "Text Validation Type OR Show Slider Number",		-> ndar::Size, ndar::ValueRange 
# "Text Validation Min",							-> ndar::Size, ndar::ValueRange
# "Text Validation Max",							-> ndar::Size, ndar::ValueRange
# Identifier?,										-> undefined, custom
# "Branching Logic (Show field only if...)",		-> undefined, custom
# "Required Field?",								-> ndar::Required
# "Custom Alignment",								-> undefined, custom
# "Question Number (surveys only)"					-> undefined, custom


def downloadFile(url_to_download, filename):
	from urllib2 import Request, urlopen, URLError, HTTPError

	#create the url and the request
	req = Request(url_to_download)

	# Open the url
	try:
		f = urlopen(req)
		print "downloading " + url_to_download

		# Open our local file for writing
		local_file = open(filename, "wb")
		#Write to our local file
		local_file.write(f.read())
		local_file.close()

	#handle errors
	except HTTPError, e:
		print "HTTP Error:",e.code , url
	except URLError, e:
		print "URL Error:",e.reason , url



def buildListFromFile(filename='ndar_list.html'):

	listinput = open(filename, 'r')

	hasTableStart = False
	hasCSVurl = False
	hasCSVdesc = False

	filelist = []
	newfile = {}

	for line in listinput:
		if 'div' in line:
			pass
		else:

			if 'href=' in line and not hasCSVurl:
				newfile['url'] = 'http://ndar.nih.gov/ndarpublicweb/' + line.split('="')[1].split('"')[0]
				# newfile['shortname'] = line.split('>')[1].split("<")[0]
				newfile['shortname'] = newfile['url'].split('short_name=')[1]
				hasCSVurl = True
				# new entry 
			
			if 'width="60' in line and not hasCSVdesc:
				newfile['desc'] = line.split('>')[1].split("<")[0]
				hasCSVdesc = True

			if 'table' in line and not hasTableStart:
				hasTableStart = True

			elif 'table' in line and hasTableStart:
				# print newfile['shortname']
				newfile['targetfile'] = os.path.abspath(os.curdir) + '/ndardata/' + newfile['shortname'] + '.csv'
				
				if not os.path.exists(newfile['targetfile']):
					csvurl = 'http://ndar.nih.gov/ndarpublicweb/csvfileopener?filetype=0&short_name=%s' % (newfile['shortname'])
					if download_files_from_ndar:
						downloadFile(csvurl, newfile['targetfile'] )
						filelist.append(newfile)
				else:
					# path exists
					filelist.append(newfile)

				hasTableStart = False
				hasCSVurl = False
				hasCSVdesc = False
				newfile = {}

	return filelist



def convertDataType(input_string, ndar_valuerange):
# ndar types: GUID, String, Integer, Float, Date
# redcap types: notes, radio, yesno, text, slider, file, checkbox, calc, dropdown
	if input_string == 'GUID':
		return 'text'

	if input_string == 'String':
		if len(ndar_valuerange.split(';')) > 1:
			# we have a multiple choice 
			return 'dropdown'
		else:
			return 'text'

	if input_string == 'Integer':
		# most likely choice if only has a few (3-5) options
		if len(ndar_valuerange.split(';')) > 1:
			# we have a multiple choice 
			return 'dropdown'
		else:
			return 'text'

	if input_string == 'Float':
		# best fit
		return 'text'

	if input_string == 'Date':
		return 'text'

	# default case... should review
	return 'text'

def convertRequired(input_string):
	if input_string == 'Required':
		return 'y'
	if input_string == 'Recommended':
		return 'y'		
	if input_string =='Optional':
		return ''

def convertValueRange(data_type, ndar_valuerange, ndar_size, fieldnotes):

	# value range, input validation, min, max
	return_array = {}
	return_array['value_str'] = ''
	return_array['validation'] = ''
	return_array['value_min'] = ''
	return_array['value_max'] = ''
	return_array['field_note'] = ''

	if ndar_valuerange == '':
		# no range supplied, do nothing
		if data_type == 'String':
			# no expected type
			return_array['field_note'] = 'Limit: %s characters' % (ndar_size)

	if data_type == 'Date':
		return_array['validation'] = 'date_ymd'

## Review this -> requires additional thought regarding GUID 
	if ndar_valuerange == 'NDAR*':
		# special value, needs additionary work 
		return_array['field_note'] = 'Requires Valid GUID'

	if len(ndar_valuerange.split(';')) > 1:
		# we have a multiple choice 
		
		notes_split = fieldnotes.split(';')
		# print notes_split

		outputstr = ''
		choice_count = 0
		choices = ndar_valuerange.split(';')
		
		if enable_dropdown_details:
			for choice in choices:
				clean_choice = choice.strip('"')

				if len(notes_split) == len(choices):
					outputstr += '%s, %s' % (clean_choice, notes_split[choice_count])
					if choice_count < len(choices)-1:
						outputstr += ' | '
					choice_count += 1
				else:
					outputstr += '%s, %s' % (clean_choice, clean_choice)
					if choice_count < len(choices)-1:
						outputstr += ' | '
					choice_count += 1


		else:
			for choice in choices:
				clean_choice = choice.strip('"')			
				outputstr += '%s, %s' % (clean_choice, clean_choice)
				if choice_count < len(choices)-1:
					outputstr += ' | '
				choice_count += 1
			
		return_array['value_str'] = outputstr

	elif ' to ' in ndar_valuerange:
		# we have a range option
		bounds = ndar_valuerange.split(' to ')
		lower = bounds[0].strip('"')
		upper = bounds[1].strip('"')
		return_array['value_min'] = lower
		return_array['value_max'] = upper
		return_array['validation'] = 'number'

	elif '+' in ndar_valuerange:
		bounds = ndar_valuerange.split('+')
		lower = bounds[0].strip('"')
		
		return_array['validation'] = 'number'
		return_array['value_min'] = lower
		# return_array['value_max'] = upper

	else:
		return_array['field_note'] = fieldnotes

	return return_array




####################################################################################
# main script
####################################################################################

# script settings
download_files_from_ndar = False
enable_dropdown_details = True

outputfilename = 'generated_file_for_upload.csv'


# generate list of files from ndar html file
ndar_file_list = buildListFromFile()

redcap_items = []

# to limit number of items processed (debug use only)
run_limit = 3000
run_count = 0

print 'Files to process: %d' % (len(ndar_file_list))

# process each file in list
for ndar_input in ndar_file_list:

	if run_count < run_limit:
		run_count +=1

		print 'Parsing ' + ndar_input['targetfile']
		first_load = True
		fexample = open(ndar_input['targetfile'], 'r')
		reader = csv.reader(fexample)

		items = []

		item_count = 0
		item_limit = 200

		section_list = []

		# parsing file
		for line in reader:
			if first_load:
				first_load = False
				column_headers = line #.split(',')

				for column in column_headers:
					stripped = column.split('"')
				# print column_headers
			else:
				# not first load
				if item_count < item_limit:
					item_count += 1
					item_dict = {}
					items_array = line #.split(',')

					item_dict['element_name'] 	= items_array[0]
					item_dict['data_type'] 		= items_array[1]
					item_dict['response_size'] 	= items_array[2]
					item_dict['response_units']	= items_array[3]
					item_dict['required'] 		= items_array[4]
					item_dict['element_description'] = items_array[5]
					item_dict['value_range'] 	= items_array[6]
					item_dict['keywords'] 		= items_array[7]
					item_dict['element_notes'] 	= items_array[8]
					item_dict['section'] 		= items_array[9]
					# print item_dict['section']
					item_dict['Aliases'] 		= items_array[10].split('\n')[0]

					items.append(item_dict)

		print 'Found %d items in %s' % (len(items), ndar_input['targetfile'])


		# for each parsed item, add to list 
		for ndar_item in items:
			redcap_item = []

		# "Variable / Field Name", 							-> ndar::ElementName
			redcap_item.append('a'+str(run_count) + '_' + ndar_item['element_name'])

		# "Form Name", 										-> ndar::filename (ados_input)
			redcap_item.append(ndar_input['desc'])

		# "Section Header",									-> undefined, custom
			
			if ndar_item['section'] in section_list:
				redcap_item.append('')
			else:
				redcap_item.append(ndar_item['section'])
				section_list.append(ndar_item['section'])

		# "Field Type",										-> ndar::DataType
			redcap_item.append(convertDataType(ndar_item['data_type'], ndar_item['value_range']))

		# "Field Label",									-> ndar::ElementDescription
			redcap_item.append(ndar_item['element_description'])


			value_dictionary = convertValueRange(ndar_item['data_type'], ndar_item['value_range'], ndar_item['response_size'], ndar_item['element_notes'])

		# "Choices, Calculations, OR Slider Labels",		-> ndar::Size, ndar::ValueRange
			redcap_item.append(value_dictionary['value_str'])	

		# "Field Note",			 							-> ndar::ValueRange, placeholder text

			if enable_dropdown_details:
				if len(ndar_item['element_notes'].split(';')) > 1:
					redcap_item.append('')
				else:	
					redcap_item.append(ndar_item['element_notes'])
			else:
				redcap_item.append(ndar_item['element_notes'])

		# "Text Validation Type OR Show Slider Number",		-> ndar::Size, ndar::ValueRange 
			redcap_item.append(value_dictionary['validation'])

		# "Text Validation Min",							-> ndar::Size, ndar::ValueRange
			redcap_item.append(value_dictionary['value_min'])

		# "Text Validation Max",							-> ndar::Size, ndar::ValueRange
			redcap_item.append(value_dictionary['value_max'])

		# Identifier?,										-> undefined, custom
			redcap_item.append('')

		# "Branching Logic (Show field only if...)",		-> undefined, custom
			redcap_item.append('')

		# "Required Field?",								-> ndar::Required
			redcap_item.append(convertRequired(ndar_item['required']))

		# "Custom Alignment",								-> undefined, custom
			redcap_item.append('')

		# "Question Number (surveys only)"					-> undefined, custom
			redcap_item.append('')


			redcap_items.append(redcap_item)


# finally, write list to CSV for upload 

f = open(outputfilename, 'wt')
try:
    writer = csv.writer(f)
    writer.writerow(("Variable / Field Name","Form Name","Section Header","Field Type","Field Label","Choices, Calculations, OR Slider Labels","Field Note","Text Validation Type OR Show Slider Number","Text Validation Min","Text Validation Max","Identifier?","Branching Logic (Show field only if...)","Required Field?","Custom Alignment","Question Number (surveys only)"))

    for item in redcap_items:
    	writer.writerow(item)

finally:
    f.close()





