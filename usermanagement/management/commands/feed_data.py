from requests.auth import HTTPBasicAuth
import requests
from urllib3.util.retry import Retry
from django.core.management.base import BaseCommand
from usermanagement.models import *
from requests.adapters import HTTPAdapter
import os

class Command(BaseCommand):
    help = 'Import Movies from 3rd party api.'
    def handle(self, *args, **options):
        API_KEY = os.environ.get("API_KEY", "token")
        base_url='https://demo.credy.in/api/v1/maya/movies/'
        print(base_url)
        # process args if provided, otherwise set default values
        auth = HTTPBasicAuth('iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0',
                             'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1')
        payload = {
            'token': API_KEY,
        }
        headers = {'Content-type': 'application/json; charset=utf-8'}
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        def get_results():
            first_page = session.get(base_url,params=payload,headers=headers,auth=auth).json()
            yield first_page

            for page in range(1, 4547):
                new_payload = payload
                new_payload['page'] = page
                print(page,'pa')
                next_page = session.get(base_url, params=new_payload,headers=headers,auth=auth).json()
                # c += 1
                yield next_page

        # issue pagination api requests accumulating results into result_set
        def data():
            result_set = []
            for page in get_results():
                data = page.get('results', [])
                result_set.append(data)
            return result_set

        #bulk save
        for results in data():
            for movie in results:
                post = Movies(
                        title=movie["title"],
                        description=movie["description"],
                        genres=movie["genres"],
                        uuid=movie["uuid"]
                    )
                post.save()
