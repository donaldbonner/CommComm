from setuptools import setup, find_packages
setup{
	name = 'CommComm'
	version = '1.0'
	packages = find_packages(),
	scripts = ['CommComm.py', 'tcp_client_b.py', 'tcp_server_b.py', 'discover.py']
}
setup(
	name = 'CommComm',
	version = '1.0',
	packages = find_packages(),
	scripts = ['CommComm.py', 'tcp_client_b.py', 'tcp_server_b.py', 'discover.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],
"""
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    }
"""
    # metadata for upload to PyPI
    author = "DJ Bonner",
    author_email = "donsbons@gmail.com",
    description = "Common Communication over a local area network",
    license = "LOL!",
    keywords = "TCP python bonjour chat message local network",
    url = "https://github.com/donaldbonner/CommComm",   # project home page

    # could also include long_description, download_url, classifiers, etc.
)
