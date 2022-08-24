from datetime import datetime
import os
import discord
from dotenv import load_dotenv
from command import commandes

async def not_found(msg: discord.Message, args, **kwargs):
  # ignorez les "???" ou les "?!"
  if all(i in '?.! ' for i in msg.content):
    return
  await msg.reply(content='Cette commande n\'existe pas')


class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UPTIME = datetime.now().timestamp()
    async def on_ready(self): print('En ligne!')
    async def on_message(self, msg: discord.Message):
      message_str: str = msg.system_content
      # Pas de MPs
      if msg.author.bot or type(msg.author) is not discord.Member or type(msg.channel) is not discord.TextChannel:
            return
      if not message_str.startswith(os.environ['PREFIX']): return
      time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
      print(
        f'Commande envoyée par {msg.author.name}#{msg.author.discriminator} vers {time}: {message_str}')
      prefix_len = len(os.environ['PREFIX'])
      args: list[str] = message_str[prefix_len:].split(' ')
      if os.environ.get('PROD', None):
        try:
          await commandes.get(args[0], not_found)(msg, args, bot=self)
        except: await msg.reply('Erreur lors de l\'exécution')
      else: await commandes.get(args[0], not_found)(msg, args, bot=self)


load_dotenv()

# Ayant un problème d'intents avec discord.py, on utilise la valeur 46665 qui consiste en perms de :
# GUILDS
# GUILDS_EMOJIS_AND_STICKERS
# GUILD_INVITES
# GUILD_MESSAGES (de même pour dm)
# GUILD_MESSAGES_REACTIONS (de même pour dm)
# MESSAGE_CONTENT
intents = discord.Intents._from_value(46665)

client = Bot(intents=intents)
try:
    client.run(os.environ['TOKEN'])
finally:
    print('-- Arrêt en cours -- ')
    # ???
    # client.message.exit()
    # client.database.close()