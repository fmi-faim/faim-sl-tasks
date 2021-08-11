import luigi
from tifffile import imread

from faim_sl.MultiFileTask import MultiFileTask


class SingleChannelIlluminationFieldCorrectionTask(MultiFileTask):
    # Params
    in_illumination_field = None

    scale = luigi.IntParameter(default=255)

    ill_field_img = None

    def prepare(self):
        self.ill_field_img = imread(self.in_illumination_field().path)

    def run_computation(self, img):
        return self.compute(img, illumination_field=self.ill_field_img, scale=self.scale)

    @staticmethod
    def compute(img, illumination_field, scale):
        return (img / illumination_field * scale).astype(img.dtype)
