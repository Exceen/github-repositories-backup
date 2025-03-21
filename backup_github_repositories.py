from subprocess import Popen, PIPE
import os
import re

workpath = os.path.dirname(os.path.realpath(__file__))

CLONE_CMD = 'git clone --mirror git@github.com:%s.git %s'

def call_on_shell(command):
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return (out + err).strip().decode('UTF-8')


def main():
    username = re.search(r'account (.+?) ', call_on_shell('gh auth status | grep "Logged in"')).group(1)
    print('Backing up repositories for', username)

    repository_list = [row.split()[0] for row in call_on_shell('gh repo list -L 100000').split('\n') if row.startswith(username + '/')]

    download_dir = os.path.join(workpath, 'repositories')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for repository in repository_list:
        print('Backing up ' + str(repository) + '...')
        repository_dir = os.path.join(download_dir, repository.split('/')[1])

        call_on_shell(CLONE_CMD % (repository, repository_dir))



if __name__ == '__main__':
    main()