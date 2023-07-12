import requests
from bs4 import BeautifulSoup

# Obtener el contenido HTML de la página web
wikiurl = "https://tibia.fandom.com/wiki/Main_Page"
response = requests.get(wikiurl)
html_content = response.text

# Crear un objeto BeautifulSoup para analizar el contenido HTML
soup = BeautifulSoup(html_content, "html.parser")
# Encontrar el elemento con la clase "compact-box compact-box-boss no-pseudoelements-container"
elemento = soup.find("div", class_="compact-box compact-box-boss no-pseudoelements-container")
# Obtener el título
boss_name = elemento.find("b").text.strip()
#Hp **************
hp_span = elemento.find("span", class_="creature-stats-hp")
hp_value = hp_span.find("span", class_="tibiatext").text
# Exp******************
exp_span = elemento.find("span", class_="creature-stats-exp")
exp_value = exp_span.find("span", class_="tibiatext").text
# obtener Imagen ******************
image_span = elemento.find("span", class_="no-pseudoelements-container")
boss_img = image_span.find("img")["data-src"]
print(boss_name)
print(boss_img)
print(hp_value, " ", exp_value)