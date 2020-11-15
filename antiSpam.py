import discord
from discord.ext import commands
import asyncio

#PREFIJOS E INTENTS
intents = discord.Intents.default()
intents.guild_reactions = True
intents.guild_messages = True
intents.messages = True
client = commands.Bot(command_prefix="!",intents=intents)

#ACCIONES QUE HACE CUANDO EL BOT SE INICIA:
@client.event
async def on_ready():
    print("Estoy preparadisimo!!!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="un antispam!")) #CONFIGURA EL TEXTO DE LA ACTIVIDAD QUE ESTÁ HACIENDO

#FUNCIÓN PARA SILENCIAR:
async def silenciarUsuario(user, razon=".", temp=120):
    await user.add_roles(discord.utils.get(user.guild.roles, name="🔇SILENCIADO")) #LE PONE EL ROL DE SILENCIADO
    #CREA UN EMBED (Mensaje bonito :D que se hace mediante la API)
    embedVar = discord.Embed(title=f"🔇ESTÁS SILENCIADO🔇", color=discord.Colour.red())
    embedVar.add_field(name=f"Razón: ", value=f"{razon}!", inline=True)
    embedVar.add_field(name=f"Duración silencio: ", value=f"{temp} segundos!", inline=True)
    embedVar.set_footer(text="No vuelvas a hacerlo o volverás a ser sancionado!")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/761574801063411712/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    #ENVÍA EL EMBED A EL USUARIO POR UN MENSAJE PRIVADO
    await user.send(embed=embedVar)
    #ESPERA EL TIEMPO QUE SE HAYA CONFIGURADO PARA DESPUÉS ELIMINAR EL ROL SILENCIADO
    await asyncio.sleep(temp)
    await user.remove_roles(discord.utils.get(user.guild.roles, name="🔇SILENCIADO"))

cooldown = commands.CooldownMapping.from_cooldown(10, 10, commands.BucketType.member)
@client.event
async def on_message(msg):
    if msg.author.bot: #SI ES UN MENSAJE DE UN BOT NO HACE NADA
        return
    if "🔇SILENCIADO" in str(msg.author.roles): #SI ESTÁ SILENCIADO ELIMINA EL MENSAJE
        await msg.delete()
        return
    retry_after = cooldown.update_rate_limit(msg)
    if retry_after: #SI HA MANDADO DEMASIADO MENSAJES ELIMINA 10 MENSAJES VERIFICANDO QUE SEAN DE ÉL Y LLAMA A SILENCIAR USUARIO
        def check(msgb):
            return msgb.author.id == msg.author.id
        await msg.channel.purge(limit=10, check=check, before=None)
        await silenciarUsuario(msg.author, razon="Mandar muchos mensajes")
        return
    await client.process_commands(msg) #SI NO PASA NADA DE LO ANTERIOR PROCESA EL COMANDO DEL MESNAJE(SI TIENE)

client.run("<BOT-TOKEN>")