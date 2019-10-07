#!/usr/bin/env python
# coding: utf-8

# <h1>Scraping Fidelity.com</h1>
# In this assignment, you will scrape data from fidelity.com. The goal of the exercise is to get the latest sector performance data from the US markets, and to get the total market capitalization for each sector. 
# 
# The end result is to write a function: <i>get_us_sector_performance()</i> that will return a list of tuples. Each tuple should correspond to a sector and should contain the following data:
# <li>the sector name
# <li>the amount the sector has moved
# <li>the market capitalization of the sector
# <li>the market weight of the sector
# <li>a link to the fidelity page for that sector
# 
# <p>
# The data should be sorted by decreasing order of market weight. I.e., the sector with the highest weight should be in the first tuple, etc.

# <h3>Process</h3>
# <li>Get a list of sectors and the links to the sector detail pages from the url (see function)
# <li>Loop through the list and call the function <i>get_sector_change_and_market_cap(sector_page_link)</i> for each sector
# <li>Accumulate the name, the change, the capitalization, the weight and the link for each sector in output_list (see function)
# <li>Sort the list by market weight

# <b>Notes:</b>
# <li>Note that the market weight is a string with a % sign at the back. You will need to get rid of the % and convert the string into a float before you can sort it
# <li>Your starting data is the url listed below. You need to extract all data, including links to the sector pages, from the page at this url
# <li>To sort a list of tuples by an arbitrary element, use the example at the bottom of this notebook

# In[4]:


def get_us_sector_performance():
    output_list = list()
    url = "https://eresearch.fidelity.com/eresearch/goto/markets_sectors/landing.jhtml"

    
    #**** Your code goes here ****
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    results_page = BeautifulSoup(response.content, 'lxml')
    output_list = []
    for result in results_page.find_all('div', class_ = 'heading')[1:]:
        sector_link = "https://eresearch.fidelity.com" + result.find('a').get('href')
        response_sector = requests.get(sector_link)
        sector_page  = BeautifulSoup(response_sector.content, 'lxml')
        sector_name = sector_page.find('h1').get_text()
        sector_move = float(sector_page.find('table', class_ = 'snapshot-data-tbl').find_all('span')[1].get_text().strip('+').strip('%'))
        sector_cap = sector_page.find('table', class_ = 'snapshot-data-tbl').find_all('span')[3].get_text()
        sector_weight = float(sector_page.find('table', class_ = 'snapshot-data-tbl').find_all('span')[5].get_text().strip('%'))
        output_list.append((sector_name, sector_move, sector_cap, sector_weight, sector_link))
    
    output_list.sort(key=lambda k: k[3], reverse = True)
    
    return output_list
    


# In[5]:


def get_sector_change_and_market_cap(sector_page_link):
    
#    **** Your code goes here ****
    import requests
    from bs4 import BeautifulSoup
    response_sector = requests.get(sector_page_link)
    sector_page  = BeautifulSoup(response_sector.content, 'lxml')
    sector_change = float(sector_page.find('table', class_ = 'snapshot-data-tbl').find_all('span')[1].get_text().strip('+').strip('%'))
    sector_market_cap = sector_page.find('table', class_ = 'snapshot-data-tbl').find_all('span')[3].get_text()
    sector_market_weight = float(sector_page.find('table', class_ = 'snapshot-data-tbl').find_all('span')[5].get_text().strip('%'))
    return sector_change,sector_market_cap,sector_market_weight


# In[6]:


#Test get_sector_change_and_market_cap()
link = "https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=25"
get_sector_change_and_market_cap(link)
#Should return (-0.40, $3.58T, 6.80)
#Note that neither the -0.40, nor the 6.80, end with a %sign


# In[7]:


get_us_sector_performance()


# In[5]:


#Test get_us_sector_performance()
get_us_sector_performance()
#Should return (example: obviously the results will vary over time!)
"""
[('Telecommunication Services',
  0.21,
  '$1.74T',
  2.0,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=50'),
 ('Materials',
  0.22,
  '$1.95T',
  2.49,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=15'),
 ('Real Estate',
  -0.45,
  '$1.22T',
  2.7,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=60'),
 ('Utilities',
  -0.33,
  '$1.25T',
  2.86,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=55'),
 ('Energy',
  0.76,
  '$3.90T',
  5.83,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=10'),
 ('Consumer Staples',
  -0.32,
  '$3.58T',
  6.8,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=30'),
 ('Industrials',
  0.72,
  '$4.31T',
  9.83,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=20'),
 ('Consumer Discretionary',
  1.03,
  '$5.76T',
  12.9,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=25'),
 ('Financials',
  0.39,
  '$7.45T',
  13.71,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=40'),
 ('Health Care',
  0.76,
  '$5.70T',
  14.71,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=35'),
 ('Information Technology',
  0.81,
  '$9.84T',
  26.17,
  'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml?tab=learn&sector=45')]
  
"""


# <h3>Sorting</h3>

# In[ ]:


x = [('a',23.2,'b'),('c',17.4,'f'),('d',29.2,'z'),('e',1.74,'bb')]
x.sort() #Sorts by the first element of the tuple
x


# In[ ]:


x = [('a',23.2,'b'),('c',17.4,'f'),('d',29.2,'z'),('e',1.74,'bb')]
x.sort(key=lambda k: k[1], reverse = True) #Sorts by the element at position 1
x


# In[ ]:




