from PIL import Image
import re
import zipfile
import os

morsecode = {
		'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
}

def rgb_to_hex(rgb):
  rgb = eval(rgb)
  r = rgb[0]
  g = rgb[1]
  b = rgb[2]
  return '#%02X%02X%02X' % (r,g,b)

def hex_to_rgb(hex):
	if hex[0] == '#':
		hex = hex[1:]
	assert(len(hex) == 6)
	rgb = int(hex[:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)
	return rgb

def read_file(file):
	file_handle = open(file, 'rb')

	im = Image.open(file) 
	px = im.load()

	width,height=im.size
	hex = ""
	for i in range(width):
		rgb = str(im.getpixel( (i,0) ) )
		hex = hex + rgb_to_hex(rgb)
	hex_to_morse(hex)

def write_file(msg, filename):
	lop = msg
	size = (len(lop),1)
	im = Image.new('RGB',size)
	px = im.load()

	for i in range (len(lop)):
		rgb = hex_to_rgb(lop[i])
		px[i,0] = rgb
	im.save(filename)

def text_to_morse(theMsg):
	morseC = ' '
	for char in theMsg:
		morseC = morseC + morsecode[char.upper()]+' '
	return morseC

def text_to_hex(message):
	mrs = text_to_morse(message)	
	list_of_hex = morse_to_hex(mrs)
	return list_of_hex

def morse_to_text(urlencode):
	morseTable = re.split(' ',urlencode)
	deciphered=''
	for key in morseTable:
		for item in morsecode:
			if (key == morsecode[item]):
				deciphered = deciphered + item
	print (deciphered) 

def morse_to_hex(theMorse):
	lohex = list(theMorse)
	for n,i in enumerate(lohex):
		if i == '-':
			lohex[n] = '#00002D'	
		if i == '.':
			lohex[n] = '#00002E'
		if i == ' ':
			lohex[n] = '#000020'
	return lohex

def hex_to_morse(theHex):
	urlencode = theHex.replace('#0000','%')
	urlencode = urlencode.replace('%2D','-')
	urlencode = urlencode.replace('%2E','.')
	urlencode = urlencode.replace('%20',' ')
	morse_to_text(urlencode)


def create_zip():
	outerfile = input("Give filename of container file (existing image) - eg: forest.png \n")
	innerfile = input("Give filename of hidden file (will be created) - eg: hidden.png \n")
	message = input("Give plaintext message to hide (only english characters and numbers) - eg: hello1 \n")
	try:
		colors = text_to_hex(message)
		infile = write_file(colors, innerfile)	
		infname = innerfile.split('.')

		print ('creating archive')

		with zipfile.ZipFile(infname[0]+'.zip', "w") as zf:
			zf.write(innerfile)
		os.system('cat '+infname[0]+'.zip >> '+outerfile)
		os.system('rm '+infname[0]+'.zip')
		os.system('rm '+innerfile)
		#copy /b inJPG + somefile.zip somepic_new.jpg
	finally:
	    zf.close()


def read_zip():
	img = input("Give filename of morseC to read :\n")
	try:
		print ('unziping archive')
		with zipfile.ZipFile(img, "r") as z:
			contents = z.namelist()
			extract = z.extractall()
			read_file(contents[0])
	except ValueError:
		print ("Something went badly wrong.. Now Exiting..")
#------------------
#		main
#------------------
choice = input("Press 1 to create a morseC steganography or \nPress 2 to read a morseC steganography \n")
if (int(choice) == 1):
	create_zip()
elif (int(choice) == 2):
	read_zip()
else :
	exit()
