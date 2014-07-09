#coding:utf8
import sae
import sae.const
import web
import os
urls=(
        '/',"index",
        '/look','seeData',  # 查看维修报表
        '/frame/top.html','readTop',
        '/frame/main.html','readMain',
        '/frame/right.html','readRight',
        '/sendSubmit','sendSubmit', #提交
        '/oklist','okList', #列出故障
        '/list','noList', #列出故障
        '/nolist','noList', #列出故障
        '/yeslist','yesList',
        '/yesDeal','yesDeal',
        '/yesDeal/post','yesDealPost',
        '/login/?','login', # 登录
        '/login/loginPost','loginPost',
        '/logout','logout',
        '/linux/?','adminIndex',
        '/admin/frame/top.html',"areadTop",
        '/admin/frame/main.html',"areadMain",
        '/admin/setList','setList', # 成员
        '/admin/setList/post','setListPost', # 成员
        '/admin/setMess','setMess', # 成员
        '/admin/setMess/post','setMessPost', # 成员
        '/admin/setKey','setKey',
        '/admin/setKey/rpost','rsetKeyPost',
        '/admin/setKey/opost','osetKeyPost',
        '/admin/clearBugsList','clearBugsList',
        '/admin/clearBugsList/post','clearBugsListPost',
        )
web.config.debug = False
app_root=os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
db=web.database(port=int(sae.const.MYSQL_PORT), host=sae.const.MYSQL_HOST,dbn="mysql",
        user=sae.const.MYSQL_USER,pw=sae.const.MYSQL_PASS,
        db=sae.const.MYSQL_DB)

def get_bugsList(): 
    class BugsList:
        yes=0
        no=0
        yeslist=[]
        nolist=[]
    buglist=BugsList()
    buglist.yeslist=db.select('bugs',where="IsOver = 1")
    buglist.nolist=db.select('bugs',where="IsOver <> 1")
    buglist.yes=len(buglist.yeslist)
    buglist.no=len(buglist.nolist)
    return buglist

def get_isLoginOk(user,password):
    data=db.select('accounts',
            where="UserName=\'%s\' and PassWord=\'%s\'"%(user,password))[0]
    return int(data.Uid)

class CheckLogin:
    def __init__(self):
        try:
            username=web.cookies().user
            password=web.cookies().pwd
            self.uid=get_isLoginOk(username,password)
        except:
            raise web.seeother("/login")


def get_listDb():
    listDb=[]
    for i in db.select("listdb"):
        listDb.append((i.No,i.Name,i.Phone))
    return listDb
def get_mess():
    d=db.select("info",where="Name = \"mess\"")
    if not d:
        db.insert("info",Name="mess",Content="")
        return ""
    return d[0].Content

class send_mail():
    def __init__(self):
        self.__username="ljd31415926@126.com"
        self.__password="3.1415926"
        web.config.smtp_server="smtp.126.com"
        web.config.smtp_port=25
        web.config.smtp_username=self.__username
        web.config.smtp_password=self.__password
        web.config.smtp_starttls=True

    def sendMail(self,__subject,__message):
        web.sendmail(self.__username,"q8886888@qq.com",__subject.encode("utf-8"),__message.encode("utf-8"))


def getDate(t=None):
    from datetime import date
    from calendar import monthrange
    today=date.today()
    month=today.month 
    year=today.year
    days=today.day 
    
    if t=='last':
        month=month-1 or 12
        year=month-1 and year or year-1
        days=monthrange(year,month)[1]
    return str(year),"%02.0f"%month,"%02.0f"%days

class made_Img():
    def __init__(self,data):
        import matplotlib.pyplot as plt
        from matplotlib.font_manager import FontProperties
        zfont= FontProperties(fname=os.path.abspath('SimHei.ttf'),size=14)
        import cStringIO

        year,month,days=data
        self.img=cStringIO.StringIO()
    
        plt.figure(figsize=(12,8))
        xmess=u"%s年%s月"%(year,month)
        plt.xlabel(xmess,fontproperties=zfont)
        plt.ylabel(u"故障数",fontproperties=zfont)
        plt.title(xmess+u"\n"+u"故障统计图",fontproperties=zfont)
        x=range(1,int(days)+1)
        y_bugs=self.getLen(data)
        y_yes=self.getLen(data,True)
        plt.xticks(x)
        plt.yticks(range(max(y_bugs+y_yes)+1))
        plt.plot(x,y_bugs,'r-',linewidth=2,label="number of faults")
        plt.plot(x,y_yes,'g-.',linewidth=2,label="resolved")
        plt.legend(loc="upper right")
        plt.grid(True) # 显示边框
        plt.savefig(self.img,format="png")
        
    def getImg(self):
        return self.img.getvalue()

    def getLen(self,data,isOver=False):
        year,month,days=data
        days_bugs=dict().fromkeys(range(1,int(days)+1),0)
        f="%s-%s-%%"%(year,month)
        if isOver:
            d=db.select("bugs",
                    where="IsOver = 1 and YesTime Like \"%s\""%(f))
        else:
            d=db.select("bugs",
                    where="PostTime Like \"%s\""%(f))
        for i in d:
            if isOver:
                day=int(i.YesTime.split()[0].split('-')[2]) 
            else:
                day=int(i.PostTime.split()[0].split('-')[2]) 
            days_bugs[day]+=1
        return days_bugs.values()
        
    def update(self,key):
        import qiniu.conf
        qiniu.conf.ACCESS_KEY="BbDU4MoFrx2YaF6tqBFmnKHFuDlq1EO-mm2ldlBm"
        qiniu.conf.SECRET_KEY="WWdwgm4oRmOh_L9yKbyWplcUFaIGAZXk8e_UOtDs"

        import qiniu.rs
        policy=qiniu.rs.PutPolicy("imgdata")
        uptoken=policy.token()
        
        import qiniu.io
        ret,err=qiniu.io.put(uptoken,key,self.img)
        

