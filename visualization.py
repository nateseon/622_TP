import streamlit as st
import graphviz

# Streamlit 앱 설정
st.title("B+, Prefix, Red/Black Tree Visualization")

# 선택 메뉴
tree_type = st.selectbox("Choose Tree Type", ("B+ Tree", "Prefix Tree", "Red/Black Tree"))

# 노드 클래스 정의
class Node:
    def __init__(self, key, color=None):
        self.key = key
        self.color = color
        self.children = []
        self.parent = None

# B+ Tree 구현
class BPlusTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            # 간단한 B+ 트리 삽입 로직 (완전한 구현은 아님)
            new_node = Node(key)
            self.root.children.append(new_node)

    def visualize(self):
        dot = graphviz.Digraph()
        if self.root:
            self._add_nodes(dot, self.root)
        return dot

    def _add_nodes(self, dot, node):
        dot.node(str(id(node)), str(node.key))
        for child in node.children:
            dot.edge(str(id(node)), str(id(child)))
            self._add_nodes(dot, child)

# Prefix Tree (Trie) 구현
class PrefixTree:
    def __init__(self):
        self.root = Node("")

    def insert(self, word):
        current_node = self.root
        for char in word:
            found = False
            for child in current_node.children:
                if child.key == char:
                    current_node = child
                    found = True
                    break
            if not found:
                new_node = Node(char)
                current_node.children.append(new_node)
                current_node = new_node

    def visualize(self):
        dot = graphviz.Digraph()
        if self.root:
            self._add_nodes(dot, self.root)
        return dot

    def _add_nodes(self, dot, node):
        dot.node(str(id(node)), str(node.key))
        for child in node.children:
            dot.edge(str(id(node)), str(id(child)))
            self._add_nodes(dot, child)

# Red/Black Tree 구현
class RedBlackTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node(key, color="black")
        else:
            # 간단한 Red/Black 트리 삽입 로직 (완전한 구현은 아님)
            new_node = Node(key, color="red")
            self.root.children.append(new_node)

    def visualize(self):
        dot = graphviz.Digraph()
        if self.root:
            self._add_nodes(dot, self.root)
        return dot

    def _add_nodes(self, dot, node):
        dot.node(str(id(node)), f'{node.key} ({node.color})', style="filled", fillcolor=node.color)
        for child in node.children:
            dot.edge(str(id(node)), str(id(child)))
            self._add_nodes(dot, child)

# 트리 선택에 따른 시각화
if tree_type == "B+ Tree":
    tree = BPlusTree()
    elements = st.text_input("Insert elements (comma separated):", "10, 20, 30")
elif tree_type == "Prefix Tree":
    tree = PrefixTree()
    elements = st.text_input("Insert words (comma separated):", "cat, dog, cap")
elif tree_type == "Red/Black Tree":
    tree = RedBlackTree()
    elements = st.text_input("Insert elements (comma separated):", "10, 20, 30")

# 입력된 요소 삽입 및 트리 시각화
if st.button("Visualize"):
    for element in elements.split(","):
        if tree_type == "Prefix Tree":
            tree.insert(element.strip())
        else:
            tree.insert(int(element.strip()))
    
    st.graphviz_chart(tree.visualize())
