from setuptools import setup

setup(
    name='gmailwrap',
    version='0.1',
    py_modules=['gmailwrap'],
    install_requires=[
        'Click',
        'email-validator',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ],
    entry_points='''
        [console_scripts]
        gmailwrap=gmailwrap:main
    ''',
)
