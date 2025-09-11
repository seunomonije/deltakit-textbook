from __future__ import annotations

project = "deltakit-textbook"
copyright = "2025, Riverlane Ltd"
author = "Riverlane Ltd"
version = "0.0.1"

extensions = [
    "myst_nb",
    "sphinx_copybutton",
    "sphinx_book_theme",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_design",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "colon_fence",
]

source_suffix = [".rst", ".md"]
exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    ".venv",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = ""
html_theme = "sphinx_book_theme"
# html_logo = "_static/logo-wide.svg"
# html_favicon = "_static/logo-square.svg"
html_theme_options = {
    "github_url": "https://github.com/deltakit/deltakit-textbook",
    "repository_url": "https://github.com/deltakit/deltakit-textbook",
    "repository_branch": "main",
    "home_page_in_toc": True,
    "path_to_docs": "docs",
    "show_navbar_depth": 1,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "use_repository_button": True,
    "use_download_button": True,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "notebook_interface": "classic",
    },
    "navigation_with_keys": False,
    # Move page ToC into the left sidebar and remove the right one
    "show_nav_level": 1,
    "show_toc_level": 1,
    "secondary_sidebar_items": [],  # hide right sidebar
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
templates_path = ["_templates"]
html_css_files = ["overrides.css"]
html_sidebars = {
    "**": [
        "sbt-sidebar-nav.html",
        "page-toc.html",   # ← moves "On this page" into the left sidebar
    ]
}

copybutton_selector = "div:not(.output) > div.highlight pre"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

nitpick_ignore = [
    ("py:class", "_io.StringIO"),
    ("py:class", "_io.BytesIO"),
]

always_document_param_types = True
jupyter_execute_notebooks = 'off'
nb_execution_timeout = 60
