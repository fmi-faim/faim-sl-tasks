import cv2 as cv
import luigi

from faim_sl.MultiFileTask import MultiFileTask


class GaussianFilterApproximationTask(MultiFileTask):
    """
    Fast blur approx

    Notes:
    ------
    fast gaussian filter approximation:

    KOVESI, Peter. Fast almost-gaussian filtering. In: Digital Image Computing:
    Techniques and Applications (DICTA), 2010 International Conference on. IEEE, 2010. S. 121-125.
    """

    # Params
    ksize = luigi.IntParameter(description="Kernel size.")

    def run_computation(self, img):
        return self.compute(img, ksize=self.ksize)

    @staticmethod
    def compute(img, ksize):
        """
        Apply box-filter three times as approximation of a Gaussian filter.

        :param img: to filter
        :param ksize: of the box filter
        :return: filtered image
        """
        img = cv.boxFilter(img, -1, (ksize, ksize))
        img = cv.boxFilter(img, -1, (ksize, ksize))
        return cv.boxFilter(img, -1, (ksize, ksize))
