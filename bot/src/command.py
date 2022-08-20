from discord import Message, Embed
import aiohttp as http
from csv import reader
from io import StringIO
from datetime import datetime
import os

def almost(s: str):
  return s.lower().replace('è', 'e').replace(' ', '')

async def test(msg: Message, args: list[str], **kwargs):
  return await msg.reply('Ceci est un test')


# Cache pour les données, seulement en production
cache_delay = 60 * 5 if os.environ.get('PROD') else 0 # 5 mins
last_updated = 0
content: list[list[str]] = None

async def pull(msg: Message, args: list[str], **kwargs):
  global content, last_updated
  resp: list[list[str]] = None
  if content is not None or last_updated + cache_delay > datetime.utcnow().timestamp():
    resp = content
  else:
    cli = http.ClientSession()
    response: http.ClientResponse = await cli.request(url=os.environ['CSV_URL'], method='GET')
    if response.status != 200: return await msg.reply('Erreur durant l\'exécution')
    # Pandas -> Liste 2d
    resp: list[list[str]] = list(reader(StringIO(await response.text()), delimiter=',',quotechar='"'))
    content = resp
    last_updated = datetime.utcnow().timestamp()
    await cli.close()
  nom_commande = ' '.join(args[1:])
  # Afficher la liste de noms acceptés :
  if nom_commande == 'list' or nom_commande == 'liste' or nom_commande == '':
    emb = Embed(title=f"Liste des options acceptées pour {os.environ['PREFIX']}pull <nom_commande>: ")
    fields = [[]]
    for row in resp[1:]:
      nom = row[0]
      if row[0].strip() == '':
        fields += [[]]
      fields[-1] += [row[0]]

    final_fields = []
    longest_field_count = max(len(field) for field in fields)
    for field in fields:
      if len(field) == 0: continue
      max_field_char = max(len(nom) for nom in field)
      final_field = list(map(lambda nom:nom.ljust(max_field_char, ' '), field))
      final_field+=[' '*max_field_char]*(longest_field_count - len(field))
      final_fields += [final_field]

    emb.add_field(name='\u200B', value='```'+'\n'.join(' | '.join(i) for i in list(zip(*final_fields)))+'```')
    emb.set_footer(text='Les options restent valables quel que soit la casse.')
    return await msg.reply(embed=emb)
  # -- end  

  col = -1
  for [i,row] in enumerate(resp[1:]):
    if almost(row[0]) == almost(nom_commande): col = i+1
  if col == -1: return await msg.reply(f'Aucune commande a été trouvée sous le nom de {nom_commande}')
  data = resp[col]
  # Couleur selon les vagues
  color = 0x000000
  if 0<int(data[2])<4: color=([0x0000FF,0x00FF00,0xFF0000][int(data[2])-1])
  emb = Embed(title=f"L'état de la commande des pulls pour {nom_commande} : ", color=color)
  
  #Vague
  emb.add_field(name=resp[0][2], value=data[2])
  for [nom, val] in list(zip(resp[0], data))[3:]:
    state,*date = val.split(' ')
    field_value = ("✅" if state=="V" else ("⌛" if state=="X" else "❌"))
    if len(date) > 0: field_value += f' depuis {date[0]}'
    emb.add_field(name=nom, value=field_value, inline=False)
  
  # Remarques
  if data[1]:
    emb.set_footer(text='Dernière mise à jour')
    emb.description = f'Remarque : {data[1]}'
  emb.timestamp = datetime.fromtimestamp(last_updated)
  return await msg.reply(embed=emb)

async def invite(msg: Message, args, bot):
  return await msg.reply(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=274877974592&scope=bot")

commandes = {
  "test": test,
  "pull": pull,
  "pulls": pull,
  "invite": invite,
}