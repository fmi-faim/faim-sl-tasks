import luigi
from tifffile import imread

from faim_sl.MultiFileTask import MultiFileTask


class SingleChannelIlluminationFieldCorrectionTask(MultiFileTask):
    # Params
    illumination_field_path = None
    illumination_field = None

    scale = luigi.IntParameter(default=255)

    def prepare_inputs(self):
        self.illumination_field_path = self.in_data['illumination_field']().path
        self.in_data = self.in_data['batch']

    def prepare(self):
        self.illumination_field = imread(self.illumination_field_path)

    def run_computation(self, img):
        return self.compute(img, illumination_field=self.illumination_field, scale=self.scale)

    @staticmethod
    def compute(img, illumination_field, scale):
        return (img / illumination_field * scale).astype(img.dtype)
