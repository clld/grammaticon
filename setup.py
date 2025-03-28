from setuptools import setup, find_packages


setup(
    name='grammaticon',
    version='0.0',
    description='grammaticon',
    long_description='',
    install_requires=[
        'csvw',
        'clld>=9.2.1',
        'clldmpg>=4.2',
        'markdown',
        'sqlalchemy<2.0',
        'waitress',
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox',
            'psycopg2',
        ],
        'test': [
            'mock',
            'pytest>=3.6',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="grammaticon",
    entry_points="""\
[paste.app_factory]
main = grammaticon:main
""")
