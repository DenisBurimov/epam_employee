from setuptools import setup, find_packages

"""
These install requirements are to install on Ubuntu 20.04.
If you want to get this app up and running on any other os,
you should replace 'mysqlclient' by the specific driver for certain os.

Except this, mysql doesn't deploy to the linux server automatically,
without next operations:

sudo apt install python3-dev build-essential

sudo apt install libssl1.1

sudo apt install libssl1.1=1.1.1f-1ubuntu2

sudo apt install libssl-dev

sudo apt install libmysqlclient-dev
"""

setup(
    name='epam_employee',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Bcrypt-Flask',
        'Flask-Login',
        'Flask-WTF',
        'email-validator',
        'mysqlclient',
        'mysqlserver'
    ]
)