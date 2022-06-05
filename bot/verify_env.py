from dotenv import load_dotenv
from os import environ
import re
load_dotenv()
if not environ.get('TOKEN') or not environ.get('PREFIX') or not environ.get('CSV_URL'): 
  print('[ERREUR]: Fichier ENV incomplet')
  exit()
if not re.fullmatch('https://docs.google.com/spreadsheets/u/0/d/\\w+/export\\?format=csv&id=\\w+(&gid=\w+)?', environ.get('CSV_URL', '')): 
  print('[ERREUR]: Lien CSV incorrect')
  exit()