class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        parts = []
        for k, v in self.props.items():
            parts.append(f'{k}="{v}"')
        return " " + " ".join(parts)
  
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        
        attrs = self.props_to_html()
        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag found")
        
        if self.children is None or self.children == []:
            raise ValueError("No children value present")
        
        inner = "".join(child.to_html() for child in self.children)
        attrs= self.props_to_html()
        return f"<{self.tag}{attrs}>{inner}</{self.tag}>"
        
        

        