import urllib as u
import youtube_dl
import pafy
import sys
import soundcloud as sc
import os
import time
import re
import lxml
import json
import Tkinter as tk
import tkFont
import ttk
from   lbox import *
from   lxml import etree
from   Tkinter import *

cid="50aaa3de7469fde7c1e5e6ad7c91275c"
client=sc.Client(client_id=cid)

class Search():
  def __init__(self,search_queary,limits):
    pass

def searchSC(terms,limit=50):
  tracks=client.get('/tracks',q=terms,filter="public",limit=limit)
  x=[]
  for i in tracks:
    try:
      z={}
      s,ms=divmod(i.fields()['duration'],1000)
      m,s=divmod(s,60)
      h,m=divmod(m,60)
      dur="%d:%02d:%02d" % (h,m,s)
      z["title"]=str(i.fields()['title'])
      z["length"]=dur
      z['url']=str(i.fields()['permalink_url'])
      x.append(z)
    except UnicodeEncodeError:
      pass
  return x

def fetchSC(url,path=os.getcwd()):
  track = client.get('tracks/%s'%(client.get('/resolve', url=url).id))
  stream_url = client.get(track.stream_url, allow_redirects=False)
  f=open(path+"/"+track.title+'.mp3','wb')
  f.write(u.urlopen(str(stream_url.location)).read())
  f.close()
  print "Done"

def searchYT(terms,limit=50):
  results=[]
  page=1
  while len(results)<=limit:
    query_string = u.urlencode({"search_query" : terms,"page" : page})
    html_content = u.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read())
    for i in search_results:
      if not results.__contains__(i):
        results.append(i)
    page+=1
  x=[]
  for i in results:
    try:
      z={}
      title,dur=getYT(i)
      z["title"]=str(title)
      z["length"]=dur
      z['url']=str(i)
      x.append(z)
    except UnicodeEncodeError:
      pass
  return x

def fetchYT(ident,path=os.getcwd()):
  v=pafy.new("http://www.youtube.com/watch?v="+ident)
  audio=v.getbestaudio()
  audio.download(path,True)
  if str(audio).find("mp3")==-1:
    os.system("./ffmpeg/ffmpegLinArmhf -i '%s' -codec:a libmp3lame -qscale:a 2 %s.mp3"%(
      path+"/"+str(v.title)+"."+str(audio).split(":",1)[1].split("@",1)[0],path+"/"+str(v.title)))
  print "Done"

def getYT(ident):
  youtube = etree.HTML(u.urlopen("http://www.youtube.com/watch?v=KQEOBZLx-Z8").read())
  video_title = youtube.xpath("//span[@id='eow-title']/@title")
  title=''.join(video_title)
  api_key='AIzaSyCf-aoW-PqU_4XcldbFv1WrwtCFtc95QnY'
  searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+ident+"&key="+api_key+"&part=contentDetails"
  response = u.urlopen(searchUrl).read()
  data = json.loads(response)
  all_data=data['items']
  contentDetails=all_data[0]['contentDetails']
  duration=contentDetails['duration']
  dur=duration.strip("PT")
  try:
    h,m=dur.split("H")
    m,s=m.split("M")
    s=s.strip("S")
  except ValueError:
    try:
      h="0"
      m,s=dur.split("M")
      s=s.strip("S")
    except ValueError:
      h="0"
      m="0"
      s=dur.strip("S")
  return title,"%d:%02d:%02d"%(int(h),int(m),int(s))

w=Tk()
w.title("Muzez Client")
lf=LabelFrame(w)
search=Entry(lf)
search.config(width=50)
search.grid(row=1,column=1)
submit=Button(lf,text="Search").grid(row=1,column=2)
lbox=MultiListbox(lf,(("Title",47),("Duration",10)))
lbox.grid(row=2,column=1,columnspan=2)
for i in [("Hello","World"),("World","Hello")]:
  lbox.insert(END,i)
lf.grid(row=1,column=1)
w.mainloop()
