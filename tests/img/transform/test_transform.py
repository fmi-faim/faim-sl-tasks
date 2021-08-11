import numpy as np
import os
import shutil
import unittest

from faim_sl_tasks.img.transform.BlockReduceTask import BlockReduceTask
from faim_sl_tasks.img.transform.SliceTask import SliceTask


class TransformTest(unittest.TestCase):

    def test_blockReduce(self):
        img = np.random.normal(size=(100, 100)).astype(np.float32)

        output_mean = BlockReduceTask.compute(img, (2, 2), 'np.mean')

        expected_mean = np.stack([img[::2, ::2], img[1::2, ::2], img[::2, 1::2], img[1::2, 1::2]]).mean(0)

        np.testing.assert_allclose(output_mean, expected_mean, atol=1e-7, rtol=1e-7)

    def test_slice(self):
        img = np.random.normal(size=(17, 28, 13))

        s = slice(3, 5)

        s0_output = SliceTask.compute(img, s, axis=0)
        s0_expected = img[s]

        s1_output = SliceTask.compute(img, s, axis=1)
        s1_expected = img[:, s]

        s2_output = SliceTask.compute(img, s, axis=2)
        s2_expected = img[:, :, s]

        np.testing.assert_allclose(s0_output, s0_expected)
        np.testing.assert_allclose(s1_output, s1_expected)
        np.testing.assert_allclose(s2_output, s2_expected)


def tearDown(self) -> None:
    if os.path.exists('log'):
        shutil.rmtree('log')
