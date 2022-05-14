from bs4 import BeautifulSoup
import requests
import os

# Customize your categories here. Add and remove
#Web developer languages
#categories = ["html", "css", "js", "jquery", "nodejs", "bootstrap4", "php", "sql", "mysql", "java", "kotlin", "python", "cpp", "cs"]

#App developer languages
# categories = ["java", "kotlin", "python", "cpp", "cs"]

#categories = ['react', 'typescript', 'angular', 'c']

#categories = ['bootstrap5', 'django']

#categories = ['icons', 'colors', 'howto']
categories = ['django', 'r']


baseurl = "https://www.w3schools.com/"


# Gets html response
def get_htmlstring(url):
	response = requests.get(url)
	return response.text

# Gets all required links outputs as an array
def get_links(categ):
	url = baseurl+categ
	html_string = get_htmlstring(url)
	soup = BeautifulSoup(html_string, "html.parser")
	links = []
	for div in soup.findAll('div', attrs={'id':'leftmenuinnerinner'}):
		for link in div.findAll('a', attrs={"target":"_top"}):
			links.append(link.get('href'))
	return links

# Does some replacements
def get_replaced_string(html_string):
	fav_replaced = html_string.replace("/favicon", "../favicon")
	lib_replaced = fav_replaced.replace("/lib/", "../lib/")
	img_replaced = lib_replaced.replace("/images", "../images")
	php_replaced = img_replaced.replace(".php", ".html")
	asp_replaced = php_replaced.replace(".asp", ".html")
	top_links_replaced = asp_replaced.replace("href='/", "href='../")
	top_links_replaced2 = top_links_replaced.replace("""href="/""", """href="../""")
	jq_replaced = top_links_replaced2.replace("https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js", "../lib/jquery.min.js")
	footer_replaced = jq_replaced.replace("w3schools_footer.js?update=20210902", "w3schools_footer.js")
	loader_replaced = footer_replaced.replace("my-learning.js?v=1.0.2", "my-learning.js")
	cdn_replaced = loader_replaced.replace("https://cdn.snigelweb.com/adengine/w3schools.com/loader.js", "../lib/loader.js")
	return cdn_replaced

# Saves html pages into some folder
def save_page(replaced_string, link, categ):
	try:
		fname = link.split(".")[0] + ".html"
		if not os.path.exists(categ):
		    os.makedirs(categ)
		f = open(f"{categ}/{fname}", "w", encoding='utf-8')
		f.write(replaced_string)
		f.close()
	except Exception as e:
		print(e)
		pass
	


# default func
def run():

	for categ in categories:
		links = get_links(categ)
		print(f"Now scrapping {categ}...")
		for link in links:
			page_url = baseurl + categ +"/"+ link
			print(page_url)
			html_string = get_htmlstring(page_url)
			replaced_html = get_replaced_string(html_string)
			save_page(replaced_html, link, categ)
		print("Scrapping completed!")

if __name__ =="__main__":
	run()
