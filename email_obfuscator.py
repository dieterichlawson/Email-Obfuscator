#!/usr/bin/env python
# encoding: utf-8
"""
email_obfuscator.py

Created by Dieterich Lawson on 2011-01-26.
"""

import sys
import getopt


help_message = '''Email Obfuscator v1.0

    Email Obfuscator prints Javascript that helps you obfuscate email addresses.
    Simply pass in all email addresses separated by spaces and it will output the required Javascript.
    The javascript assumes that you have <span> elements on your HTML page with ids like:

        email-x

    Where x is a number, starting from 1, that represent's the email's placement on the page.
'''

javascript_body = '''<script type="text/javascript">
var key = %s;
var cypher = %s;

window.onload=function(){
	for (var email_id in cypher){
		var email_text = "";
		var char_list = cypher[email_id];
		for(var i in char_list){
			email_text+=key[char_list[i]];
		}
		document.getElementById(email_id).innerHTML=email_text;
	}
}
</script>'''

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "h", ["help"])
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		for option, value in opts:
			if option in ("-h", "--help"):
				raise Usage(help_message)
				
		char_list = []
		email_dict = {}
		
		for arg in args:
			for pos, char in enumerate(arg):
				if char not in char_list:
					char_list.append(char)
		for pos1, arg in enumerate(args):
			email_list=[]
			for char in arg:
				for pos, dict_char in enumerate(char_list):
					if char == dict_char:
						email_list.append(pos)
			email_dict["email-" + str(pos1+1)]=email_list		
				
		print javascript_body % (str(char_list), str(email_dict))
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		return 2


if __name__ == "__main__":
	sys.exit(main())
