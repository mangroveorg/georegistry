import pycurl, urllib
import StringIO
from georegistry import settings

def create_tx_webhook(result_list, url=None):
    if not url:
        URL=settings.TX_CREATE_WEBHOOK_URL
    else:
        URL=url
    
    post_dict={}
    pf=[]
    post_dict.update(result_list[0])
    post_dict['webhook_key']=settings.TX_WEBHOOK_KEY
    for o in post_dict:
        x=(str(o), str(post_dict[o]))
        pf.append(x) 
    
    #pf=urllib.urlencode(pf)

    #URL="%s?%s" %(URL, pf)
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.URL, URL)
    c.setopt(c.HTTPPOST, pf)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.perform() 
    responsedict={}
    responsedict['code']=c.getinfo(c.HTTP_CODE)
    responsedict['body']=b.getvalue()
    return responsedict