FROM python:3.11.9-slim-bullseye AS builder

RUN apt-get update && apt-get upgrade --yes

RUN useradd --create-home cur_user
USER cur_user
WORKDIR /home/cur_user

ENV VIRTUALENV=home/cur_user/venv
RUN python3 -m venv ${VIRTUALENV}
ENV PATH="${VIRTUALENV}/bin:${PATH}"

COPY --chown=cur_user pyproject.toml constraints.txt ./
RUN python -m pip install --upgrade pip setuptools && python -m pip install --no-cache-dir -c constraints.txt ".[dev]"

COPY --chown=cur_user src/ src/
COPY --chown=cur_user test/ test/

RUN python -m pip install . -c constraints.txt && python -m pytest test/unit/ && python -m flake8 src/ && \
    python -m isort src/ --check && \
    python -m black src/ --check --quiet && \
    python -m pylint src/ --disable=C0114,C0116,R1705 && \
    python -m bandit -r src/ --quiet && \
    python -m pip wheel --wheel-dir dist/ . -c constraints.txt



FROM python:3.11.9-slim-bullseye

RUN apt-get update && apt-get upgrade --yes

RUN useradd --create-home cur_user
USER cur_user
WORKDIR /home/cur_user

ENV VIRTUALENV=/home/cur_user/venv
RUN python3 -m venv ${VIRTUALENV}
ENV PATH="${VIRTUALENV}/bin:${PATH}"

COPY --from=builder home/cur_user/dist/package_tracker_flask*.whl /home/cur_user
RUN ls
RUN python -m pip install --upgrade pip setuptools && \
    python -m pip install --verbose --no-cache-dir package_tracker_flask*.whl


CMD [ "flask", "--app", "page_tracker.app", "run", "--host", "0.0.0.0", "--port", "5000" ]