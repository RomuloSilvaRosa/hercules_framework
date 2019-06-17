import setuptools
from setuptools import find_packages

import hercules_framework


def long_description():
    with open('README.md', encoding='utf8') as f:
        return f.read()


INSTALL_REQUIRES = ['python-dateutil==2.7.5', 'python-decouple==3.1', 'redis==3.0.1',
                    'tornado==5.1.1', 'boto3==1.9.86', 'boto3-type-annotations==0.3.0',
                    'stringcase==1.2.0', 'elastic-apm==3.0.4', 'dataslots==1.0.1', 'requests==2.*']
INSTALL_REQUIRES_DEV = ['coverage>=4.4.1', 'colour_runner>=0.0.5', 'flake8>=3.3.0',
                        'xmlrunner==1.7.7', 'coverage-badge>=0.2.0', 'flake8-html>=0.4.0',
                        'pylint>=1.9.2', 'anybadge==1.1.1', 'bandit==1.5.1']


setuptools.setup(
    name='hercules_framework',
    version=hercules_framework.__version__,

    url='https://github.com/romulosilvarosa/hercules_framework',
    description='Biblioteca de ferramentas do projeto Hercules.',
    long_description=long_description(),

    author='Romulo Rosa',
    author_email='romulo.rosa@furg.br',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],

    include_package_data=True,
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    install_requires=[INSTALL_REQUIRES],
    extras_require={'tests': INSTALL_REQUIRES_DEV},
)
