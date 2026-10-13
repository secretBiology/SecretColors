# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("_ext"))

from SecretColors import __version__ as release  # noqa: E402

project = "SecretColors"
author = "Rohit Suratekar"
copyright = f"2019-{date.today().year}, {author}"
version = ".".join(release.split(".")[:2])

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "swatches",
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
language = "en"
exclude_patterns = ["_build"]

myst_enable_extensions = ["colon_fence", "deflist", "attrs_inline",
                          "attrs_block"]
myst_heading_anchors = 3

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_google_docstring = False
napoleon_numpy_docstring = False

copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
}

html_theme = "furo"
html_title = f"SecretColors {release}"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_favicon = "_static/favicon.png"
html_theme_options = {
    "light_logo": "logo-light.png",
    "dark_logo": "logo-dark.png",
    "sidebar_hide_name": True,
    "source_repository": "https://github.com/secretBiology/SecretColors/",
    "source_branch": "master",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#0f62fe",
        "color-brand-content": "#0f62fe",
        "color-brand-visited": "#8a3ffc",
        "font-stack--headings": "'Helvetica Neue', Helvetica, Arial, "
                                "sans-serif",
    },
    "dark_css_variables": {
        "color-brand-primary": "#78a9ff",
        "color-brand-content": "#78a9ff",
        "color-brand-visited": "#be95ff",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/secretBiology/SecretColors",
            "html": '<svg stroke="currentColor" fill="currentColor" '
                    'stroke-width="0" viewBox="0 0 16 16"><path '
                    'fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 '
                    '2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-'
                    '.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-'
                    '1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 '
                    '1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64'
                    '-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08'
                    '-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 '
                    '1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.'
                    '08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 '
                    '3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21'
                    '.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z">'
                    '</path></svg>',
            "class": "",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/SecretColors/",
            "html": '<svg viewBox="0 0 24 24" fill="currentColor"><path '
                    'd="M12 2 3 7v10l9 5 9-5V7l-9-5Zm0 2.3 6.6 3.7L12 11.7 '
                    '5.4 8 12 4.3ZM5 9.7l6 3.4v6.6l-6-3.4V9.7Zm8 10v-6.6l6-'
                    '3.4v6.6l-6 3.4Z"/></svg>',
            "class": "",
        },
    ],
}
pygments_style = "default"
pygments_dark_style = "monokai"

latex_documents = [
    (master_doc, "SecretColors.tex", "SecretColors Documentation", author,
     "manual"),
]
epub_title = project
epub_exclude_files = ["search.html"]
