'''
Author: Nisarga Patel

This file will contain the JSON Schemas for HackCRM

'''


'''

This JSON schema is used to validate contacts 


'''
contact = {

	"type" : "object",
	"properties" : {

		"name" : {"type" : "string", "description" : "Name of the contact"},
		"company" : {"type" : "string", "description" : "Company of the contact"},
		"datetime" : {"type" : "string", "description" : "Datetime"},
		"email" : {"type" : "string", "description" : "Email of the contact"},
		"phone" : {"type" : "string", "description" : "Phone Number"},
		"address" : {"type" : "string", "description" : "Address of the contact"},
		"profile_img" : {"type" : "string", "description" : "Profile Image of the contact"}
	},
	"required" : ["name", "company", "datetime", "email", "phone"]
}
