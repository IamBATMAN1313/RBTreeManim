# rbtree_documentation.md
# Red-Black Tree Visualization Library Documentation

This library provides a comprehensive set of tools for creating animated red-black tree visualizations using Manim. It includes classes for tree nodes, tree structures, arrows, and various tree operations.

The Header file assumes the tree depth will be at most 6 and uses 63 nodes. Change the number if you need more.

## Classes

### TreeNode(VGroup)

A visual representation of a tree node with customizable color and size.

**Constructor:**
```python
TreeNode(label, color_char="B", radius=0.3, **kwargs)
```

**Parameters:**
- `label`: Text to display in the node
- `color_char`: Color code ("B"=Black, "R"=Red, "O"=Orange, "W"=White, "b"=Blue, "G"=Green)
- `radius`: Size of the node circle

**Methods:**
- `set_node_color(color_char)`: Change node color
- `update_label(new_label)`: Update the text label
- `scale_node(scale_factor)`: Resize the node

### TreeArrow

Creates and manages arrows pointing to tree nodes.

**Constructor:**
```python
TreeArrow(scene, tree_structure, color=YELLOW)
```

**Methods:**
- `create_arrow(index)`: Create arrow pointing to node at index
- `move_to(new_index)`: Move arrow to different node
- `remove()`: Remove the arrow

### TreeStructure

Main class for managing the complete tree visualization.

**Constructor:**
```python
TreeStructure(scene, radius=0.3, h_spacing=5.0, v_spacing=1.2, root_pos=None)
```

**Parameters:**
- `scene`: Manim scene object
- `radius`: Default node radius
- `h_spacing`: Horizontal spacing between levels
- `v_spacing`: Vertical spacing between levels
- `root_pos`: Position of root node

**Key Methods:**
- `add_node(index, label, color_char="B", animate=True)`: Add a node
- `remove_node(index, animate=True)`: Remove a node
- `swap_nodes(index1, index2, animate=True)`: Swap two nodes
- `highlight_node(index, color=YELLOW, duration=0.5)`: Highlight a node
- `move_tree(dx=0, dy=0, scale_factor=1.0, duration=1.5)`: Move/scale entire tree
- `rebuild_edges()`: Recreate all edges based on current structure

## Tree Operations

### Rotations

**left_rotate(scene, tree_structure, l_index, highlight=True)**
- Performs left rotation on node at l_index
- Animates the rotation process
- Updates tree structure accordingly

**right_rotate(scene, tree_structure, r_index, highlight=True)**
- Performs right rotation on node at r_index
- Mirror operation of left rotation

### Node Manipulation

**swap_node_values(scene, tree_structure, index1, index2, duration=1.5)**
- Swaps the values between two nodes with animation
- Shows the exchange visually

**delete_node(scene, tree_structure, target_index)**
- Implements complete BST deletion with three cases:
  - Case 1: No children (leaf node)
  - Case 2: One child
  - Case 3: Two children (uses inorder successor)

### Utility Functions

**build_tree_from_list(tree_structure, data)**
- Builds tree from array representation
- Format: ["B5", "R3", "B8", None, "R7", ...]

**collect_subtree_nodes(tree_structure, root_index)**
- Returns all node indices in a subtree

**find_inorder_successor(tree_structure, node_index)**
- Finds the inorder successor of a given node

**count_children(tree_structure, node_index)**
- Returns number of children (0, 1, or 2)

## Color Codes

- "B": Black
- "R": Red  
- "O": Orange
- "W": White
- "b": Blue
- "G": Green

## Index System

The library uses binary heap indexing:
- Root: index 1
- Left child of node i: index 2*i
- Right child of node i: index 2*i+1
- Parent of node i: index i//2

## Animation Features

- Smooth node movements and rotations
- Color-coded highlighting
- Edge animations that follow node movements
- Configurable timing and effects
- Support for scaling and repositioning entire trees

## Advanced Features

- **Subtree Operations**: Move entire subtrees while maintaining structure
- **Relative Positioning**: Calculate positions based on tree relationships
- **Path Finding**: Get paths between nodes for complex operations
- **Edge Management**: Automatic edge creation and updates
- **Visual Effects**: Highlights, arrows, and deletion markers

This library is designed for educational purposes, making complex tree operations visually understandable through step-by-step animations.