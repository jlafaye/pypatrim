from distutils.core import setup

entry_points = {
    'console_scripts': [
        'patrim-pdf2csv = patrim.cli:run_pdf_to_csv'
    ]
}

setup(name='pypatrim',
    version='0.1',
    description='Helper package to process & parse real estate '
                'transaction files from French Governement Patrim website',
    author='Julien Lafaye',
    author_email='jlafaye@gmail.com',
    packages=['patrim'],
    entry_points=entry_points,
    install_requires=[
        'pandas', 'textract',
        'numpy', 'requests',
        'gmaps'
    ]
)
