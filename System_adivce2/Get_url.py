from webbrowser import get
import requests
import Database_connect
from lxml import etree
import re
import io
from PIL import Image,ImageTk

# get address of movies on website
def get_movie_url(movieid):
    conn, cur = Database_connect.Connect_sql()
    cur.execute("select imdbId from Advice_Database.links where movieId = {}".format(movieid))
    imdbid = str(cur.fetchall()[0][0])
    Database_connect.Close_sql(conn,cur)
    imdbid="0"*(7-len(imdbid)) + imdbid
    url_imbid = "http://www.imdb.com/title/tt{}/".format(imdbid)
    return url_imbid

# data mining to get data online. description, title and genres
def  get_detail_movie(url, movieid):
     header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'}

     print(movieid)
     html = requests.get(url,headers=header)
     bs = etree.HTML(html.text)
     # src = bs.xpath('//div[@class="poster"]/a/img/@src')[0]

     src = bs.xpath('//link[@rel="image_src"]/@href')[0]
     conn,cur = Database_connect.Connect_sql()
     sql = "select title,genres from Advice_Database.movies where movieid = {}".format(movieid)
     cur.execute(sql)
     data = cur.fetchall()
     text = bs.xpath('//script[@type="application/ld+json"]')[0].text
     briefinfo = bs.xpath('normalize-space(//div[@class="summary_text"]/text())')
     # briefinfo = re.findall('^.*?"description": "(.*?)",\n  "date', text, flags=re.S)[0].strip(', "')
     print(data[0][0])

     title = re.findall('(.*)\(', data[0][0])[0].strip(' ')
     date = re.findall('\((\d*)\)', data[0][0])[0].strip(' ')
     genres_list = data[0][1].strip('\r').split('|')
     genres = "\n".join(genres_list)
     Database_connect.Close_sql(conn,cur)
     return src, title, date, genres, briefinfo

# covert information into suitable size we need.
def resize(w, h, w_box, h_box, pil_image):
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


# data mining to get images of movies
def  get_image(src, w_box=80,h_box=120):
     html = requests.get(src).content        #detail of this functions
     data_stream=io.BytesIO(html)
     pil_image = Image.open(data_stream)
     w, h = pil_image.size
     pil_image_resized = resize(w, h, w_box, h_box, pil_image)
     tk_image = ImageTk.PhotoImage(pil_image_resized)  # 转tk_image
     return tk_image

def get_similar_movie_list(movieId,type="ALS"):
    conn, cur = Database_connect.Connect_sql()
    if type == "SVD":
        sql = "select similarId,similarDegree from Advice_Database.movie_similar_svd where movieId={} order by similarDegree desc limit 20;".format(movieId)

    cur.execute(sql)
    data = cur.fetchall()
    Database_connect.Close_sql(conn,cur)
    return data
