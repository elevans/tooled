# ImageJ tools: ijt

import scyjava as sj
from functools import lru_cache


class ImageProcess:
    """For image processing functions. Note this class
    only supports ImgLib2 images.
    """

    def __init__(self, ij_instance=None):
        self.ij = ij_instance

    def gauss_sub(self, image: "net.imglib2.RandomAccessibleInterval", sigma):
        """Apply a guassian blur subtraction.
        """

        self._check_ij_gateway()
        img = self.ij.op().convert().int32(image)
        img_g = self.ij.op().filter().gauss(img, sigma)
        return img_g - img

    def gauss_sub_stack(self, stack, sigma: float):
        stack = self.ij.op().convert().int32(stack)
        gauss_slices = []
        for i in range(stack.shape[2]):
            s = self.ij.py.to_dataset(stack[:, :, i])
            s_g = self.ij.op().filter().gauss(s, sigma)
            s_gs = s - s_g
            gauss_slices.append(s_gs)
        return _Views().stack(*gauss_slices)

    def invert(self, image: "net.imglib2.RandomAccessibleInterval"):
        if self.ij == None:
            self._get_imagej_gateway()

        image_i = self.ij.dataset().create(image)
        self.ij.op().run("image.invert", image_i, image)
        return image_i

    def _check_ij_gateway(self):
        if self.ij == None:
            self._get_imagej_gateway()

    def _get_imagej_gateway(self):
        try:
            from imagej import ij

            self.ij = ij
        except ImportError:
            print(f"PyImageJ has not been initialized.")


class Deconvolution:
    """Deconvolve an image with ImageJ Ops implementation of Richardson Lucy.

    :param iterations: Number of iterations (defualt=30)
    :param numerical_aperture: Numerical aperture of the objective used (default=0.75)
    :param wavelength: Wavelength in nm used in the image (default=550)
    :param particle_pos: Position of the particle (positive value in nm) relative to the coverlsip (0)
    """

    def __init__(
        self,
        iterations=30,
        numerical_aperture=0.75,
        wavelength=550,
        lateral_res=100,
        axial_res=100,
        particle_pos=2000,
        reg_factor=0.01,
        ri_immersion=1.5,
        ri_sample=1.4,
        psf=None,
        ij_instance=None,
    ):
        self.iterations = iterations
        self.numerical_aperture = numerical_aperture
        self.wavelength = wavelength * 1e-9
        self.lateral_res = lateral_res * 1e-9
        self.axial_res = axial_res * 1e-9
        self.particle_pos = particle_pos * 1e-9
        self.reg_factor = reg_factor
        self.ri_immersion = ri_immersion
        self.ri_sample = ri_sample
        self.ij = ij_instance
        self.psf = psf

    def get_config(self):
        """Return the current configuration for deconvolution"""
        print("\nDeconvolution configuration")
        print(f"\tIterations: {self.iterations}")
        print(f"\tNumerical Aperture: {self.numerical_aperture}")
        print(f"\tWavelength: {self.wavelength / 1e-9} nm")
        print(f"\tLateral resolution: {self.lateral_res / 1e-9} nm")
        print(f"\tAxial resolution: {self.axial_res / 1e-9} nm")
        print(f"\tParticle position: {round(self.particle_pos / 1e-9)} nm")
        print(f"\tRi Immersion: {self.ri_immersion}")
        print(f"\tRi Sample: {self.ri_sample}")
        print(f"\tReg factor: {self.reg_factor}")
        if self.psf == None:
            print(f"\tPSF: synthetic (default)\n")
        else:
            print(f"{self.psf}\n")


    def get_iterations(self):
        return self.iterations

    def set_iterations(self, iterations):
        self.iterations = iterations

    def get_numerical_aperture(self):
        return self.numerical_aperture

    def set_numerical_aperture(self, numerical_aperture):
        self.numerical_aperture = numerical_aperture

    def get_wavelength(self):
        return self.wavelength

    def set_wavelength(self, wavelength):
        self.get_wavelength = wavelength * 1e-9

    def get_lateral_res(self):
        return self.lateral_res

    def set_lateral_res(self, lateral_res):
        self.lateral_res = lateral_res * 1e-9

    def get_axial_res(self):
        return self.axial_res

    def set_axial_res(self, axial_res):
        self.axial_res = axial_res * 1e-9

    def get_particle_pos(self):
        return self.particle_pos

    def set_particle_pos(self, particle_pos):
        self.particle_pos = particle_pos * 1e-9

    def get_ri_immersion(self):
        return self.ri_immersion

    def set_ri_immersion(self, ri_immersion):
        self.ri_immersion = ri_immersion

    def get_ri_sample(self):
        return self.ri_sample

    def set_ri_sample(self, ri_sample):
        self.ri_sample = ri_sample

    def get_reg_factor(self):
        return self.reg_factor

    def set_reg_factor(self, reg_factor):
        self.reg_factor = reg_factor

    def get_psf(self):
        return self.psf

    def set_psf(self, psf):
        self.psf = psf

    def deconvolve(self, image: "net.imglib2.RandomAccessibleInterval", psf=None):
        """Deconvolve images"""
        if self.ij == None:
            self._get_imagej_gateway()

        # convert image to float
        image_f = self.ij.op().convert().float32(image)

        # create synthetic PSF if none supplied.
        if self.psf == None:
            self.create_synthetic_psf(image)

        # deconvolve image
        image_decon = self.ij.op().namespace(_CreateNamespace()).img(image_f)
        self.ij.op().deconvolve().richardsonLucyTV(
            image_decon, image_f, self.psf, self.iterations, self.reg_factor
        )

        return image_decon

    def create_synthetic_psf(self, image: "net.imglib2.RandomAccessibleInterval"):
        """Create a synthetic PSF."""
        if self.ij == None:
            self._get_imagej_gateway()

        psf_dims = []
        for i in range(len(image.shape)):
            psf_dims.append(image.dimension(i))

        psf_size = _FinalDimensions()(psf_dims)
        psf = (
            self.ij.op()
            .namespace(_CreateNamespace())
            .kernelDiffraction(
                psf_size,
                self.numerical_aperture,
                self.wavelength,
                self.ri_sample,
                self.ri_immersion,
                self.lateral_res,
                self.axial_res,
                self.particle_pos,
                _FloatType()(),
            )
        )

        self.psf = psf

    def _get_imagej_gateway(self):
        try:
            from imagej import ij

            self.ij = ij
        except ImportError:
            print(f"PyImageJ has not been initialized.")


def image_conversion_check(imagej_instance):
    """
    Test ImageJ/ImgLib2 image conversions.
    """
    # get image classes
    ImagePlus = sj.jimport("ij.ImagePlus")
    Dataset = sj.jimport("net.imagej.Dataset")
    ImgPlus = sj.jimport("net.imagej.ImgPlus")
    Img = sj.jimport("net.imglib2.img.Img")
    RandomAccessibleInterval = sj.jimport("net.imglib2.RandomAccessibleInterval")

    # perform conversion checks
    image_classes = [Dataset, ImagePlus, ImgPlus, Img, RandomAccessibleInterval]
    for i in range(len(image_classes)):
        src_class = image_classes[i]
        dest_classes = image_classes.copy()
        dest_classes.remove(src_class)
        for j in range(len(dest_classes)):
            print(
                f"{src_class} [--->] {dest_classes[j]}: {imagej_instance.convert().supports(src_class, dest_classes[j])}"
            )


@lru_cache
def _CreateNamespace():
    return sj.jimport("net.imagej.ops.create.CreateNamespace")


@lru_cache
def _FinalDimensions():
    return sj.jimport("net.imglib2.FinalDimensions")


@lru_cache
def _FloatType():
    return sj.jimport("net.imglib2.type.numeric.real.FloatType")

@lru_cache
def _Views():
    return sj.jimport("net.imglib2.view.Views")
