import os
import discord
import random
import requests

from dotenv import load_dotenv
from openai import OpenAI

from google import genai
from google.genai import types

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class GruntBot(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	async def on_ready(self):
		print(f"Logged in as {self.user} (ID: {self.user.id})")
		print("Bot is ready!")

	async def on_message(self, message):
		if message.author == self.user:
			return

		if message.content.lower() == "grunt":
			try:
				with open('./res/grunts.txt') as grunts_file:
					contents = grunts_file.readlines()
				grunts = [line.strip() for line in contents]
				grunt = random.choice(grunts)
				await message.channel.send(grunt)

			except:
				await message.channel.send("Zug zug")
				return
   
		elif message.content.lower().startswith("grunt"):
			try:
				# client = OpenAI(
				# 	api_key = OPENAI_API_KEY,
				# )

				# response = client.responses.create(
				# 	model="gpt-4o",
				# 	instructions="You are an Orc from World of Warcraft",
				# 	input=message.content.removeprefix("grunt"),
				# )
    
				# await message.channel.send(response.output_text)

				client = genai.Client()

				response = client.models.generate_content(
					model="gemini-2.5-flash",
					config=types.GenerateContentConfig(
						system_instruction="You are an Orc Peon from World of Warcraft, answer in one or two sentences",),
					contents=message.content.removeprefix("grunt")
				)
    
				await message.channel.send(response.text)
    
			except:
				await message.channel.send("Me too tired now, come back later")
				return

intents = discord.Intents.default()
intents.message_content = True

client = GruntBot(intents=intents)
client.run(DISCORD_TOKEN)