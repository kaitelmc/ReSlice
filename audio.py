import soundfile as sf

#load audio for display and slicing, return info to ui
def load_audio(filename): 
    data, samplerate = sf.read(filename) 
    info = sf.info(filename)
    return data, samplerate, info 
