import requests
import crawler

def test_get_content(requests_mock):
  requests_mock.get("https://www.yoyowallet.com/", content=b"html dom properties")
  assert crawler.get_content('https://www.yoyowallet.com/') == "html dom properties".encode()

def test_get_href():
  html_href = """<!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
    </head>
    <body>
      <a href="/retailers/index.html">BBC News</a>
    </body> 
  </html>"""
  html_no_href = """<!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
      <title>title</title>
    </head>
    <body>
      <img src="https://unsplash.com/photos/8uXthE3xeBI"  alt="mountains"  />
    </body> 
  </html>"""
  assert crawler.get_href(html_href) == ["/retailers/index.html"]
  assert crawler.get_href(html_no_href) == []

def test_get_other_assets():  
  html_no_other_assets = """<!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
    </head>
    <body>
      <a href="/retailers/index.html">BBC News</a>
    </body> 
  </html>"""
  html_other_assets = """<!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
      <link rel="stylesheet" type="text/css" href="theme.css">
      <script src="myscripts.js"></script>
    </head>
    <body>
      <img src="https://unsplash.com/photos/8uXthE3xeBI"  alt="mountains"  />
    </body> 
  </html>"""
  assert crawler.get_other_assets(html_other_assets) == ["stylesheet", "myscripts.js", "https://unsplash.com/photos/8uXthE3xeBI"]
  assert crawler.get_other_assets(html_no_other_assets) == []


def test_get_html():
  html_sample = """<!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
      <link rel="stylesheet" type="text/css" href="theme.css">
      <script src="myscripts.js"></script>
    </head>
    <body>
      <img src="https://unsplash.com/photos/8uXthE3xeBI"  alt="mountains"  />
       <a href="/retailers/index.html">BBC News</a>
    </body> 
  </html>"""
  assert crawler.get_html(html_sample) == {
    "href": ["/retailers/index.html"],
    "other": ["stylesheet", "myscripts.js", 
    "https://unsplash.com/photos/8uXthE3xeBI"], 
    "all": ["/retailers/index.html", "stylesheet", "myscripts.js", "https://unsplash.com/photos/8uXthE3xeBI"]
    }

def test_get_root_url():
  page_to_crawl = "https://www.yoyowallet.com/"
  assert crawler.get_root_url(page_to_crawl) == "yoyowallet.com"

def test_clean_links():
  all_links = [
    '/retailers/index.html', 
    '/caterers/index.html', 
    '/banks/index.html', 
    'https://blog.yoyowallet.com/', 
    'https://support.yoyowallet.com/hc/en-gb/categories/200398989-Help-Centre', 
    '/careers.html', 
    '/assets.html', 
    'https://support.yoyowallet.com/hc/en-gb/categories/201132913-Legal-and-T-Cs', 
    '/', 
    'http://www.twitter.com/yoyowallet', 
    'http://www.facebook.com/yoyowallet', 
    'https://www.linkedin.com/company/yoyo-wallet'
    ]
  cleaned_links = {
    '/retailers/index.html', 
    '/assets.html',
    '/banks/index.html',
    '/careers.html', 
    '/', 
    '/caterers/index.html'
    }
  assert crawler.clean_links(all_links) == cleaned_links


def test_crawl():
  sitemap = [
    '/',
    '/about.html',
    '/assets.html',
    '/banks/index.html',
    '/basket-data.html', 
    '/careers.html', 
    '/case-studies/caffe-nero-case-study.html', 
    '/caterers/index.html', 
    '/cookies.html', 
    '/epos.html', 
    '/get-in-touch.html', 
    '/reports/caterers-report.html', 
    '/retailers/index.html'
    ]
  page_to_crawl = "https://www.yoyowallet.com/"
  assert crawler.crawl(page_to_crawl)['sitemap'] == sitemap