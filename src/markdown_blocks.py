from htmlnode import HTMLNode, LeafNode, ParentNode
from enum import Enum, auto
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
import re


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    ULIST = auto()
    OLIST = auto()

def block_to_block_type(block):
    lines = block.splitlines()
    
    if len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE
    
    if block.startswith("#"):
        i = 0
        while i < len(block) and block[i] == "#":
            i += 1
        if 1 <= i <= 6 and i < len(block) and block [i] == " ":
            return BlockType.HEADING
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    
    ok = True
    for idx, line in enumerate(lines, start=1):
        prefix = f"{idx}. "
        if not line.startswith(prefix):
            ok = False
            break
    if ok:
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH







def markdown_to_blocks(markdown):
    chunks = markdown.split("\n\n")
    blocks = []
    
    for chunk in chunks:
        clean = chunk.strip()
       
        if clean != "":
            blocks.append(clean)
    return blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    container = ParentNode(tag="div", children=[])
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            i = 0
            while i < len(block) and block[i] == '#':
                i += 1
            level = min(i, 6)
            heading_text = block[i:].lstrip()
            tag = f"h{level}"
            node = ParentNode(tag, text_to_children(heading_text))
            container.children.append(node)
        
        elif block_type == BlockType.CODE:
            lines = block.splitlines()
            inner_lines = lines[1:-1]
            non_empty = [ln for ln in inner_lines if ln.strip() != ""]
            if non_empty:
                min_indent = min(len(ln) - len(ln.lstrip(" ")) for ln in non_empty)
            else:
                min_indent = 0

            cleaned = [ln[min_indent:] if len(ln) >= min_indent else ln for ln in inner_lines]
            inner = "\n".join(cleaned) + "\n"
            code_leaf = LeafNode(None, inner)
            code_node = ParentNode("code", [code_leaf])
            pre_node = ParentNode("pre", [code_node])
            container.children.append(pre_node)

        
        elif block_type == BlockType.QUOTE:
            raw_lines = block.splitlines()
            cleaned = []
            for line in raw_lines:
                if line.startswith("> "):
                    cleaned.append(line[2:])
                elif line.startswith(">"):
                    cleaned.append(line[1:])
                else:
                    cleaned.append(line)
            text = "\n".join(cleaned)
            node = ParentNode("blockquote", text_to_children(text))
            container.children.append(node)  
        
        elif block_type == BlockType.ULIST:
            lines = block.splitlines()
            li_nodes = []
            for line in lines:
                if line.startswith("- ") or line.startswith("* "):
                    item_text = line[2:].strip()
                    li_nodes.append(ParentNode("li", text_to_children(item_text)))
            ul = ParentNode("ul", li_nodes)
            container.children.append(ul)

        
        elif block_type == BlockType.OLIST:
            lines = block.splitlines()
            li_nodes = []
            for line in lines:
                idx = line.find(". ")
                if idx != -1 and line[:idx].isdigit():
                    item_text = line[idx + 2 :].strip()
                    li_nodes.append(ParentNode("li", text_to_children(item_text)))
            ol = ParentNode("ol", li_nodes)
            container.children.append(ol)


        elif block_type == BlockType.PARAGRAPH:
            raw = block.strip()
            parts = [ln.strip() for ln in raw.splitlines() if ln.strip() != ""]
            text = " ".join(parts)
            p = ParentNode("p", text_to_children(text))
            container.children.append(p)
        
        else:
            pass
        
       
         
    return container
        
            


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in nodes]


