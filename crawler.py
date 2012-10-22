from HTMLParser import HTMLParser
from urlparse import urlparse
import urllib
import sys
import random

start_url = sys.argv[1]
parse_no = sys.argv[2]

if urlparse(start_url).scheme == 'https':
  print "\nCannot parse 'https'. Please enter an 'http' url.\n"
  sys.exit()

# write start url to repository file URLfile.txt.
fp = open('URLfile.txt', 'w')
fp.write(start_url) 
fp.close()

crawled_urls = []
print "\nThe parsed url's are listed below. File 'URLfile.txt' contains the complete list of url's\n"
for x in range(0,int(parse_no)):
  
  # Select a random link from repository file.
  while True:
    random_line = random.choice(open('URLfile.txt').readlines())
    random_line = random_line.rstrip('\n')
    
    # Ignore links already parsed.
    if random_line in crawled_urls: 
      continue
	  
    # Ignore links with the following extentions.
    elif random_line.find('.msi') != -1 or random_line.find('.tar.bz') != -1 or random_line.find('.rdf') != -1 or random_line.find('.zip') != -1:
      continue
	  
    elif random_line.find('https') != -1:
      continue
    else:
      crawled_urls.append(random_line)
      print random_line
      break

  # Get the main url part from the random url selected.
  main_url =  urlparse(random_line).scheme + '://' + urlparse(random_line).netloc
  
  # With the random link/url open the corresponding page and get all its contents.
  f = urllib.urlopen(random_line)
  s = f.read()
  
  # Open the repository again to append the new links into it.
  fp = open('URLfile.txt', 'a')

  # From the page contents, retrieve all the links.
  class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
      if tag == 'a':
        for name, value in attrs:
          if name == 'href':
            flag = False; 
 
            # Set flag as True.
            if value == '/' or value == '#' or value == '':
              flag = True
	   
            # If the link is an absolute url containing 'http'.
            elif value[0:4] == 'http':
              link = value     

            # If the link is a relative url and contains no initial '/'
            elif value[:1] != '/':
              link = main_url + '/' + value
			  
            # If the link is a relative url.
            else:
              link = main_url + value
	  
            # Append the new link into the repository.
            if flag == False:
              fp.write('\n')
              fp.write(link)
			
  parser = MyHTMLParser()

  # Feed the page's content obtained above to the parser.
  parser.feed(s)
  fp.close()