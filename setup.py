import os
import shutil
from subprocess import run
from distutils.cmd import Command

from setuptools import setup,find_packages

__version__ = __import__("autogame").__version__


def rm(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


class CDocsCommand(Command):
    SPHINX_APIDOC = "sphinx-apidoc"
    MAKE = "make"
    description = "generate API documents automatically"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        rm("docs/build")
        rm("docs/source/__api")
        run([self.SPHINX_APIDOC, "-o", "source/__api", "../autogame","-fMeT"], cwd="docs")
        run([self.MAKE, "html"], cwd="docs")


with open("README.md") as f:
    long_description = f.read()

setup(
    name='autogame',
    author="Invoker",
    author_email="invoker-bot@outlook.com",
    description="A python framework for automatic game playing, which can be used to develop automatic game scripts.",
    keywords="automatic game python development script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "tensorflow",
    ],
    tests_require=[],
    setup_requires=[
        "sphinx",
        "sphinx-rtd-theme",
    ],
    extras_require={
        "gpu": "tensorflow-gpu",
        ":sys_platform == 'win32'": [],
    },
    url="https://github.com/invokerrrr/autogame-python",
    license="MIT",
    download_url="https://github.com/invokerrrr/autogame-python/archive/main.zip",
    # project_urls={"Documentation": "",},
    classifiers=[  # see https://pypi.org/pypi?:action=list_classifiers
        "Development Status :: 1 - Planning",
        # Development Status :: 1 - Planning
        # Development Status :: 2 - Pre-Alpha
        # Development Status :: 3 - Alpha
        # Development Status :: 4 - Beta
        # Development Status :: 5 - Production/Stable
        # Development Status :: 6 - Mature
        # Development Status :: 7 - Inactive
        "Environment :: Console",
        "Environment :: GPU",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
    is_pure=True,
    zip_safe=True,
    platforms="any",
    cmdclass={
        'docs': CDocsCommand
    }
)
