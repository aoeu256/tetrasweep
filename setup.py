#@PydevCodeAnalysisIgnore
from distutils.core import setup
#import py2exe
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
#	console = ['system.py'],
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("helloworld", ["helloworld.pyx"])]
)