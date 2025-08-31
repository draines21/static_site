from textnode import TextType, TextNode
def main():
    node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()
