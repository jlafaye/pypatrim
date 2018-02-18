import requests
import numpy as np
import logging
import json

GMAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
GMAPS_API_KEY = 'AIzaSyCwuAC6FdsFyVqeFDvkusYvlpPBhs0OGMo'

def get_location(address):
    gapi_url = GMAPS_API_URL
    params = {
        'address': address,
        'key': GMAPS_API_KEY
    }

    r = requests.get(gapi_url, params=params)
    obj = json.loads(r.text)
    try:
        location = obj['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    except:
        import traceback
        logging.warn('Unable to retrieve location for idx[{}]:\n{}'\
                        .format(idx, traceback.format_exc()))
        return None

def fill_locations(df):
    for idx, row in df.iterrows():        
        if not np.isnan(df.loc[idx, 'LATITUDE']) and \
            not np.isnan(df.loc[idx, 'LONGITUDE']):
            continue
        
        logging.debug('Fetching location for index[{}]'.format(idx))        

        query = row['ADRESSE'] + ' ' + row['COMMUNE']
        # @HACK@ dirtiest trick ever
        query = query.replace('LUCIEN PERQUEL', 'PERQUEL')
        
        location = get_location(query)
        
        if location is not None:
            latitude, longitude = location
            df.loc[idx, 'LATITUDE'] = latitude
            df.loc[idx, 'LONGITUDE'] = longitude
