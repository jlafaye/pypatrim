import textract
import logging
import pandas as pd
import re

TRANSACT_REGEXP = re.compile('([\w\d]+)\s+'# + 1:CAD
                    '((?:\d{3}\/\/[A-Z]{2}\/\d+\/\/[0-9]*)\s+)+' # 2:REF
                    "(\d+)\s+([\w ']+)\s+"# 4: DEPT + COMMUNE 
                    '(\d+[ \w\']+)\s+' # ADRESSE
                    '(\d{2}\/\d{2}\/\d{4})\s+' # 5:DATE
                    '(\d{4})\s+' # 6 ANNEE
                    '(\d+)\s+' # 7 PIECEs
                    '((?:\d )?\d{3} \d{3})\s+' # 8: PRIX
                    '(\d+)\s+' # 9: TERRAIN
                    '(\d+)\s+' # 10: SURFACE
                    '([\d\,]+)'
                   )

def read_pdf(filename):
    text = textract.process(filename)
    return read_text(text.decode('utf-8'))

def read_text(text):

    rows = []
    
    for line in text.split('9504P03'):
 
        m = TRANSACT_REGEXP.search(line.replace('\n', ' '))

        if m:
            row = [m.group(i) for i in range(1, 13)]
            rows.append(row)
        else:
            logging.warning('unparsable line: \"%s\"' % line.replace('\n', ' '))

    df = pd.DataFrame(rows, columns=['CAD', 'REF', 'DEPT',
                                     'COMMUNE', 'ADRESSE',
                                     'DATE', 'ANNEE', 'PIECES',
                                     'PRIX', 'TERRAIN', 'SURFACE',
                                     'PRIX_M2'])

    for column in ['DEPT', 'PIECES', 'PRIX', 'TERRAIN', 'SURFACE']:
        df[column] = df[column].str.replace(' ', '').astype(int)
    for column in ['PRIX_M2']:
        df[column] = df[column].str.replace(',', '.').astype(float)
    for column in ['ADRESSE', 'COMMUNE']:
        df[column] = df[column].str.strip()
    return df
