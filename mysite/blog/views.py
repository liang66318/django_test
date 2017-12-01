from django.shortcuts import render
from .models import Post
import urllib.request
from bs4 import BeautifulSoup
import ssl

# Create your views here.

class detail_struct():
	def __init__(self, title, text, picture, video):
		self.title = title
		self.text = text
		self.picture = picture
		self.video = video

def post_list(request):

    if request.GET:
        gcon = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        page = urllib.request.urlopen(request.GET["url_k"], context=gcon)
        soup = BeautifulSoup(page, "html.parser")
        name_box = soup.find("div", attrs={"id": "story_body_content"})

        p_detailed = detail_struct(title=name_box.find("h1").text,
                                   text=name_box.find("p").text,
                                   picture=name_box.find("img").attrs["data-src"],
                                   video=name_box.find("div", attrs={"class": "video-container"}).find("iframe").attrs[
                                       "src"])

        return render(request, 'blog/post_detail.html', {'detail': p_detailed})

    else:
        gcon = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        page = urllib.request.urlopen("https://nba.udn.com/nba/index?gr=www", context=gcon)
        soup = BeautifulSoup(page, "html.parser")
        name_box = soup.find("div", attrs={"class":"box_body"})
        big_box = name_box.find("dt",attrs={"class":"big"})
        all_box = name_box.find_all("dt")

        fil = Post.objects.filter(big=1)
        if len(fil) > 0:
            get_o = Post.objects.get(big=1)
            if get_o.title == big_box.find("h3").text:
                for obj in all_box:
                    get_o1 = Post.objects.get(title=obj.find("h3").text)
                    get_o1.created_time = obj.find("b").text
                    get_o1.save()
            else:
                Post.objects.all().delete()

        fil = Post.objects.filter(big=1)
        if len(fil) == 0:
            for obj in all_box:
                Post.objects.create(created_time = obj.find("b").text,
                                    title =        obj.find("h3").text,
                                    text =         obj.find("p").text,
                                    detailed =     "https://nba.udn.com"+obj.find("a").attrs["href"],
                                    picture =      obj.find("img").attrs["src"].split("&")[0],
                                    big =          len(obj.attrs))



        posts = Post.objects.filter(created_time__isnull=False).order_by('created_time')
        return render(request, 'blog/post_list.html', {'posts': posts})

