import sys
import argparse
import json
import datetime
from rparser import Reader
import os
import pdfkit

path_wkhtmltopdf = r'C:\Users\Asus\Anaconda3\Lib\site-packages\wkhtmltopdf\wkhtmltox\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

version = "1.1"

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('site', metavar='URL', type=str, nargs='+', default=["https://finance.yahoo.com/rss/"],
                    help='a link')
    parser.add_argument('--version',
            action='version', help="Print version info", version='%(prog)s {}'.format (version))
    parser.add_argument("--json", help="Print result as JSON  in stdout", action="store_true") 
    parser.add_argument("--verbose", action="store_true",
                    help="Outputs status messages")
    parser.add_argument("--limit",type=int, help="Limit news topics if this parameter provide", default=12)
    parser.add_argument("-d","--date", type=lambda s: datetime.datetime.strptime(s, '%Y%m%d') )
    parser.add_argument("--topdf", help="Converting the result to pdf", action="store_true")
    parser.add_argument("--tohtml", help="Converting the result to html", action="store_true")
    
    return parser
 
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    print (namespace)
 
    for site in namespace.site:
            
            RSS=Reader(site)                
            if namespace.verbose:
               RSS.state()     
            if namespace.date:
                if namespace.json:
                    json.dumps(RSS.date(namespace.limit, namespace.date))
                else:
                    RSS.date(namespace.limit, namespace.date)
                    
            else:
                if namespace.json:
                    json.dumps(RSS.read_news(namespace.limit))
                   
                else:
                    RSS.read_news(namespace.limit)
            if namespace.tohtml:
                with open("rss.txt") as file:
                    with open ("rss.html", "w") as output:
                       file = file.read()
                       file.replace("\n", "<p>")
                       output.write(file)
            if namespace.topdf:
                pdfkit.from_file("rss.txt", "rss.pdf", configuration=config) 
                os.startfile("rss.pdf")
               
            
                
                                 
                            
                        
                    
                          

                    