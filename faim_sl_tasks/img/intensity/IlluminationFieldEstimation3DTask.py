from os.path import join

import luigi
import numpy as np
import sciluigi as sl
from scipy.optimize import curve_fit
from tifffile import imread, imsave


class IlluminationFieldEstimation3DTask(sl.Task):
    # Params
    in_data = None

    target_dir = luigi.Parameter(description='Target directory.')
    file_name = luigi.Parameter('File suffix.')

    def out_file(self):
        return sl.TargetInfo(self, path=join(self.target_dir, self.file_name))

    def run(self):
        illumination_field = self.compute(self.in_data())
        imsave(self.out_file().path, illumination_field)

    @staticmethod
    def compute(in_data):
        def gaussian(coords, sigma, mu_y, mu_x, scale):
            return scale / (sigma * np.sqrt(2 * np.pi)) * np.exp(
                -((coords[1] - mu_x) ** 2 + (coords[0] - mu_y) ** 2) / (2 * sigma ** 2))

        illumination = None
        dtype = None
        n_imgs = len(in_data)
        for path, target_info in in_data.items():
            if illumination is None:
                img = imread(target_info.path)
                dtype = img.dtype
                illumination = img / n_imgs
            else:
                illumination = illumination + (imread(target_info.path) / n_imgs)

        y, x = np.meshgrid(range(illumination.shape[2]), range(illumination.shape[1]), indexing='xy')

        coords = np.stack([y.flatten(), x.flatten()])

        illumination_field = np.zeros_like(illumination)
        for i in range(illumination_field.shape[0]):
            mean = illumination[i].mean()
            try:
                popt, pcov = curve_fit(gaussian, coords, illumination[i].flatten(), maxfev=100)
                fit = gaussian(coords, *popt)
                fit = fit.reshape(x.shape)
                illumination_field[i] = fit
            except RuntimeError:
                print('Could not find a fit for slice {}. Setting illumiation field to uniform mean.'.format(i))
                illumination_field[i] = mean

        return illumination_field.astype(dtype)
