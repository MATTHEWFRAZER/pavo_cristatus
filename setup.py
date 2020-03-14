import os

from setuptools import setup, find_packages

package_name = "pavo_cristatus"
requirements_file = "requirements.txt"
if not os.path.exists(requirements_file):
      # when we deploy this, this is where requirements.txt will be
      requirements_file = os.path.join("{0}.egg-info".format(package_name), "requires.txt")

with open(requirements_file) as req:
    # handles custom package repos
    requirements = [requirement for requirement in req.read().splitlines() if not requirement.startswith("-")]

setup(name=package_name,
      install_requires=requirements,
      description="type hints ide plugin",
      keywords="ide plugin",
      url="https://github.com/MATTHEWFRAZER/pavo_cristatus",
      author="Matthew Frazer",
      author_email="mfrazeriguess@gmail.com",
      packages=find_packages(),
      include_package_data=False,
      zip_safe=False,
      version="1.0.0",
      classifiers=[
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            ]
      )


