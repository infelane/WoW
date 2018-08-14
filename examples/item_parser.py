import asyncore
import string, socket
from io import StringIO
from email.mime import mimetools
from urllib.parse import urlparse
import pickle
import re

start = 13359
finish = 13370
blizzard = "http://us.battle.net/wow/en/item/"
wowhead = "http://www.wowhead.com/item="
url = wowhead
outputdir = "G:/Documents/MiscScripts/WoWItemScraper/"


class AsyncHTTP(asyncore.dispatcher_with_send):
    # HTTP requestor
    
    def __init__(self, uri, consumer):
        asyncore.dispatcher_with_send.__init__(self)
        
        self.uri = uri
        self.consumer = consumer
        
        # turn the uri into a valid request
        scheme, host, path, params, query, fragment = urlparse.urlparse(uri)
        assert scheme == "http", "only supports HTTP requests"
        try:
            host, port = string.split(host, ":", 1)
            port = int(port)
        except (TypeError, ValueError):
            port = 80  # default port
        if not path:
            path = "/"
        if params:
            path = path + ";" + params
        if query:
            path = path + "?" + query
        
        self.request = "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host)
        
        self.host = host
        self.port = port
        
        self.status = None
        self.header = None
        
        self.data = ""
        
        # get things going!
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
    
    def handle_connect(self):
        # connection succeeded
        self.send(self.request)
    
    def handle_expt(self):
        # connection failed; notify consumer (status is None)
        self.close()
        try:
            http_header = self.consumer.http_header
        except AttributeError:
            pass
        else:
            http_header(self)
    
    def handle_read(self):
        data = self.recv(2048)
        if not self.header:
            self.data = self.data + data
            try:
                i = string.index(self.data, "\r\n\r\n")
            except ValueError:
                return  # continue
            else:
                # parse header
                fp = StringIO.StringIO(self.data[:i + 4])
                # status line is "HTTP/version status message"
                status = fp.readline()
                self.status = string.split(status, " ", 2)
                # followed by a rfc822-style message header
                self.header = mimetools.Message(fp)
                # followed by a newline, and the payload (if any)
                data = self.data[i + 4:]
                self.data = ""
                # notify consumer (status is non-zero)
                try:
                    http_header = self.consumer.http_header
                except AttributeError:
                    pass
                else:
                    http_header(self)
                if not self.connected:
                    return  # channel was closed by consumer
        
        self.consumer.feed(data)
    
    def handle_close(self):
        # self.consumer.close()
        self.close()


class DummyConsumer:
    size = 0
    text = ''
    
    def http_header(self, request):
        # handle header
        if request.status is None:
            print
            "connection failed"
    
    def feed(self, data):
        # handle incoming data
        self.size = self.size + len(data)
        self.text = self.text + data

    # def close(self):
    # end of data
    # print self.size, "bytes in body"
    # print self.text


#
# try it out

itemCounter = start
while itemCounter < finish:
    consumer = DummyConsumer()
    consumer.text = ''
    
    request = AsyncHTTP(
        "%s" % str(url) + str(itemCounter),
        consumer
    )
    
    asyncore.loop()
    print
    "%s" % str(url) + str(itemCounter)
    itemCounter = itemCounter + 1
    itemDB = {}
    log = open(outputdir + 'log.txt', 'a')
    
    x = consumer.text
    print
    "Result: %d length, %s" % (len(x), x[0:10])
    
    if '<b class="q' in x:
        print
        'FOUND AN ITEM'
        name = x.split('<b class="q')
        x = x.replace(name[0], '')
        name[1] = name[1].replace(name[1][0:3], '')
        name = name[1].split('</b>')[0]
        itemDB[name] = []
        x = x.replace(name, '')
        x = x.split("ge('icon")[0]
        x = x.rstrip(' \t\n\r')
        results = re.compile('>(.*?)<', re.DOTALL | re.IGNORECASE).findall(x)
        for y in results:
            if len(y) > 1 and '\n' not in y:
                itemDB[name].append(y)
        print
        'Adding %s : item %s with attributes:' % (name, itemCounter)
        log.write('Adding %s : item %s with attributes:' % (name, itemCounter))
        for x in itemDB[name]:
            print
            ' ' + x
            log.write(' ' + x)
        print
        '\n'
        log.write('\n')
    
    log.write("%s" % str(url) + str(itemCounter) + '\n')
    log.close

log.close
str_path = open(outputdir + 'itemdatabase.db', 'wb')
pickle.dump(itemDB, str_path)
str_path.close()
print
"Complete and written to '%sitemdatabase.db'!" % outputdir
