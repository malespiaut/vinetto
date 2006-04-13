from distutils.core import setup
setup (name='vinetto',
    version='0.04pre-alpha',
    scripts=['vinetto'],
    data_files=[('/usr/share/vinetto', ['res/header', 'res/huffman', 'res/quantization'])],
    description='vinetto : a forensics tool to examine Thumbs.db files.',
    author='Michel Roukine',
    author_email='rukin@users.sf.net',
    url='http://vinetto.sourceforge.net/',
    license='GNU GPL',
    platforms='LINUX',
)
