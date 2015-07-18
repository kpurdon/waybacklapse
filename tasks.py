from invoke import task, run


@task
def build():
    run('docker-compose build')


@task
def up():
    run('docker-compose up')


@task(pre=[up])
def help():
    run('docker-compose run wayback python3 /usr/src/app/waybacklapse.py --help')


@task(default=True, pre=[build, up])
def default():
    cmd = 'docker-compose run wayback python3 /usr/src/app/waybacklapse.py'
    cmd += ' -u google.com'
    cmd += ' -b 1996'
    cmd += ' -e 2015'
    cmd += ' -c 4'
    cmd += ' -s 50'
    cmd += ' -l 2'
    cmd += ' -w 1280'
    cmd += ' -h 720'
    cmd += ' -v'
    run(cmd)


@task(pre=[build, up])
def runner():
    run('docker-compose run wayback python3 /usr/src/app/waybacklapse.py')


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
