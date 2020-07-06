# -*- coding: utf-8 -*-
"""All Nox sessions."""
# Special thanks to Claudio Jolowicz and his series Hypermodern Python
# https://cjolowicz.github.io/posts/hypermodern-python-01-setup/

import tempfile
from typing import Any

import nox
from nox.sessions import Session

package = 'crypto_candlesticks'
nox.options.sessions = (
    'xdoctest',
    'safety',
    'tests',
)
locations = (
    'src',
    'tests',
    'noxfile.py',
    'docs/conf.py',
)


def install_with_constraints(  # type: ignore
    session: Session, *args: str, **kwargs: Any,
) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.

    """
    with tempfile.NamedTemporaryFile(delete=True) as requirements:
        session.run(
            'poetry',
            'export',
            '--dev',
            '--format=requirements.txt',
            f'--output={requirements.name}',
            external=True,
        )
        session.install(
            f'--constraint={requirements.name}', *args, **kwargs,
        )


@nox.session(python='3.8')  # type: ignore
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(
        session, 'black',
    )
    session.run(
        'black', *args,
    )


@nox.session(python='3.8')  # type: ignore
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        'flake8',
        'flake8-annotations',
        'flake8-bandit',
        'flake8-black',
        'flake8-bugbear',
        'flake8-docstrings',
        'flake8-import-order',
        'darglint',
    )
    session.run(
        'flake8', *args,
    )


@nox.session(python='3.8')  # type: ignore
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile(delete=True) as requirements:
        session.run(
            'poetry',
            'export',
            '--dev',
            '--format=requirements.txt',
            '--without-hashes',
            f'--output={requirements.name}',
            external=True,
        )
        install_with_constraints(
            session, 'safety',
        )
        session.run(
            'safety', 'check', f'--file={requirements.name}', '--full-report',
        )


@nox.session(python='3.8')  # type: ignore
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(
        session, 'mypy',
    )
    session.run(
        'mypy', *args,
    )


@nox.session(python='3.8')  # type: ignore
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or [
        '--cov',
    ]
    session.run('poetry', 'install', '--no-dev', external=True)
    install_with_constraints(
        session, 'coverage[toml]', 'pytest', 'pytest-cov', 'pytest-mock',
    )
    session.run(
        'pytest', *args,
    )


@nox.session(python='3.8')  # type: ignore
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ['all']
    session.run('poetry', 'install', '--no-dev', external=True)
    install_with_constraints(
        session, 'xdoctest',
    )
    session.run(
        'python', '-m', 'xdoctest', package, *args,
    )


@nox.session(python='3.8')  # type: ignore
def coverage(session: Session) -> None:
    """Upload the coverage data."""
    session.run('poetry', 'install', external=True)
    session.run('coverage', 'xml', '--fail-under=0')
    session.run('codecov', *session.posargs)


@nox.session(python='3.8')  # type: ignore
def docs(session: Session) -> None:
    """Build the Sphinx documentation."""
    session.run('poetry', 'install', '--no-dev', external=True)
    install_with_constraints(
        session, 'sphinx', 'sphinx-autodoc-typehints',
    )
    session.run(
        'sphinx-build', 'docs', 'docs/_build/html',
    )
