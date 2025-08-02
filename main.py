from rbtree import *

class BasicTreeExample(Scene):
    def construct(self):
        """Creating a basic tree"""
        title = Text("Basic Tree Creation", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        # Create tree structure
        tree = TreeStructure(self, radius=0.3, h_spacing=4, v_spacing=1.2)
        
        # Add nodes one by one
        nodes_data = [
            (1, "10", "B"),  # Root
            (2, "5", "R"),   # Left child
            (3, "15", "B"),  # Right child
            (4, "3", "B"),   # Left-left
            (5, "7", "B"),   # Left-right
            (6, "12", "R"),  # Right-left
            (7, "18", "R")   # Right-right
        ]
        
        for index, label, color in nodes_data:
            tree.add_node(index, label, color, animate=True)
            self.wait(0.3)
        
        # Build edges
        tree.rebuild_edges()
        self.wait(2)

class ColorDemonstration(Scene):
    def construct(self):
        """Different colors and highlighting"""
        title = Text("Colors and Highlighting", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        tree = TreeStructure(self, radius=0.35, h_spacing=3, v_spacing=1.0)
        
        # Create nodes with different colors
        color_demo = [
            (1, "B", "B"),   # Black
            (2, "R", "R"),   # Red
            (3, "O", "O"),   # Orange
            (4, "W", "W"),   # White
            (5, "Bl", "b"),  # Blue
            (6, "G", "G")    # Green
        ]
        
        for index, label, color in color_demo:
            tree.add_node(index, label, color, animate=True)
            self.wait(0.2)
        
        tree.rebuild_edges()
        self.wait(1)
        
        # Demonstrate highlighting
        for index in [1, 2, 3, 4, 5, 6]:
            if index in tree.nodes:
                highlight = tree.highlight_node(index, color=YELLOW, duration=0.3)
                self.wait(0.5)
                tree.remove_highlight(highlight, duration=0.3)

class ArrowDemo(Scene):
    def construct(self):
        """Using arrows"""
        title = Text("Arrow Demonstrations", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        tree = TreeStructure(self, radius=0.3, h_spacing=4, v_spacing=1.2)
        
        # Build tree
        tree_data = ["B8", "R4", "B12", "B2", "B6", "R10", "R14"]
        build_tree_from_list(tree, tree_data)
        self.wait(1)
        
        # Create arrow
        arrow = TreeArrow(self, tree, color=RED)
        
        # Move arrow through different nodes
        for index in [1, 2, 4, 5, 3, 6, 7]:
            if index <= len(tree_data):
                arrow.create_arrow(index) if index == 1 else arrow.move_to(index)
                self.wait(1)
        
        arrow.remove()
        self.wait(1)

class SwapAndMovement(Scene):
    def construct(self):
        """Node swapping and value changes"""
        title = Text("Swapping and Updates", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        tree = TreeStructure(self, radius=0.3, h_spacing=4, v_spacing=1.2)
        
        # Build initial tree
        initial_data = ["B5", "R3", "B8", "B1", "B4", "R7", "R9"]
        build_tree_from_list(tree, initial_data)
        self.wait(2)
        
        # Demonstrate value swapping
        explanation = Text("Swapping values between nodes 1 and 3", font_size=24, color=YELLOW)
        explanation.to_edge(DOWN)
        self.play(Write(explanation), run_time=1)
        
        swap_node_values(self, tree, 1, 3, duration=2)
        self.wait(2)
        
        self.play(FadeOut(explanation), run_time=0.5)
        
        # Demonstrate color changes
        explanation2 = Text("Changing node colors", font_size=24, color=GREEN)
        explanation2.to_edge(DOWN)
        self.play(Write(explanation2), run_time=1)
        
        # Change colors of nodes 2 and 6
        tree.update_node_data(2, new_color_char="B")
        tree.update_node_data(6, new_color_char="G")
        
        self.wait(2)

class RotationDemo(Scene):
    def construct(self):
        """Tree rotations"""
        title = Text("Tree Rotations", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        tree = TreeStructure(self, radius=0.3, h_spacing=5, v_spacing=1.2)
        
        # Build tree for rotation demo
        rotation_data = ["B10", "R5", "B15", "B3", "B8", "R12", "R18"]
        build_tree_from_list(tree, rotation_data)
        self.wait(2)
        
        # Left rotation demonstration
        left_text = Text("Left Rotation on node 10", font_size=24, color=GREEN)
        left_text.to_corner(DR)
        self.play(Write(left_text), run_time=1)
        
        left_rotate(self, tree, 1)
        self.wait(2)
        
        self.play(FadeOut(left_text), run_time=0.5)
        
        # Right rotation demonstration
        right_text = Text("Right Rotation on node 15", font_size=24, color=BLUE)
        right_text.to_corner(DR)
        self.play(Write(right_text), run_time=1)
        
        right_rotate(self, tree, 1)
        self.wait(2)

class DeletionDemo(Scene):
    def construct(self):
        """Node deletion cases"""
        title = Text("Tree Node Deletion", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        tree = TreeStructure(self, radius=0.3, h_spacing=4, v_spacing=1.2)
        
        # Build tree for deletion
        deletion_data = ["B20", "R10", "B30", "B5", "R15", "B25", "R35", "B3", "B7", "B12", "B18"]
        build_tree_from_list(tree, deletion_data)
        self.wait(2)
        
        # Case 1: Delete leaf node (index 5 - node "25")
        case1_text = Text("Case 1: Deleting leaf node (25)", font_size=24, color=YELLOW)
        case1_text.to_corner(DR)
        self.play(Write(case1_text), run_time=1)
        
        delete_node(self, tree, 5)
        self.wait(2)
        self.play(FadeOut(case1_text), run_time=0.5)
        
        # Case 2: Delete node with one child (index 3 - node "30")
        case2_text = Text("Case 2: Deleting node with one child (30)", font_size=24, color=ORANGE)
        case2_text.to_corner(DR)
        self.play(Write(case2_text), run_time=1)
        
        delete_node(self, tree, 3)
        self.wait(2)
        self.play(FadeOut(case2_text), run_time=0.5)
        
        # Case 3: Delete node with two children (index 2 - node "10")
        case3_text = Text("Case 3: Deleting node with two children (10)", font_size=24, color=RED)
        case3_text.to_corner(DR)
        self.play(Write(case3_text), run_time=1)
        
        delete_node(self, tree, 2)
        self.wait(2)

class TreeMovementDemo(Scene):
    def construct(self):
        """Moving and scaling trees"""
        title = Text("Tree Movement and Scaling", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        tree = TreeStructure(self, radius=0.25, h_spacing=3, v_spacing=1.0)
        
        # Build compact tree
        movement_data = ["B8", "R4", "B12", "B2", "B6", "R10", "R14"]
        build_tree_from_list(tree, movement_data)
        self.wait(2)
        
        # Demonstrate movement
        move_text = Text("Moving tree right and up", font_size=24, color=GREEN)
        move_text.to_corner(DL)
        self.play(Write(move_text), run_time=1)
        
        tree.move_tree(dx=2, dy=1, scale_factor=1.0, duration=2)
        self.wait(1)
        
        self.play(Transform(move_text, Text("Scaling tree larger", font_size=24, color=BLUE).to_corner(DL)), run_time=1)
        
        tree.move_tree(dx=0, dy=0, scale_factor=1.5, duration=2)
        self.wait(1)
        
        self.play(Transform(move_text, Text("Moving and shrinking", font_size=24, color=ORANGE).to_corner(DL)), run_time=1)
        
        tree.move_tree(dx=-3, dy=-1, scale_factor=0.7, duration=2)
        self.wait(2)

class ComplexOperationsDemo(Scene):
    def construct(self):
        """Complex tree operations"""
        title = Text("Complex Operations", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        tree = TreeStructure(self, radius=0.3, h_spacing=4, v_spacing=1.2)
        
        # Build initial tree
        complex_data = ["B50", "R25", "B75", "B12", "R37", "B62", "R87", "B6", "B18", "B31", "B43"]
        build_tree_from_list(tree, complex_data)
        self.wait(2)
        
        # Demonstrate finding inorder successor
        successor_text = Text("Finding inorder successor of 25", font_size=24, color=YELLOW)
        successor_text.to_corner(DR)
        self.play(Write(successor_text), run_time=1)
        
        # Highlight node 25 (index 2)
        highlight1 = tree.highlight_node(2, color=RED, duration=0.5)
        
        # Find and highlight successor
        successor_idx = find_inorder_successor(tree, 2)
        if successor_idx:
            highlight2 = tree.highlight_node(successor_idx, color=GREEN, duration=0.5)
            self.wait(3)
            tree.remove_highlight(highlight2, duration=0.3)
        
        tree.remove_highlight(highlight1, duration=0.3)
        self.play(FadeOut(successor_text), run_time=0.5)
        
        # Demonstrate subtree collection
        subtree_text = Text("Highlighting subtree rooted at 25", font_size=24, color=BLUE)
        subtree_text.to_corner(DR)
        self.play(Write(subtree_text), run_time=1)
        
        subtree_nodes = collect_subtree_nodes(tree, 2)
        highlights = []
        colors = [BLUE, PURPLE, ORANGE, PINK, TEAL]
        
        for i, node_idx in enumerate(subtree_nodes):
            color = colors[i % len(colors)]
            highlight = tree.highlight_node(node_idx, color=color, duration=0.3)
            highlights.append(highlight)
            self.wait(0.3)
        
        self.wait(2)
        
        # Remove all highlights
        for highlight in highlights:
            tree.remove_highlight(highlight, duration=0.2)
        
        self.wait(1)

    def construct(self):
        """Example 9: Educational step-by-step demonstration"""
        title = Text("Example 9: Educational Red-Black Tree Operations", font_size=28, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        tree = TreeStructure(self, radius=0.3, h_spacing=4, v_spacing=1.2, root_pos=ORIGIN + UP * 1.5)
        
        # Step 1: Build tree
        step1 = Text("Step 1: Building Red-Black Tree", font_size=24, color=GREEN)
        step1.to_corner(DL)
        self.play(Write(step1), run_time=1)
        
        educational_data = ["B10", "R5", "R15", "B3", "B7", "B12", "B20"]
        for i, data in enumerate(educational_data, 1):
            if data:
                color_char = data[0]
                label = data[1:]
                tree.add_node(i, label, color_char, animate=True)
                self.wait(0.5)
        
        tree.rebuild_edges()
        self.wait(1)
        
        # Step 2: Demonstrate property violation
        step2 = Text("Step 2: Identifying Red-Red Violation", font_size=24, color=RED)
        self.play(Transform(step1, step2), run_time=1)
        
        # Highlight red nodes
        red_highlights = []
        for idx in [2, 3]:  # Nodes 5 and 15
            highlight = tree.highlight_node(idx, color=YELLOW, duration=0.5)
            red_highlights.append(highlight)
        
        self.wait(2)
        
        # Step 3: Fix with rotation
        step3 = Text("Step 3: Fixing with Left Rotation", font_size=24, color=BLUE)
        self.play(Transform(step1, step3), run_time=1)
        
        # Remove highlights
        for highlight in red_highlights:
            tree.remove_highlight(highlight, duration=0.3)
        
        # Perform rotation
        left_rotate(self, tree, 1)
        self.wait(2)
        
        # Step 4: Final result
        step4 = Text("Step 4: Balanced Red-Black Tree", font_size=24, color=GREEN)
        self.play(Transform(step1, step4), run_time=1)
        self.wait(3)