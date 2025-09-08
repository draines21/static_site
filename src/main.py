import os, shutil
import sys
from textnode import TextType, TextNode
from copystatic import copy_static
from gencontent import generate_page, generate_pages_recursive




def main():
   
    public_dir = "public"
    static_dir = "static"
    template_path = "template.html"
    content_dir = "content"
    out_dir = "docs"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    shutil.copytree(static_dir, out_dir, dirs_exist_ok=True)
    
    generate_pages_recursive(content_dir, template_path, out_dir, basepath)


if __name__ == "__main__":
    main()
