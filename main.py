import argparse
import sys
import re

def check_syntax(string):
	operators=["while","if","do","for","foreach"]
	for operator in operators:
	        if len(re.findall("{operator}\s*\(.*\)".format(operator=operator),string))>0:
			return True
	if len(re.findall("[^<]*\w+\s*([:!+-]?=|={2,3}|[<>]=?|!=)\s*\w+",string))>0:
		return True
	if len(re.findall("TODO",string))>0:
		return True
	if len(re.findall("FIXME",string))>0:
		return True
	### maybe ###
	if len(re.findall("\w+\s*\(.*\)",string))>0:
		return True
	return False

def case(x,filebody,index):
	n=0
	if x == "\"":
		char,n=stringCheck(filebody,index,"\"")
	elif x == "'":
		char,n=stringCheck(filebody,index,"'")
	elif x == "`":
		char,n=stringCheck(filebody,index,"`")
	elif x == "/":
		char,n=commentCheck(filebody,index)
	elif x == "\n":
		char=index
		n=1
	else:
		char=index
	return char,n

def casePerl(x,filebody,index):
	n=0
	if x == "\"":
		char,n=stringCheck(filebody,index,"\"")
	elif x == "'":
		char,n=stringCheck(filebody,index,"'")
	elif x == "`":
		char,n=stringCheck(filebody,index,"`")
	elif x == "#":
		char,n=commentCheckPerl(filebody,index)
	elif x == "\n":
		char=index
		n=1
	else:
		char=index
	return char,n

def commentCheckPerl(string,i):
	n=0
	while string[i]!="\n":
		i+=1
	return (i,n)

def commentCheck(string,i):
	n=0
	if string[i+1]=="/":
		while string[i]!="\n":
			i+=1
		return (i,n)
	elif string[i+1]=="*":
		while True:
			if string[i]=="\n":
				n+=1
			if string[i-1]=="*" and string[i]=="/":
				break
			i+=1
		return (i+1,n)
	return (i,n)

def stringCheck(string,i,n):
	nc=0
	for char in range(i+1,len(string)-1):
		if string[char]=="\n":
			nc+=1
		if string[char]==n:
			backslashes=0
			while string[char-1-backslashes]=="\\":
				backslashes+=1
			if backslashes%2==0:
				return char+1,nc

def getRegularFile(filename):
	file=open(filename, "r")
	filebody=file.read()
	file.close()
	char=0
	delete_mas=[]
	tmp=""
	final=[]
	filebody_len=len(filebody)-1
	glob_n=1
	while char!=filebody_len:
		curr_char=filebody[char]
		if args.perl:
			check,n=casePerl(curr_char, filebody, char)
		else:
			check,n=case(curr_char, filebody, char)
		if check==char:
			char+=1
		elif filebody[char] in "\"'`":
			char=check
		else:
			start_line=0
			tmp_char=char
			while filebody[tmp_char]!="\n":
				start_line+=1
				tmp_char-=1
			string="{}:{}:{}".format(glob_n,start_line,filebody[char:check]).split("\n")
			tmp_n=glob_n
			tmp_len=len(string)-1
			for i in range(1,tmp_len):
				tmp_n+=1
				string[i]="{}:{}".format(tmp_n,string[i])
			if tmp_len>0:
				start_line=0
				tmp_char=char
				while filebody[tmp_char]!="\n":
					start_line+=1
					tmp_char-=1
				string[-1]="{}:{}:{}".format(tmp_n,start_line,string[-1])
			string="\n".join(string)
			delete_mas.append([char,check])
			if check_syntax(string) or args.regex:
				final.append(string)
			char=check
		glob_n+=n
	if args.delete:
		for pallet in delete_mas[::-1]:
			filebody=filebody[0:pallet[0]]+filebody[pallet[1]:]
		file=open(filename, "w")
		file.write(filebody)
		file.close()
	return "\n".join(final)

if __name__=="__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument('--regex','-r', dest="regex", action="store_false", help='Syntax regex search')
        parser.add_argument('--perl','-p', dest="perl", action="store_true", help='Syntax for Perl/Python')
        parser.add_argument('--delete','-d', dest="delete", action="store_true", help='Delete all comments(DO BACKUP!)')
	parser.add_argument('input', action="store", help='Input file with path of searching files')
	parser.add_argument('output', action="store", help='Output file for report')
        args = parser.parse_args()
	file=open(args.output,"w")

	file_r=open(args.input,"r")
	files_mas=file_r.read().split("\n")[:-1]
	file_r.close()
	len_f=len(files_mas)

	for i in files_mas:
		sys.stderr.write("{}/{}\r".format(files_mas.index(i)+1,len_f))
		try:
			comments=getRegularFile(i)
			if comments:
				file.write("### {} ###\n".format(i))
				file.write(comments)
				file.write("\n\n")
		except:
			pass
	file.close()
	sys.stderr.write("\n")
