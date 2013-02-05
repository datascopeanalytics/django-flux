#!/usr/bin/env python

import os
from distutils.core import setup
from setuptools import find_packages

# Here are a few resources that were useful in putting this together
#   * http://guide.python-distribute.org/creation.html
#   * http://bruno.im/2010/may/05/packaging-django-reusable-app/
#   * http://stackoverflow.com/questions/5360873/how-do-i-package-a-python-application-to-make-it-pip-installable
#   * http://blog.nyaruka.com/adding-a-django-app-to-pythons-cheese-shop-py

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# read in the dependencies from the virtualenv requirements file
dependencies = []
filename = "REQUIREMENTS"
with open(filename, 'r') as stream:
    for line in stream:
        package = line.strip().split('#')[0]
        if package:
            dependencies.append(package)

# get a list of all the packages to include in scr_dir. inspiration
# from the django setup.py
src_dir = 'flux'
packages = []
#data_files = []
package_data = {src_dir:[]}
for dirpath, dirnames, filenames in os.walk(src_dir):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.') or dirname == '__pycache__':
            del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        # data_files.append([dirpath, 
        #                    [os.path.join(dirpath, f) for f in filenames]])
        package_data[src_dir].extend([os.path.join(dirpath, f) 
                                      for f in filenames])

github_url = "http://github.com/datascopeanalytics/django-flux"

setup(
    name="django-flux",
    version=__import__("flux").__version__,
    description="locally fetch, store, and present social media flux",
    long_description=open('README.rst').read(),
    author="Dean Malmgren",
    author_email="dean.malmgren@datascopeanalytics.com",
    license="MIT, see LICENSE.rst",
    url=github_url,
    download_url="%s/archives/master" % github_url,
    install_requires=dependencies,
    packages=packages,
    package_data=package_data,
    include_package_data=True,

    # # data files are installed on the system path. for details see
    # # http://docs.python.org/2/distutils/setupscript.html#installing-additional-files
    # data_files=data_files,
)
