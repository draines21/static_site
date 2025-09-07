import os, shutil
from textnode import TextType, TextNode
from copystatic import copy_static
from gencontent import generate_page




def main():
   
    public_dir = "public"
    static_dir = "static"
    from_path = "content/index.md"
    template_path = "template.html"
    dest_path = os.path.join(public_dir, "index.html")

    print(f"Generating page form {from_path} to {dest_path} using {template_path}")
    
    if os.path.isdir(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)

    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)

    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
