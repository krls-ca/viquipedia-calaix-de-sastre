# -*- coding: utf-8 -*-

class Ranking():
	def __init__(self):
		self.globalNumberEditions = 0
		self.globalEditedArticles = 0 
		self.usersEngaged = []
		self.bytesAdded = 0

		self.globalRanking = {}

		self.politicsRanking = {}
		self.economicsRanking = {}
		self.societyRanking = {}
		self.cultureRanking = {}
		self.artsRanking = {}
		self.religionRanking = {}

		self.mediterraniSudOcc = {}
		self.mediterraniCen = {}
		self.mediterraniSudOr = {}
		self.llevant = {}
		self.anatolia = {}
		self.mediterraniNordOr = {}
		self.balcans = {}
		self.italica = {}
		self.mediterraniNordOcc = {}
		self.alboran = {}
		self.illesOest = {}
		self.illesEst = {}

		self.era = {u'gener': self.mediterraniSudOcc, u'febrer': self.mediterraniCen, u'març': self.mediterraniSudOr, u'abril': self.llevant, u'maig': self.anatolia, u'juny': self.mediterraniNordOr, u'juliol': self.balcans, u'agost': self.italica, u'setembre': self.mediterraniNordOcc, u'octubre': self.alboran, u'novembre': self.illesOest, u'desembre': self.illesEst}
		self.category = {u'P': self.politicsRanking, u'E': self.economicsRanking, u'S': self.societyRanking, u'C': self.cultureRanking, u'A': self.artsRanking, u'R': self.religionRanking} 

class Article():

	def __init__(self, name, category, value, month):
		self.name = name
		self.category = category
		self.value = value
		self.month = month

import pywikibot
import sys
import re
from datetime import datetime, date
import codecs

ranking = Ranking()

def setArticles(page):
	listArticles = {}
	articles = page.split('\n')
	for art in articles:
		atributes = art.split('|')
		name = atributes[0].strip()
		article = Article(name, atributes[1].strip(), atributes[2].strip(), atributes[3].strip())
		listArticles[name] = article
	return listArticles

def readArticles():
	site = pywikibot.Site("ca", "wikipedia")
	page = pywikibot.Page(site, u"Viquiprojecte:PESCAR/seguiment 2018/articles")
	text = page.get()
	listArticles = setArticles(text)
	return listArticles

def convertToPuntation(puntuation, article):
	convertedList = {}
	for punt in puntuation:
		points = puntuation[punt] / 1000
		if points > 0:
			convertedList[punt] = int(points) * int(article.value)
	return convertedList

def getScore(listArticles):
	site = pywikibot.Site("ca", "wikipedia")
	globalPuntuation = {}
	for art in listArticles:
		article = listArticles[art]
		print article.name
		page = pywikibot.Page(site, article.name)
		try:
			if page.isRedirectPage():
				page = page.getRedirectTarget()
			text = page.get()
			specificPuntuation = {}
			found = False
			for rev in page.revisions():
				#print dir(rev)
				date = rev.timestamp
				if date >= datetime(2018,1, 1, 0, 0, 0) and date < datetime(2019, 1, 1, 0, 0, 0):
					found = True
					ranking.globalNumberEditions += 1 #countEditions
					previousRevLength = 0 if rev.parent_id == 0 else len(page.getOldVersion(rev.parent_id))
					currentRevLength = len(page.getOldVersion(rev.revid))
					diffFromPrecedingVersion = currentRevLength-previousRevLength
					ranking.bytesAdded += diffFromPrecedingVersion #countBytesAdded
					if rev.user in specificPuntuation:
						specificPuntuation[rev.user] = specificPuntuation[rev.user] + diffFromPrecedingVersion
					else:
						if rev.user not in ranking.usersEngaged:
							ranking.usersEngaged.append(rev.user) #countUsersEngaged
						specificPuntuation[rev.user] = diffFromPrecedingVersion
			if found:
				ranking.globalEditedArticles += 1 #countEditedArticles
			convertedList = convertToPuntation(specificPuntuation, article)
			globalPuntuation[article.name] = convertedList
		except pywikibot.exceptions.NoPage as nopage:
			print "EXCEPTION " + article.name

	return globalPuntuation

def assignPuntuation(score, listArticles):
	for articlePunt in score:
		sortedPunt = sorted(score[articlePunt].iteritems(), key=lambda x: x[1], reverse=True)

		for elem in sortedPunt:
			#Global Puntuation assignation
			if elem[0] not in ranking.globalRanking:
				ranking.globalRanking[elem[0]] = elem[1]
			else:
				ranking.globalRanking[elem[0]] += elem[1]
			
			#Era assignation
			month = listArticles[articlePunt].month
			monthEra = ranking.era[month]

			if elem[0] in monthEra:
				monthEra[elem[0]] += elem[1]
			else:
				monthEra[elem[0]] = elem[1]

			#Category assignation:

			category = listArticles[articlePunt].category
			categoryList = ranking.category[category]

			if elem[0] in categoryList:
				categoryList[elem[0]] += elem[1]
			else:
				categoryList[elem[0]] = elem[1]

def showSpecificRanking(rank):
	text = u''
	sortedRank = sorted(rank.iteritems(), key=lambda x: x[1], reverse=True)
	for i in range(0, min(5, len(sortedRank))):
		elem = sortedRank[i]
		user = elem[0]
		punt = elem[1]
		if i > 10:
			#Els 3 primers només en negreta
			text += u"# '''{{{{u|{0}}}}}''' {1} punts\n".format(user, int(punt)) 
		else:
			text += u"# {{{{u|{0}}}}} {1} punts\n".format(user, int(punt))
	if len(sortedRank) > 5:
		text += u'\n\n{{collapse top|Llista completa|bg=#fff}}\n{|class="wikitable sortable"\n! Nombre !! Viquipèdia !! Punts\n'
		for i in range(0, len(sortedRank)):
			elem = sortedRank[i]
			user = elem[0]
			punt = elem[1]
			text += u'|-\n| {0} || {{{{u|{1}}}}} || {2}\n'.format(i+1, user, int(punt))

		text += u'|}\n{{collapse bottom}}\n'
	return text

def showPuntuation():
	site = pywikibot.Site("ca", "wikipedia")
	page = pywikibot.Page(site, "Viquiprojecte:PESCAR/seguiment 2018")
	text = u"<center>[[File:P-AvenidaBoyacáCentro.png|50px]][[File:E-NQS Central.png|50px]][[File:S_Societat.svg|50px]][[File:TransMilenio Estacion C Suba.svg|50px]][[File:A-Caracas.svg|50px]][[File:R_Religió.svg|50px]]</center>\nEstadístiques de seguiment del [[Viquiprojecte:PESCAR]]. Les dades són relacionades amb les edicions documentades amb l\'etiqueta [https://tools.wmflabs.org/hashtags/search/PESCAR #PESCAR] en el resum d'edició durant el 2017 en algun dels articles llistats a la pàgina de projecte.\n\n:\'\'Darrera actualització: {0}\'\'".format(datetime.utcnow())
	
	#showGlobalStatistic

	text += u"\n== Resum Global PESCAR ==\n# '''{0}''' edicions\n# '''{1}''' articles editats\n# '''{2}''' participants\n# '''{3}''' bytes modificats\n".format(int(ranking.globalNumberEditions), int(ranking.globalEditedArticles), int(len(ranking.usersEngaged)), int(ranking.bytesAdded))
	

	#showGlobalRanking
	text += u"== Rànquing Global PESCAR ==\nRànquing de viquipedistes per nombre de punts:\n"
	text += showSpecificRanking(ranking.globalRanking)

	#ShowEixos
	text += u"== Rànquing per eixos ==\n"
	#showPolitics
	text += u"=== [[File:P-AvenidaBoyacáCentro.png|50px]] ([[política]]) ===\n"
	text += showSpecificRanking(ranking.category[u'P'])
	#showEconomics
	text += u"=== [[File:E-NQS Central.png|50px]] ([[economia]]) ===\n"
	text += showSpecificRanking(ranking.category[u'E'])
	#showSociety
	text += u"=== [[File:S_Societat.svg|50px]] ([[societat]]) ===\n"
	text += showSpecificRanking(ranking.category[u'S'])
	#showCulture
	text += u"=== [[File:TransMilenio Estacion C Suba.svg|50px]] ([[cultura]]) ===\n"
	text += showSpecificRanking(ranking.category[u'C'])
	#showArts
	text += u"=== [[File:A-Caracas.svg|50px]] ([[arts]]) ===\n"
	text += showSpecificRanking(ranking.category[u'A'])
	#showReligion
	text += u"=== [[File:R_Religió.svg|50px]] ([[religió]]) ===\n"
	text += showSpecificRanking(ranking.category[u'R'])

	#ShowEras
	text += u"== Rànquing per Zones ==\n"

	text += u"=== [[File:Babuchas 01 -- 2014 -- Marrakech, Marruecos.jpg|50px]] ===\n"
	text += showSpecificRanking(ranking.era[u'gener'])

	text += u"=== [[File:Kobet el hawa - Belveder.JPG|50px]] Mediterrani central ===\n"
	text += showSpecificRanking(ranking.era[u'febrer'])

	text += u"=== [[File:Pyramid 1.jpg|50px]] Mediterrani sud-oriental ===\n"
	text += showSpecificRanking(ranking.era[u'març'])
	
	text += u"=== [[File:מוסלמית בדרכה לכיפת הסלע.jpg|50px]] Llevant ===\n"
	text += showSpecificRanking(ranking.era[u'abril'])
	
	text += u"=== [[File:Little AraratDSC 3125.jpg|50px]] Anatòlia ===\n"
	text += showSpecificRanking(ranking.era[u'maig'])
	
	text += u"=== [[File:Temple of Poseidon at Cape Sounion (DSC 3781).jpg|50px]] Mediterrani nord-oriental ===\n"
	text += showSpecificRanking(ranking.era[u'juny'])
	
	text += u"=== [[File:Muzeu Etnografik Gjakovë - Ballkoni.jpg|50px]] Balcans i mar Adriàtica ===\n"
	text += showSpecificRanking(ranking.era[u'juliol'])
	
	text += u'=== [[File:" Arco della Vittoria ".jpg|50px]] Península Itàlica ===\n'
	text += showSpecificRanking(ranking.era[u'agost'])
	
	text += u"=== [[File:Notre Dame de la Garde.jpg|50px]] Mediterrani nord-occidental ===\n"
	text += showSpecificRanking(ranking.era[u'setembre'])
	
	text += u"=== [[File:La banyera de la russa-calella de palafurgell-8-2013.JPG|50px]] Mar d'Alborán ===\n"
	text += showSpecificRanking(ranking.era[u'octubre'])
	
	text += u"=== [[File:Mallorca.jpg|50px]] Illes de l'oest ===\n"
	text += showSpecificRanking(ranking.era[u'novembre'])
	
	text += u"=== [[File:Cyprus lrg.jpg|50px]] Illes de l'est ===\n"
	text += showSpecificRanking(ranking.era[u'desembre'])
	print text
	page.put(text, comment=u'Actualitzant puntuació #PESCAR', minorEdit = True)
	
def main():
	listArticles = readArticles()
	#listArticles = {u'Civilitzaci\xf3 cicl\xe0dica': listArticles[u'Civilitzaci\xf3 cicl\xe0dica']}
	score = getScore(listArticles)
	assignPuntuation(score, listArticles)
	showPuntuation()

if __name__ == '__main__':
	main()
