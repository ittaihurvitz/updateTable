import sys
import datetime
from bs4 import BeautifulSoup

# Must install BeautifulSoap  !!! Use one of the following methods - 
#   $ apt-get install python-bs4 (for Python 2)
#   $ apt-get install python3-bs4 (for Python 3)
#   or $ pip install beautifulsoup4




def updateBubble(bubbleName,user,htmlPath):
    print "updateBubble run with:" + bubbleName +", " + user + ", " + htmlPath

    currentTime = datetime.datetime.now().strftime("%d/%m/%y  %H:%M")

    html_doc = open(htmlPath,'r')
    soup = BeautifulSoup(html_doc, 'html.parser')

    print "Data for debugging - Before change:"
    rows = soup.findAll('tr')
    for row in rows:
        print row

    print "############### Start ###################"

    parent = None
    tags = soup.findAll('td', text = bubbleName)
    print tags

    if len(tags) > 0 :

        # Get parent tag  (TODO - get it without loop)
        for tag in tags:
            parent = tag.parent

        # Check if have the data
        if parent == None:
            print "Exit because didn't succeed manipulating the file"
            exit()

        # Update all <td> under this <tr>
        for child in parent.children:
            if child['id'] == 'name':
                print "do nothing. Its the key"
            elif child['id'] == 'number':
                child.string = user
            elif child['id'] == 'date':
                child.string = currentTime
            else:
                print "Not found"
        print "Data for debugging - The row that was changed:"
        print parent
                
    else: # Didn't find a bubble with this name so add a new row
        print "will add" + bubbleName
        table = soup.findAll('table')
        data1 = soup.new_tag('td', id='name')
        data1.string = bubbleName
        data2 = soup.new_tag('td', id='number')
        data2.string = user
        data3 = soup.new_tag('td', id='date')
        data3.string = currentTime
        newTr = soup.new_tag('tr')
        newTr.append(data1)
        newTr.append(data2)
        newTr.append(data3)
        table[0].append(newTr)
        
        print "Data for debugging - The row that was added:"
        print newTr

    html_doc.close()

    # Update the file
    html = str(soup)
    with open(htmlPath, "wb") as file:
        file.write(html)

    print 'Finished'



if __name__ == "__main__":
    bubbleName = sys.argv[1]
    user = sys.argv[2]
    htmlPath = sys.argv[3]
    updateBubble(bubbleName,user,htmlPath)
