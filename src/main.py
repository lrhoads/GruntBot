import os
import discord
import random
import requests

from dotenv import load_dotenv
from chats import chats
from chat import chatsvc

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class GruntBot(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@property
	def chats(self):
		if not hasattr(self, '_chats'):
			self._chats = chats(timeout=300)  # 5 minutes timeout
		return self._chats

	async def on_ready(self):
		print(f"Logged in as {self.user} (ID: {self.user.id})")
		print("Bot is ready!")

	async def on_member_join(self, member):
		if member.guild.system_channel is not None:
			try:
				with open('./res/greetings.txt') as grunts_file:
					contents = grunts_file.readlines()
				grunts = [line.strip() for line in contents]
				grunt = random.choice(grunts)
    
				await member.guild.system_channel.send(
					f"{member.mention}, {grunt}"
				)

			except:
				return

	async def on_message(self, message):
		if message.author == self.user:
			return

		# Check if "grunt" or "grunty" is mentioned anywhere in the message
		message_lower = message.content.lower()
		if "grunt" in message_lower or "grunty" in message_lower:
			
			# Special handling for just "grunt" - give traditional grunt response
			if message.content.lower().strip() == "grunt":
				try:
					with open('./res/grunts.txt') as grunts_file:
						contents = grunts_file.readlines()
					grunts = [line.strip() for line in contents]
					grunt = random.choice(grunts)
					await message.channel.send(grunt)
				except:
					await message.channel.send("Zug zug")
					return
			
			else:
				# Check for learning opportunities first
				learning_response = self.chats.process_message_for_learning(message.author.name, message.content)
				if learning_response:
					await message.channel.send(learning_response)
					return
				
				# AI response for any other message containing "grunt" or "grunty" based on user profile
				try:
					chat = self.chats.get_chat(message.author.name)    
					response = await chat.prompt(message.content)
					await message.channel.send(response)
	    
				except Exception as e:
					print(f"Error processing message: {e}")
					await message.channel.send("Me tired, come back later")
					return

intents = discord.Intents.default()
intents.message_content = True

client = GruntBot(intents=intents)
client.run(DISCORD_TOKEN)