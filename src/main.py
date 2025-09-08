import os, shutil
from textnode import TextType, TextNode
from copystatic import copy_static
from gencontent import generate_page, generate_pages_recursive




def main():
   
    public_dir = "public"
    static_dir = "static"
    template_path = "template.html"
    content_dir = "content"

    
    if os.path.isdir(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)

    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)
    
    generate_pages_recursive(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()
