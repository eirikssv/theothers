import pandas as pd, numpy as np

def load_seddel():
    data = pd.read_pickle('fangstdata_2021.pkl')
    object_to_date = [  'Dokument salgsdato', 
                        # 'Dokument versjonstidspunkt', 
                        # 'Oppdateringstidspunkt', 
                        'Siste fangstdato',
                        'Landingsdato',
                        ]
    float_to_int = [ 'Landingskommune (kode)', 
                    'Mottaker ID', 
                    'Landingsfylke (kode)', 
                    'Produksjonskommune (kode)', 
                    'Mottakende fartøytype (kode)', 
                    'Fisker ID',
                    'Fiskerkommune (kode)',
                    'Fartøy ID',
                    'Besetning',
                    'Fartøykommune (kode)',
                    'Fartøyfylke (kode)',
                    'Lengdegruppe (kode)',
                    'Bruttotonnasje 1969',
                    'Bruttotonnasje annen',
                    'Byggeår',
                    'Ombyggingsår',
                    'Motorkraft',
                    'Motorbyggeår',
                    'Fangstdagbok (nummer)',
                    'Fangstdagbok (turnummer)',
                    'Anvendelse (kode)',
                    'Anvendelse hovedgruppe (kode)',
                    'Antall stykk'

                    ]
    object_to_float = [ 'Bruttovekt', 
                        'Produktvekt', 
                        'Rundvekt', 
                        'Rundvekt over kvote', 
                        'Produktvekt over kvote',
                        'Lon (hovedområde)',
                        'Lat (hovedområde)',
                        'Lon (lokasjon)',
                        'Lat (lokasjon)',
                        'Største lengde'
                        ]
    for el in object_to_float:
        data[el] = data[el].str.replace(",",".").astype(float)
    for el in object_to_date:
        data[el] = pd.to_datetime(data[el], dayfirst=True)
    for el in float_to_int:
        data[el] = data[el].astype('Int64')


    arter = ['Breiflabb', 'Brosme', 'Kveite', 'Gapeflyndre']

    data = data[data['Fangstgruppe'].isin(arter)]
    return data  
    