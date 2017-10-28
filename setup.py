from setuptools import setup

setup(
    name="cfcli",
    version='0.0.1',
    py_modules=['cfcli'],
    install_requires=[
        'Click', 'Cloudflare'
    ],
    entry_points='''
        [console_scripts]
        cfcli=cfcli.cli:cli
    ''',
)