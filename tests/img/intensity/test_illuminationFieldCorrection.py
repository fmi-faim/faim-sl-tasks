from os.path import join

import numpy as np
import os
import sciluigi as sl
import shutil
import unittest
from tifffile import imsave

from faim_sl_tasks.img.intensity.IlluminationFieldEstimation3DTask import IlluminationFieldEstimation3DTask
from faim_sl_tasks.img.intensity.SingleChannelIlluminationFieldCorrectionTask import \
    SingleChannelIlluminationFieldCorrectionTask


class IlluminationFieldCorrectionTest(unittest.TestCase):
    @staticmethod
    def gaussian(coords, sigma, mu_y, mu_x, scale):
        return scale / (sigma * np.sqrt(2 * np.pi)) * np.exp(
            -((coords[1] - mu_x) ** 2 + (coords[0] - mu_y) ** 2) / (2 * sigma ** 2))

    def test_illuminationFieldEstimation3DTask(self):
        y, x = np.meshgrid(range(173), range(251))
        coords = np.stack([y, x])

        input_img = self.gaussian(coords, sigma=80, mu_y=83, mu_x=141, scale=20000)[np.newaxis]

        os.mkdir('test_ife3d')
        test_imgs = {}
        for i in range(10):
            input_img_noisy = input_img + np.random.normal(size=input_img.shape)
            path = join('test_ife3d', 'img_{}.tiff'.format(i))
            imsave(path, input_img_noisy.astype(np.float32))
            test_imgs[path] = sl.TargetInfo(None, path)

        output = IlluminationFieldEstimation3DTask.compute(test_imgs)

        np.testing.assert_allclose(output, input_img, atol=1e-2, rtol=1e-3)
        shutil.rmtree('test_ife3d')

    def test_singleChannelIlluminationFieldCorrection(self):
        y, x = np.meshgrid(range(173), range(251))
        coords = np.stack([y, x])

        ill_field = self.gaussian(coords, sigma=80, mu_y=83, mu_x=141, scale=2000)[np.newaxis]

        output = SingleChannelIlluminationFieldCorrectionTask.compute(ill_field, ill_field, scale=255)
        np.testing.assert_allclose(output, np.ones_like(ill_field) * 255)

    def tearDown(self) -> None:
        if os.path.exists('log'):
            shutil.rmtree('log')
