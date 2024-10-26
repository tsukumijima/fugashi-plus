import pathlib
import setuptools
import sys
from setuptools import setup, Extension

from fugashi_util import check_libmecab

# get the build parameters
if sys.argv[1] == "sdist":
    # hack for automated builds
    output, data_files = [], []
else:
    output, data_files = check_libmecab()

# pad the list in case something's missing
mecab_config = list(output) + ([""] * 5)
include_dirs = mecab_config[0].split()
library_dirs = mecab_config[1].split()
libraries = mecab_config[2].split()
extra_objects = mecab_config[3].split()
extra_link_args = mecab_config[4].split()

extensions = Extension(
    "fugashi.fugashi",
    ["fugashi/fugashi.pyx"],
    libraries=libraries,
    library_dirs=library_dirs,
    include_dirs=include_dirs,
    extra_objects=extra_objects,
    extra_link_args=extra_link_args,
)

setup(
    name="fugashi-plus",
    use_scm_version=True,
    author="Paul O'Leary McCann",
    author_email="polm@dampfkraft.com",
    description="A Cython MeCab wrapper for fast, pythonic Japanese tokenization and morphological analysis with additional improvements.",
    long_description=pathlib.Path("README.md").read_text("utf8"),
    long_description_content_type="text/markdown",
    url="https://github.com/tsukumijima/fugashi-plus",
    packages=setuptools.find_packages(),
    package_data={
        "fugashi": [
            "py.typed",
            "fugashi.pyi",
        ],
    },
    zip_safe=False,  # Required for type hints to work
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Japanese",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Cython",
        "Topic :: Text Processing :: Linguistic",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    ext_modules=[extensions],
    data_files=data_files,
    entry_points={
        "console_scripts": [
            "fugashi = fugashi.cli:main",
            "fugashi-info = fugashi.cli:info",
            "fugashi-build-dict = fugashi.cli:build_dict",
        ],
    },
    extras_require={
        "unidic": ["unidic"],
        "unidic-lite": ["unidic-lite"],
    },
    setup_requires=["wheel", "Cython>=3.0.0", "setuptools_scm"],
)
