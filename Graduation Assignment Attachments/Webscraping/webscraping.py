import requests 
from bs4 import BeautifulSoup
import pandas as pd


# 1. Retrieve the URLs for Nutri-Scored categories from the Albert Heijn website
# Base URL broad categories
b_c_base_url = "https://www.ah.nl/producten"
all_pages = "&page=10"


# Lists for the broad product categories.  
# WARNING: Loop seperately in order to prevent rejections from ah.nl

list_req_b_cat = ["/salades-pizza-maaltijden", "/kaas-vleeswaren-tapas", "/zuivel-plantaardig-en-eieren", "/bakkerij-en-banket", ]
list_req_b_cat = ["/ontbijtgranen-broodbeleg-tussendoor", ]
list_req_b_cat = ["/ontbijtgranen-broodbeleg-tussendoor", "/pasta-rijst-en-wereldkeuken", "/soepen-sauzen-kruiden-olie", "/snoep-koek-chips-en-chocolade"  ]
list_req_b_cat = ["/snoep-koek-chips-en-chocolade"]
list_req_b_cat = ["/aardappel-groente-fruit", "/salades-pizza-maaltijden", "/kaas-vleeswaren-tapas", "/zuivel-plantaardig-en-eieren", "/bakkerij-en-banket", "/ontbijtgranen-broodbeleg-tussendoor", "/pasta-rijst-en-wereldkeuken", "/soepen-sauzen-kruiden-olie", "/snoep-koek-chips-en-chocolade"  ]
all_req_b_cat = []

# Lists for the smaller product categories, only with Nutri-Scores 
list_req_ns_cats = ["?kenmerk=nutriscore%3Aa", "?kenmerk=nutriscore%3Ab", "?kenmerk=nutriscore%3Ac", "?kenmerk=nutriscore%3Ad", "?kenmerk=nutriscore%3Ae"]
all_req_ns_cats = []

# 1.1 Retrieve broad product categories 
for c in range(len(list_req_b_cat)):
    all_cats = str(b_c_base_url + list_req_b_cat[c])
    all_req_b_cat.append(all_cats)

    # 1.2 Retrieve Nutri-Score labelled produtcs
    for n in range(len(list_req_ns_cats)):
        all_ns = all_req_b_cat[c] + list_req_ns_cats[n] + all_pages
        all_req_ns_cats.append(all_ns)
# 1.3 List of all Nutri-Scored labelled categories
ns_cat = all_req_ns_cats

# 2. Retrieve the URLs for each Nutri-Scored product fro the Albert Heijn website
# List for each product 
list_products = []

# Lists for the information of each product
list_info_p = []

# Create BeautifulSoup for retrieving information of each product
# Base URL for products from AH
main_URLs = [] 

for u in range(len(ns_cat)):
    URLs = ns_cat[u]
    main_URLs.append(URLs)

p_base_URL = "https://www.ah.nl"

# List for each product URL
list_p_URL = []
all_p_URLs = []
    
for r in main_URLs:
    page = requests.get(r)
    soup = BeautifulSoup(page.content, "html.parser")

    for the_product_URL in soup.find_all("a", class_="link_root__65rmW", href=True):
        URL = the_product_URL["href"]
        list_p_URL.append(URL)

        for p in range(len(list_p_URL)):
            p_URL = p_base_URL + list_p_URL[p]
            all_p_URLs.append(p_URL)

# Remove duplicates
all_p_URLs = list(dict.fromkeys(all_p_URLs))

# 3. Get the data for every product
list_title = []
list_prices = []
list_nutriscore = []
list_descr = []
list_allergies = []
list_nutrients = []
list_labels = []

for all_s in all_p_URLs:
    # Connect to BeautifulSoup HTML parser
    page = requests.get(all_s)
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the product titles
    titles = soup.find("h1").text
    list_title.append(str(titles))
    print(titles)
        # Get the product prices

    # try: 
    #     prices = soup.find(class_="price-amount_root__37xv2").text
    #     list_prices.append(str(prices))   
    # except:
    #     pass
    
        # list_prices.append(str(prices))

    # Get the Nutri-Score
    nutriscore = soup.find(class_="nutriscore_root__cYcXV").text
    nutriscore = nutriscore.replace("Wat is Nutri-Score?", "")
    list_nutriscore.append(nutriscore)

    # Get the short descrption (if not exsist: ignore)
    # try:
    #     descr = soup.find(class_="product-info-description_list__MUNdA").text
    #     list_descr.append(descr)
    # except: 
    #     pass


    
    # Get the labels (if not exsist: ignore)
for l in range(len(list_title)):
    for e in l: 
        for labels in soup.find_all(class_="product-info-icons_name__3VAUu"):
            list_labels.append(labels.text)

    

    # # Get the allergies (if not exsist: ignore)

    # for allergies in soup.find_all(class_="product-info-definition-list_value__kspp6"):
    #  list_allergies.append(allergies)
  

    # Get the nutrients (if not exsist: ignore))
    # try:
    #     nutrients = soup.find(class_="product-info-nutrition_table__1PDio").text
    #     list_nutrients.append(nutrients)
    # except:
    #     pass

product_titles = list_title
product_prices = list_prices
product_ns = list_nutriscore
product_descr = list_descr
product_nutrients = list_nutrients
product_labels = list_labels
product_allergies = list_allergies




# 4. Create DF
d = {"Title": product_titles,"Nutri-Score": product_ns, "Labels": product_labels}
# Ultimately: d = {"Title": product_titles,"Nutri-Score": product_ns, "Description": product_descr, "Price": product_prices, "Labels": product_labels, "Nutrients": product_nutrients}

# Accept arrays are not the same length (2 products are off, these are removed in the xlsx sheet afterwards)
df = pd.DataFrame.from_dict(d, orient="index")
df = df.transpose()

# Drop duplicates
df.drop_duplicates(subset="Title", keep = False, inplace = True)
print(df)

# 5. Create Excel output
df.to_excel("ah_products_first_version.xlsx")