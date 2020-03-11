from setuptools import setup, find_packages

setup(
    name='grammaticon',
    version='0.0',
    description='grammaticon',
    long_description='',
    install_requires = [
        'clld>=4.0',
        'clldmpg>=3.1.1',
        'markdown',
        'sqlalchemy',
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
            'pytest>=3.1',
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
