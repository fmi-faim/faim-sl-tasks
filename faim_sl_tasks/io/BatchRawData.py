from glob import glob
from os.path import join

import luigi
import sciluigi as sl


class BatchRawData(sl.ExternalTask):
    dir = luigi.Parameter()
    pattern = luigi.Parameter()
    recursive = luigi.BoolParameter(default=False)

    def out_file(self):
        files = glob(join(self.dir, self.pattern), recursive=self.recursive)
        batch = {}
        for f in files:
            batch[f] = sl.TargetInfo(self, f)
        return batch
