#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Radim Rehurek <radimrehurek@seznam.cz>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
Run with:

sudo python ./setup.py install
"""

import os
import platform
import sys
import warnings
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

PY2 = sys.version_info[0] == 2

if sys.version_info[:2] < (2, 7) or ((3, 0) <= sys.version_info[:2] < (3, 5)):
    raise Exception('This version of gensim needs Python 2.7, 3.5 or later.')

# the following code is adapted from tornado's setup.py:
# https://github.com/tornadoweb/tornado/blob/master/setup.py
# to support installing without the extension on platforms where
# no compiler is available.


class custom_build_ext(build_ext):
    """Allow C extension building to fail.

    The C extension speeds up word2vec and doc2vec training, but is not essential.
    """

    warning_message = """
********************************************************************
WARNING: %s could not
be compiled. No C extensions are essential for gensim to run,
although they do result in significant speed improvements for some modules.
%s

Here are some hints for popular operating systems:

If you are seeing this message on Linux you probably need to
install GCC and/or the Python development package for your
version of Python.

Debian and Ubuntu users should issue the following command:

    $ sudo apt-get install build-essential python-dev

RedHat, CentOS, and Fedora users should issue the following command:

    $ sudo yum install gcc python-devel

If you are seeing this message on OSX please read the documentation
here:

http://api.mongodb.org/python/current/installation.html#osx
********************************************************************
"""

    def run(self):
        try:
            build_ext.run(self)
        except Exception:
            e = sys.exc_info()[1]
            sys.stdout.write('%s\n' % str(e))
            warnings.warn(
                self.warning_message +
                "Extension modules" +
                "There was an issue with your platform configuration - see above.")

    def build_extension(self, ext):
        name = ext.name
        try:
            build_ext.build_extension(self, ext)
        except Exception:
            e = sys.exc_info()[1]
            sys.stdout.write('%s\n' % str(e))
            warnings.warn(
                self.warning_message +
                "The %s extension module" % (name,) +
                "The output above this warning shows how the compilation failed.")

    # the following is needed to be able to add numpy's include dirs... without
    # importing numpy directly in this script, before it's actually installed!
    # http://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
    def finalize_options(self):
        build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        # https://docs.python.org/2/library/__builtin__.html#module-__builtin__
        if isinstance(__builtins__, dict):
            __builtins__["__NUMPY_SETUP__"] = False
        else:
            __builtins__.__NUMPY_SETUP__ = False

        import numpy
        self.include_dirs.append(numpy.get_include())


model_dir = os.path.join(os.path.dirname(__file__), 'gensim', 'models')
gensim_dir = os.path.join(os.path.dirname(__file__), 'gensim')

cmdclass = {'build_ext': custom_build_ext}

WHEELHOUSE_UPLOADER_COMMANDS = {'fetch_artifacts', 'upload_all'}
if WHEELHOUSE_UPLOADER_COMMANDS.intersection(sys.argv):
    import wheelhouse_uploader.cmd
    cmdclass.update(vars(wheelhouse_uploader.cmd))


LONG_DESCRIPTION = u"""
==============================================
gensim -- Topic Modelling in Python
==============================================

|Travis|_
|Wheel|_

.. |Travis| image:: https://img.shields.io/travis/RaRe-Technologies/gensim/develop.svg
.. |Wheel| image:: https://img.shields.io/pypi/wheel/gensim.svg

.. _Travis: https://travis-ci.org/RaRe-Technologies/gensim
.. _Downloads: https://pypi.python.org/pypi/gensim
.. _License: http://radimrehurek.com/gensim/about.html
.. _Wheel: https://pypi.python.org/pypi/gensim

Gensim is a Python library for *topic modelling*, *document indexing* and *similarity retrieval* with large corpora.
Target audience is the *natural language processing* (NLP) and *information retrieval* (IR) community.

Features
---------

* All algorithms are **memory-independent** w.r.t. the corpus size (can process input larger than RAM, streamed, out-of-core),
* **Intuitive interfaces**

  * easy to plug in your own input corpus/datastream (trivial streaming API)
  * easy to extend with other Vector Space algorithms (trivial transformation API)

* Efficient multicore implementations of popular algorithms, such as online **Latent Semantic Analysis (LSA/LSI/SVD)**,
  **Latent Dirichlet Allocation (LDA)**, **Random Projections (RP)**, **Hierarchical Dirichlet Process (HDP)**  or **word2vec deep learning**.
* **Distributed computing**: can run *Latent Semantic Analysis* and *Latent Dirichlet Allocation* on a cluster of computers.
* Extensive `documentation and Jupyter Notebook tutorials <https://github.com/RaRe-Technologies/gensim/#documentation>`_.


If this feature list left you scratching your head, you can first read more about the `Vector
Space Model <http://en.wikipedia.org/wiki/Vector_space_model>`_ and `unsupervised
document analysis <http://en.wikipedia.org/wiki/Latent_semantic_indexing>`_ on Wikipedia.

Installation
------------

This software depends on `NumPy and Scipy <http://www.scipy.org/Download>`_, two Python packages for scientific computing.
You must have them installed prior to installing `gensim`.

It is also recommended you install a fast BLAS library before installing NumPy. This is optional, but using an optimized BLAS such as `ATLAS <http://math-atlas.sourceforge.net/>`_ or `OpenBLAS <http://xianyi.github.io/OpenBLAS/>`_ is known to improve performance by as much as an order of magnitude. On OS X, NumPy picks up the BLAS that comes with it automatically, so you don't need to do anything special.

The simple way to install `gensim` is::

    pip install -U gensim

Or, if you have instead downloaded and unzipped the `source tar.gz <http://pypi.python.org/pypi/gensim>`_ package,
you'd run::

    python setup.py test
    python setup.py install


For alternative modes of installation (without root privileges, development
installation, optional install features), see the `install documentation <http://radimrehurek.com/gensim/install.html>`_.

This version has been tested under Python 2.7, 3.5 and 3.6. Support for Python 2.6, 3.3 and 3.4 was dropped in gensim 1.0.0. Install gensim 0.13.4 if you *must* use Python 2.6, 3.3 or 3.4. Support for Python 2.5 was dropped in gensim 0.10.0; install gensim 0.9.1 if you *must* use Python 2.5). Gensim's github repo is hooked against `Travis CI for automated testing <https://travis-ci.org/RaRe-Technologies/gensim>`_ on every commit push and pull request.

How come gensim is so fast and memory efficient? Isn't it pure Python, and isn't Python slow and greedy?
--------------------------------------------------------------------------------------------------------

Many scientific algorithms can be expressed in terms of large matrix operations (see the BLAS note above). Gensim taps into these low-level BLAS libraries, by means of its dependency on NumPy. So while gensim-the-top-level-code is pure Python, it actually executes highly optimized Fortran/C under the hood, including multithreading (if your BLAS is so configured).

Memory-wise, gensim makes heavy use of Python's built-in generators and iterators for streamed data processing. Memory efficiency was one of gensim's `design goals <http://radimrehurek.com/gensim/about.html>`_, and is a central feature of gensim, rather than something bolted on as an afterthought.

Documentation
-------------
* `QuickStart`_
* `Tutorials`_
* `Tutorial Videos`_
* `Official Documentation and Walkthrough`_

Citing gensim
-------------

When `citing gensim in academic papers and theses <https://scholar.google.cz/citations?view_op=view_citation&hl=en&user=9vG_kV0AAAAJ&citation_for_view=9vG_kV0AAAAJ:u-x6o8ySG0sC>`_, please use this BibTeX entry::

  @inproceedings{rehurek_lrec,
        title = {{Software Framework for Topic Modelling with Large Corpora}},
        author = {Radim {\\v R}eh{\\r u}{\\v r}ek and Petr Sojka},
        booktitle = {{Proceedings of the LREC 2010 Workshop on New
             Challenges for NLP Frameworks}},
        pages = {45--50},
        year = 2010,
        month = May,
        day = 22,
        publisher = {ELRA},
        address = {Valletta, Malta},
        language={English}
  }

----------------

Gensim is open source software released under the `GNU LGPLv2.1 license <http://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>`_.
Copyright (c) 2009-now Radim Rehurek

|Analytics|_

.. |Analytics| image:: https://ga-beacon.appspot.com/UA-24066335-5/your-repo/page-name
.. _Analytics: https://github.com/igrigorik/ga-beacon
.. _Official Documentation and Walkthrough: http://radimrehurek.com/gensim/
.. _Tutorials: https://github.com/RaRe-Technologies/gensim/blob/develop/tutorials.md#tutorials
.. _Tutorial Videos: https://github.com/RaRe-Technologies/gensim/blob/develop/tutorials.md#videos
.. _QuickStart: https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/gensim%20Quick%20Start.ipynb

"""

#
# 1.11.3 is the oldest version of numpy that we support, for historical reasons.
# 1.16.1 is the last numpy version to support Py2.
#
# Similarly, 4.6.4 is the last pytest version to support Py2.
#
# https://docs.scipy.org/doc/numpy/release.html
# https://docs.pytest.org/en/latest/py27-py34-deprecation.html
#
if PY2:
    NUMPY_STR = 'numpy >= 1.11.3, <= 1.16.1'
    PYTEST_STR = 'pytest == 4.6.4'
else:
    NUMPY_STR = 'numpy >= 1.11.3'
    PYTEST_STR = 'pytest'

distributed_env = ['Pyro4 >= 4.27']

win_testenv = [
    PYTEST_STR,
    'pytest-rerunfailures',
    'mock',
    'cython',
    # temporarily remove pyemd to work around appveyor issues
    # 'pyemd',
    'testfixtures',
    'Morfessor==2.0.2a4',
    'python-Levenshtein >= 0.10.2',
    'visdom >= 0.1.8, != 0.1.8.7',
]

if sys.version_info[:2] == (2, 7):
    #
    # 0.20.3 is the last version of scikit-learn that supports Py2.
    # Similarly, for version 5.1.1 of tornado.  We require tornado indirectly
    # via visdom.
    #
    win_testenv.append('scikit-learn==0.20.3')
    win_testenv.append('tornado==5.1.1')
else:
    win_testenv.append('scikit-learn')


linux_testenv = win_testenv[:]

if sys.version_info < (3, 7):
    linux_testenv.extend([
        'tensorflow <= 1.3.0',
        'keras >= 2.0.4, <= 2.1.4',
        'annoy',
    ])

if (3, 0) < sys.version_info < (3, 7):
    linux_testenv.extend(['nmslib'])

docs_testenv = linux_testenv + distributed_env + [
    'sphinx',
    'sphinxcontrib-napoleon',
    'plotly',
# Pattern's version is specified to install Pattern 3.6, which adds python3 support
    'Pattern >= 3.6',
    'sphinxcontrib.programoutput',
]
#
# Get Py2.7 docs to build, see https://github.com/RaRe-Technologies/gensim/pull/2552
#
if sys.version_info == (2, 7):
    docs_testenv.insert(0, 'doctools==0.14')

ext_modules = [
    Extension('gensim.models.word2vec_inner',
        sources=['./gensim/models/word2vec_inner.c'],
        include_dirs=[model_dir]),
    Extension('gensim.models.doc2vec_inner',
        sources=['./gensim/models/doc2vec_inner.c'],
        include_dirs=[model_dir]),
    Extension('gensim.corpora._mmreader',
        sources=['./gensim/corpora/_mmreader.c']),
    Extension('gensim.models.fasttext_inner',
        sources=['./gensim/models/fasttext_inner.c'],
        include_dirs=[model_dir]),
    Extension('gensim.models._utils_any2vec',
        sources=['./gensim/models/_utils_any2vec.c'],
        include_dirs=[model_dir]),
    Extension('gensim._matutils',
        sources=['./gensim/_matutils.c']),
    Extension('gensim.models.nmf_pgd',
        sources=['./gensim/models/nmf_pgd.c'])
]

if not (os.name == 'nt' and sys.version_info[0] < 3):
    extra_args = []
    system = platform.system()

    if system == 'Linux':
        extra_args.append('-std=c++11')
    elif system == 'Darwin':
        extra_args.extend(['-stdlib=libc++', '-std=c++11'])

    ext_modules.append(
        Extension('gensim.models.word2vec_corpusfile',
                  sources=['./gensim/models/word2vec_corpusfile.cpp'],
                  language='c++',
                  extra_compile_args=extra_args,
                  extra_link_args=extra_args)
    )

    ext_modules.append(
        Extension('gensim.models.fasttext_corpusfile',
                  sources=['./gensim/models/fasttext_corpusfile.cpp'],
                  language='c++',
                  extra_compile_args=extra_args,
                  extra_link_args=extra_args)
    )

    ext_modules.append(
        Extension('gensim.models.doc2vec_corpusfile',
                  sources=['./gensim/models/doc2vec_corpusfile.cpp'],
                  language='c++',
                  extra_compile_args=extra_args,
                  extra_link_args=extra_args)
    )

setup(
    name='gensim',
    version='3.8.1',
    description='Python framework for fast Vector Space Modelling',
    long_description=LONG_DESCRIPTION,

    ext_modules=ext_modules,
    cmdclass=cmdclass,
    packages=find_packages(),

    author=u'Radim Rehurek',
    author_email='me@radimrehurek.com',

    url='http://radimrehurek.com/gensim',
    download_url='http://pypi.python.org/pypi/gensim',

    license='LGPLv2.1',

    keywords='Singular Value Decomposition, SVD, Latent Semantic Indexing, '
        'LSA, LSI, Latent Dirichlet Allocation, LDA, '
        'Hierarchical Dirichlet Process, HDP, Random Projections, '
        'TFIDF, word2vec',

    platforms='any',

    zip_safe=False,

    classifiers=[  # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],

    test_suite="gensim.test",
    setup_requires=[
        NUMPY_STR,
    ],
    install_requires=[
        NUMPY_STR,
        'scipy >= 0.18.1',
        'six >= 1.5.0',
        'smart_open >= 1.8.1',
    ],
    tests_require=linux_testenv,
    extras_require={
        'distributed': distributed_env,
        'test-win': win_testenv,
        'test': linux_testenv,
        'docs': docs_testenv,
    },

    include_package_data=True,
)
