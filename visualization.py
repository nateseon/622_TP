import streamlit as st
import graphviz

# Node class for B+ Tree
class BPlusNode:
    def __init__(self, key=None, is_leaf=False):
        self.key = key
        self.keys = [] if key is None else [key]
        self.is_leaf = is_leaf
        self.children = []

    def add_child(self, child):
        self.children.append(child)

# Node class for Prefix Tree (Trie)
class PrefixNode:
    def __init__(self, key=None, is_leaf=False):
        self.key = key
        self.is_leaf = is_leaf
        self.children = []

    def add_child(self, child):
        self.children.append(child)

# Node class for Red/Black Tree
class RedBlackNode:
    def __init__(self, key=None, color="red"):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

# B+ Tree implementation
class BPlusTree:
    def __init__(self, max_keys=3):
        self.root = BPlusNode(is_leaf=True)
        self.max_keys = max_keys

    def insert(self, key):
        root = self.root
        if len(root.keys) == self.max_keys:
            new_root = BPlusNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        if node.is_leaf:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == self.max_keys:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, index):
        node = parent.children[index]
        mid_index = len(node.keys) // 2
        mid_key = node.keys[mid_index]

        new_node = BPlusNode(is_leaf=node.is_leaf)
        parent.keys.insert(index, mid_key)
        parent.children.insert(index + 1, new_node)

        new_node.keys = node.keys[mid_index + 1:]
        node.keys = node.keys[:mid_index]

        if not node.is_leaf:
            new_node.children = node.children[mid_index + 1:]
            node.children = node.children[:mid_index + 1]

    def visualize(self):
        dot = graphviz.Digraph()
        if self.root:
            self._add_nodes(dot, self.root)
        return dot

    def _add_nodes(self, dot, node):
        dot.node(str(id(node)), " | ".join(map(str, node.keys)))
        for child in node.children:
            dot.edge(str(id(node)), str(id(child)))
            self._add_nodes(dot, child)

# Prefix Tree (Trie) implementation
class PrefixTree:
    def __init__(self):
        self.root = PrefixNode(key="", is_leaf=True)

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
                new_node = PrefixNode(key=char, is_leaf=True)
                current_node.add_child(new_node)
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

# Red/Black Tree implementation
class RedBlackTree:
    def __init__(self):
        self.TNULL = RedBlackNode(key=0, color="black")  # Sentinel node
        self.root = self.TNULL

    def insert(self, key):
        new_node = RedBlackNode(key=key, color="red")
        new_node.left = self.TNULL
        new_node.right = self.TNULL

        parent = None
        current = self.root

        while current != self.TNULL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        if new_node.parent is None:
            new_node.color = "black"
            return

        if new_node.parent.parent is None:
            return

        self._fix_insert(new_node)

    def _fix_insert(self, k):
        while k.parent.color == "red":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self._left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self._right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "black"

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def visualize(self):
        dot = graphviz.Digraph()
        if self.root != self.TNULL:
            self._add_nodes(dot, self.root)
        return dot

    def _add_nodes(self, dot, node):
        if node != self.TNULL:
            dot.node(str(id(node)), f'{node.key} ({node.color})', style="filled", fillcolor=node.color)
            if node.left != self.TNULL:
                dot.edge(str(id(node)), str(id(node.left)))
                self._add_nodes(dot, node.left)
            if node.right != self.TNULL:
                dot.edge(str(id(node)), str(id(node.right)))
                self._add_nodes(dot, node.right)

# Streamlit app setup
st.title("Tree Visualization")
tree_type = st.selectbox("Choose Tree Type", ("B+ Tree", "Prefix Tree", "Red/Black Tree"))

# Tree selection and visualization
if tree_type == "B+ Tree":
    tree = BPlusTree()
    elements = st.text_input("Insert elements (comma separated):", "10, 20, 30, 5, 6, 12, 30, 7, 17")
elif tree_type == "Prefix Tree":
    tree = PrefixTree()
    elements = st.text_input("Insert words (comma separated):", "cat, dog, cap, bat, ball, bark")
elif tree_type == "Red/Black Tree":
    tree = RedBlackTree()
    elements = st.text_input("Insert elements (comma separated):", "10, 20, 30, 5, 6, 12")

# Insert elements and visualize tree
if st.button("Visualize"):
    for element in elements.split(","):
        if tree_type == "Prefix Tree":
            tree.insert(element.strip())
        else:
            tree.insert(int(element.strip()))

    st.graphviz_chart(tree.visualize())
