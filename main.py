from rbtree import *

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