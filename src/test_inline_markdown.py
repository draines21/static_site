import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

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



if __name__ == "__main__":
    unittest.main()