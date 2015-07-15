from invoke import task, run


@task
def build():
    run('docker-compose build')


@task
def up():
    run('docker-compose up')


@task(pre=[build, up])
def help():
    run('docker-compose run wayback python3 /usr/src/app/waybacklapse.py --help')


@task(default=True, pre=[build, up])
def default():
    run('docker-compose run wayback python3 /usr/src/app/waybacklapse.py -v -l 2')


@task
def develop():
    run('pip install -r requirements.dev.txt')


@task(pre=[develop])
def test():
    run('flake8 --config .flake8rc $(find . -name "*.py") --verbose')
    run('nosetests --rednose --verbose')


@task
def clean():
    run('find . -name "*.pyc" -exec rm -rf {} \;')
