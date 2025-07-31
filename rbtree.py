from manim import *
import numpy as np

class TreeNode(VGroup):
    def __init__(self, label, color_char="B", **kwargs):
        super().__init__(**kwargs)
        color_map = {"B": BLACK, "R": RED, "O": ORANGE, "W": WHITE, "BLUE": BLUE, "G": GREEN}
        fill_color = color_map.get(color_char, WHITE)

        self.circle = Circle(radius=0.3, color=WHITE, stroke_width=3).set_fill(fill_color, opacity=1)
        self.text = Text(label, font_size=24).move_to(self.circle.get_center())

        self.add(self.circle, self.text)
        self.label = label
        self.color_char = color_char

    def set_node_color(self, color_char):
        color_map = {"B": BLACK, "R": RED, "O": ORANGE, "W": WHITE, "BLUE": BLUE, "G": GREEN}
        self.circle.set_fill(color_map.get(color_char, WHITE), opacity=1)
        self.color_char = color_char

    def update_label(self, new_label):
        """Update the label and recreate the text object"""
        self.remove(self.text)
        self.text = Text(new_label, font_size=24).move_to(self.circle.get_center())
        self.add(self.text)
        self.label = new_label

class TreeArrow:
    def __init__(self, scene, tree_structure, color=YELLOW):
        self.scene = scene
        self.tree_structure = tree_structure
        self.color = color
        self.arrow = None
        self.current_index = None

    def create_arrow(self, index):
        if index in self.tree_structure.nodes:
            node = self.tree_structure.nodes[index]
            start = node.get_top() + UP * 1.2
            end = node.get_top() + UP * 0.1
            self.arrow = Arrow(start=start, end=end, color=self.color, buff=0, stroke_width=6)
            self.scene.add(self.arrow)
            self.scene.play(GrowArrow(self.arrow), run_time=0.3)
            self.current_index = index

    def move_to(self, new_index):
        if new_index in self.tree_structure.nodes and self.arrow:
            node = self.tree_structure.nodes[new_index]
            new_start = node.get_top() + UP * 1.2
            new_end = node.get_top() + UP * 0.1
            new_arrow = Arrow(start=new_start, end=new_end, color=self.color, buff=0, stroke_width=6)
            self.scene.play(Transform(self.arrow, new_arrow), run_time=0.3)
            self.current_index = new_index

    def remove(self):
        if self.arrow:
            self.scene.play(FadeOut(self.arrow), run_time=0.2)
            self.arrow = None
            self.current_index = None

class TreeStructure:
    def __init__(self, scene):
        self.scene = scene
        self.nodes = {}  # index -> TreeNode
        self.edges = {}  # (parent_index, child_index) -> Line
        self.tree_data = {}  # index -> (label, color)
        self.positions = {}  # index -> position
        
        # Tree layout parameters
        self.root_pos = ORIGIN + 2.3 * UP
        self.level_height = 1.2
        self.base_h_spacing = 5.0

    def find_node_index(self, target_node):
        for index, node in self.nodes.items():
            if node is target_node:  # Using 'is' for object identity
                return index
        return None  # Node not found
    
    def calculate_position(self, index, level=0):
        """Calculate the fixed position for a node based on its index"""
        if index == 1:  # Root
            return self.root_pos
        
        # For binary heap indexing: parent = index // 2
        parent_index = index // 2
        parent_pos = self.calculate_position(parent_index, level - 1)
        
        # Calculate horizontal offset based on level
        h_spacing = self.base_h_spacing / (2 ** level)
        
        if index % 2 == 0:  # Left child
            return parent_pos + DOWN * self.level_height + LEFT * h_spacing
        else:  # Right child
            return parent_pos + DOWN * self.level_height + RIGHT * h_spacing

    def add_node(self, index, label, color_char="B", animate=True):
        """Add a node at the specified index"""
        if index in self.nodes:
            return  # Node already exists
        
        position = self.calculate_position(index, self._get_level(index))
        node = TreeNode(label, color_char).move_to(position)
        
        self.nodes[index] = node
        self.tree_data[index] = (label, color_char)
        self.positions[index] = position
        
        if animate:
            self.scene.add(node)
            self.scene.play(FadeIn(node), run_time=0.3)
        else:
            self.scene.add(node)

    def add_edge(self, parent_index, child_index, animate=True):
        """Add an edge between parent and child"""
        if parent_index not in self.nodes or child_index not in self.nodes:
            return
        
        parent_node = self.nodes[parent_index]
        child_node = self.nodes[child_index]
        
        edge = Line(parent_node.get_bottom(), child_node.get_top(), color=WHITE)
        self.edges[(parent_index, child_index)] = edge
        
        if animate:
            self.scene.add(edge)
            self.scene.play(Create(edge), run_time=0.2)
        else:
            self.scene.add(edge)

    def remove_node(self, index, animate=True):
        """Remove a node and its connected edges"""
        if index not in self.nodes:
            return
        
        node = self.nodes[index]
        
        # Find all edges connected to this node
        connected_edges = []
        edges_to_remove = []
        
        for (parent, child), edge in self.edges.items():
            if parent == index or child == index:
                connected_edges.append(edge)
                edges_to_remove.append((parent, child))
        
        # Remove from scene
        if animate:
            fade_objects = [node] + connected_edges
            self.scene.play(*[FadeOut(obj) for obj in fade_objects], run_time=0.5)
        else:
            self.scene.remove(node, *connected_edges)
        
        # Remove from data structures
        del self.nodes[index]
        del self.tree_data[index]
        del self.positions[index]
        
        for edge_key in edges_to_remove:
            del self.edges[edge_key]

    def swap_nodes(self, index1, index2, animate=True):
        """Swap two nodes by exchanging their data and positions"""
        if index1 not in self.nodes or index2 not in self.nodes:
            return
        
        node1 = self.nodes[index1]
        node2 = self.nodes[index2]
        
        # Get positions
        pos1 = self.positions[index1]
        pos2 = self.positions[index2]
        
        # Get data
        label1, color_char1 = self.tree_data[index1]
        label2, color_char2 = self.tree_data[index2]
        
        if animate:
            # Animate the movement
            self.scene.play(
                node1.animate.move_to(pos2),
                node2.animate.move_to(pos1),
                run_time=0.8
            )
        else:
            node1.move_to(pos2)
            node2.move_to(pos1)
        
        # Swap the nodes in our data structure
        self.nodes[index1] = node2
        self.nodes[index2] = node1
        
        # Update the tree data
        self.tree_data[index1] = (label2, color_char2)
        self.tree_data[index2] = (label1, color_char1)

    def update_node_data(self, index, new_label=None, new_color_char=None):
        """Update node's label and/or color"""
        if index not in self.nodes:
            return
        
        node = self.nodes[index]
        
        if new_label is not None:
            node.update_label(new_label)
            label, color_char = self.tree_data[index]
            self.tree_data[index] = (new_label, color_char)
        
        if new_color_char is not None:
            node.set_node_color(new_color_char)
            label, color_char = self.tree_data[index]
            self.tree_data[index] = (label, new_color_char)

    def rebuild_edges(self):
        """Rebuild all edges based on current node positions"""
        # Remove all existing edges
        for edge in self.edges.values():
            self.scene.remove(edge)
        self.edges.clear()
        
        # Rebuild edges based on heap structure
        for index in sorted(self.nodes.keys()):
            left_child = 2 * index
            right_child = 2 * index + 1
            
            if left_child in self.nodes:
                self.add_edge(index, left_child, animate=False)
            if right_child in self.nodes:
                self.add_edge(index, right_child, animate=False)

    def _get_level(self, index):
        """Get the level of a node (root is level 0)"""
        level = 0
        while index > 1:
            index //= 2
            level += 1
        return level

    def highlight_node(self, index, color=YELLOW, duration=0.5):
        """Highlight a node with a colored border"""
        if index not in self.nodes:
            return None
        
        node = self.nodes[index]
        highlight_circle = Circle(
            radius=0.5, 
            color=color, 
            stroke_width=6
        ).move_to(node.get_center())
        
        self.scene.play(Create(highlight_circle), run_time=duration)
        return highlight_circle

    def remove_highlight(self, highlight_circle, duration=0.3):
        """Remove a highlight"""
        if highlight_circle:
            self.scene.play(FadeOut(highlight_circle), run_time=duration)

def build_tree_from_list(tree_structure, data):
    """Build tree from list representation"""
    for i, item in enumerate(data, 1):
        if item is not None:
            color_char = item[0]
            label = item[1:]
            tree_structure.add_node(i, label, color_char)
    
    # Add edges
    tree_structure.rebuild_edges()

def collect_subtree_nodes(tree_structure, root_index):
    """Collect all nodes in a subtree rooted at root_index"""
    subtree = []
    
    def collect_recursive(index):
        if index in tree_structure.nodes:
            subtree.append(index)
            collect_recursive(2 * index)      # left child
            collect_recursive(2 * index + 1)  # right child
    
    collect_recursive(root_index)
    return subtree

def is_in_subtree(node_index, root_index):
    """Check if node_index is in the subtree rooted at root_index"""
    if node_index == root_index:
        return True
    
    # Traverse up from node_index to see if we reach root_index
    current = node_index
    while current > root_index:
        current = current // 2
    
    return current == root_index

def get_relative_path(node_index, root_index):
    """Get the path from root_index to node_index as a list of 'L'/'R' moves"""
    if node_index == root_index:
        return []
    
    path = []
    current = node_index
    
    while current != root_index:
        if current % 2 == 0:  # Left child
            path.append('L')
        else:  # Right child
            path.append('R')
        current = current // 2
    
    return path[::-1]  # Reverse to get path from root to node

def apply_relative_path(root_index, path):
    """Apply a path of 'L'/'R' moves starting from root_index"""
    current = root_index
    for move in path:
        if move == 'L':
            current = 2 * current
        else:  # move == 'R'
            current = 2 * current + 1
    return current

def move_subtree(tree_structure, new_node_map, new_data_map, old_root, new_root):
    """
    Helper function to move an entire subtree from old_root to new_root position.
    First moves the root, then recursively moves children based on parent-child relationships.
    """
    if old_root not in tree_structure.nodes:
        return
    
    # Create a mapping from old indices to new indices
    index_mapping = {}
    
    # First, move the root
    new_node_map[new_root] = tree_structure.nodes[old_root]
    new_data_map[new_root] = tree_structure.tree_data[old_root]
    index_mapping[old_root] = new_root
    
    # Get all nodes in subtree and sort them by level (breadth-first order)
    # This ensures parents are processed before children
    subtree_nodes = []
    for old_index in range(1, 63):
        if (is_in_subtree(old_index, old_root) and 
            old_index in tree_structure.nodes and 
            old_index != old_root):
            subtree_nodes.append(old_index)
    
    # Sort by level (smaller indices = higher levels, processed first)
    subtree_nodes.sort()
    
    # Process nodes level by level
    for old_index in subtree_nodes:
        # Find the parent of this node
        old_parent_index = old_index // 2
        
        # The parent should already be in index_mapping
        if old_parent_index not in index_mapping:
            continue  # Skip if parent not processed yet
            
        new_parent_index = index_mapping[old_parent_index]
        is_left_child = (old_index % 2 == 0)  # Even indices are left children

        # Calculate new index based on parent-child relationship
        if is_left_child:
            new_index = 2 * new_parent_index      # Left child
        else:
            new_index = 2 * new_parent_index + 1  # Right child
                
        # Move the node
        new_node_map[new_index] = tree_structure.nodes[old_index]
        new_data_map[new_index] = tree_structure.tree_data[old_index]
        index_mapping[old_index] = new_index

def left_rotate(scene, tree_structure, l_index):

    right_child_index = 2 * l_index + 1  # Right child of l
    
    if l_index not in tree_structure.nodes or right_child_index not in tree_structure.nodes:
        return
    
    # # Show rotation text
    rotation_text = Text("Left Rotation", font_size=36, color=YELLOW).to_edge(UP)
    scene.play(Write(rotation_text), run_time=0.5)
    
    # # Highlight the nodes being rotated
    l_highlight = tree_structure.highlight_node(l_index, color=RED, duration=0.3)
    right_highlight = tree_structure.highlight_node(right_child_index, color=GREEN, duration=0.3)
    scene.wait(0.5)
    
    # Get the nodes involved in rotation
    l_node = tree_structure.nodes[l_index]
    r_node = tree_structure.nodes[right_child_index]
    l_data = tree_structure.tree_data[l_index]
    r_data = tree_structure.tree_data[right_child_index]
    
    # Calculate indices for all relevant positions
    l_left_index = 2 * l_index          # Left child of l (A)
    r_left_index = 2 * right_child_index    # Left child of r (B)  
    r_right_index = 2 * right_child_index + 1  # Right child of r (C)
    
    # Create new node and data mappings
    new_node_map = {}
    new_data_map = {}
    
    # Perform the rotation:

    # Things that don't move (Necessary to rebuild edges)
    for index in range(1,63):
        if not is_in_subtree(index, l_index) and index in tree_structure.tree_data:
            new_data_map[index] = tree_structure.tree_data[index]
            new_node_map[index] = tree_structure.nodes[index]

    # 1. r (right child) moves to l's position
    new_node_map[l_index] = r_node
    new_data_map[l_index] = r_data
    
    # 2. l moves to r's left child position
    new_node_map[l_index*2] = l_node
    new_data_map[l_index*2] = l_data
    
    # 3. Handle subtree movements
    # r's left child (B) becomes l's right child
    if r_left_index in tree_structure.nodes:
        # Move B subtree to be right child of l in its new position
        move_subtree(tree_structure, new_node_map, new_data_map, 
                    r_left_index, (2 * l_index)*2 + 1)
    if l_left_index in tree_structure.nodes:
        move_subtree(tree_structure, new_node_map, new_data_map,l_left_index, 2 * l_left_index)
    if r_right_index in tree_structure.nodes:
        # Move C subtree to be left child of r in its new position
        move_subtree(tree_structure, new_node_map, new_data_map, 
                    r_right_index, 2 * l_index + 1)

    # Create animations for all nodes to move to their new positions
    node_animations = []
    for new_index, node in new_node_map.items():
        level = tree_structure._get_level(new_index)
        new_pos = tree_structure.calculate_position(new_index, level)
        node_animations.append(node.animate.move_to(new_pos))
    
    # Create edge animations that follow the nodes
    edge_animations = []
    for (parent_idx, child_idx), edge in tree_structure.edges.items():
        if parent_idx in tree_structure.nodes and child_idx in tree_structure.nodes:
            parent_node = tree_structure.nodes[parent_idx]
            child_node = tree_structure.nodes[child_idx]
            
            def create_edge_updater(edge_line, p_node, c_node):
                def update_edge(mob, alpha):
                    # Update edge endpoints to follow nodes
                    start_point = p_node.get_bottom()
                    end_point = c_node.get_top()
                    edge_line.put_start_and_end_on(start_point, end_point)
                    return mob
                return UpdateFromAlphaFunc(edge_line, update_edge)
            
            edge_animation = create_edge_updater(edge, parent_node, child_node)
            edge_animations.append(edge_animation)
    
    # Execute all animations simultaneously (nodes + edges)
    all_animations = node_animations + edge_animations
    if all_animations:
        scene.play(*all_animations, run_time=1.2)
    

    # Update tree structure with new mapping
    tree_structure.nodes = new_node_map
    tree_structure.tree_data = new_data_map
    
    # Update positions
    for new_index, node in new_node_map.items():
        level = tree_structure._get_level(new_index)
        new_pos = tree_structure.calculate_position(new_index, level)
        tree_structure.positions[new_index] = new_pos
    
    # Rebuild edges to match new tree structure
    tree_structure.rebuild_edges()

    
    
    # Remove highlights
    tree_structure.remove_highlight(l_highlight, duration=0.3)
    tree_structure.remove_highlight(right_highlight, duration=0.3)
    
    scene.play(FadeOut(rotation_text), run_time=0.3)

def right_rotate(scene, tree_structure, r_index):

    l_index = 2 * r_index 
    if r_index not in tree_structure.nodes or l_index not in tree_structure.nodes:
        return
    
    # Show rotation text
    rotation_text = Text("Right Rotation", font_size=36, color=YELLOW).to_edge(UP)
    scene.play(Write(rotation_text), run_time=0.5)
    
    # Highlight the nodes being rotated
    r_highlight = tree_structure.highlight_node(r_index, color=RED, duration=0.3)
    left_highlight = tree_structure.highlight_node(l_index, color=GREEN, duration=0.3)
    scene.wait(0.5)
    
    # Get the nodes involved in rotation
    l_node = tree_structure.nodes[l_index]
    r_node = tree_structure.nodes[r_index]
    l_data = tree_structure.tree_data[l_index]
    r_data = tree_structure.tree_data[r_index]
    
    # Calculate indices for all relevant positions
    l_right_child = 2 * l_index +1  
    l_left_child = 2 * l_index
    r_right_child= 2 * r_index + 1  
    
    # Create new node and data mappings
    new_node_map = {}
    new_data_map = {}
    
    # Perform the rotation:

    # Things that don't move (Necessary to rebuild edges)
    for index in range(1,63):
        if not is_in_subtree(index, r_index) and index in tree_structure.tree_data:
            new_data_map[index] = tree_structure.tree_data[index]
            new_node_map[index] = tree_structure.nodes[index]

    # 1. l moves to r's position
    new_node_map[r_index] = l_node
    new_data_map[r_index] = l_data
    new_node_map[r_right_child] = r_node
    new_data_map[r_right_child] = r_data
    
    # 3. Handle subtree movements
    if l_left_child in tree_structure.nodes:
        move_subtree(tree_structure, new_node_map, new_data_map, l_left_child, l_index)
    if l_right_child in tree_structure.nodes:
        move_subtree(tree_structure, new_node_map, new_data_map, l_right_child, 2*(r_index*2+1))
    if r_right_child in tree_structure.nodes:
        move_subtree(tree_structure, new_node_map, new_data_map, r_right_child, r_right_child*2+1)

    
    # Create animations for all nodes to move to their new positions
    node_animations = []
    for new_index, node in new_node_map.items():
        level = tree_structure._get_level(new_index)
        new_pos = tree_structure.calculate_position(new_index, level)
        node_animations.append(node.animate.move_to(new_pos))
    
    # Create edge animations that follow the nodes
    edge_animations = []
    for (parent_idx, child_idx), edge in tree_structure.edges.items():
        if parent_idx in tree_structure.nodes and child_idx in tree_structure.nodes:
            parent_node = tree_structure.nodes[parent_idx]
            child_node = tree_structure.nodes[child_idx]
            
            def create_edge_updater(edge_line, p_node, c_node):
                def update_edge(mob, alpha):
                    # Update edge endpoints to follow nodes
                    start_point = p_node.get_bottom()
                    end_point = c_node.get_top()
                    edge_line.put_start_and_end_on(start_point, end_point)
                    return mob
                return UpdateFromAlphaFunc(edge_line, update_edge)
            
            edge_animation = create_edge_updater(edge, parent_node, child_node)
            edge_animations.append(edge_animation)
    
    # Execute all animations simultaneously (nodes + edges)
    all_animations = node_animations + edge_animations
    if all_animations:
        scene.play(*all_animations, run_time=1.2)
    
    # Update tree structure with new mapping
    tree_structure.nodes = new_node_map
    tree_structure.tree_data = new_data_map
    
    # Update positions
    for new_index, node in new_node_map.items():
        level = tree_structure._get_level(new_index)
        new_pos = tree_structure.calculate_position(new_index, level)
        tree_structure.positions[new_index] = new_pos
    
    # Rebuild edges to match new tree structure
    tree_structure.rebuild_edges()
    
    # Remove highlights
    tree_structure.remove_highlight(r_highlight, duration=0.3)
    tree_structure.remove_highlight(left_highlight, duration=0.3)
    
    scene.play(FadeOut(rotation_text), run_time=0.3)

def left_swap(scene, tree_structure, x_index):
    """Simple left swap - just exchange positions of x and its right child"""
    y_index = 2 * x_index + 1  # Right child of x
    
    if x_index not in tree_structure.nodes or y_index not in tree_structure.nodes:
        return
    
    # Show swap text
    swap_text = Text("Left Swap (Position Only)", font_size=32, color=BLUE).to_edge(UP)
    scene.play(Write(swap_text), run_time=0.5)
    
    # Highlight the nodes being swapped
    x_highlight = tree_structure.highlight_node(x_index, color=RED, duration=0.3)
    y_highlight = tree_structure.highlight_node(y_index, color=GREEN, duration=0.3)
    scene.wait(0.5)
    
    # Perform the swap by exchanging positions only
    tree_structure.swap_nodes(x_index, y_index)
    
    # Update edges
    scene.wait(0.5)
    tree_structure.rebuild_edges()
    
    # Remove highlights
    tree_structure.remove_highlight(x_highlight, duration=0.3)
    tree_structure.remove_highlight(y_highlight, duration=0.3)
    
    scene.play(FadeOut(swap_text), run_time=0.3)

def right_swap(scene, tree_structure, y_index):
    """Simple right swap - just exchange positions of y and its left child"""
    x_index = 2 * y_index  # Left child of y
    
    if y_index not in tree_structure.nodes or x_index not in tree_structure.nodes:
        return
    
    # Show swap text
    swap_text = Text("Right Swap (Position Only)", font_size=32, color=BLUE).to_edge(UP)
    scene.play(Write(swap_text), run_time=0.5)
    
    # Highlight the nodes being swapped
    y_highlight = tree_structure.highlight_node(y_index, color=RED, duration=0.3)
    x_highlight = tree_structure.highlight_node(x_index, color=GREEN, duration=0.3)
    scene.wait(0.5)
    
    # Perform the swap by exchanging positions only
    tree_structure.swap_nodes(y_index, x_index)
    
    # Update edges
    scene.wait(0.5)
    tree_structure.rebuild_edges()
    
    # Remove highlights
    tree_structure.remove_highlight(y_highlight, duration=0.3)
    tree_structure.remove_highlight(x_highlight, duration=0.3)
    
    scene.play(FadeOut(swap_text), run_time=0.3)

def swap_node_values(scene, tree_structure, index1, index2, duration=1.5):
    """Swap values between two nodes with animation"""
    if index1 not in tree_structure.nodes or index2 not in tree_structure.nodes:
        return
    
    # Highlight nodes
    highlight1 = tree_structure.highlight_node(index1, color=YELLOW, duration=0.3)
    highlight2 = tree_structure.highlight_node(index2, color=BLUE, duration=0.3)
    
    scene.wait(0.5)
    
    # Get current data
    label1, color_char1 = tree_structure.tree_data[index1]
    label2, color_char2 = tree_structure.tree_data[index2]
    
    # Create temporary text for animation
    node1 = tree_structure.nodes[index1]
    node2 = tree_structure.nodes[index2]
    
    temp_text1 = Text(label1, font_size=24, color=WHITE).move_to(node1.get_center())
    temp_text2 = Text(label2, font_size=24, color=WHITE).move_to(node2.get_center())
    
    tree_structure.update_node_data(index1, new_label=" ")
    tree_structure.update_node_data(index2, new_label=" ")
    scene.add(temp_text1, temp_text2)
    
    # Animate text movement
    scene.play(
        temp_text1.animate.move_to(node2.get_center()),
        temp_text2.animate.move_to(node1.get_center()),
        run_time=duration
    )
    
    scene.remove(temp_text1, temp_text2)
    
    # Update the actual node data
    tree_structure.update_node_data(index1, new_label=label2)
    tree_structure.update_node_data(index2, new_label=label1)
    
    # Remove highlights
    tree_structure.remove_highlight(highlight1, duration=0.3)
    tree_structure.remove_highlight(highlight2, duration=0.3)

def mark_for_deletion(scene, tree_structure, index, duration=0.8):
    """Mark a node for deletion with blue X"""
    if index not in tree_structure.nodes:
        return None
    
    node = tree_structure.nodes[index]
    
    # Create X mark
    x_mark = VGroup(
        Line(UP * 0.3 + LEFT * 0.3, DOWN * 0.3 + RIGHT * 0.3, color=BLUE, stroke_width=8),
        Line(UP * 0.3 + RIGHT * 0.3, DOWN * 0.3 + LEFT * 0.3, color=BLUE, stroke_width=8)
    ).move_to(node.get_center())
    
    scene.play(Create(x_mark), run_time=duration)
    return x_mark

def find_inorder_successor(tree_structure, node_index):
    """Find the inorder successor of a node (leftmost node in right subtree)"""
    # Go to right child
    right_child = 2 * node_index + 1
    if right_child not in tree_structure.nodes:
        return None
    
    # Keep going left until no more left children
    current = right_child
    while 2 * current in tree_structure.nodes:  # While left child exists
        current = 2 * current
    
    return current

def count_children(tree_structure, node_index):
    """Count how many children a node has"""
    left_child = 2 * node_index
    right_child = 2 * node_index + 1
    
    count = 0
    if left_child in tree_structure.nodes:
        count += 1
    if right_child in tree_structure.nodes:
        count += 1
    
    return count

def move_subtree_up(scene, tree_structure, deleted_index, child_index):
    """Move an entire subtree up when its parent is deleted"""
    if child_index not in tree_structure.nodes:
        return
    
    # Get all nodes in the subtree rooted at child_index
    subtree_nodes = collect_subtree_nodes(tree_structure, child_index)
    
    # Create mapping: child_index takes deleted_index position, 
    # and all other nodes in subtree maintain their relative structure
    new_mapping = {}
    
    # The child takes the deleted node's position
    new_mapping[child_index] = deleted_index
    
    # For other nodes in subtree, we need to maintain the tree structure
    # by calculating their new positions relative to the new root
    for node_idx in subtree_nodes:
        if node_idx != child_index:
            # Find the path from child_index to node_idx
            path = get_relative_path(node_idx, child_index)
            # Apply this path starting from the new position (deleted_index)
            new_index = apply_relative_path(deleted_index, path)
            new_mapping[node_idx] = new_index
    
    # Animate movement
    animations = []
    for old_idx, new_idx in new_mapping.items():
        if old_idx in tree_structure.nodes:
            node = tree_structure.nodes[old_idx]
            new_pos = tree_structure.calculate_position(new_idx, tree_structure._get_level(new_idx))
            animations.append(node.animate.move_to(new_pos))
    
    if animations:
        scene.play(*animations, run_time=1.0)
    
    # Update tree structure
    new_nodes = {}
    new_data = {}
    new_positions = {}
    
    for old_idx, new_idx in new_mapping.items():
        if old_idx in tree_structure.nodes:
            new_nodes[new_idx] = tree_structure.nodes[old_idx]
            new_data[new_idx] = tree_structure.tree_data[old_idx]
            new_positions[new_idx] = tree_structure.calculate_position(new_idx, tree_structure._get_level(new_idx))
    
    # Remove old entries
    for old_idx in subtree_nodes:
        if old_idx in tree_structure.nodes:
            del tree_structure.nodes[old_idx]
            del tree_structure.tree_data[old_idx]
            if old_idx in tree_structure.positions:
                del tree_structure.positions[old_idx]
    
    # Add new entries
    tree_structure.nodes.update(new_nodes)
    tree_structure.tree_data.update(new_data)
    tree_structure.positions.update(new_positions)
    
    # Rebuild edges
    tree_structure.rebuild_edges()

def delete_node(scene, tree_structure, target_index):
    """Delete a node following the three cases of binary tree deletion"""
    if target_index not in tree_structure.nodes:
        return
    
    # Show deletion text
    target_label = tree_structure.tree_data[target_index][0]
    deletion_text = Text(f"Deleting node {target_label}", font_size=32, color=RED).to_edge(UP)
    scene.play(Write(deletion_text), run_time=0.8)
    
    # Highlight target
    target_highlight = tree_structure.highlight_node(target_index, color=RED, duration=0.5)
    scene.wait(1)
    
    # Count children to determine deletion case
    num_children = count_children(tree_structure, target_index)
    left_child = 2 * target_index
    right_child = 2 * target_index + 1
    
    if num_children == 0:
        # Case 1: No children - simply delete the node
        case_text = Text("Case 1: No children - simple deletion", font_size=24, color=YELLOW).next_to(deletion_text, DOWN)
        scene.play(Write(case_text), run_time=0.8)
        scene.wait(1)
        
        deletion_mark = mark_for_deletion(scene, tree_structure, target_index, duration=0.8)
        scene.wait(1)
        
        scene.play(FadeOut(deletion_mark), run_time=0.3)
        tree_structure.remove_node(target_index, animate=True)
        scene.play(FadeOut(case_text), run_time=0.5)

    if num_children == 1:
        # Case 2: One child - delete node and move subtree up
        child_index = left_child if left_child in tree_structure.nodes else right_child
        child_label = tree_structure.tree_data[child_index][0]
        
        case_text = Text(f"Case 2: One child ({child_label}) - move subtree up", font_size=24, color=YELLOW).next_to(deletion_text, DOWN)
        scene.play(Write(case_text), run_time=0.8)
        
        # Highlight the child
        child_highlight = tree_structure.highlight_node(child_index, color=GREEN, duration=0.5)
        scene.wait(1)
        
        # Remove the target node first
        deletion_mark = mark_for_deletion(scene, tree_structure, target_index, duration=0.8)
        scene.wait(1)
        scene.play(FadeOut(deletion_mark), run_time=0.3)
        tree_structure.remove_node(target_index, animate=True)
        
        # Move the subtree up
        scene.play(Transform(case_text, 
                Text("Moving subtree up...", font_size=24, color=BLUE).next_to(deletion_text, DOWN)), 
                run_time=0.5)
        
        # Prepare new node mapping
        new_node_map = {}
        new_data_map = {}
        for index in range(1, 63):
            if index in tree_structure.nodes and not is_in_subtree(index, target_index):
                new_node_map[index] = tree_structure.nodes[index]
                new_data_map[index] = tree_structure.tree_data[index]
        
        move_subtree(tree_structure, new_node_map, new_data_map, child_index, target_index)
        
        # Create animations for all nodes to move to their new positions
        node_animations = []
        for new_index, node in new_node_map.items():
            level = tree_structure._get_level(new_index)
            new_pos = tree_structure.calculate_position(new_index, level)
            node_animations.append(node.animate.move_to(new_pos))
        
        # Create edge animations - only for edges that will persist
        edge_animations = []
        edges_to_remove = []
        
        for (parent_idx, child_idx), edge in tree_structure.edges.items():
            # Check if this edge will exist after the transformation
            parent_new_idx = None
            child_new_idx = None
            
            # Find where parent and child will be in new mapping
            for new_idx, old_node in new_node_map.items():
                if old_node == tree_structure.nodes.get(parent_idx):
                    parent_new_idx = new_idx
                if old_node == tree_structure.nodes.get(child_idx):
                    child_new_idx = new_idx
            
            if parent_new_idx is not None and child_new_idx is not None:
                # This edge will persist - animate it
                parent_node = tree_structure.nodes[parent_idx]
                child_node = tree_structure.nodes[child_idx]
                
                def create_edge_updater(edge_line, p_node, c_node):
                    def update_edge(mob, alpha):
                        start_point = p_node.get_bottom()
                        end_point = c_node.get_top()
                        edge_line.put_start_and_end_on(start_point, end_point)
                        return mob
                    return UpdateFromAlphaFunc(edge_line, update_edge)
                
                edge_animation = create_edge_updater(edge, parent_node, child_node)
                edge_animations.append(edge_animation)
            else:
                # This edge will be removed - mark it for deletion
                edges_to_remove.append(edge)
        
        # Remove edges that won't exist anymore
        if edges_to_remove:
            scene.play(*[FadeOut(edge) for edge in edges_to_remove], run_time=0.3)
        


        # Execute node animations and persisting edge animations simultaneously
        tree_structure.remove_highlight(child_highlight, duration=0.3) #remove the highlight
        all_animations = node_animations + edge_animations
        if all_animations:
            scene.play(*all_animations, run_time=1.0)
        
        # Update tree structure with new mapping AFTER animation
        tree_structure.nodes = new_node_map
        tree_structure.tree_data = new_data_map
        
        # Update positions
        for new_index, node in new_node_map.items():
            level = tree_structure._get_level(new_index)
            new_pos = tree_structure.calculate_position(new_index, level)
            tree_structure.positions[new_index] = new_pos
        
        # Create new edges that didn't exist before
        tree_structure.rebuild_edges()
        
        # Animate in any new edges
        new_edges = []
        for (parent_idx, child_idx), edge in tree_structure.edges.items():
            # This is a newly created edge
            new_edges.append(edge)
        
        if new_edges:
            scene.play(*[Create(edge) for edge in new_edges], run_time=0.5)
        
        scene.play(FadeOut(case_text), run_time=0.5)
        
    else:
        # Case 3: Two children - find successor, swap values, then delete successor
        successor_index = find_inorder_successor(tree_structure, target_index)
        
        if successor_index:
            successor_label = tree_structure.tree_data[successor_index][0]
            case_text = Text(f"Case 3: Two children - find successor ({successor_label})", font_size=24, color=YELLOW).next_to(deletion_text, DOWN)
            scene.play(Write(case_text), run_time=0.8)
            
            # Highlight the successor
            successor_highlight = tree_structure.highlight_node(successor_index, color=GREEN, duration=0.5)
            scene.wait(1)
            
            # Show successor finding process
            scene.play(Transform(case_text, 
                               Text("Finding successor: go right, then left until no more left", font_size=20, color=BLUE).next_to(deletion_text, DOWN)), 
                               run_time=0.8)
            scene.wait(1.5)
            
            # Swap values
            scene.play(Transform(case_text, 
                               Text("Swapping values with successor...", font_size=24, color=YELLOW).next_to(deletion_text, DOWN)), 
                               run_time=0.5)
            
            swap_node_values(scene, tree_structure, target_index, successor_index, duration=1.5)
            scene.wait(1)
            
            # Now delete the successor (which will have at most one child)
            scene.play(Transform(case_text, 
                               Text("Now deleting successor node...", font_size=24, color=RED).next_to(deletion_text, DOWN)), 
                               run_time=0.5)
            
            tree_structure.remove_highlight(successor_highlight, duration=0.3)
            scene.play(FadeOut(case_text), run_time=0.5)
            
            # Recursively delete the successor (it will be case 1 or 2)
            delete_node(scene, tree_structure, successor_index)
    
    tree_structure.remove_highlight(target_highlight, duration=0.3)
    scene.play(FadeOut(deletion_text), run_time=0.5)

def show_deletion_steps(scene, tree_structure, target_index, successor_index=None):
    """Demonstrate complete deletion process using proper binary tree deletion"""
    delete_node(scene, tree_structure, target_index)

def animate_rebalancing(scene, tree_structure, affected_indices, duration=2.0):
    """Animate rebalancing process"""
    rebalance_text = Text("Rebalancing tree...", font_size=32, color=BLUE).to_edge(UP)
    scene.play(Write(rebalance_text), run_time=0.5)
    
    # Highlight affected nodes
    highlights = []
    colors = [BLUE, PURPLE, ORANGE, PINK, TEAL]
    
    for i, index in enumerate(affected_indices):
        if index in tree_structure.nodes:
            color = colors[i % len(colors)]
            highlight = tree_structure.highlight_node(index, color=color, duration=0.3)
            highlights.append(highlight)
            scene.wait(0.2)
    
    scene.wait(duration)
    
    # Remove highlights
    for highlight in highlights:
        tree_structure.remove_highlight(highlight, duration=0.2)
    
    scene.play(FadeOut(rebalance_text), run_time=0.5)

def change_colors(scene, tree_structure, indices, colors):
    """Change colors of multiple nodes"""
    animations = []
    color_map = {"B": BLACK, "R": RED, "O": ORANGE}
    
    for i, c in zip(indices, colors):
        if i in tree_structure.nodes:
            node = tree_structure.nodes[i]
            animations.append(node.circle.animate.set_fill(color_map.get(c, WHITE)))
            tree_structure.update_node_data(i, new_color_char=c)
    
    if animations:
        scene.play(*animations, run_time=0.4)

class RedBlackTreeDeletionDemo(Scene):
    def construct(self):
        # Create tree structure
        tree = TreeStructure(self)
        
        # Title
        title = Text("Red-Black Tree Operations Demo", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        self.wait(1)
        
        # Build tree
        data = ["B7", "R4", "R10", None, "B5", "B8", "B12", None, None, "R3"]
        build_tree_from_list(tree, data)
        self.wait(1)
        
        # Demo 1: Highlighting
        demo_text = Text("Demo 1: Node highlighting", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(demo_text), run_time=0.8)
        
        highlight1 = tree.highlight_node(2, color=YELLOW, duration=0.5)
        self.wait(0.5)
        highlight2 = tree.highlight_node(5, color=GREEN, duration=0.5)
        self.wait(1)
        
        tree.remove_highlight(highlight1)
        tree.remove_highlight(highlight2)
        self.play(FadeOut(demo_text), run_time=0.5)
        self.wait(0.5)
        
        # Demo 2: Value swapping
        demo_text = Text("Demo 2: Value swapping", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(demo_text), run_time=0.8)
        
        swap_node_values(self, tree, 2, 5, duration=1.5)
        self.wait(1)
        self.play(FadeOut(demo_text), run_time=0.5)
        
        # Demo 3: Rotations
        demo_text = Text("Demo 3: Tree rotations", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(demo_text), run_time=0.8)
        
        left_rotate(self, tree, 1)
        self.wait(1)
        right_rotate(self, tree, 2)
        self.wait(1)
        self.play(FadeOut(demo_text), run_time=0.5)
        
        # Demo 4: Deletion
        demo_text = Text("Demo 4: Node deletion", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(demo_text), run_time=0.8)
        
        show_deletion_steps(self, tree, target_index=2)
        self.wait(1)
        self.play(FadeOut(demo_text), run_time=0.5)
        
        # Demo 5: Rebalancing
        demo_text = Text("Demo 5: Rebalancing animation", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(demo_text), run_time=0.8)
        
        animate_rebalancing(self, tree, [1, 4, 6], duration=2.5)
        self.play(FadeOut(demo_text), run_time=0.5)
        
        self.play(FadeOut(title), run_time=1)
        self.wait(2)