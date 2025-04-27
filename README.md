# APs-associated-with-Locations

Ce script Python automatise l'export des sites (locations) et de leurs points d'accès associés (identifiers) dans un fichier Excel (.xlsx).  
Il utilise l'API Cloudi-Fi Manage API v1 et produit :

- Un premier onglet avec le détail des sites et de leurs identifiers.
- Un deuxième onglet qui résume le nombre de points d'accès par site.

## Fonctionnalités

- Gestion automatique du refresh token.
- Authentification avec Bearer Token.
- Export complet des locations et de leurs Access Points (identifiers).
- Suppression automatique des champs inutiles.
- Format de date français dans les noms de fichier et les noms des feuilles (exemple : 27-04-2025).
- Deux feuilles Excel générées :
  - "Locations" : détail des sites avec les identifiers en colonnes.
  - "Résumé du {date}" : synthèse du nombre de points d'accès par site.

## Prérequis

- Python 3.7 ou supérieur
- Bibliothèques Python :
  - requests
  - pandas
  - openpyxl (pour écrire au format .xlsx)

Installation des dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

1. Cloner ou télécharger ce dépôt Git.
2. Ouvrir le fichier `get_locations.py`.
3. Mettre à jour la valeur du `refresh_token` dans le script avec votre token Cloudi-Fi valide.
4. Exécuter le script avec la commande suivante :

```bash
python get_locations.py
```

5. Le script générera un fichier Excel nommé comme suit :

```
locations_with_identifiers_27-04-2025.xlsx
```

Le nom du fichier contient la date du jour au format français (jour-mois-année).

## Structure du fichier Excel

### Feuille 1 : Locations

Cette feuille contient :

- L'identifiant du site (`id`)
- Le nom du site (`name`)
- Les clés (`key`) et alias (`alias`) de chaque Access Point associé, organisés par colonnes :
  - `identifier_1_key`, `identifier_1_alias`
  - `identifier_2_key`, `identifier_2_alias`
  - `identifier_3_key`, `identifier_3_alias`
  - etc.

### Feuille 2 : Résumé du {date}

Cette feuille contient un résumé indiquant :

- L'identifiant du site (`Location ID`)
- Le nom du site (`Location Name`)
- Le nombre de points d'accès associés (`Nombre d'APs`)

## Informations importantes

- La valeur du `refresh_token` doit être mise à jour manuellement dans le script avant utilisation.
- Tous les sites sont exportés, même ceux qui n'ont pas d'Access Points associés (les colonnes correspondantes seront vides).
- Vous pouvez ajuster la liste `excluded_fields` dans le script pour personnaliser les champs exportés.
- Le format de date utilisé est le format français (jour-mois-année).

## Licence
Ce projet est sous licence MIT.