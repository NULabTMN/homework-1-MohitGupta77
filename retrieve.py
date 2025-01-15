import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET 
import urllib.parse
import urllib.request

# Step 1: Fetch the webpage content
urls = ['https://guides.loc.gov/chronicling-america-16th-amendment/selected-articles', 'https://guides.loc.gov/chronicling-america-april-fools/selected-articles', 'https://guides.loc.gov/chronicling-america-cocaine/selected-articles']

query_url = "https://chroniclingamerica.loc.gov/search/pages/results/"
search_terms = ['income tax', 'april first', 'narcotic']

params = []
params.append({'andtext': search_terms[0],
            'page': 1,
            'rows': 5,
            'date1': '1909',
            'date2': '1915',
            'dateFilterType': 'yearRange',
            'searchType': 'basic',})
params.append({
            'andtext': search_terms[1],
            'page': 1,
            'rows': 5,
            'searchType': 'basic',})
params.append({
            'andtext': search_terms[2],
            'page': 1,
            'rows': 5,
            'date1': '1898',
            'date2': '1915',
            'dateFilterType': 'yearRange',
            'searchType': 'basic',})

def create_xml(filename, count=0):
    topics = ET.Element('topics')

    for url in urls:
        topic = ET.SubElement(topics, 'topic')
        id = ET.SubElement(topic, 'id')
        id.text = url

        response = requests.get(url)

    # Step 2: Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        header = soup.find('h2', text='Selected Articles from Chronicling America')

        if header:
            parent_element = header.parent
            links = parent_element.find_all('a', href=True)
            # find only the first 10 links (or all if less than 10)
            if len(links) > 10:
                links = links[:10]

        results = ET.SubElement(topic, 'results')
        for rel in links:
            result = ET.SubElement(results, 'result')
            id_rel = ET.SubElement(result, 'id')
            
            new_url = str(rel['href']) + '&st=text'
            id_rel.text = new_url
            relevance = ET.SubElement(result, 'rel')
            relevance.text = '1'
            
            response = requests.get(new_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            match = re.search(r"viewerComponents\['text'\]\.html = '(.*?)</div>", response.text, re.DOTALL)

            if match:
            # Extract the HTML string from the first capture group
                html_content = match.group(1)
            
            # Clean up the HTML string:
            # - Replace \n with actual newlines
            # - Replace \" with actual quotes
                html_content = html_content.replace('\\', '').replace('n            ', '')
            
            # Create a new BeautifulSoup object from this HTML string
                inner_soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find the specific div containing the text
                fulltext_div = inner_soup.find('div', id='fulltext-box')
            
            if fulltext_div:
                content = fulltext_div.text
                text = ET.SubElement(result, 'text')
                text.text = content

        response = requests.get(query_url, params=params[count])
        soup = BeautifulSoup(response.content, 'html.parser')
        header = soup.find('table', {'class':'search_results'})
        query_links = header.find_all('input', {'name':'id'})

        for link in query_links:
            new_link_id = 'https://chroniclingamerica.loc.gov/' + str(link['value'])
            new_link = 'https://chroniclingamerica.loc.gov/' + str(link['value']) + 'ocr.txt'
            result = ET.SubElement(results, 'result')
            id_rel = ET.SubElement(result, 'id')
            id_rel.text = new_link_id
            relevance = ET.SubElement(result, 'rel')

            response = requests.get(new_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            if (count == 0 and 'amendment' in soup.text.lower()) or (count == 1 and 'april fool' in soup.text.lower()) or (count == 2 and 'cocaine' in soup.text.lower()):
                text = ET.SubElement(result, 'text')
                text.text = soup.text
                relevance.text = '1'
            else:
                relevance.text = '0'
        count += 1

    tree = ET.ElementTree(topics)
    ET.indent(tree, '  ')
    tree.write(filename, encoding="utf-8", xml_declaration=True) 

if __name__ == "__main__":  
    create_xml("topics.xml")
