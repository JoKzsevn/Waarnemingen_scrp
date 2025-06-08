from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

inheemse_planten = [
    "Duizendblad",
    "Wilde bertram",
    "Kruipend zenegroen",
    "Bieslook",
    "Echte heemst",
    "Gewone ossentong",
    "Bosanemoon",
    "Grote engelwortel",
    "Gele kamille",
    "Fluitenkruid",
    "Wondklaver",
    "Wilde akelei",
    "Engels gras",
    "Stinkende ballote",
    "Bevertjes",
    "Gewone dotterbloem",
    "Prachtklokje",
    "Akkerklokje",
    "Grasklokje",
    "Ruigklokje",
    "Knoopkruid",
    "Grote centaurie",
    "Wilde cichorei",
    "Bosrank",
    "Borstelkrans",
    "Ruwe smele",
    "Kartuizer anjer",
    "Steenanjer",
    "Vingerhoedskruid",
    "Grote kaardebol",
    "Voorjaarszonnebloem",
    "Slangenkruid",
    "Moerasspirea",
    "Knolspirea",
    "Grote bosaardbei",
    "Bosaardbei",
    "Lievevrouwebedstro",
    "Geel walstro",
    "Donkere ooievaarsbek",
    "Beemdooievaarsbek",
    "Knikkend nagelkruid",
    "Oranje havikskruid",
    "Muizenoor",
    "Sint-janskruid",
    "Beemdkroon",
    "Hartgespan",
    "Gewone margriet",
    "Vlasbekje",
    "Gewone rolklaver",
    "Grote wederik",
    "Grote kattenstaart",
    "Vijfdelig kaasjeskruid",
    "Muskuskaasjeskruid",
    "Middelste teunisbloem",
    "Wilde marjolein",
    "Adderwortel",
    "Grote bevernel",
    "Gewone salomonszegel",
    "Slanke sleutelbloem",
    "Gulden sleutelbloem",
    "Gewone brunel",
    "Gevlekt longkruid",
    "Veldsalie",
    "Kleine pimpernel",
    "Grote pimpernel",
    "Zeepkruid",
    "Duifkruid",
    "Knopig helmkruid",
    "Dagkoekoeksbloem",
    "Echte koekoeksbloem",
    "Avondkoekoeksbloem",
    "Nachtsilene",
    "Blaassilene",
    "Echte guldenroede",
    "Betonie",
    "Bosandoorn",
    "Blauwe knoop",
    "Gewone smeerwortel",
    "Boerenwormkruid",
    "Valse salie",
    "Grote tijm",
    "Echte valeriaan",
    "Zwarte toorts",
    "Brede ereprijs",
    "Gewone ereprijs",
    "Lange ereprijs",
    "Mannetjesereprijs",
    "Maarts viooltje",
    "Spaanse aak / Veldesdoorn",
    "Zwarte els",
    "Berberis / Zuurbes",
    "Ruwe Berk",
    "Zachte berk",
    "Haagbeuk",
    "Wilde clematis / Bosrank",
    "Gele kornoelje",
    "Rode kornoelje",
    "Hazelaar",
    "Tweestijlige meidoorn",
    "Eenstijlige meidoorn",
    "Brem",
    "Kardinaalsmuts",
    "Beuk",
    "Gewone es",
    "Duindoorn",
    "Hulst",
    "Wilde liguster",
    "Wilde kamperfoelie",
    "Wilde appel",
    "Wilde mispel",
    "Zwarte populier",
    "Zoete kers / Boskriek",
    "Inheemse vogelkers",
    "Sleedoorn",
    "Wintereik",
    "Zomereik",
    "Wegedoorn",
    "Sporkehout / Vuilboom",
    "Zwarte bes",
    "Aalbes",
    "Kruisbes",
    "Hondsroos",
    "Heggenroos",
    "Egelantier",
    "Schietwilg",
    "Geoorde wilg",
    "Boswilg",
    "Grauwe wilg",
    "Kraakwilg",
    "Laurierwilg",
    "Bittere wilg",
    "Amandelwilg",
    "Katwilg",
    "Gewone Vlier",
    "Lijsterbes",
    "Venijnboom",
    "Winterlinde",
    "Zomerlinde",
    "Gelderse Roos"
]


# Selenium instellingen
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Resultatenlijst
results = []

# Basis-URL
base_url = "https://waarneming.nl"

try:
    # Startpagina openen
    driver.get(base_url)
    time.sleep(2)

    for term in inheemse_planten:
        print(f"\n🔍 Zoeken naar: {term}")

        try:
            # Zoekbalk openen
            search_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "js-navbar-search-button"))
            )
            search_button.click()

            # Zoekveld invullen
            search_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.app-navbar-search-input"))
            )
            search_input.clear()
            search_input.send_keys(term)
            search_input.send_keys(Keys.ENTER)

            # Wacht op <li class="lead"> link naar soort
            species_link = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.lead > a[href^='/species/']"))
            )
            species_link.click()

            # Titel en URL ophalen
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "title"))
            )
            current_url = driver.current_url
            full_title = driver.title.strip()

            # Wetenschappelijke naam extraheren uit de title
            try:
                parts = full_title.split(" - ")
                scientific_name = parts[1].split(" |")[0].strip() if len(parts) > 1 else full_title
            except:
                scientific_name = full_title

            print(f"✅ Geopend: {scientific_name} | {current_url}")

            results.append({
                "Nederlandse naam": term,
                "Pagina titel": scientific_name,
                "URL": current_url
            })

        except Exception as e:
            print(f"⚠️ Fout bij '{term}':", e)
            results.append({
                "Nederlandse naam": term,
                "Pagina titel": "Niet gevonden",
                "URL": "Niet gevonden"
            })

        # Alleen terug naar homepage als de sessie nog geldig is
        try:
            driver.get(base_url)
            time.sleep(2)
        except:
            print("❌ Kan niet terugkeren naar homepage, sessie is ongeldig.")
            break

finally:
    # Sluit browser netjes af
    driver.quit()

# DataFrame bouwen
df = pd.DataFrame(results)
print("\n📋 Resultaten:")
print(df)

df['Id'] = df['URL'].apply(lambda x: x.rstrip('/').split('/')[-1] if x != "Niet gevonden" else None)
df
