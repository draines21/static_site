import unittest
from src.markdown_blocks import block_to_block_type, BlockType, markdown_to_html_node

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Hi"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Hi"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Hi"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nno end"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> a\n> b"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> a\na"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- a\n- b"), BlockType.ULIST)
        self.assertEqual(block_to_block_type("-a\n- b"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. a\n2. b"), BlockType.OLIST)
        self.assertEqual(block_to_block_type("1. a\n3. b"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("just words"), BlockType.PARAGRAPH)




    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )   

    


    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
             "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        ) 




    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>")




if __name__ == "__main__":
    unittest.main()