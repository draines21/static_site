import os
import shutil

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(dst_path)

        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            copy_static(src_path, dst_path)

    
