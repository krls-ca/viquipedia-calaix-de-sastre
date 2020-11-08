#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
== Descripció ==
Programa que s'encarrega de revisar la categoria dels articles orfes i eliminar
la plantilla en cas que l'article rebi com a mínim un enllaç intern d'un altre
article.

L'enllaç que rebi no pot ser de cap article d'anys (per exemple: 1991 o 123) o
dies (2 d'agost), l'enllaç tampoc pot provenir d'una pàgina de desambiguació.

En alguns articles ens trobem que l'enllaç que hi ha forma part d'una plantilla
que enllaça cap a l'altre article, però, no hi manté cap tipus de relació (per
exemple: la plantilla polisèmia) en aquests casos es comprovarà si hi ha més
d'un enllaç cap a l'article.

== Coses a fer ==
- Permetre la inclusió de parametres inicials que ens permetin modificar els
camps següents:
    - verbose: activa el mode 'verbose', per defecte està desactivat
    - edit: activa el mode 'edit', els canvis es desaran a la Viquipèdia,
    - minlink: nombre mínim d'enllaços per a eliminar la plantilla d'orfe,
               per defecte és 1
    - page : només s'actuarà sobre una pàgina
    - start : comença a partir d'un article fins al final

- Revisar que no faltin plantilles conflictives a les variables: templates_re i
  other_tpl_re

== Historial ==
Gener/2011 - Joancreus, primera versió del programa
Juliol/2011 - Coet, optimitzades les expressions regulars utilitzades
Juliol/2011 - Joancreus, arreglats diversos errors en les expressions regulars
Febrer/2013 - Castor, segona versió, afegit el suport a noves plantilles,
              arreglada la detecció dels anys, afegida la detecció de mesos,
              d'enllaços interns a través de plantilles, documentació del codi.
Agost/2014 - Coet: anglicise variables (en tenim en català i en anglés, i sempre
             que estiguen en anglés facilita que altres ho entenguen i afegisc
             la possibilitat de "paràmetres inicials", a més de modificar el
             codi i reestructurar-lo per a complir amb els estàndards i
             convencions pythòniques.
Desembre/2017 - KRLS, refactoritzo codi utilitzant noves llibreries perquè pugui 
				tornar a funcionar el codi

== Ús ==
Des de la consola, terminal, cmd... executar:

python desorfena.py

"""
import re, sys
import pywikibot

def main():
    arts = pywikibot.Category(site, u"Articles orfes").articlesList(recurse=3) if \
        not args.page else (pywikibot.page(site, args.page),)
    
    

    #Varibles amb expressions regulars:
    #templates_re: conté totes les plantilles de desambiguacio
    templates_re = re.compile(ur"\{\{(?:[Dd]esambigua|[Dd]isambig|[Dd]esambigCurta|[Aa]crònim|[Oo]nomàstica|[Bb]iografies|[Bb]iografia)\}?\}?")
    
    #other_tpl_re: conté plantilles que enllaçen cap a l'article orfe
    other_tpl_re = re.compile(ur"\{\{([Vv]egeu|[Vv]egeu3|[pP]olisèmia|[Ff]usió des de|[Ff]usió de|[Cc]onfusió)")
    
    #year_re: expressió per detectar anys. No s'hauria de modificar
    #months_re: conté totes les categories dels mesos. No s'hauria de modificar
    year_re = re.compile(r"\d+")
    months_re=re.compile(ur"\[\[Categoria:([Gg]ener|[Ff]ebrer|[Mm]arç|[Aa]bril|[Mm]aig|[Jj]uny|[Jj]uliol|[Aa]gost|[Ss]etembre|[Oo]ctubre|[Nn]ovembre|[Dd]esembre)")
    
    start = args.start
         
    for art in arts:
        if start and art.title != start: continue
        elif start and art.title == start: start = False
        if args.debug: pywikibot.output(u">>> %s <<<" % art.title())
        #Aquesta query, retorna tots els enllaços de l'article a l'espai principal.
        it = art.backlinks(namespaces=0, filterRedirects=False, content=False)
        links_to_page = list(it)
        if args.debug: pywikibot.output(u"Hi ha %d enllaços, a l'espai principal" % len(links_to_page))
        if len(links_to_page)>2:
            years = 0 #Num articles d'anys
            desambigs = 0 #Num. articles desambiguacions o que tenen plantilles amb enllaços
            months = 0 #Num d'articles que tenen com a categoria algun mes
            links = re.compile(u"\[\[%s" % art.title()) #Expressio per trobar enllaços interns cap a l'article orfe
            
            #Recorrem tots els articles que tenen enllaços cap a l'article orfe
            for p in links_to_page:
                #print p.title()
                #page = pywikibot.page(site, p.title())
                text = p.get()
                if args.debug: pywikibot.output("\tRevisant article: %s" % p.title())
                if re.match(year_re, p.title()):
                    years+=1
                elif re.search(templates_re,text):
                    desambigs+=1
                elif re.search(months_re,text):
                    months+=1
                elif re.search(other_tpl_re,text):
                    if len(re.findall(links,text))<2:
                                            #Comptabilitzem la pagina com si fos de desambiguacio
                        desambigs+=1
    
                    #El total de pagines d'anys, mesos i desambiguacions son inferiors al nombre de pagines que enllacen cap a l'article orfe, tenim algun enllaç valid
            if ((years+desambigs+months) < len(links_to_page)): 
                text = art.get()	#Agafem el text de la pagina que revisem i eliminem la plantilla d'orfe
                new_text = re.sub(r"\{\{[Oo]rfe(.*?)\}\}\n","", text)
                if args.debug: pywikibot.showDiff(text,new_text)
                #Diferenciem el cas d'un enllaç de multiples, queda mes maco
                if len(links_to_page) > 1:
                    if args.edit: art.put(new_text, u"""#QQ17: Es treu la plantilla "Orfe" ja que l'article rep %d enllaços, dels quals %d són desambiguacions o anys""" % (len(links_to_page),(desambigs+years)))
                else:
                    if args.edit: art.put(new_text, u"""QQ17: Es treu la plantilla "Orfe" ja que l'article rep %d enllaç, que no és ni desambiguació ni any.""" % len(links_to_page))
                if args.debug: pywikibot.output("QQ17: Es treu la plantilla Orfe")
            else:
                if not args.debug: pywikibot.output("No fem res")

if __name__ == '__main__':
	args = lambda: x
	args.edit = args.verbose = False
	args.start = args.page = None
	args.num = 1
	for arg in pywikibot.handleArgs():
		if ":" in arg:
			arg, value = arg.split(":", 1)
		if arg in ("-d", "--debug"):
			args.debug = True
			print u"Mode \3{lightpurple}verbose\3{default} activat."
		elif arg in ("-e", "--edit"):
			args.edit = True
			print u"Mode \3{lightpurple}verbose\3{default} activat, s'editarà!."
		elif arg in ("-n", "--num"):
			args.num = int(value) if value.isdigit() else 1
			print u"Nombre d'enllaços canviat a \3{lightpurple}%i\3{default}." % args.num
		elif arg in ("-p", "--page"):
			args.page = value.strip()
			print u"Es revisarà \3{lightpurple}%s\3{default}." % args.page
		elif arg in ("-s", "--start"):
			args.start = value.strip()
			print u"Es començara per l'article \3{lightpurple}%s\3{default}." % args.start
	site = pywikibot.getSite()
	main()
	pywikibot.stopme()

