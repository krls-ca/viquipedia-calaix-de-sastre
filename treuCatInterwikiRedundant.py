#!/usr/bin/python
# -*- coding: utf-8 -*-

import pywikibot, re
import time

def main():
	site = pywikibot.Site("ca", "wikipedia")
	#stre = u"Cos"
	arts = pywikibot.Category(site, u"Articles amb interviquis locals").articles(recurse=1, reverse=True, content=True)
	for art in arts:
		print art.title
		text = art.text
		match = re.search(u"\[\[([a-z]{2,3}):(.*)]]", text)
		if not match:
			new_text = text.replace("[[Categoria:Articles amb interviquis locals]]", "")
			pywikibot.showDiff(text,new_text)
			#sure = raw_input('Are you sure? (y/n)')
			sure = 'y'
			if sure == 'y':   # etc.
				art.put(new_text, comment = u'#QQ17: No hi ha interwikis locals. Elimino la "Categoria:Articles amb interviquis locals".', minorEdit=True)
			else:
				continue
		else:
			if len(match.groups()) == 2:
				try:
					site2 = pywikibot.Site(match.group(1), "wikipedia")
					page = pywikibot.Page(site2, match.group(2))
					if page.isRedirectPage():
						page = page.getRedirectTarget()		
						#sure = raw_input('Are you sure? (y/n)')
						sure = 'y'						
						if sure == 'y':
							print sure
							new_text = text.replace(match.group(0), "")
							pywikibot.showDiff(text,new_text)
							#sure2 = raw_input('Are you sure? (y/n)')
							sure2 = 'y'							
							if sure2 == 'y':   # etc.
								art.put(new_text, comment = u'#QQ17: Elimino interwikis erroni', minorEdit=True)
				except pywikibot.exceptions.NoPage as nopage:
					print "EXCEPTION " + match.group(2)
				except pywikibot.exceptions.InconsistentTitleReceived as inconsistentTitleReceived:
					continue
				except pywikibot.exceptions.UnknownSite as UnknownSite:
					continue

if __name__ == '__main__':
	main()
