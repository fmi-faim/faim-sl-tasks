import sciluigi as sl
import luigi
from faim_sl.Parameters import IntListParameter

from skimage.measure import block_reduce
from skimage.io import imread, imsave
import numpy as np

from faim_sl.MultiFileTask import MultiFileTask


class BlockReduceTask(MultiFileTask):
    """
    Down sample an image.
    """

    # Params
    factors = IntListParameter(description="Tuple of image rescaling factors.")
    reduce_function = luigi.Parameter(default='np.sum', description="Function used to reduce the image.")
    compress = luigi.IntParameter(default=9, description="skimage.io.imsave compress factor.")
    check_contrast = luigi.BoolParameter(default=False, description="skimage.io.imsave check_contrast.")

    def get_save_function(self):
        def imsave_configured(path, img):
            imsave(path, img, compress=self.compress, check_contrast=self.check_contrast)

        return imsave_configured

    def run_computation(self, img):
        return self.compute(img=img, factors=self.factors, reduce_function=self.reduce_function)

    @staticmethod
    def compute(img, factors, reduce_function):
        return block_reduce(img, factors, func=eval(reduce_function)).astype(np.uint16)
