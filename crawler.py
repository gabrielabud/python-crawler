import requests
import re

def get_content(page):
  try:
    response = requests.get(page)
    if not str(response.status_code).startswith("4"):
      return (response.content)
    return None
  except: 
    return None

def get_href(html_dom):
  return re.findall(r'<a href="(.*?)"', html_dom)

def get_other_assets(html_dom):
  return re.findall(r'<(?:img src|link rel|script src)="(.*?)"', html_dom)
  
def get_html(content):
  output = {}
  if content: 
    output['href'] = get_href(str(content))
    output['other'] = get_other_assets(str(content))
    output['all'] = output['href'] + output['other']
    return output
  return []

def get_root_url(page):
  get_root_url = re.findall(r"^https?:\/\/[w\d.]*([\S][^\/]+)", page)
  if get_root_url:
      return get_root_url[0]

def clean_links(html_links):
  root_url =  get_root_url(page_to_crawl)
  clean_links = set()
  for value in html_links:
      link_root  = get_root_url(value)
      if link_root == root_url \
      or not link_root \
      and not value.startswith(("#","/#", "mailto:", "tel:")) \
      and not value.endswith(".zip") \
      and value not in clean_links:
        clean_links.add(value)
  return clean_links


def crawl(page, all_links = set(), assets = {} ):
  html_elements = get_html(get_content(page))
  links = clean_links(html_elements['href'])  
  assets[page] = html_elements['all']
  if not links.issubset(all_links):
    all_links.update(links)
    for link in links:
      crawl(page_to_crawl+link[1:], all_links, assets)
  return { "sitemap": sorted(all_links), "mapped_assets": assets }

page_to_crawl = "https://www.yoyowallet.com/"
results = crawl(page_to_crawl)
print("sitemap",results['sitemap'])
print("assets", results["mapped_assets"][page_to_crawl])

def print_assets_to_page(results):
  for link in results["sitemap"]:
    print(link+" has the following assets:")
    print("--------------------------------")
    for elem in results["mapped_assets"][page_to_crawl+link[1:]]:
      print(elem)
      print()

print_assets_to_page(results)

