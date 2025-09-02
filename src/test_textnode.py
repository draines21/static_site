import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_equal_when_url_none(self):
        node = TextNode("x", TextType.LINK)
        node2 = TextNode("x", TextType.LINK)
        self.assertEqual(node, node2)
    
    def test_equal_when_url_differs(self):
        node = TextNode("x", TextType.LINK, "http://node" )
        node2 = TextNode("x", TextType.LINK, "http://node2")
        self.assertNotEqual(node, node2)
    
    def test_not_equal_when_text_differs(self):
        node = TextNode("x", TextType.BOLD)
        node2 = TextNode("y", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_when_type_differs(self):
        node = TextNode("x", TextType.BOLD)
        node2 = TextNode("x", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_equal_when_all_fields_match(self):
        node = TextNode("x", TextType.BOLD, "http://same")
        node2 = TextNode("x", TextType.BOLD, "http://same")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link_to_leaf(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Boot.dev")
        self.assertEqual(html.props, {"href": "https://boot.dev"}) 

    def test_textnode_bold_to_leafnode_b(self):
        node = TextNode("roar", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag,"b")
        self.assertEqual(html.value, "roar")
        self.assertIsNone(html.props)

    def test_textnode_italic_to_leafnode_i(self):
        node = TextNode("wow", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "wow")
        self.assertIsNone(html.props)

    def test_textnode_code_to_leafnode_code(self):
        node = TextNode("code", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "code")
        self.assertIsNone(html.props)
    
    def test_textnode_link_to_leafnode_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Boot.dev")
        self.assertEqual(html.props,{"href": "https://boot.dev"})

    def test_textnode_img_to_leafnode_img(self):
        node = TextNode("alt text", TextType.IMAGE, "https://img.url/x.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(html.props, {"src": "https://img.url/x.png", "alt": "alt text"})

    def test_textnode_unsupported_type_raises(self):
        class FakeType: pass
        node = TextNode("x", FakeType)  
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()