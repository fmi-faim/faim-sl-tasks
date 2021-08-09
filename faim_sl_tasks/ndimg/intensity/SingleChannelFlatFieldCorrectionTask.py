import luigi

from skimage.exposure import rescale_intensity
from skimage.io import imsave
import numpy as np

from faim_sl.MultiFileTask import MultiFileTask
from faim_sl_tasks.ndimg.filters.GaussianFilterApproximationTask import GaussianFilterApproximationTask


class SingleChannelFlatFieldCorrectionTask(MultiFileTask):
    # Params
    ksize = luigi.IntParameter(default=19, description='Blur kernel size.')
    background_value = luigi.IntParameter(default=0, description='Background value.')

    def get_save_function(self):
        def configured_imsave(path, img):
            imsave(path, img, compress=7)

        return configured_imsave

    def run_computation(self, img):
        return self.compute(img, ksize=self.ksize, background_value=self.background_value)

    @staticmethod
    def compute(img, ksize, background_value=0):

        tile_mask = (img != background_value)
        img[~tile_mask] = img[tile_mask].mean()

        mean = img.mean()
        max = img.max()
        blurred = GaussianFilterApproximationTask.compute(img, ksize=ksize)

        img[tile_mask] = img[tile_mask] * mean / blurred[tile_mask]
        img[~tile_mask] = background_value

        return rescale_intensity(img, in_range=(background_value, max), out_range=np.uint16)