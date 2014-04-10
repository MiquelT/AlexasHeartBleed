from BeautifulSoup import BeautifulSoup
import urllib2
import sys
import os

import ssltest

url = "http://www.alexa.com"
topsite = "/topsites/countries"
globalurl = "/topsites/global;"
path = "countryList/"

file_path = ""

b = 0
x = 500;

def usage():
    print "\nsslTestAlexasSites\n\nUsage:\n"
    print "python main.py [-h] [-g [X]] [-c [X]] [-f filePath]"
    print "\nWithout options: \tCheck the vulnerabilty of all Top Sites by Country."
    print "\n-h:\tHelp - prints this usage."
    print "-c:\tCheck top X sites by Country."
    print "-g:\tCheck global top X sites on the web."
    print "-f:\tCheck urls from file."
    print " \t\t1 <= X <= 500"

    sys.exit(0)


def init_args():
    global b
    global x
    global file_path
    if len(sys.argv) == 1:
        b = 1
    elif len(sys.argv) >= 2:
        if sys.argv[1] == '-g':
            b = 0
            if len(sys.argv) == 3:
                try:
                    x = int(sys.argv[2])
                    if x > 500 or x < 1:
                        usage()
                except:
                    usage()
        elif sys.argv[1] == '-c':
            b = 1
            if len(sys.argv) == 3:
                try:
                    x = int(sys.argv[2])
                    if x > 500 or x < 1:
                        usage()
                except:
                    usage()
        elif sys.argv[1] == '-f':
            b = 2
            if len(sys.argv) == 3:
                try:
                    file_path = sys.argv[2]
                except:
                    usage()
        else:
            usage()
    else:
        usage();

def global_search(test):

    count = 0

    list = []

    for i in range(20):
        urlF=url + globalurl + str(i)

        page=urllib2.urlopen(urlF)
        soup=BeautifulSoup(page.read())

        sect = soup.findAll('section')
        fsec = None
        for s in sect:
            if s['class'] == "td col-r":
                fsec = s
        sites=fsec.findAll('li')
        for site in sites:
            if count == x:
                break

            count += 1;

            site_url = site.a.string.lower()

            print str(count) + "- "+site_url

            v = False
            try:
                v = test.ssltest(site_url)
            except:
                # print "Retrying..."
                site_url = "www."+site_url
                try:
                    v = test.ssltest(site_url)
                except:
                    print "FAIL - impossible to connect with: " + site_url[4:]
                    continue
            if v: list.append(site_url)

        if count == x:
            break
    create_global_document(list)



def get_sites_by_country(country,final_url,test):
    print country + ":"
    count = 0

    list = []

    for i in range(20):
        urlF = url + topsite + ";" + str(i) + "/" + final_url

        page=urllib2.urlopen(urlF)
        soup=BeautifulSoup(page.read())

        sect = soup.findAll('section')
        fsec = None
        for s in sect:
            if s['class'] == "td col-r":
                fsec = s
        sites=fsec.findAll('li')
        for site in sites:
            if count == x:
                break

            site_url = site.a.string.lower()
            count += 1;
            print str(count) + "- "+site_url
            v = False
            try:
                v = test.ssltest(site_url)
            except:
                # print "Retrying..."
                site_url = "www."+site_url
                try:
                    v = test.ssltest(site_url)
                except:
                    print "FAIL - impossible to connect with: " + site_url[4:]
                    continue

            if v: list.append(site_url)
        if count == x:
            break
    return list


def by_countries(test):

    urlF= url + topsite

    page=urllib2.urlopen(urlF)
    soup=BeautifulSoup(page.read())

    sect = soup.findAll('section')
    fsec = None
    for s in sect:
        if s['class'] == "td col-r":
            fsec = s
    sites=fsec.findAll('li')

    map = {}

    for site in sites:
        final_url =  site.a.get('href').split('/')[3]
        country = site.a.string
        list = get_sites_by_country(country,final_url,test)
        if len(list) > 0: map[country] = list

    create_country_document(map)


def by_file(test):
    list = []
    try:
        f = open(file_path, 'r')
    except:
        print "FAIL - impossible to open file: " + file_path
        sys.exit(0)


    for line in f:
        line = line.strip()
        port = 443
        if len(line.split(" ")) == 2:
            port = line.split(" ")[1]
            line = line.split(" ")[0]

        v = False
        try:
            v = test.ssltest(line,port)
        except:
            # print "Retrying..."
            line = "www."+line
            try:
                v = test.ssltest(line)
            except:
                print "FAIL - impossible to connect with: " + line[4:]
                continue

        if v: list.append(line)

    create_global_document(list)


def create_global_document(list):
    if len(list) > 0:
        create_directory()
        f = open(path+"Globallist.txt", 'w')
        total = len(list)
        f.write("Total: " + str(total) + "\n")
        for l in list:
            f.write(l + "\n")
        f.close()

def create_country_document(map):
    if len(map) > 0:
        create_directory()
        f = open(path+"Countrylist.txt", 'w')
        for key in map:
            total = len(map[key])
            f.write(key +": (" + str(total) + ")\n")
            for l in map[key]:
                f.write(l + "\n")
            f.write("\n")
        f.close()


def create_directory():
    if not os.path.isdir(path):
        os.makedirs(path)


if __name__ == "__main__":
    test = ssltest.Ssltest()
    init_args()
    if b == 0:
        global_search(test)
    elif b == 1:
        by_countries(test)

    elif b == 2:
        by_file(test)
    else:
        usage()
    print "\nDone!\n"

