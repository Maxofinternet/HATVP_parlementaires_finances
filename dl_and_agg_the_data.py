import pandas as pd
import requests
import json
import pandas_read_xml as pdx
companies = list()
shares = list()
valuation = list()
id = list()

def fetchxmlandread(tdf):
    mostrecent = []
    tdfs = tdf.sort_values(by=['date_depot'], ascending=False)
    for complementurl in tdfs['open_data'] :
        try:
            URL = "https://www.hatvp.fr/livraison/dossiers/" + complementurl
            response = requests.get(URL).text
            df = pdx.read_xml(response, encoding='utf-8')
            depjson = json.loads(df.to_json())
            mostrecent = depjson['declaration']['0']['participationFinanciereDto']['items']
            break
        except:
            continue
    return mostrecent




URL = "http://www.hatvp.fr/files/open-data/liste.csv"
completeliste = pd.read_csv(URL, sep=';')
completeliste.head()
completeliste = completeliste.dropna(axis=0, subset=['date_publication', 'open_data'])
completeliste = completeliste[(completeliste['type_mandat'] == 'depute') | (completeliste['type_mandat'] == 'senateur')]
completeliste['date_depot'] = pd.to_datetime(completeliste['date_depot'])
for i in set(completeliste['classement']) :
    tempdf = completeliste[completeliste['classement'] == i]
    declarationrecente = fetchxmlandread(tempdf)
    if declarationrecente is not None and len(declarationrecente) >=1 :
        if type(declarationrecente['items']) is list :
            itvar = declarationrecente['items']
        else :
            itvar = [declarationrecente['items']]
        for z in itvar:
            if '[DonnÃ©es non publiÃ©es]' not in z['nomSociete'] :
                formattedname = z['nomSociete'].replace('Ã©', 'e')
                formattedname = formattedname.replace('ã¨', 'e')
                formattedname = formattedname.lower()
                print(formattedname, z['nombreParts'], z['evaluation'])
                companies.append(formattedname)
                shares.append(z['nombreParts'])
                valuation.append(z['evaluation'])
                id.append(i)

dictf = {'entreprises' : companies, 'parts' : shares, 'valeur': valuation, 'id' :id}
dffinal = pd.DataFrame(dictf)
dffinal.to_excel("output.xlsx")
print('done')
