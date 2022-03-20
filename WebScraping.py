from unittest import result
import requests, json
from bs4 import BeautifulSoup


def main():
    # Website url
    url = 'https://wltest.dns-systems.net/'

    # get url 
    response = requests.get(url)

    # Website connection test
    if response.status_code != 200:
      print('Status: ', response.status_code, 'Problem with request, exiting')
      exit()
    
    #soup = website content
    soup = BeautifulSoup(response.content,'lxml')

    #results data array
    results = []

    #for item in soup (website content), find all divs which have the class name col-xs-4 col-cs-4
    for item in soup.find_all('div', {'class': ['col-xs-4', 'col-cs-4']}):
      option = item.h3.text.strip() 

      description = item.find('div', class_='package-description').text 
      #u"\xA3" = unicode for £ symbol
      price = item.find('span', class_='price-big').text.replace('\n',' ').strip().replace(u"\xA3", '')

      vat_price = item.find('div', class_='package-price').text.strip()
      vat_id = vat_price.split('(')[1] #remove brackets
      vat_id = vat_id.replace(')',' ').split('\n')[0]

      #Try: look for a discount (p tag) Except: discount = No discount (u"\xA3" = unicode for £ symbol)
      try: 
        discount = item.find('p', style='color: red').text.strip().replace(u"\xA3", '')
      except:
        discount = 'No discount'  
      
      # test = discount.split("on")
      # print(test)
      
      #Append data into dictionary
      results_data = [{
        'option title': option,
        'description': description,
        'price': price +' '+ vat_id,
        'discount': discount
      }]

      ## Not reversing the order according to highest price (future use)
      #test = {k:v for k,v in sorted(results_data.items(), key= lambda v:[1], reverse=False)}
      results.append(results_data)


    #reverse the layout to put the highest annual price first. (Not efficient method, needs to be changed)
    results.reverse()

    #create json array (Remove ascii characters)
    json_data = json.dumps(results,indent=2, ensure_ascii=False)
    return json_data

json_arary = main()
print(json_arary)