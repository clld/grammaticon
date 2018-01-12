from setuptools import setup, find_packages


requires = [
    'clldmpg>=1.1.0',
    'markdown',
    'waitress'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'mock==1.0.0',
]


setup(
    name='grammaticon',
    version='0.0',
    description='grammaticon',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    extras_require={
        'dev': ['flake8', 'waitress', 'psycopg2'],
        'test': [
            'tox',
            'mock',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    test_suite="grammaticon",
    entry_points="""\
[paste.app_factory]
main = grammaticon:main
""")
