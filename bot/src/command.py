from discord import Message, Embed
import aiohttp as http
import os

def almost(s: str):
  return s.lower().replace('è', 'e').replace(' ', '')

async def test(msg: Message, args: list[str], **kwargs):
  return await msg.reply('Ceci est un test')

async def pull(msg: Message, args: list[str], **kwargs):
  cli = http.ClientSession()
  response: http.ClientResponse = await cli.request(url=os.environ['CSV_URL'], method='GET')
  if response.status != 200: return await msg.reply('Erreur durant l\'exécution')
  # Str -> Liste 2D
  resp: list[list[str]] = list(col.replace('\r', '').split(',') for col in (await response.text()).split('\n'))
  await cli.close()
  nom_commande = ' '.join(args[1:])
  col = -1
  for [i,row] in enumerate(resp[1:]):
    if almost(row[0]) == almost(nom_commande): col = i+1
  if col == -1: return await msg.reply(f'Aucune commande a été trouvée sous le nom de {nom_commande}')
  data = resp[col]
  color = 0x000000
  if 0<int(data[1])<4: color=([0x0000FF,0x00FF00,0xFF0000][int(data[1])-1])
  emb = Embed(title=f"L'état de la commande des pulls pour {nom_commande} : ", color=color)
  emb.add_field(name=resp[0][1], value=data[1])
  for [nom, val] in list(zip(resp[0], data))[2:]:
    emb.add_field(name=nom, value=("✅" if val=="X" else ("⌛" if val else "❌")), inline=False)
  return await msg.reply(embed=emb)

async def invite(msg: Message, args, bot):
  return await msg.reply(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=274877974592&scope=bot")

commandes = {
  "test": test,
  "pull": pull,
  "pulls": pull,
  "invite": invite,
}