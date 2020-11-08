#!/usr/bin/python
# -*- coding: utf-8 -*-

import pywikibot, re

def main():
	site = pywikibot.Site("ca", "wikipedia")
	arts = pywikibot.Category(site, u"Articles amb interviquis dins del text").articlesList(recurse=1)
	for art in arts:
		print art.title
		text = art.text
		match = re.search(u"(\[\[:.*?\]\])", text)
		if not match:
			new_text = text.replace("[[Categoria:Articles amb interviquis dins del text]]", "")
			pywikibot.showDiff(text,new_text)
			art.put(new_text, u'No té interwikis dins el text. Elimino la "Categoria:Articles amb interviquis dins del text".')
		else:
			for item in match.groups():
				piece = re.escape(item)
				pieceREF = u'(<ref>.*?{0}.*?<\/ref>)'.format(piece)
				matchREF = re.search(pieceREF, text)
				if matchREF:
					if len(matchREF.groups()) > 0:
						new_text = text.replace(matchREF.group(1), "")
						pywikibot.showDiff(text,new_text)
						do = raw_input('Do you want to erase this reference? (y/n)')
						if do == 'y':
							text = new_text
				else:
					splittedPiece = item.split(u"|")
					new_text = text.replace(u"{0}|".format(splittedPiece[0]), "[[")
					pywikibot.showDiff(text,new_text)
					do = raw_input('Do you want to erase this link? (y/n)')
					if do == 'y':
						text = new_text
			if art.text != text:
				match = re.search(u"(\[\[:.*?\]\])", text)
				if not match:
					text = text.replace("[[Categoria:Articles amb interviquis dins del text]]", "")
				pywikibot.showDiff(art.text, text)
				do = raw_input('Do you want to save all changes? (y/n)')
				if do == 'y':
					art.put(text, u'Eliminat enllaços dins el text a d\'altres wikis.')
	

if __name__ == '__main__':
	main()
