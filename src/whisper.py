from faster_whisper import WhisperModel


model = WhisperModel("large-v3")
segments, info = model.transcribe("min_norsk.m4a", language="no")
print("".join(s.text for s in segments))



# pip install faster-whisper
