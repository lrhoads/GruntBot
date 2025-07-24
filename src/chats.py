import json
import re
import os

from chat import chatsvc
from utils import first

class chats:
	def __init__(self, timeout):
		self._chats = {}
		self._timeout = timeout

	def get_chat(self, name):
		chat = self._chats.get(name, None)
      
		if not chat:
			profile = self.load_profile(name)
			display_name = profile['displayName'] if profile and 'displayName' in profile else name
			hint = self.load_all_profile_hints()
			# Create more positive context
			context = f"You are a friendly Orc Warrior from World of Warcraft. {display_name} is addressing you. {hint}. Respond warmly and positively in 1-4 sentences, using simple orc speech." if hint else "You are a friendly Orc Warrior from World of Warcraft. Respond warmly and positively in 1-4 sentences, using simple orc speech."
			chat = chatsvc(name, display_name, context)
			self._chats[name] = chat
		elif not chat.is_active:
			del chat
			chat = None
			self.chats[name] = None
      
		if not chat:
			profile = self.load_profile(name)
			display_name = profile['displayName'] if profile and 'displayName' in profile else name
			hint = self.load_all_profile_hints()
			context = f"You are a friendly Orc Warrior from World of Warcraft. {display_name} is addressing you. {hint}. Respond warmly and positively in 1-4 sentences, using simple orc speech." if hint else "You are a friendly Orc Warrior from World of Warcraft. Respond warmly and positively in 1-4 sentences, using simple orc speech."
			chat = chatsvc(name, display_name, context)
			self._chats[name] = chat

		return chat

	def load_profile(self, name):
		try:
			with open('./res/profiles.json') as f:
				profiles = json.load(f)
			profile = first(x for x in profiles if x['name'].lower() == name.lower())
			return profile
		except FileNotFoundError:
			print("Profile file not found.")
			return None
		except json.JSONDecodeError:
			print("Error decoding JSON from profile file.")
			return None
		except StopIteration:
			print(f"No profile found for {name}.")
			return None

	def load_all_profile_hints(self):
		try:
			with open('./res/profiles.json') as f:
				profiles = json.load(f)
			hints = ""
			for profile in profiles:
				if hints:
					hints += ", "
				hints += profile['hint']
			return hints
		except:
			return None

	def load_profile_hint(self, name):
		try:
			with open('./res/profiles.json') as f:
				profiles = json.load(f)
			profile = first(x for x in profiles if x['name'].lower() == name.lower())
			return profile['hint']
		except FileNotFoundError:
			print("Profile file not found.")
			return None
		except json.JSONDecodeError:
			print("Error decoding JSON from profile file.")
			return None
		except StopIteration:
			print(f"No profile found for {name}.")
			return None

	def learn_about_user(self, username, message):
		"""Extract learning information from user messages and update their profile"""
		learning_patterns = [
			r"(?:grunt,?\s+)?(?:i am|i'm|my name is|call me)\s+(\w+)",
			r"(?:grunt,?\s+)?(?:i am|i'm)\s+(.*?)(?:\.|!|$)",
			r"(?:grunt,?\s+)?(?:remember|know)\s+(?:that\s+)?(?:i am|i'm)\s+(.*?)(?:\.|!|$)"
		]
		
		message_lower = message.lower().strip()
		learned_info = None
		
		# Check for name learning patterns
		for pattern in learning_patterns:
			match = re.search(pattern, message_lower)
			if match:
				learned_info = match.group(1).strip()
				break
		
		if learned_info:
			self.update_profile(username, learned_info, message_lower)
			return f"Grunt remember! {learned_info}. Grunt know you now!"
		
		return None

	def update_profile(self, username, learned_info, full_message):
		"""Update or create a user profile with learned information"""
		try:
			# Load existing profiles
			profiles = []
			if os.path.exists('./res/profiles.json'):
				with open('./res/profiles.json', 'r') as f:
					profiles = json.load(f)
			
			# Find existing profile or create new one
			existing_profile = None
			for profile in profiles:
				if profile['name'].lower() == username.lower():
					existing_profile = profile
					break
			
			if existing_profile:
				# Update existing profile
				if 'displayName' not in existing_profile or existing_profile['displayName'] == username:
					existing_profile['displayName'] = learned_info.title()
				
				# Update hint with new information
				if learned_info.lower() not in existing_profile.get('hint', '').lower():
					if 'hint' in existing_profile:
						existing_profile['hint'] += f", also known as {learned_info}"
					else:
						existing_profile['hint'] = f"{learned_info} is a friend of Grunt"
				
				# Add personality traits from message
				if any(word in full_message for word in ['evil', 'bad', 'dark']):
					if 'mischievous' not in existing_profile['hint']:
						existing_profile['hint'] += ", has a mischievous side"
				elif any(word in full_message for word in ['good', 'nice', 'kind', 'friendly']):
					if 'kind' not in existing_profile['hint']:
						existing_profile['hint'] += ", is kind and friendly"
			else:
				# Create new profile
				hint = f"{learned_info} is a friend of Grunt"
				if any(word in full_message for word in ['evil', 'bad', 'dark']):
					hint += ", has a mischievous side"
				elif any(word in full_message for word in ['good', 'nice', 'kind', 'friendly']):
					hint += ", is kind and friendly"
				
				new_profile = {
					"name": username,
					"displayName": learned_info.title(),
					"hint": hint
				}
				profiles.append(new_profile)
			
			# Save updated profiles
			with open('./res/profiles.json', 'w') as f:
				json.dump(profiles, f, indent="\t")
			
			# Update chat context if exists
			if username in self._chats:
				del self._chats[username]  # Force reload with new profile
			
		except Exception as e:
			print(f"Error updating profile: {e}")

	def process_message_for_learning(self, username, message):
		"""Check if message contains learning information and process it"""
		learning_keywords = ['i am', "i'm", 'my name is', 'call me', 'remember', 'know that']
		message_lower = message.lower()
		
		if any(keyword in message_lower for keyword in learning_keywords):
			return self.learn_about_user(username, message)
		
		return None