#coding:utf8
from config import *
from submit import *
from listbug import *
from login import *
from admin import *
from error import *

class index:
    def GET(self):
        return render.index()
class readTop:
    def GET(self):
        buglist=get_bugsList()
        return render.frame.top(buglist.yes,buglist.no)

class readMain:
    def GET(self):
        return render.frame.main()

class readRight:
    def GET(self):
        return render.frame.right(get_mess(),get_listDb())

class seeData:
    def GET(self):
        data=web.input()
        try:
            t=data['type']
            data=getDate(t)
        except KeyError:
            data=getDate()

        if not int(data[2]): #如果是1号，就报错
            return render.look()

        img=made_Img(data).getImg()

        return img

app=web.application(urls,globals())
app.notfound=notfound
app=app.wsgifunc()
application=sae.create_wsgi_app(app)
