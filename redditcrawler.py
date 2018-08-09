import requests
from bs4 import BeautifulSoup
import json

lastid="" #sayfadaki son id (sonraki sayfaya geçebilmek için)

dongudencik=0 
arraycomments = [] #commentleri tutan array
postarray = [] #son 6 aydaki tüm postları tutar
p= {} 
c = {}
subreddit = input("Enter the subreddit: ")
def my_function():
    global lastid

    url="" #istek yapılacak adresi tutar
    r="" 
    if lastid=="": #subreddite yapılan ilk istek
       url = "https://www.reddit.com/r/"+subreddit+"/new"
    else: #sonraki istekler için
       url = "https://www.reddit.com/r/"+subreddit+"/new/?after=t3_"+lastid
    payload = {'some': 'data'}
    headers={ #istek yaparken hata almamak için
            'User-Agent': 'r/turkey Reddit Crawler 0.1.0 by /u/omer'
        }
    try:
        r = requests.get(url, headers=headers) #url e request
    except requests.exceptions.RequestException as e:
        print("")

    source = BeautifulSoup(r.content,"html.parser") #kaynak kodu

    solmenu = source.find_all("div",attrs={"class" : "scrollerItem"}) #postların classı scroller itemdir ve postları solmenude tutuyoruz

    a="" #
    sayac=0 #ekrana bastırırken kontrol etmek için

    for link in solmenu:
       try:
         print(sayac)
         sayac+=1;
         postid=""
         urlname=""
         imageurl=""
         hours=""
         postvote=""
         html_doc = str(link)
         source2 = BeautifulSoup(html_doc, 'html.parser') # subredditin içindeki her posta girmek için

         urlreq = source2.find_all("a",attrs={"class":"SQnoC3ObvgnGjWt90zD9Z"}) #classı verilen a taglarını getir
         g = str(urlreq).split("</h2>")[0].split(">")
         urlname = g[-1] #urlname = postun başlığı
         if len(str(urlreq).split(" ")) >=3 : url=str(urlreq).split(" ")[3].split(">")[0].split('"')[1] #post linki

         postid=str(url).split('/')[4] #postid urlin içinde yer alıyor


         lastid=postid

         image = source2.find_all("div",attrs={"class" : "_2c1ElNxHftd8W_nZtcG9zf"}) #img tagı
         if "background-image" in str(image): imageurl=str(image).split("background-image")[1].split(')')[0].split('(')[1]  #img url parsing

         if len(imageurl)==0: imageurl="" #img yoksa "" olarak tut


         hoursago = source2.find_all("a",attrs={"class" : "_3jOxDPIQ0KaOWpzvSQo-1s"})
         if len(str(hoursago).split('_blank">'))>=2: hours=str(hoursago).split('_blank">')[1].split('<')[0] #hours ago döner

         global dongudencik #6 aylık veriler gelene kadar devam etmesi için
         print(hours)
         if ("6 months ago" in hours):
             dongudencik=2
             break #6 aylık veriyi bulunca işlem dursun

         postedbysource = source2.find_all("a",attrs={"class" : "_2tbHP6ZydRpjI44J3syuqC"}) #postedby elemanı
         if len(str(postedbysource).split("u/"))>=2: postedby = str(postedbysource).split("u/")[1].split('<')[0] #postedby döner

         vote = source2.find_all("div",attrs={"class" : "_1rZYMD_4xY3gRcSS3p8ODO"}) #vote elemanı
         postvote = str(vote).split(">")[1].split('<')[0] #vote döner

         global p #postun verilerini tutan obje
         p = {}
         p["Post_Name"] = urlname
         p["Url"] = url
         p["Post_Id"] = postid
         p["Image_Url"] = imageurl
         p["Video_Url"] = ""
         p["Date"] = hours
         p["Posted_By"] = postedby
         p["Post_Vote"] = postvote

         purl=""
         a = "https://www.reddit.com"+url
         purl=a

         if 'http' in url: purl=url

         payload = {'some': 'data'}
         headers={
                 'User-Agent': 'r/turkey Reddit Crawler 0.1.0 by /u/omer'
             }
         r = requests.get(purl, headers=headers)

         source = BeautifulSoup(r.content,"html.parser")

         solmenu = source.find_all("div",attrs={"class":"fxv3b9-2"})

         array = []
         array = str(solmenu).split(',')

         p["Header_Comment"] = ""
         p["Comment_Count"] = ""
         p["Comment_Upvoted"] = ""
         #dataforheader = BeautifulSoup(r.content,"html.parser")
         #postheaderinfo = source.find_all("div",attrs={"class":"s1w0aodp-7"}) #original post info
         #info_doc = str(postheaderinfo)
         #info_query = BeautifulSoup(html_doc, 'html.parser')
         info_text = source.find_all("p",attrs={"class":"s570a4-10"}) #main post content
         info_video_youtube = source.find_all("iframe",attrs={"class":"media-element"}) #youtube video link
         info_video_native = source.find_all("video",attrs={"class":"HTML5StreamPlayer_video_regular"}) #native video link
         info_head_arr = []
         try:
             info_head_arr.append(str(info_video_youtube).split('src="')[1].split('"')[0])
         except Exception as e:
             print("")
         try:
             info_head_arr.append(str(info_video_native).split('src="')[1].split('"')[0])
         except Exception as e:
             print("")

