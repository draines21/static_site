import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
 
class TestHTMLNodeProps(unittest.TestCase):
    def test_props_is_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_multiple(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')






class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_none_tag_returns_value(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_props_render(self):
        node = LeafNode("a", "Click", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click</a>')

    def test_value_none_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()



class TestParentNode(unittest.TestCase):
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        kids = [LeafNode("b", "A"), LeafNode(None, "B"), LeafNode("i", "C")]
        parent = ParentNode("p", kids)
        self.assertEqual(parent.to_html(), "<p><b>A</b>B<i>C</i></p>")

    def test_to_html_raises_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("b", "x")]).to_html()

    def test_to_html_raises_with_none_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_raises_with_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_with_props_on_parent(self):
        child = LeafNode(None, "hi")
        parent = ParentNode("div", [child], props={"id": "x", "class": "y"})
        self.assertEqual(parent.to_html(), '<div id="x" class="y">hi</div>')

    def test_nested_siblings(self):
        bold = LeafNode("b", "A")
        ital = LeafNode("i", "B")
        inner = ParentNode("span", [bold, ital])
        outer = ParentNode("div", [LeafNode(None, "X"), inner, LeafNode(None, "Y")])
        self.assertEqual(outer.to_html(), "<div>X<span><b>A</b><i>B</i></span>Y</div>")

    def test_child_is_parentnode_among_leaves(self):
        mid = ParentNode("em", [LeafNode(None, "mid")])
        parent = ParentNode("p", [LeafNode(None, "start"), mid, LeafNode(None, "end")])
        self.assertEqual(parent.to_html(), "<p>start<em>mid</em>end</p>")
  
if __name__ == "__main__":
    unittest.main()