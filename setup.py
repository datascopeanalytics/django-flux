import os
from distutils.core import setup
from setuptools import find_packages

# Here are a few resources that were useful in putting this together
#   * http://guide.python-distribute.org/creation.html
#   * http://bruno.im/2010/may/05/packaging-django-reusable-app/
#   * http://stackoverflow.com/questions/5360873/how-do-i-package-a-python-application-to-make-it-pip-installable

# read in the dependencies from the virtualenv requirements file
dependencies = []
filename = "REQUIREMENTS"
with open(filename, 'r') as stream:
    for line in stream:
        package = line.strip().split('#')[0]
        if package:
            dependencies.append(package)

setup(
    name="django-flux",
    version="0.1.0",
    description="locally fetch, store, and present social media flux",
    long_description=open('README.rst').read(),
    author="Dean Malmgren",
    author_email="dean.malmgren@datascopeanalytics.com",
    license="MIT, see LICENSE.rst",
    url="http://github.com/deanmalmgren/django-flux",
    install_requires=dependencies,
    packages=['flux'],
    install_package_data=True,
)
