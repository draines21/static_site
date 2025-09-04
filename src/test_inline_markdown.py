import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType
from markdown_blocks import markdown_to_blocks


class TestInlineMarkdown(unittest.TestCase):
    def test_split_unbalanced_raises(self):
        node = TextNode("a `b c", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_no_delimiter(self):
        node = TextNode("hello world", TextType.TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].text, "hello world")
        self.assertEqual(out[0].text_type, TextType.TEXT)

    def test_split_code_simple(self):
        node = TextNode("a `b` c", TextType.TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("a ", TextType.TEXT), ("b", TextType.CODE), (" c", TextType.TEXT)],
        )

    def test_non_text_passthrough(self):
        bold = TextNode("bold", TextType.BOLD)
        out = split_nodes_delimiter([bold], "`", TextType.CODE)
        self.assertEqual(out, [bold])

    def test_split_bold(self):
        node = TextNode("x **y** z", TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("x ", TextType.TEXT), ("y", TextType.BOLD), (" z", TextType.TEXT)],
        )


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links("See [A](https://a.com) and [B](https://b.org)")
        self.assertEqual([("A", "https://a.com"), ("B", "https://b.org")], matches)

    def test_no_matched_links(self):
        self.assertEqual([], extract_markdown_links("Just text, no links here"))

    def test_mixed_markdown_text_links(self):
        text = "![logo](http://img) and [site](http://site)"
        self.assertEqual([("logo", "http://img")], extract_markdown_images(text))
        self.assertEqual([("site", "http://site")], extract_markdown_links(text))
    

    def test_empty_alt_text(self):
        self.assertEqual([("", "http://x")], extract_markdown_images("![](http://x)"))

    

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )


    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a [link](https://boot.dev) and another [second link](https://blog.boot.dev)",
        TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://blog.boot.dev"
            ),
        ],
        new_nodes,
    )




    def test_text_to_textnode_plain(self):
        result = text_to_textnodes("hello world") 
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "hello world")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_to_textnodes_code(self):
        result = text_to_textnodes("`code`")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "code")
        self.assertEqual(result[0].text_type, TextType.CODE)

    def test_to_textnodes_link(self):
        result = text_to_textnodes("a [link](https://boot.dev)")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://boot.dev")

    def test_text_to_textnodes_image(self):
        result = text_to_textnodes("before ![alt](u) after"
                                   )
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "before ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "u")
        self.assertEqual(result[2].text, " after")
        self.assertEqual(result[2].text_type, TextType.TEXT)


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_whitespace_only(self):
        self.assertEqual(markdown_to_blocks(" \n \n "), [])

    def test_preserve_internal_newlines(self):
        md = "Line 1\nLine 2\n\nNext block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Line 1\nLine 2", "Next block"],
        )

    def test_single_block(self):
        md = "Only one block here"
        self.assertEqual(markdown_to_blocks(md), ["Only one block here"])


    def test_blocks_with_extra_blank_lines(self):
        md = "\n\nPara 1 \n\n\n\nPara 2\n\n"
        self.assertEqual(markdown_to_blocks(md),["Para 1", "Para 2"],)

    



if __name__ == "__main__":
    unittest.main()