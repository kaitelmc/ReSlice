import os
import soundfile as sf 

class Exporter:

    def __init__(self):
        pass

    def export_slices(self, data, samplerate, sample_slices, output_folder):

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for i, current_slice in enumerate(sample_slices):

            start = current_slice[0]
            end = current_slice[1]

            slice_audio = data [start:end]

            filename = f"{i+1:03}.wav"

            filepath = os.path.join(
                output_folder, 
                filename
            )
            sf.write(
                filepath,
                slice_audio,
                samplerate
            )
            print(f"Exported: {filename}")

        return True