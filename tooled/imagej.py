import tooled.util
import scyjava as sj

from functools import lru_cache


class Deconvolution:
    """Deconvolve an image with ImageJ Ops implementation of Richardson Lucy.
    """
    def __init__(
        self,
        OpService,
        iterations=30,
        numerical_aperture=0.75,
        wavelength=550,
        xy_spacing=110,
        z_spacing=800,
        depth=0,
        reg_factor=0.01,
        ri_immersion=1.5,
        ri_sample=1.4,
    ):
        self.OpService = OpService
        self.iterations = iterations
        self.numerical_aperture = numerical_aperture
        self.wavelength = wavelength * 1e-9
        self.xy_spacing = xy_spacing * 1e-9
        self.z_spacing = z_spacing * 1e-9
        self.depth = depth
        self.reg_factor = reg_factor
        self.ri_immersion = ri_immersion
        self.ri_sample = ri_sample

    def get_config(self):
        """Return the current configuration for deconvolution
        """
        print("\nDeconvolution configuration")
        print(f"\tIterations: {self.iterations}")
        print(f"\tNA: {self.numerical_aperture}")
        print(f"\tWavelength: {self.wavelength}")
        print(f"\tXY spacing: {self.xy_spacing}")
        print(f"\tZ spacing: {self.z_spacing}")
        print(f"\tDepth: {self.depth}")
        print(f"\tReg factor:{self.reg_factor}")
        print(f"\tRi Immersion: {self.ri_immersion}")
        print(f"\tRi Sample: {self.ri_sample}\n")

    def set_config(self):
        return

    def deconvolve(self, image: "net.imglib2.RandomAccessibleInterval", psf=None):
        """Deconvolve images"""
        # convert image to float
        image_f = self.OpService.convert().float32(image)

        # create synthetic PSF if none supplied.
        if psf == None:
            psf = self._create_synthetic_psf(image)

        # deconvolve image
        image_decon = self.OpService.namespace(_CreateNamespace()).img(image_f)
        with tooled.util.Loader("Deconvolving image...", style='build'):
            self.OpService.deconvolve().richardsonLucyTV(
                image_decon, image_f, psf, self.iterations, self.reg_factor
            )

        return image_decon

    def _create_synthetic_psf(self, image: "net.imglib2.RandomAccessibleInterval"):
        psf_dims = []
        for i in range(len(image.shape)):
            psf_dims.append(image.dimension(i))

        psf_size = _FinalDimensions()(psf_dims)
        psf = self.OpService.namespace(_CreateNamespace()).kernelDiffraction(
            psf_size,
            self.numerical_aperture,
            self.wavelength,
            self.ri_sample,
            self.ri_immersion,
            self.xy_spacing,
            self.z_spacing,
            self.depth,
            _FloatType()(),
        )

        return psf


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


@lru_cache(maxsize=None)
def _CreateNamespace():
    return sj.jimport("net.imagej.ops.create.CreateNamespace")


@lru_cache(maxsize=None)
def _FinalDimensions():
    return sj.jimport("net.imglib2.FinalDimensions")


@lru_cache(maxsize=None)
def _FloatType():
    return sj.jimport("net.imglib2.type.numeric.real.FloatType")
