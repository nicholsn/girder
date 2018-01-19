# -*- coding: utf-8 -*-

import os
import pkg_resources

import sphinx_rtd_theme
from sphinx.domains.python import PythonDomain

needs_sphinx = '1.6'


for _package_location in [
        '..',  # girder
        os.path.join('..', 'clients', 'python')  # girder_client
    ]:
    print os.path.abspath(os.path.join(os.path.dirname(__file__), _package_location))

    print os.listdir(_package_location)

    print list(pkg_resources.find_distributions(
        os.path.abspath(os.path.join(os.path.dirname(__file__), _package_location))
    ))

_packages = [
    # next(pkg_resources.find_distributions(
    #     os.path.abspath(os.path.join(os.path.dirname(__file__), _package_location)),
    #     only=True
    # ))
    # for _package_location in [
    #     '..',  # girder
    #     os.path.join('..', 'clients', 'python')  # girder_client
    # ]
]
_requirements = {
    _requirement.project_name.lower()
    for _package in _packages
    for _requirement in _package.requires(_package.extras)
}
for _package in _packages:
    # Add the package to sys.path, so autodoc can import it
    _package.activate()

# Add importable module names that are different from package names
_requirements |= {
    'botocore',
    'bson',
    'dateutil',
    'requests_toolbelt',
    'yaml'
}
# The funcsigs package (only used in Python2) is necessary to ensure import-time logic in girder
# executes correctly. For some reason (which doesn't apply to six), mocking it interferes with its
# import, even if it's installed.
_requirements.discard('funcsigs')

master_doc = 'index'

project = u'Girder'
copyright = u'2014-2018, Kitware, Inc.'
release = _packages[0].version
version = '.'.join(release.split('.')[:2])

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_favicon = 'favicon.ico'

latex_documents = [
    ('index', 'Girder.tex', u'Girder Documentation', u'Kitware, Inc.', 'manual'),
]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode'
]

autodoc_mock_imports = list(_requirements)

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pymongo': ('https://api.mongodb.com/python/current/', None)
}


# Override the resolution of some targets
class PatchedPythonDomain(PythonDomain):
    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        # References to "list" may ambiguously resolve to several Girder methods named "list",
        # instead of just the built-in Python 'list' (due to the mechanism described at
        # http://www.sphinx-doc.org/en/stable/domains.html#role-py:obj ). This results in incorrect
        # xrefs and causes Sphinx to emit warnings. So, rather than require all references to
        # explicitly name ":py:obj:`list`", override this method to do the right thing.
        if target == 'list':
            # References to built-in symbols natively return None
            return None
        return super(PatchedPythonDomain, self).resolve_xref(
            env, fromdocname, builder, typ, target, node, contnode)


def setup(sphinx):
    sphinx.override_domain(PatchedPythonDomain)
