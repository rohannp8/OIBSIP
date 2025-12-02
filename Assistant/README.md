Voice Assistant Python Project 🤖

A simple voice assistant in Python that can listen to your commands, respond via speech, tell the current date & time, open websites, and perform Google searches.

Features ✨

Greets the user on startup

Responds to greetings like "hello", "hi", "hey"

Tells today's date and current time

Opens websites like Google Chrome and YouTube

Performs Google searches based on your voice command

Stops when commanded ("stop assistant" or "stop ok fine")

Technologies Used 🛠️

Python 3.x

speech_recognition – To convert speech to text

pyttsx3 – Text-to-speech engine

datetime – To get the current date and time

webbrowser – To open websites

Installation 💻

Clone the repository:

git clone https://github.com/yourusername/voice-assistant.git
cd voice-assistant


Install required packages:

pip install -r requirements.txt


requirements.txt example:

speechrecognition
pyttsx3
pyaudio


Note: On some systems, installing pyaudio may require extra steps. For Windows, use:

pip install pipwin
pipwin install pyaudio


Run the assistant:

python assistant.py

Usage 🎤

Speak commands clearly when the assistant says "Listening..."

Examples of commands:

"Hello" / "Hi" / "Hey" → Greeting

"Today's date" → Get today's date

"Tell me the time" → Get current time

"Open Chrome" → Opens Google Chrome

"Open YouTube" → Opens YouTube

"Search for [query]" → Searches Google

"Stop assistant" → Stops the program

Contribution 🤝

Contributions are welcome!

Fork the repository

Create your branch: git checkout -b feature-name

Commit your changes: git commit -m 'Add some feature'

Push to the branch: git push origin feature-name

Open a Pull Request

License 📄

This project is open-source under the MIT License.