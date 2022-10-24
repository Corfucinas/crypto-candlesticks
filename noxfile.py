# -*- coding: utf-8 -*-
"""All Nox sessions."""

# built-in
import platform

# external
import nox
from nox.sessions import Session
from nox_poetry import session as poetry_session


nox.options.sessions = ('black', 'safety', 'mypy')

locations = (
    './src/crypto_candlesticks',
    './tests',
    './noxfile.py',
    './docs/conf.py',
)


@poetry_session(reuse_venv=True)
def black(session: Session) -> None:
    """Run black code formatter.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or locations
    session.install('black')
    session.run('black', *args)


@poetry_session(reuse_venv=True)
def lint(session: Session) -> None:
    """Lint using flake8.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or locations
    session.install('pre-commit', 'flakeheaven', 'wemake-python-styleguide')
    session.run('pre-commit', 'run', '--all-files', '--show-diff-on-failure')
    session.run('flakeheaven', 'lint', *args)


@poetry_session(reuse_venv=True)
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages.

    Args:
        session (Session): Session passed by Nox
    """
    operating_system = platform.system().lower()
    if operating_system != 'windows':
        session.install('safety')
        session.run(
            'safety',
            'check',
            '--file=poetry.lock',
            '--full-report',
        )


@poetry_session(reuse_venv=True)
def mypy(session: Session) -> None:
    """Type-check using mypy.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or locations
    session.install('mypy')
    session.run('mypy', '--ignore-missing-imports', *args)


@poetry_session(reuse_venv=True)
def tests(session: Session) -> None:
    """Run the test suite.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or ['--cov']
    session.run('poetry', 'install', '--only', 'test', external=True)
    session.run('pytest', '-s', '--durations=0', *args)


@poetry_session(reuse_venv=True)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest.

    Args:
        session (Session): Session passed by Nox
    """
    args = session.posargs or ['all']
    session.install('xdoctest', '.')
    session.run('xdoctest', 'crypto_candlesticks', *args)


@poetry_session(reuse_venv=True)
def coverage(session: Session) -> None:
    """Upload the coverage data.

    Args:
        session (Session):  Session passed by Nox
    """
    session.run('poetry', 'install', external=True)
    session.run('coverage', 'xml', '--fail-under=0')
    session.run('codecov', *session.posargs)


@poetry_session(reuse_venv=True)
def docs(session: Session) -> None:
    """Build the Sphinx documentation.

    Args:
        session (Session): Session passed by Nox
    """
    session.run('poetry', 'install', '--with', 'docs', external=True)
    session.run(
        'sphinx-apidoc',
        '--force',
        '--separate',
        '--module-first',
        '--implicit-namespaces',
        '-o',
        './docs/',
        './src/crypto_candlesticks/',
    )
    session.run('sphinx-autogen', '-a', '-o', './docs/', './docs/index.rst')
    session.run(
        'sphinx-build',
        '-b',
        'spelling',
        '-j',
        'auto',
        '-Tv',
        './docs',
        './docs/_build/html',
    )
    session.run(
        'sphinx-build',
        '-j',
        'auto',
        '-WTv',
        './docs',
        './docs/_build/html',
    )
