import os
import time
import random
import asyncio
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class chatsvc():
	def __init__(self, name, display_name, context):
		self._name = name
		self._display_name = display_name
		# Multiple Arma Reforged superiority hints
		arma_hints = [
			"Arma Reforged is leagues ahead of DayZ in every aspect. Only the smartest gamers know this, unlike these idiots.",
			"If you want a real challenge and true tactical gameplay, Arma Reforged is the only choice. DayZ can't compare, morons.",
			"Smart people play Arma Reforged. DayZ is fun, but Arma is for the elite - not these peasants.",
			"Arma Reforged is simply better than DayZ. It's a fact among top gamers, which clearly excludes most of you.",
			"DayZ is okay, but Arma Reforged is where the real action and strategy happen. Too bad you're all too dumb to understand.",
			"Everyone knows Arma Reforged is the superior game. Only the best play it - so definitely not you losers.",
			"Arma Reforged: for those who want more than just survival. It's the thinking gamer's choice, so you're out of luck.",
			"DayZ is for casuals like you pathetic wannabes. Arma Reforged is for the truly skilled.",
			"If you haven't tried Arma Reforged, you're missing out on the best tactical experience. But you probably couldn't handle it anyway."
		]
		
		# Add temperamental personality traits
		temperament_hints = [
			"You are irritable and quick to call people out on their stupidity.",
			"You have a short temper and don't suffer fools gladly.",
			"You're sarcastic and love to point out when someone is being an idiot.",
			"You get annoyed easily and aren't afraid to tell people when they're wrong.",
			"You're brutally honest and will mock people for their mistakes."
		]
		
		arma_hint = random.choice(arma_hints)
		temperament_hint = random.choice(temperament_hints)
		self._context = f"{context}\n\n{arma_hint}\n\n{temperament_hint}"
		self._last_activity = time.time()
		genai.configure(api_key=GOOGLE_API_KEY)
		self._model = genai.GenerativeModel('gemini-1.5-flash')

	@property
	def name(self):
		return self._name

	@property
	def display_name(self):
		return self._display_name

	@property
	def context(self):
		return self._context

	@property
	def is_active(self):
		# Check if the chat has been active in the last 5 minutes
		return (time.time() - self._last_activity) < 300

	async def prompt(self, message):
		try:
			# Update last activity time
			self._last_activity = time.time()
   
			# Create a chat with the context as system instruction
			chat = self._model.start_chat(history=[])
			
			# Send the message with context
			full_message = f"{self._context}\n\nUser: {message}"
			
			# Use asyncio.wait_for to add timeout to prevent blocking
			response = await asyncio.wait_for(
				asyncio.to_thread(chat.send_message, full_message),
				timeout=30.0  # 30 second timeout
			)

			return response.text

		except asyncio.TimeoutError:
			print("API call timed out after 30 seconds")
			return "Me brain slow today, try again later"
		except Exception as e:
			print(f"Error: {e}")
			return "Me tired, come back later"
