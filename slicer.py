class Slicer:
    def __init__(self):
        self.number_of_slices = 4

        self.visual_slices = []
        self.sample_slices = []

    def create_slices(self, waveform_width):
        self.visual_slices = []

        slice_width = waveform_width / self.number_of_slices

        start = 0      

         
        for i in range(self.number_of_slices):
            end = start + slice_width
            self.visual_slices.append([start, end])
            start = end

    def create_sample_slices(self, waveform_width, sample_count):

        self.sample_slices = []

        for current_slice in self.visual_slices:

            start = self.pixel_to_sample(
                current_slice[0],
                waveform_width,
                sample_count
        )

            end = self.pixel_to_sample(
                current_slice[1],
                waveform_width,
                sample_count
        )
            self.sample_slices.append([start, end])

    #converts visual slices to audio slices
    def pixel_to_sample(self, pixel, waveform_width, sample_count):
        samples_per_pixel = sample_count / waveform_width
        sample_position = pixel * samples_per_pixel

        return int(sample_position)