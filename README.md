Les instructions et le code ont été fait via un PC Windows.

## I. Introduction

L’objectif du projet est de construire un pipeline de données permettant de :
  1. Collecter les données depuis des différentes sources ;
  2. Produire un jeu de données final propre et cohérent;
  3. Créer une base SQL finale exploitable ;
  4. Exposer via une API un/des indicateur(s) métier simple(s) 

## II. Installer les dépendances

  1. Récupérer les fichiers depuis GitHub
  2. Après les avoir récupérés, placer les dans un dossier qu'on nommera par exemple `RNCP`.
  3. Ouvrir le terminal de l'ordinateur.
  4. A partir du terminal, accéder au dossier `RNCP`. A partir du chemin du terminal : exécuter `cd RNCP`. Vous êtes à présent dans le dossier  `RNCP` et vous pouvez exécuter ce code : `pip install -r requirements.txt`.

## III. Exécuter le pipeline

Cette étape doit être réalisée avant le lancement de l'API.

  ### Comment exécuter le pipeline :

  1. Vérifier que `base_de_données_bookworld.csv` et `bookworld_reference.db` sont dans le dossier `RNCP` avant de lancer le pipeline. 
  2. Aller dans le terminal, accéder au dossier `RNCP` sur le terminal puis exécuter  le fichier `pipeline` (`python pipeline.py`).
  3. Le rendu sera un fichier `tables_finales.db`.

## IV. Lancer l’API

  ### A. Créer le fichier .env 
  
  Afin d'exécuter l'api, il faut d'abord créer le fichier `.env` dans le dossier `RNCP` contenant le projet :

  - Le fichier .env sert à stocker la clé API  en dehors du code, elle permettra à accéder aux données
    via le terminal sans la copier pour des raisons de sécurité. La clé API sert à protéger l'accès à l'API.

  - Le fichier .env.example que vous trouverez dans le dossier sert d'exemple au fichier env. Vous pouvez l'utiliser comme modèle afin de créer le contenu du fichier .env. Vous devrez placer au lieu de `Saisir_la_clé_API` votre mot de passe qui sera la clé API. Faites attention à ne pas placer d'espaces avant ou après le =.
  
  ### B. Lancer l'API 
  
  Une fois la pipeline lancée et le fichier `.env` créé, l'API se lance avec la commande `python api.py` dans le terminal. Ne pas oublier d'exécuter la commande dans le dossier `RNCP` via le terminal.
  Si succès le code suivant s'affiche :

    * Serving Flask app 'api'
    * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on http://127.0.0.1:5000
    Press CTRL+C to quit

L'API est lancée mais on ne peut pas encore afficher les données dans le terminal, l'authentification via la clé API est nécessaire.
  
### Attention : Il faut impérativement laisser le code  tourner sur l'onglet où `python api.py` a été exécuté. Il ne faut donc pas pour l'instant cliquer sur CTRL+C. Si fait, relancer `python api.py`.


## V. Utiliser l’authentification par token afin d'exposer les données via une API en local

  ### A. Lire la clé API

  
  Afin d'exposer les données sur le terminal il faut :

  1. Ouvrir un nouvel onglet dans le terminal qu'on nommera "deux". Les manipulations suivantes se feront dans ce terminal. 


  2. Lire la clé du fichier .env et la charger comme variable d’environnement depuis le terminal "deux" :
    - Il faut exécuter dans le terminal "deux" la commande : 
    `$env:API_KEY = (Get-Content .env | Where-Object { $_-match '^API_KEY=' } | Select-Object -First 1) -replace '^API_KEY=', ''`
  
  3. Maintenant que la clé a été chargée les données seront disponibles  en local à l'adresse `http://127.0.0.1:5000` via  trois chemins d'accès (endpoints) :

    - `/health`, qui permet de vérifier si l'API fonctionne.
    - `/sales-by-country`, qui renvoie les ventes par pays.
    - `/sales-by-category`, qui renvoie les ventes par catégorie.
  
  4. Afin d’interroger l’API, en fonction de l’endpoint auquel on souhaite accéder, il faudra exécuter dans le terminal “deux” la commande :

    - Pour `/health` :
    `curl.exe -H "X-API-Key: $env:API_Key" http://127.0.0.1:5000/health`
    -  Pour `/sales-by-country`:
    `curl.exe -H "X-API-Key: $env:API_Key" http://127.0.0.1:5000/sales-by-country`
    - Pour `/sales-by-category`:
    `curl.exe -H "X-API-Key: $env:API_Key" http://127.0.0.1:5000/sales-by-category`
    
  ##### Les données sont affichées.

  5. Il faut maintenant exécuter ce code dans le terminal afin de retirer la variable API_KEY de son environnement (pour des raisons de sécurité) :

     - `Remove-Item Env:API_KEY`

## VI. Les principaux fichiers du projet :


1. Les fichiers d'entrée du pipeline : à placer dans le dossier `RNCP`, avec `pipeline.py`, avant de l'exécuter.
  - `base_de_données_bookworld.csv` : C'est le fichier CSV descriptif des commandes. 
  - `bookworld_reference.db` : C'est une base SQLite contenant les tables `category_rules` (données par genre de livre), `channels` (données par canal d'acquisition) et `countries` (données par pays).



2. `requirements.txt` : Il liste les bibliothèques Python nécessaires au projet (`flask`, `pandas`, `python-dotenv`, `requests` et `beautifulsoup4`). Elles s'installent avec la commande `pip install -r requirements.txt` (voir partie II).

3. `pipeline.py` :

Le fichier pipeline contient 3 fonctions afin d'obtenir tables_finales.db .

  - extract() qui permet de charger les tables depuis les bases de données fournies, de récupérer les données scrapées depuis `https://books.toscrape.com/` et récupérer les taux de change depuis de l'API publique Frankfurter.
  - transform() contient le nettoyage et la fusion des tables afin d'obtenir le dataframe final et les agrégations sales_by_country et sales_by_category.
  - load() : permet de convertir les dataframes en tables SQL, d'afficher la table principale et les agrégations.

4. `tables_finales.db`,c'est une base SQLite qui contient sept tables :
  - Une table factuelle : `orders` (données sur les commandes) qui une fois transformée et fusionnée avec les tables dimensionnelles est nommée `orders_final`.
  - Des tables dimensionnelles : `books_scrap_category` ( données scrapées des livres et les données par catégorie de livre), `countries` (Données par pays), `channels` (Données par canal d'acquisition),  et `exchange_rate` (Les taux de change par date).
  - Des tables des données agrégées : `sales_by_country` (revenus/bénéfices par pays) et `sales_by_category` (revenus/bénéfices par category).
  - Seules  `sales_by_country` et`sales_by_category` sont utilisées par l’API, pour les endpoints /sales-by-country et /sales-by-category.

5. `api.py` : Ce fichier est une API REST qui permet  d'exposer les données du fichier tables_finales.db. Elle propose trois endpoints présentés auparavant. Tous les endpoints sont protégés par une clé API. Les clés valides sont lues depuis la variable d’environnement API_KEY (fichier .env).

6. `queries.sql` : Ce fichier regroupe les requêtes SQL  nécessaires à la collecte des données depuis la base SQLite utilisées dans le projet.
  - Pour `pipeline.py` : la lecture des tables `channels` et `category_rules` (avec le filtre `is_active=1` et l'exclusion des colonnes `is_active`) et de la table `countries`.
  - Pour `api.py` : la lecture des tables `sales_by_country` et `sales_by_category`.

7. `schema_final.sql` : Ce fichier décrit la structure de la base finale `tables_finales.db` : les tables, leurs colonnes et leurs type de données, leurs clés primaires et leurs clés étrangères.
  - Il sert de documentation de la base finale, les tables étant créées par `pipeline.py`.

8. `.gitignore` sert à masquer les fichiers suivants lors de la publication sur GitHub :

    -  `.env` et tous les `.env.*`, mais pas `.env.example`.
    - `__pycache__/` et `*.pyc`, les fichiers générés par Python
    - `venv/` et `.venv/`, les environnements virtuels ;
    - `*.log`, les fichiers de logs ;
    - `.ipynb_checkpoints/`, les sauvegardes automatiques de notebooks ;
    - `.vscode/`, les réglages de l’éditeur.

9. `.env` : C'est le fichier, créé par l'utilisateur, qui contient la clé API réelle. Il est lu par `api.py` (variable `API_KEY`) et n'est pas publié sur GitHub, car il est masqué par le fichier `.gitignore`.

10. `.env.example` : C'est un modèle du fichier `.env`. Il contient la ligne `API_KEY=Saisir_la_clé_API`, qu'il faut recopier dans un fichier `.env` en remplaçant `Saisir_la_clé_API` par sa propre clé (voir partie IV.A). 


## VII. Utiliser l’authentification par clé SSH

Cette section est dédiée à l'utilisation de la clé SSH. Il est supposé que le dépot a été créé,que Git a été initialisé dans le projet et qu’au moins un commit a été effectué.

L'authentification SSH permet de prouver à GitHub que l'on a le droit de publier sur le dépôt, sans saisir de mot de passe à chaque `git push`.
  -  Indications : 
      Dans les commandes ci-dessous, remplacer `<username>` par votre nom d'utilisateur GitHub. 
      On suppose que le dépôt GitHub s'appelle aussi `RNCP`.

1. Aller dans le terminal, accéder au dossier `RNCP` et exécuter le code suivant dedans.

  2. Créer une clé SSH avec ce code :

    - `ssh-keygen -t ed25519 -C "votre_email@example.com"`
    - Appuyer sur Entrée pour toutes les questions (chemin par défaut, pas de mot de passe).

  3. Exécuter ce code dans le terminal afin de récupérer la clé SSH :
    - `cat ~/.ssh/id_ed25519.pub`

  4. Copier la clé affichée en entier (elle commence par `ssh-ed25519`).

  5. Ajouter la clé sur GitHub :

    - Aller sur : https://github.com/settings/keys
    - Cliquer sur `New SSH key`
    - Donner un titre à la clé, puis coller la clé
    - Enregistrer

  6. Vérifier la connexion SSH :

    - `ssh -T git@github.com`
    - À la première connexion, le terminal demande de confirmer l'empreinte de GitHub : répondre `yes`. Un message de confirmation doit apparaître :
  `Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.`

  7. Lier le projet local au dépôt GitHub.

    - `git branch -M main`
    - `git remote add origin git@github.com:<username>/RNCP.git`
    - Si le remote existe déjà vous aurez l'erreur « remote origin already exists », exécuter ce code à la place:
  `git remote set-url origin git@github.com:<username>/RNCP.git`

  8. Envoyer le code sur GitHub :

    `git push -u origin main`

  9. Vérification dans le terminal (Cela doit afficher au moins un commit):

    `git log --oneline`


## VIII. Documentation de l’API

Cette partie décrit l'API Flask plus en détails : les routes disponibles, la méthode utilisée, les données attendues, les réponses renvoyées et les erreurs possibles.

### A. Informations générales

  - Adresse de base (en local) : `http://127.0.0.1:5000`
  - Méthode HTTP : toutes les routes utilisent la méthode `GET`.
  - Paramètres : aucune route n'attend de paramètre ni de corps de requête. Seule la clé API est nécessaire.
  - Authentification : la clé API doit être envoyée dans l'en-tête `X-API-Key` à chaque requête (voir partie V). Les clés valides sont celles du fichier `.env` (variable `API_KEY`).
  - Format des réponses : JSON.

### B. Résumé des routes

1. Routes de l'API :

  - `/health`
  - `/sales-by-country`  
  - `/sales-by-category`

2. Méthode de l'API : Type de la requête HTTP utilisée sur les 3 routes = `GET`.
3. Entrée à fournir : L'utilisateur a besoin de fournir une Clé API.
4. Sortie (ce que l'API renvoie en fonction de sa route) :
  - `/health` --> renvoie un petit message JSON : {"message": "L'API fonctionne."} 
  - `/sales-by-country` --> Ventes agrégées par pays (liste d'objets JSON) 
  - `/sales-by-category` --> Ventes agrégées par catégorie (liste d'objets JSON) 
5. Erreur possible : 401 si la clé est invalide ou absente

### C. Détail des routes

  #### 1. `/health`

  Elle permet de vérifier que l'API fonctionne.

  - Requête : `curl.exe -H "X-API-Key: $env:API_Key" http://127.0.0.1:5000/health`
  - Réponse (code 200) :

        {"message": "L'API fonctionne."}

  #### 2. `/sales-by-country`

  Elle renvoie le contenu de la table `sales_by_country`, avec une ligne par pays, classés par bénéfice en euros (profit_total_eur) décroissant.

  - Requête : `curl.exe -H "X-API-Key: $env:API_Key" http://127.0.0.1:5000/sales-by-country`
  - Réponse (code 200) : une liste d'objets JSON, un par pays. Exemple :

  [{"country_code": "DE",
    "country_name": "Germany",
    "profit_total_eur": 893.75,
    "profit_total_gbp": 753.16,
    "total_orders": 40,
    "total_quantity": 110,
    "total_revenue_eur": 4757.98,
    "total_revenue_gbp": 4014.7}]

  - Champs :
    - `country_code` et `country_name` : le code et le nom du pays.
    - `total_orders` : le nombre de commandes.
    - `total_quantity` : le nombre de livres achetés.
    - `total_revenue_gbp` et `total_revenue_eur` : le chiffre d'affaires en livres et en euros.
    - `profit_total_gbp` et `profit_total_eur` : le profit en livres et en euros.

  #### 3. `/sales-by-category`

  Elle renvoie le contenu de la table `sales_by_category`, avec une ligne par catégorie de livres, classées par bénéfice en euros (profit_total_eur) décroissant.

  - Requête : `curl.exe -H "X-API-Key: $env:API_Key" http://127.0.0.1:5000/sales-by-category`
  - Réponse (code 200) : une liste d'objets JSON, un par catégorie. 
  - Les champs sont les mêmes que pour `/sales-by-country`, sauf `country_code` et `country_name` qui sont remplacés par `category_name` (le nom de la catégorie). Exemple :

  [{"category_name": "Nonfiction",
    "profit_total_eur": 843.99,
    "profit_total_gbp": 713.36,
    "total_orders": 62,
    "total_quantity": 173,
    "total_revenue_eur": 7563.41,
    "total_revenue_gbp": 6383.39}]


### D. Erreurs possibles

1. Erreur 401 : Clé API invalide ou absente. 
   - La cause : L'en-tête `X-API-Key` est manquant ou ne correspond à aucune clé du fichier `.env`. La réponse est `{"error": "Clé API invalide ou absente"}`.

2. Erreur 404 : Route introuvable. 
   - La cause : L'adresse demandée ne correspond à aucun des trois endpoints. 

3. Erreur 500 : Erreur interne du serveur. 
   - La cause : La base `tables_finales.db` ou la table demandée n'existe pas, car `pipeline.py` n'a pas été exécuté avant l'API.
