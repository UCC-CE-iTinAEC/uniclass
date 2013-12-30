import csv
import sys
import datetime


# Read in file from command line to uniclass2_array

cmdargs = str(sys.argv)
uniclass2_array = []

with open(str(sys.argv[1]), 'rb') as csvfile:
  spam = csv.reader(csvfile, delimiter=',', quotechar='\"')
  count = 0
  for row in spam:
	uniclass2_array.append([]) 
	uniclass2_array[count] = row
	count += 1

# get current time - use for inserting into xml

now_day = datetime.date.today().strftime("%d")
now_month = datetime.date.today().strftime("%m")
now_year = datetime.date.today().strftime("%y")

# rest counter - used as flag when going through each line of the file
count = 0

# get letter of first item - make that one to check against when inserting xml headers for each section

letter_check = uniclass2_array[0][0]
first_letter = letter_check[0:2]

#print intro headers
xml_name = "<Name>"+first_letter+"</Name>"


xml_description = "<Description>Classifies construction works and spaces according to user activity or intended purpose based on Uniclass2 specifications.'Apply' creates a Classification Reference for selected IFC entity, using Uniclass2-required attributes derived from the item that you choose in the following list.</Description>"

xml_applicable_to = "<ApplicableTo><ClassName>IfcProject</ClassName><ClassName>IfcSpatialStructureElement</ClassName><ClassName>IfcGroup</ClassName><ClassName>IfcActor</ClassName><ClassName>IfcControl</ClassName><ClassName>IfcSpaceType</ClassName></ApplicableTo>"

xml_data_intro = "<Data><DataDescriptors><DataDescriptor Variable=\"number\" Title=\"Code\" /><DataDescriptor Variable=\"title\" Title=\"Description\" /></DataDescriptors><DataEntries>"

xml_data_outro = "</DataEntries></Data><Script><CreateClassificationReference><IfcRelAssociatesClassification Name=\"Uniclass2 - "+first_letter+"\"><IfcClassificationReference Name=\"$title\" ItemReference=\"$number\" Location=\"www.cpic.org.uk\"><IfcClassification Source=\"www.cpic.org.uk\" Name=\"Uniclass2\" Edition=\""+first_letter+"\"><IfcCalendarDate DayComponent=\""+now_day+"\" MonthComponent=\""+now_month+"\" YearComponent=\""+now_year+"\"/> <!-- EditionDate --></IfcClassification></IfcClassificationReference></IfcRelAssociatesClassification></CreateClassificationReference></Script>"

# print xml_header
print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<Rules Name=\"Uniclass2\">"
print "<Rule>"
print xml_name
print xml_description
print xml_applicable_to
print xml_data_intro

for row in uniclass2_array:

	letter_check = uniclass2_array[count][0]
	check_letter = letter_check[0:2]

	# check if we're onto a new section of codes - if so, insert new header

	if first_letter != check_letter:
		print xml_data_outro
		print "</Rule>"
		print "<Rule>"	

		first_letter = check_letter
		xml_name = "<Name>"+first_letter+"</Name>"

		print xml_name
		print xml_description
		print xml_applicable_to
		print xml_data_intro
 
	# if code is 11 long and next one isn't 14 print with included closing tag	
	# if next is 8 print closing tag

	if len(uniclass2_array[count][0]) == 11:
		
		if (count < len(uniclass2_array)-1):		
			if(len(uniclass2_array[count+1][0]) == 14):
				print "<DataEntry number=\""+uniclass2_array[count][0]+"\" title=\""+uniclass2_array[count][1]+"\">"
			else:
				print "<DataEntry number=\""+uniclass2_array[count][0]+"\" title=\""+uniclass2_array[count][1]+"\"/>"
		if (count < len(uniclass2_array)-1):		
			if(len(uniclass2_array[count+1][0]) == 8):
				print "</DataEntry>"

	# if code is 14 long print with included closing tag	
	# if next is 11 print closing tag
	# if next is 8 long print 2 closing tags
	# if next is 5 long print 3 closing tags
	if len(uniclass2_array[count][0]) == 14:
		
		print "<DataEntry number=\""+uniclass2_array[count][0]+"\" title=\""+uniclass2_array[count][1]+"\"/>"

		if (count < len(uniclass2_array)-1):		
			if(len(uniclass2_array[count+1][0]) == 11):
				print "</DataEntry>"
			if(len(uniclass2_array[count+1][0]) == 8):
				print "</DataEntry>"
				print "</DataEntry>"
			if(len(uniclass2_array[count+1][0]) == 5):
				print "</DataEntry>"
				print "</DataEntry>"
				print "</DataEntry>"
	

	# if code is 8 long print
	# if next is 8, close tag
	# if next is 5, close tag
	elif len(uniclass2_array[count][0]) == 8:
		print "<DataEntry number=\""+uniclass2_array[count][0]+"\" title=\""+uniclass2_array[count][1]+"\">"
		if (count < len(uniclass2_array)-1):		
			if(len(uniclass2_array[count+1][0]) == 5):

				end_letter_check = uniclass2_array[count][0]
				end_check_letter = end_letter_check[0:2]

				next_letter_check = uniclass2_array[count+1][0]
				next_check_letter = next_letter_check[0:2]


				if next_check_letter != end_check_letter:
					print "</DataEntry>"
					print "</DataEntry>"
				else:					
					print "</DataEntry>"
			if(len(uniclass2_array[count+1][0]) == 8):
				print "</DataEntry>"


	
	# if code is 5 long print
	# if previous is 8, close tag
	# if previous is 11, close tag twice
	# if next code is 5 close tag 	
	elif len(uniclass2_array[count][0]) == 5:
		if count > 0:
			if(len(uniclass2_array[count-1][0]) == 11):
				print "</DataEntry>"
				print "</DataEntry>"
			if(len(uniclass2_array[count-1][0]) == 8):

					end_letter_check = uniclass2_array[count][0]
					end_check_letter = end_letter_check[0:2]
		
					first_letter_check = uniclass2_array[count-1][0]
					first_check_letter = first_letter_check[0:2]
	
					if first_check_letter == end_check_letter:
						print "</DataEntry>"

		print "<DataEntry number=\""+uniclass2_array[count][0]+"\" title=\""+uniclass2_array[count][1]+"\">"

		if (count < len(uniclass2_array)-1):		

			if(len(uniclass2_array[count+1][0]) == 5):
				print "</DataEntry>"

				end_letter_check = uniclass2_array[count][0]
				end_check_letter = end_letter_check[0:2]

				next_letter_check = uniclass2_array[count+1][0]
				next_check_letter = next_letter_check[0:2]

				first_letter_check = uniclass2_array[count-1][0]
				first_check_letter = first_letter_check[0:2]


				if next_check_letter != end_check_letter:
					if next_check_letter == first_check_letter:				
						print "</DataEntry>"


	count +=1

#end tags

if(len(uniclass2_array[len(uniclass2_array)-1][0]) == 11):
	print "</DataEntry>"
	print "</DataEntry>"
	print "</DataEntry>"

if(len(uniclass2_array[len(uniclass2_array)-1][0]) == 8):
	print "</DataEntry>"
	print "</DataEntry>"

if(len(uniclass2_array[len(uniclass2_array)-1][0]) == 5):
	print "</DataEntry>"

print xml_data_outro
print "</Rule>"
print "</Rules>"
