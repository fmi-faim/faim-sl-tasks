import luigi

from skimage.exposure import rescale_intensity
from skimage.io import imsave
import numpy as np

from faim_sl.MultiFileTask import MultiFileTask
from faim_sl_tasks.ndimg.filters.GaussianFilterApproximationTask import GaussianFilterApproximationTask


class RGBFlatFieldCorrectionTask(MultiFileTask):
    # Params
    ksize = luigi.IntParameter(default=19, description='Blur kernel size.')
    background_value = luigi.IntParameter(default=0, description='Background value.')
    channel_axis = luigi.IntParameter(default=-1, description='Channel axis index.')

    def get_save_function(self):
        def configured_imsave(path, img):
            imsave(path, img, compress=7)

        return configured_imsave

    def run_computation(self, img):
        return self.compute(img, ksize=self.ksize, background_value=self.background_value,
                            channel_axis=self.channel_axis)

    @staticmethod
    def compute(img, ksize, background_value=0, channel_axis=-1):
        tile_mask = (img == background_value).sum(axis=channel_axis) == 0
        bounds = np.quantile(img[tile_mask], 0.5, axis=0)
        img[~tile_mask] = bounds

        blurred = GaussianFilterApproximationTask.compute(img, ksize=ksize)
        blurred = blurred / blurred.min()
        img = img / blurred

        bounds = np.quantile(img[tile_mask], (0.01, 0.95), axis=0)
        return rescale_intensity(img, in_range=(bounds[0].min(), bounds[1].max()), out_range=np.uint8)
