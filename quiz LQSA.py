import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
import random


TOKEN = ""  # Pon aquí el token de tu bot- crea tu token en discord.dev

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)

# 🧠 Lista de preguntas
preguntas = [
    {"pregunta": "¿Cómo se llama el barrio donde viven los protagonistas?",
     "opciones": ["Esperanza Sur", "San Genaro", "Mirador de Montepinar"],
     "respuesta": "Mirador de Montepinar"},
    {"pregunta": "¿Cómo se llamaba la serie en la que se basó 'LQSA'?",
     "opciones": ["Aquí no hay quien viva", "Malditos vecinos", "Esta casa es una ruina"],
     "respuesta": "Aquí no hay quien viva"},
    {"pregunta": "¿Qué actor de 'La que se avecina' pone la voz al padre de Nemo en 'Buscando a Nemo'?",
     "opciones": ["José Luis Gil", "Pablo Chiapella", "Fernando Tejero"],
     "respuesta": "José Luis Gil"},
    {"pregunta": "¿Qué mítico personaje de 'LQSA' no estará en la próxima temporada?",
     "opciones": ["Fernando Tejero", "Cristina Castaño", "Pablo Chiapella"],
     "respuesta": "Cristina Castaño"},
    {"pregunta": "¿Cómo se llama el portero de 'La que se avecina'?",
     "opciones": ["Coque", "Emiliano", "Emilio"],
     "respuesta": "Coque"},
    {"pregunta": "Complete esta frase: \"Si tiene una cena elegante...\"",
     "opciones": ["lleve el dinero por delante", "llévese un bogavante", "compre en Mariscos Recio"],
     "respuesta": "llévese un bogavante"},
    {"pregunta": "¿Qué personaje de 'LQSA' era lesbiana en la serie 'Aquí no hay quien viva'?",
     "opciones": ["Berta", "La Cuqui", "Judith"],
     "respuesta": "La Cuqui"},
    {"pregunta": "¿Cómo murió la pobre Goya?",
     "opciones": ["Haciendo croquetas", "Se tiró por el balcón", "La atropelló un coche"],
     "respuesta": "Haciendo croquetas"},
    {"pregunta": "Completa esta frase: \"Qué somos leones o...\"",
     "opciones": ["huevones", "perritos", "tigres"],
     "respuesta": "huevones"},
    {"pregunta": "¿A qué se dedicaba Fermín antes de llegar a Mirador de Montepinar?",
     "opciones": ["Hacía espetos en la playa", "Era vigilante de seguridad", "Era barrendero"],
     "respuesta": "Hacía espetos en la playa"}
]

# 🧩 Comando /quiz
@slash.slash(name="quiz", description="Inicia un quiz de La que se avecina")
async def _quiz(ctx: SlashContext):
    puntos = 0
    preguntas_random = random.sample(preguntas, len(preguntas))

    for q in preguntas_random:
        opciones = q["opciones"].copy()
        random.shuffle(opciones)

        # 🔹 Crear botones con un custom_id único
        botones = [
            create_button(
                style=ButtonStyle.green,
                label=op,
                custom_id=op
            )
            for op in opciones
        ]
        action_row = create_actionrow(*botones)

        # Enviar pregunta
        await ctx.send(content=f"**{q['pregunta']}**", components=[action_row], hidden=True)

        try:
            # Esperar interacción (20 segundos máximo)
            interaction = await wait_for_component(bot, components=action_row, timeout=20)
        except Exception:
            interaction = None

        # Si no responde a tiempo
        if interaction is None or not interaction.data:
            await ctx.send("⏰ Tiempo agotado!", hidden=True)
            continue

        # ✅ Comprobar respuesta
        respuesta_usuario = interaction.data["custom_id"]

        if respuesta_usuario == q["respuesta"]:
            puntos += 1
            await interaction.send("✅ ¡Correcto!", hidden=True)
        else:
            await interaction.send(f"❌ Incorrecto, la respuesta era: {q['respuesta']}", hidden=True)

    # Resultado final
    await ctx.send(f"🎉 Has conseguido {puntos} de {len(preguntas)} puntos!", hidden=True)

# 🚀 Ejecutar el bot
bot.run(TOKEN)