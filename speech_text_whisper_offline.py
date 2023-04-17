#%%
# listening with whisper
import whisper

model = whisper.load_model("base")
result = model.transcribe("output.wav")
print(result)
#%%
