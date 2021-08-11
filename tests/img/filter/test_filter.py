from os.path import join

import numpy as np
import os
import shutil
import unittest
from tifffile import imread

from faim_sl_tasks.img.filter.GaussianFilterApproximationTask import GaussianFilterApproximationTask


class FilterTests(unittest.TestCase):
    def test_gaussianFilterApproximationTask(self):
        input_img = imread(join(os.path.dirname(__file__), 'filter_input.tiff'))
        target_img = imread(join(os.path.dirname(__file__), 'gaussian_filter_approximation_output.tiff'))

        output = GaussianFilterApproximationTask.compute(input_img, ksize=5)

        np.testing.assert_allclose(output, desired=target_img)

    def tearDown(self) -> None:
        if os.path.exists('log'):
            shutil.rmtree('log')


if __name__ == '__main__':
    unittest.main()
