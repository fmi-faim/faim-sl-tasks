import luigi
import numpy as np
import sciluigi as sl
from faim_sl.MultiFileTask import MultiFileTask

from faim_sl.Parameters import SliceParameter

class SliceTask(MultiFileTask):

    slice = SliceParameter(default="0:1")
    axis = luigi.IntParameter(default=-1)

    def run_computation(self, img):
        return self.compute(img, slice=self.slice, axis=self.axis)

    @staticmethod
    def compute(img, slice, axis):
        tmp = np.moveaxis(img, axis, 0)
        tmp = tmp[slice]
        return np.moveaxis(tmp, 0, axis).squeeze()