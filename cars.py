from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from collections import Counter

# making web requests
def fetch_url(url):
  try:
    with closing(get(url, stream=True)) as response:
      if verify_response(response):
        return response.content
      else:
        return None
  except RequestException as e:
    Log.error('Error during rewuests to {0} : {1}'.format(url, str(e)))
    return None

def verify_response(response):
  '''Checks if response is HTML and return true if so'''
  content_type = response.headers['Content-Type'].lower()
  if response.status_code == 200 and content_type is not None and content_type.find('html') > -1:
    return True
  return False

  def log_error(e):
    print (e)

# Lets now wrangle the HMTL we have extracted
# Beatiful Soup parses the HTML text to an object
def get_names():
  url = 'https://www.olx.co.ke/cars_c378'
  html_response = fetch_url(url)

  if html_response is not None:
    parsedResponse = BeautifulSoup(html_response, 'html.parser')
    cars = []
    value = "_2tW1I" # in this case I want to get car names... you could try to get item price instead
    for span in parsedResponse.find_all('span', attrs={"class": value}):
      for car in span.text.split('\n'):
        if len(car) > 0:
          cars.append(car.split(',')[0])

    # using the Counter method, lets get the count of each type of car.
    # could tell us which are selling more/ on market
    return Counter(cars)

  raise Exception('Error retrieving contents at {}'.format(url))

print(get_names())

# Returns the follwoing result:
'''Counter({'Duet Toyota': 2, 'MAZDA BONGO': 1, 'Honda stream rsz 2009': 1, 'Toyota': 1, 'Landcruiser tours': 1, 'NISSAN SUNNY': 1, '2005 Toyota IST  For Sale': 1, 'Toyota isis': 1, 'Toyota 102 ': 1, 'Toyota corolla dx 102': 1,
         'filder (2007)': 1, '2007 Toyota Fielder For Sale': 1, 'March': 1, 'Axio 1500cc': 1, 'Subaru Impreza': 1, 'Suzuki escudo': 1, 'Toyota Runx': 1, 'Toyota Fielder': 1, 'Toyota Prado': 1, 'Toyota Premio': 1})'''
