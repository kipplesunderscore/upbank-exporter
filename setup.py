from setuptools import setup

setup(
    name='upbank_csv',
    version='0.1',
    description='',
    author='kipplesunderscore',
    author_email='kipplesunderscore+github@kipples.net',
    packages=['upbank_csv'],
    install_requires=['requests', 'datetime'],
    entry_points = {
        'console_scripts': ['upbank-export=upbank_csv.upbank_csv:main']
    }
)
