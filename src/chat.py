import os
import time
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class chatsvc():
	def __init__(self, name, display_name, context):
		self._name = name
		self._display_name = display_name
		self._context = context
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
			response = chat.send_message(full_message)

			return response.text

		except Exception as e:
			print(f"Error: {e}")
			return "Me tired, come back later"
