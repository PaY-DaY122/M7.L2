import discord
from discord.ext import commands
from model import get_class

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

# ── Eventos
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user.name} ({bot.user.id})")

# ── Comandos generales
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def hello(ctx):
    await ctx.send(f"¡Hola, {ctx.author.mention}!")

@bot.command()
async def heh(ctx, count: int = 5):
    await ctx.send("heh" * count)

@bot.command()
async def loteria(ctx):
    import random
    numbers = random.sample(range(1, 50), 6)
    await ctx.send(f"Números: {', '.join(map(str, numbers))}")
    await ctx.send("¡Ganaste!" if numbers[0] == 7 else "¡Suerte la próxima!")

# ── Comando de clasificación de imágenes
@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"{file_name}")
            await ctx.send(f"¡Gracias por subir la imagen, {ctx.author.mention}! el URL de tu imagen es: {file_url}")
            class_name, confidence_score = get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=f"{file_name}")
            await ctx.send(f"Clase: {class_name} Puntuación de Confianza: {confidence_score:.2f}%")
    else:
        await ctx.send("Por favor, adjunta una imagen para que pueda clasificarla.")
    
bot.run("TOKEN")
if __name__ == "__main__":
    pass