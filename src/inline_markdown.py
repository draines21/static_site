from textnode import TextType, TextNode
import re
from htmlnode import HTMLNode 





def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Invalid Markdown Syntax")
            for i, part in enumerate(parts):
                if not part:
                    continue
                node_type = TextType.TEXT if i % 2 == 0 else text_type
                new_nodes.append(TextNode(part, node_type))
        else:
            new_nodes.append(old_node)
    return new_nodes



def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)



def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            images = extract_markdown_images(old_node.text)
            if len(images) == 0:
              new_nodes.append(old_node)
              continue
            original_text = old_node.text
            for image in images:
              sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
              if len(sections) != 2:
                  new_nodes.append(old_node)
                  break
              if sections[0]:
                  new_nodes.append(TextNode(sections[0], TextType.TEXT))
              new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
              original_text = sections[1]
            if original_text:
                new_nodes.append(TextNode(original_text, TextType.TEXT))

        else:
            new_nodes.append(old_node)
    return new_nodes

    

        


# python
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        broke = False
        for text, url in links:
            sections = original_text.split(f"[{text}]({url})", 1)
            if len(sections) != 2:
                new_nodes.append(old_node)
                broke = True
                break
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            original_text = sections[1]

        if broke:
            continue
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes,"**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes


