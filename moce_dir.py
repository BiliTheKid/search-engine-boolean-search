# Imports
import os
import shutil

# Global vars
corpus_dir = "source"
dst= "storage"
taketo= "taketo"
takeFrom= "takefrom"
# Copy directory
def copytree(src, dst, symlinks=False): ##copy files to another dir from dir
    names = os.listdir(corpus_dir)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except IOError as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        # can't copy file access times on Windows
        if why.winerror is None:
            errors.extend((src, dst, str(why)))
    if errors:
        raise IOError(errors)


# Delete current dir files
def delete_dir():
    folder = corpus_dir
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        # elif os.path.isdir(file_path): shutil.rmtree(file_path)

        except Exception as e:
            print(e)

# Call the func above
def close_things():
    delete_dir()


def delete_taketo():
    folder = taketo
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)

        except Exception as e:
            print(e)

def delete_takeFrom():
    folder = takeFrom
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)

        except Exception as e:
            print(e)
