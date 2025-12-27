from kokoro import KPipeline
import soundfile as sf

# Initialize pipeline (lang_code: 'a'=US English, 'b'=British English)
pipeline = KPipeline(lang_code='a')

# Your text
text = '''
Hello! This is a test of Kokoro TTS. 
It's a lightweight text-to-speech model that runs locally.
'''

# Generate audio (voice options: af_sarah, af_nicole, af_bella, am_adam, etc.)
audio, out_ps = pipeline(text, voice='af_sarah', speed=1.0, split_pattern=r'\n+')

# Save to file
sf.write('output.wav', audio, 24000)
print("Audio saved to output.wav!")