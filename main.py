import requests
from bs4 import BeautifulSoup as bs4
from docx import Document as doc
from docx.shared import Cm 
import sys

if len(sys.argv) != 3:
    print("The format should be \n./main.py <url> <output_file_name>")
else:
    url = sys.argv[1]
    doc_name = sys.argv[2]
    document = doc()
    
    page = requests.get(url)
    
    if(page.status_code == requests.codes.ok):
        soup = bs4(page.content,'html.parser')
        
        headings = soup.find_all("h1",class_="firstHeading")
        document.add_heading(headings[0].text)
        
        details = soup.find("div",id="bodyContent")
        
        main_soup = bs4(details.prettify(),'html.parser')
        
        #Extract the table elements to be implemented in the future
        table = main_soup.find('table').extract()
        
        #isEmpty is the lambda function that checks if a list is empty
        isEmpty = lambda x: True if(x == []) else False

        #tableElem = ('table','td','tr')

        for x in details.children:
            if x != '\n' and x !='' and x != ' ':
                if(not isEmpty(list(x.children))):
                    for i in list(x.children):
                        # print(i.string)
                        if i.string == None:
                        #print(len(list(i.children)))
                            for j in i.children:
                            #print(j.name)
                                if j.string == None:
                                    #print(j.attrs)
                                    if(j.name == 'table' or j.name == 'ol' or j.name == 'ul'):
                                        #print(j.attrs)
                                        continue
                                        #j = j.next_sibling.next_sibling
                            
                                    #search and purge references
                                    if list(j.descendants) != []:
                                        #print(list(j.descendants))
                                        for a in j.descendants:
                                            if a.string == None:
                                                attr = a.attrs.keys()
                                                #print(a.attrs)
                                                if 'class' in attr:
                                                    if 'mw-references-wrap' in a.attrs['class']:
                                                        #print(a.text)
                                                        a.decompose()
                                                        break
                                        #if 'href' in attr:
                                            #if '#References' in a.attrs['href']:
                                                #a.decompose()
                                        
                                    
                                    #print the elements
                                    document.add_paragraph(j.text)
                                    #print(j.prettify())
                                    #print('\n')
        
        if doc_name.endswith('.doc') or doc_name.endswith('.docx'):
            document.save(doc_name)
        else:
           document.save(doc_name+'.doc')

        
        
