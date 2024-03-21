import os
import base64
import shutil


def pack(path):
    result_string = ''
    dirs = []

    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(path)):
        print(dirpath, dirnames, filenames)
        short_dirpath = dirpath[len(path) + 1:]
        if i != 0:
            dirs.append(short_dirpath)
        for filename in filenames:

            with open(dirpath + "/" + filename, "rb") as f:
                filecontent = str(base64.b64encode(f.read()), 'utf-8')
                result_string += f'<F#>{short_dirpath + "/" + filename}<C#>{filecontent}'

    result_string = '<D#>'.join(dirs) + result_string

    with open(f'{path}.txt', "w") as f:
        f.write(result_string)


def unpack(path):
    maindir = path[:-4]
    shutil.rmtree(maindir, ignore_errors=True)
    os.mkdir(maindir)

    with open(path, "r") as f:
        result_string = f.read()

    files_data = result_string.split('<F#>')
    for i, file_data in enumerate(files_data):

        if i == 0:
            for dirname in file_data.split('<D#>'):
                print(maindir + '/' + dirname)
                os.mkdir(maindir + '/' + dirname)

        else:
            filepath, filecontent = file_data.split('<C#>')
            with open(maindir + '/' + filepath, "wb") as f:
                f.write(base64.b64decode(bytes(filecontent, 'utf-8')))


action = input('\nChoose action:\n1. Pack\n2. Unpack\n\n')

if action not in ('1', '2'):
    exit()

paths_list = [f for f in os.listdir('./') if (action == '1' and not os.path.isfile('./' + f)) or action == '2' and os.path.isfile('./' + f) and f.endswith('.txt')]

catalog = [f'{i+1}. {path}' for i, path in enumerate(paths_list)]
path_i = input('\nChoose path:\n' + '\n'.join(catalog) + '\n\n')

if not path_i.isnumeric() or int(path_i) > len(paths_list):
    exit()

if action == '1':
    pack(paths_list[int(path_i) - 1])

elif action == '2':
    unpack(paths_list[int(path_i) - 1])

print('\nDone!')
