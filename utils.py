import re
job = int(input("""
Bot à outils :
1) CSV_URL à partir d'un URL de google sheets
"""))
if job == 1:
  url = input('URL : ')
  ids = re.findall('(?<=^https://docs.google.com/spreadsheets/d/)[^/]+', url)
  if len(ids) < 1: 
    print('Mauvais URL')
    exit()
  sheet_id = int(input('ID de la feuille (par défaut 0): '))
  print(f'https://docs.google.com/spreadsheets/u/0/d/{ids[0]}/export?format=csv&id={ids[0]}&gid={sheet_id}')
else: exit()