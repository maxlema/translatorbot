import requests
from bs4 import BeautifulSoup
from googletrans import Translator

user='testbot'
passw='dhbot2017'
baseurl='http://wikipast.epfl.ch/wikipast/'
summary='Wikipastbot update'
names=['Henri Dunant']
translator = Translator()

# Login request
payload={'action':'query','format':'json','utf8':'','meta':'tokens','type':'login'}
r1=requests.post(baseurl + 'api.php', data=payload)

#login confirm
login_token=r1.json()['query']['tokens']['logintoken']
payload={'action':'login','format':'json','utf8':'','lgname':user,'lgpassword':passw,'lgtoken':login_token}
r2=requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

#get edit token2
params3='?format=json&action=query&meta=tokens&continue='
r3=requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
edit_token=r3.json()['query']['tokens']['csrftoken']

edit_cookie=r2.cookies.copy()
edit_cookie.update(r3.cookies)

#we fetch the text we want to translate
for name in names:
    result=requests.post(baseurl+'api.php?action=query&titles='+name+'&export&exportnowrap')
    soup=BeautifulSoup(result.text, "lxml")
    code=''
    for primitive in soup.findAll("text"):
        code += primitive.string

    translated_text = translator.translate(code[:5000], src='fr', dest='en').text
    
    #Create names with english prefix
    en_name = 'en/' + translator.translate(name, src='fr', dest='en').text

    #Ecrire le texte traduit sur la page /en/nom traduit
    #payload={'action':'edit','assert':'user','format':'json','utf8':'','appendtext':translated_text,'summary':summary,'title':en_name,'token':edit_token}



    
#cette methode sert à traduire le texte qu'on veut traduire, 5000 chars d'un coup au max
#print(translator.translate(code[:5000], src='fr', dest='en').text)

# pour rajouter le contenu après, attention de pas poster n'importe quoi sur le site

#si on veut overwrite ce qu'y a sur la page
#payload={'action':'edit','assert':'user','format':'json','utf8':'','text':content,'summary':summary,'title':en_name,'token':edit_token}

#OU

#si on veut juste rajouter le texte à la fin de celui qui est déjà sur la page
#payload={'action':'edit','assert':'user','format':'json','utf8':'','appendtext':content,'summary':summary,'title':name,'token':edit_token}

#r4=requests.post(baseurl+'api.php',data=payload,cookies=edit_cookie)
#print(r4.text)
