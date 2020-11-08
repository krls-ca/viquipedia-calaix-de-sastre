# Calaix de Sastre - Viquipèdia

> :warning: **AVERTÈNCIA:** Aquests són alguns dels codis no formals que he anat creant des que vaig començar a fer petits codis de manteniment per a la Viquipèdia el 2006. Una part d'ells no s'han mantingut des de la seva creació i poden no ser ja compatibles amb la versió actual del pywikibot. S'adjunten en aquest repositori per raons històriques i per si poden servir d'inspiració a d'altres en un futur.

Els codis tenen com a dependencia la llibreria pywikibot: https://www.mediawiki.org/wiki/Manual:Pywikibot/ca.

## Semibot - Treure enllaços interwikis (2018)
Va ser un semibot per automatitzar el procés de manteniment d'eliminar enllaços interwiki dins el codi de l'article: ja fos eliminant l'enllaç directament, enllaçant amb l'article correcte en català o deixant-lo com un enllaç en blanc. Va ser un codi vinculat a la Gran Quinzena Anual de la Qualitat 2018.

https://ca.wikipedia.org/wiki/Viquip%C3%A8dia:Gran_Quinzena_Anual_de_la_Qualitat/2018

```sh
$ python treuCatInterwikisDinsCos.py
```


## Concurs PESCAR (2016, mant. 2018)

Recompte de punts per al concurs PESCAR per a les edicions 2017 i 2018. Era un concurs en línia que tenia la intenció de millorar el coneixement sobre la història de la humanitat a la Viquipèdia. https://ca.wikipedia.org/wiki/Viquiprojecte:PESCAR

```sh
$ python PESCAR.py
```

## Desorfenar articles (gen-2011, mant. des-2017)
Programa que s'encarrega de revisar la categoria dels articles orfes i eliminar la plantilla en cas que l'article rebi com a mínim un enllaç intern d'un altre article.

L'enllaç que rebi no pot ser de cap article d'anys (per exemple: 1991 o 123) o dies (2 d'agost), l'enllaç tampoc pot provenir d'una pàgina de desambiguació.

En alguns articles ens trobem que l'enllaç que hi ha forma part d'una plantilla que enllaça cap a l'altre article, però, no hi manté cap tipus de relació (per exemple: la plantilla polisèmia) en aquests casos es comprovarà si hi ha més d'un enllaç cap a l'article.

```sh
$ python desorfena.py
```

### Coses a fer
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

### Historial
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

### Ús
Des de la consola, terminal, cmd... executar:

```sh
$ python desorfena.py
```
