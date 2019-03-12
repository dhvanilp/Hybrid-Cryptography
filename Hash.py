def newascii(character):
	return ord(character) + 104

def oldascii(asciiVal):
	return  int(asciiVal) - 104

def encode(msg):
	string_ascii = ''
	for i in msg:
		string_ascii+=str(newascii(i));
	return string_ascii;

def decode(newascii_string):
	pack = ''
	i = 0
	dec_message = ''
	while (i < len(str(newascii_string))):
		pack = newascii_string[i:i+3]
		dec_message+=chr(oldascii(pack))
		i=i+3
	return dec_message;	
