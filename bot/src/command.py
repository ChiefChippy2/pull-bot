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