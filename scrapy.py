import requests, re, sys
from docopt import docopt
from bs4    import BeautifulSoup
from time   import time as timer
from functools import partial
from multiprocessing import Pool

def get_urls(search_string, start):
    temp = []
    url = 'http://www.google.com/search'
    payload = { 'q' : search_string, 'start' : start }
    my_headers = { 'User-agent' : 'Mozilla/11.0' }
    r = requests.get( url, params = payload, headers = my_headers )
    soup = BeautifulSoup( r.text, 'html.parser' )
    h3tags = soup.find_all( 'h3', class_='r' )
    for h3 in h3tags:
        try:
            temp.append( re.search('url\?q=(.+?)\&sa', h3.a['href']).group(1) )
        except:
            continue
    return temp

def main():
    start = timer()
    result = []
    arguments = docopt( __doc__, version='MakMan Google Scrapper' )
    search = arguments['<search>']
    pages = arguments['<pages>']
    processes = int( arguments['<processes>'] )
    make_request = partial( get_urls, search )
    pagelist = [ str(x*10) for x in range( 0, int(pages) ) ]
    with Pool(processes) as p:
        tmp = p.map(make_request, pagelist)
    for x in tmp:
        result.extend(x)
    result = list( set( result ) )
    print( *result, sep = '\n' )
    print( '\nTotal URLs Scraped : %s ' % str( len( result ) ) ) 
    print( 'Script Execution Time : %s ' % ( timer() - start, ) )

if __name__ == '__main__':
    main()