from distutils.core import setup
from setuptools import find_packages

# Here are a few resources that were useful in putting this together
#   * http://guide.python-distribute.org/creation.html
#   * http://bruno.im/2010/may/05/packaging-django-reusable-app/
#   * http://stackoverflow.com/questions/5360873/how-do-i-package-a-python-application-to-make-it-pip-installable

setup(
    name="django-flux",
    version="0.1.0",
    description="locally fetch, store, and present social media flux",
    long_description=open('README.rst').read(),
    author="Dean Malmgren",
    author_email="dean.malmgren@datascopeanalytics.com",
    license="LICENSE.rst",
    url="http://github.com/deanmalmgren/django-flux",
    install_requires=[
        'Django >= 1.2.5',
        'python-twitter',
        # 'fbconsole',
        # 'mechanize',
        # 'python-linkedin',
    ],
    packages=['flux'],
    install_package_data=True,
)
