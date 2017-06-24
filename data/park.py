import re
import json

with open("parks.txt") as fh:
	strng = ''.join(fh.readlines())
	strng = strng.split('<tr>')

lst = []

for park in range(1, 60):
	regex = ur'<th scope="row"><a href="(.+?)"'
	wiki = re.findall(regex, strng[park])

	for page in wiki:
		page = 'https://en.wikipedia.org' + page
		el = {'page' : page}

	regex = ur'src=\"(.+?)\"+?'
	url = re.findall(regex, strng[park])
	el.update({'url':''.join(url)})

	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', strng[park])
	cleantext = cleantext.split('\n')

	for txt in cleantext:
		if txt == '' or txt== ' ':
			cleantext.remove(txt)

	descrip = re.sub(r'\[.*?\] ', '', cleantext[6])
	descrip = re.sub(r'\[.*?\]', '', descrip)

	el.update({
		'name':cleantext[0],
		'state':cleantext[1],
		'date':cleantext[3][23:],
		'area':re.sub(r' \(.*?\)', '', cleantext[4][22:]),
		'visitors':cleantext[5],
		'descrip':re.sub(r'\(.*?\)', '', descrip)
		})

	lst.append(el)

with open('parks.json', 'w') as fp:
	json.dump(lst, fp, indent=1)