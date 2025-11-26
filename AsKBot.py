# by bigbastik #

import asyncio
import pydle
from openai import OpenAI

# ================= CONFIGURAZIONE =================
IRC_SERVER = "SERVER IRC PREFERITO"
IRC_PORT = 6667
NICKNAME = "ASKBot"
IDENT = "askbot"
REALNAME = "AI IRC Bot"
CHANNELS = ["#CANALEPREFERITO" "#CANALEPREFERITO2!]  # Inserisci qui i tuoi canali reali

OPENAI_API_KEY = "sk-proj-*" #Inserisci qui la tua APIKEY di OPENAI. Registrazione qui: https://auth.openai.com/create-account
MODEL = "gpt-4.1-mini"

MAX_RESPONSE_LENGTH = 15000 # Modificabile a piacere.
# ==================================================

# Inizializza client OpenAI
client_ai = OpenAI(api_key=OPENAI_API_KEY)

class IRCBot(pydle.Client):

    async def on_connect(self):
        print("✅ Connesso a IRCNET")
        for channel in CHANNELS:
            await self.join(channel)

    async def on_message(self, target, source, message):
        if source == self.nickname:
            return

        print(f"[{source} -> {target}] {message}")

        if message.startswith("!ask "):
            domanda = message[5:].strip()
            risposta = await self.ask_ai(domanda)
            await self.message(target, risposta)

    async def ask_ai(self, prompt):
        try:
            completion = client_ai.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Sei un assistente IRC chiaro, conciso e utile."},
                    {"role": "user", "content": prompt}
                ]
            )

            text = completion.choices[0].message.content
            return text[:MAX_RESPONSE_LENGTH]
        except Exception as e:
            return f"Errore AI: {str(e)}"


if __name__ == "__main__":
    bot = IRCBot(NICKNAME, realname=REALNAME)
    bot.run(IRC_SERVER, IRC_PORT)
