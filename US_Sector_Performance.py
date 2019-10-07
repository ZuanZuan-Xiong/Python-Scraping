def get_us_sector_performance():
    output_list = list()
    url = "https://eresearch.fidelity.com/eresearch/goto/markets_sectors/landing.jhtml"
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
    
