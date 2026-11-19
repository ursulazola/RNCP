import pandas as pd
import sqlite3
import json
import requests
from bs4 import BeautifulSoup


def extract():

  conn = sqlite3.connect("bookworld_reference.db")
  df_channels = pd.read_sql_query("SELECT channel_code, channel_name, acquisition_cost_gbp FROM channels WHERE is_active=1", conn)
  df_countries = pd.read_sql_query("SELECT * FROM countries", conn)
  df_category_rules = pd.read_sql_query("SELECT category_name, margin_rate, strategic_flag FROM category_rules WHERE is_active=1", conn)
  conn.close()

  df_orders = pd.read_csv("base_de_données_bookworld.csv")


#Partie du code  afin de récupérer les infos sur les livres  :

  try:
      page_principale = requests.get("https://books.toscrape.com/")
      soup = BeautifulSoup(page_principale.content, "html.parser")
      groupes = soup.find_all('li',{"class" : "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
      #Liste de chaque lien des livres de la première page
      liste_liens = []
      for i in range(len(groupes)):
        lien = groupes[i].find("a", href = True, title = True)["href"]
        liste_liens.append("https://books.toscrape.com/"+lien)

      #Scraping sur les liens de chaque livre de la première page

      dictionnaire = {"book_name" : [],
              "price" : [],
              "stock" : [],
              "note" : [],
              "category_name" : []}
      for j in liste_liens :

        page_livre = requests.get(j)
        soup_livre = BeautifulSoup(page_livre.content, "html.parser")

        #Titre
        titre = soup_livre.find('div',{"class" : "col-sm-6 product_main"}).find("h1").get_text()
        dictionnaire["book_name"].append(titre)

        #Prix
        price = soup_livre.find('p',{"class" : "price_color"}).get_text()
        dictionnaire["price"].append(price)

        #Stock
        stock = soup_livre.find('p',{"class" : "instock availability"}).get_text().strip()
        dictionnaire["stock"].append(stock)

        #Note
        note = soup_livre.find("p", class_="star-rating").get("class")[1]
        dictionnaire["note"].append(note)

        #Genre
        genre_search = soup_livre.find("ul", {"class" : "breadcrumb"})
        genre = genre_search.find_all("li")[2].get_text().strip()
        dictionnaire["category_name"].append(genre)

      df_books_scrap = pd.DataFrame(dictionnaire)

  except ValueError as erreur :
      print(f"Echec de la requête sur le book scraping.\n Statuts code première requête : {page_principale.status_code} \n Status code seconde requête : {page_livre.status_code}\n Erreur : {erreur} ")


#Partie du code  afin de récupérer les données de l'API Frankfurter :

  try:


      df_date_orders = df_orders.groupby("order_date").agg(nb_dates=("order_date","count"))
      df_date_orders.reset_index(drop=False,inplace =True)



      dictionnaire2 = {"order_date" : [],
          "exchange_rate" : []}
      for date in df_date_orders["order_date"]:

        base_url = f"https://api.frankfurter.dev/v2/rates?base=gbp&quotes=eur&date={date}"

        response = requests.get(base_url,timeout=30)

        api_reponse = response.json()
        dictionnaire2["order_date"].append(date)
        dictionnaire2["exchange_rate"].append(api_reponse[0]["rate"])
      df_exchange_rate = pd.DataFrame(dictionnaire2)

  except ValueError as erreur:
      print(f"Echec de la requête de l'API Frankfurter.\n Statuts code requête : {response.status_code} \n Erreur : {erreur}")

  return df_channels,df_countries,df_category_rules,df_orders,df_books_scrap,df_exchange_rate

def transform():


  liste_df = extract()
  df_channels = liste_df[0]
  df_countries = liste_df[1]
  df_category_rules = liste_df[2]
  df_orders = liste_df[3]
  df_books_scrap = liste_df[4]
  df_exchange_rate = liste_df[5]

                                                                #df_countries

  df_countries.rename(columns={"is_active": "country_is_active"},inplace = True)

                                                                  #df_orders
  # Conversion en date de la colonne order_date de df_orders
  df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])

  # Conversion en date de la colonne order_date de df_orders
  df_exchange_rate["order_date"] = pd.to_datetime(df_exchange_rate["order_date"])

                                                              #df_book_scrap

  #Conversion de la colonne prix en float

  df_books_scrap["price"] = df_books_scrap["price"].str.replace("£","")
  df_books_scrap["price"] = df_books_scrap["price"].astype(float)
  df_books_scrap.rename(columns={"price": "price_gbp"},inplace = True)


  #Conversion de la colonne stock en int

  df_books_scrap["stock"] = df_books_scrap["stock"].str.replace("In stock (","").str.replace(" available)","")
  df_books_scrap["stock"] = df_books_scrap["stock"].astype(int)

  #Conversion de la colonne note en int
  notes = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
  df_books_scrap["note"] = df_books_scrap["note"].map(notes).astype(int)


  #Modification des genres des livres afin de match ceux de la table category_rules

  livres_categories = {
      "Shakespeare's Sonnets": "Classics",
      "Olio": "Historical Fiction",
      "The Black Maria": "Historical Fiction",
      "The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull": "Historical Fiction",
      "The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics": "Nonfiction",
      "Sapiens: A Brief History of Humankind": "Nonfiction",
      "Our Band Could Be Your Life: Scenes from the American Indie Underground, 1981-1991": "Nonfiction",
      "Rip it Up and Start Again": "Nonfiction",
      "Libertarianism for Beginners": "Nonfiction",
      "Starving Hearts (Triangular Trade Trilogy, #1)": "Romance",
      "Soumission": "Science Fiction",
      "A Light in the Attic": "Young Adult",
      "Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)": "Young Adult",
    }

  df_books_scrap["category_name"] = df_books_scrap["book_name"].map(livres_categories).fillna(df_books_scrap["category_name"])
  #Fusion de df_books_scrap et df_category_rules

  df_books_scrap_category = (df_books_scrap
                .merge(df_category_rules, on="category_name", how="left"))

  #Fusion des dataframes
  df = (df_orders
                .merge(df_books_scrap_category, on="book_name", how="left")
                .merge(df_channels, on="channel_code", how="left")
                .merge(df_countries, on="country_code", how="left")
                .merge(df_exchange_rate, on="order_date", how="left"))


                                                                #Nettoyage des valeurs NAN dans df
                                                        #Remplissage des valeurs NAN pour les Pays - Bas

  df.loc[df["country_code"] == "NL", "country_name"] = df.loc[df["country_code"] == "NL", "country_name"].fillna("The Netherlands")
  df.loc[df["country_code"] == "NL", "currency_code"] = df.loc[df["country_code"] == "NL", "currency_code"].fillna("EUR")
  df.loc[df["country_code"] == "NL", "vat_rate"] = df.loc[df["country_code"] == "NL", "vat_rate"].fillna(21.0)
  df.loc[df["country_code"] == "NL", "region"] = df.loc[df["country_code"] == "NL", "region"].fillna("Europe")
  df["country_is_active"] = df["country_is_active"].astype("object")
  df.loc[df["country_code"] == "NL", "country_is_active"] = df.loc[df["country_code"] == "NL", "country_is_active"].fillna("inconnu")


  #Le discount est pris en compte avant le calcul du revenu

  df["price_gbp_HT_with_discount"] = df["price_gbp"]*(1-df["discount_rate"])

  df["price_eur_HT_with_discount"] =  (df["price_gbp_HT_with_discount"]*df["exchange_rate"])


  # Calcul du revenu total en pounds par commande, TVA non prise en compte car elle n'est pas censée être  incluse dans le calcul du chiffre d'affaires
  df["total_revenue_gbp"] = round(df["quantity"]*df["price_gbp_HT_with_discount"],2)

  # Calcul du revenu total en euro par commande, TVA non prise en compte car elle n'est pas censée être inclus dans le calcul du chiffre d'affaires
  df["total_revenue_eur"] = round(df["quantity"]*df["price_eur_HT_with_discount"],2)


  #Afin de calculer le bénéfice on multiplie le prix par la différence entre margin rate et discount rate puis par la quantité puis on soustrait le coût d'acquisition



  df["profit_total_gbp"] = round(
                            (df["price_gbp"]
                            * (df["margin_rate"] - df["discount_rate"])
                            * df["quantity"]
                            )-df["acquisition_cost_gbp"]
                            ,2)


  df["profit_total_eur"] = round(
                            (df["price_gbp"]
                            * df["exchange_rate"]
                            * (df["margin_rate"]-df["discount_rate"])
                            * df["quantity"]
                            )-(df["acquisition_cost_gbp"]*df["exchange_rate"])
                            ,2)


  #Agrégation sales_country

  df_sales_by_country = df.groupby(["country_code","country_name"]
                                ).agg(total_orders =("order_id","count")
                                ,total_quantity =("quantity","sum")
                                ,total_revenue_gbp=("total_revenue_gbp","sum")
                                ,profit_total_gbp=("profit_total_gbp","sum")
                                ,total_revenue_eur=("total_revenue_eur","sum")
                                ,profit_total_eur=("profit_total_eur","sum")
                                ).sort_values("profit_total_eur", ascending=False).reset_index()

  df_sales_by_category = df.groupby("category_name"
                                ).agg(total_orders =("order_id","count")
                                ,total_quantity =("quantity","sum")
                                ,total_revenue_gbp=("total_revenue_gbp","sum")
                                ,profit_total_gbp=("profit_total_gbp","sum")
                                ,total_revenue_eur=("total_revenue_eur","sum")
                                ,profit_total_eur=("profit_total_eur","sum")
                                ).sort_values("profit_total_eur", ascending=False).reset_index()

  df_sales_by_country = df_sales_by_country.round(2)
  df_sales_by_category = df_sales_by_category.round(2)


  #RGPD supression des noms et prénoms de df_orders_final et df_orders
  df_name = df[["customer_first_name","customer_last_name"]].drop_duplicates().reset_index(drop=True)
  df_name["id_client"] = [f"id{i+1}" for i in range(len(df_name))]

  df_orders = df_orders.merge(df_name, on=["customer_first_name","customer_last_name"], how="left")
  df_orders = df_orders.drop(["customer_first_name","customer_last_name"], axis=1)

  df_orders_final = df.merge(df_name, on=["customer_first_name","customer_last_name"], how="left")
  df_orders_final = df_orders_final.drop(["customer_first_name","customer_last_name"], axis=1)

  dataframes = {
        "df_orders_final": df_orders_final,
        "df_sales_by_country": df_sales_by_country,
        "df_sales_by_category": df_sales_by_category,
        "df_books_scrap_category": df_books_scrap_category,
        "df_channels": df_channels,
        "df_countries": df_countries,
        "df_exchange_rate": df_exchange_rate
    }

  return dataframes

def load():
    dataframes = transform()
    df_orders_final = dataframes["df_orders_final"]
    df_sales_by_country = dataframes["df_sales_by_country"]
    df_sales_by_category = dataframes["df_sales_by_category"]
    df_books_scrap_category = dataframes["df_books_scrap_category"]
    df_channels = dataframes["df_channels"]
    df_countries = dataframes["df_countries"]
    df_exchange_rate = dataframes["df_exchange_rate"]


    conn = sqlite3.connect("tables_finales.db")

    df_orders_final.to_sql(
        "orders_final",
        conn,
        if_exists="replace",
        index=False
    )
    df_sales_by_country.to_sql(
        "sales_by_country",
        conn,
        if_exists="replace",
        index=False
    )
    df_sales_by_category.to_sql(
        "sales_by_category",
        conn,
        if_exists="replace",
        index=False
    )
    df_books_scrap_category.to_sql(
        "books_scrap_category",
        conn,
        if_exists="replace",
        index=False
    )
    df_channels.to_sql(
        "channels",
        conn,
        if_exists="replace",
        index=False
    )
    df_countries.to_sql(
        "countries",
        conn,
        if_exists="replace",
        index=False
    )
    df_exchange_rate.to_sql(
        "exchange_rate",
        conn,
        if_exists="replace",
        index=False
    )

    df_head = pd.read_sql_query("SELECT * FROM orders_final LIMIT 5", conn)
    columns_df = pd.read_sql_query("PRAGMA table_info(orders_final)", conn)

    print("\nAperçu des données enregistrées de la table principale :")
    print(df_head)

    print("\nColonnes de la table :")
    print(columns_df[["name", "type"]])

    print("\n=== Ventes par pays ===")
    print(dataframes["df_sales_by_country"])

    print("\n=== Ventes par genre ===")
    print(dataframes["df_sales_by_category"])
    conn.close()


if __name__ == "__main__":
    load()