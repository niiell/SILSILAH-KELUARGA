import graphviz

def parse_family_data(lines):
    """
    Parse the hierarchical family data from lines of text.
    Returns a nested dictionary representing the family tree.
    """
    family_tree = {}
    stack = [(family_tree, -1)]  # (current_dict, indent_level)

    for line in lines:
        stripped = line.lstrip()
        if not stripped:
            continue
        indent = len(line) - len(stripped)
        # Find parent level
        while stack and indent <= stack[-1][1]:
            stack.pop()
        parent_dict = stack[-1][0]

        # Extract name and spouse info
        # Remove leading dashes and spaces
        name = stripped.lstrip('- ').strip()
        # Add this member as a dict to parent
        parent_dict[name] = {}
        # Push this member to stack
        stack.append((parent_dict[name], indent))
    return family_tree

def print_family_summary(family_dict, level=0):
    """
    Print a summary of the family tree for verification.
    """
    indent = '  ' * level
    for member, children in family_dict.items():
        print(f"{indent}- {member}")
        print_family_summary(children, level + 1)

def print_family_detailed(family_dict, parent=None):
    """
    Print detailed family members and their children for thorough verification.
    """
    for member, children in family_dict.items():
        if parent:
            print(f"Parent: {parent} -> Child: {member}")
        else:
            print(f"Root member: {member}")
        print_family_detailed(children, member)

def add_nodes_edges(graph, family_dict, parent=None):
    """
    Recursively add nodes and edges to the graph from the family dictionary.
    """
    for member, children in family_dict.items():
        # Add node for member
        label = member.replace('(✞)', '†')  # Replace death symbol with cross
        graph.node(label, label)
        if parent:
            graph.edge(parent, label)
        # Recurse for children
        add_nodes_edges(graph, children, label)

def main():
    # Read family data from file
    with open('poparan.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    family_tree = parse_family_data(lines)

    # Create a graphviz Digraph for JPEG landscape
    dot_jpeg = graphviz.Digraph(comment='Family Tree Landscape', format='png')
    dot_jpeg.attr(rankdir='LR', dpi='600', size='11.69,8.27!')  # A4 landscape size in inches, no compression
    add_nodes_edges(dot_jpeg, family_tree)
    output_jpeg = 'family_tree_landscape.png'
    dot_jpeg.render(filename='public/family_tree_landscape', cleanup=True)
    print(f'Family tree landscape image generated: {output_jpeg}')

    # Create a graphviz Digraph for PDF landscape
    dot_pdf = graphviz.Digraph(comment='Family Tree Landscape', format='pdf')
    dot_pdf.attr(rankdir='LR', dpi='600', size='11.69,8.27!')  # A4 landscape size in inches, no compression
    add_nodes_edges(dot_pdf, family_tree)
    output_pdf = 'family_tree_landscape.pdf'
    dot_pdf.render(filename='family_tree_landscape', cleanup=True)
    print(f'Family tree landscape PDF generated: {output_pdf}')

    # Create a graphviz Digraph for JPEG portrait
    dot_jpeg_v = graphviz.Digraph(comment='Family Tree Portrait', format='png')
    dot_jpeg_v.attr(rankdir='TB', dpi='600', size='8.27,11.69!')  # A4 portrait size in inches, no compression
    add_nodes_edges(dot_jpeg_v, family_tree)
    output_jpeg_v = 'family_tree_portrait.png'
    dot_jpeg_v.render(filename='public/family_tree_portrait', cleanup=True)
    print(f'Family tree portrait image generated: {output_jpeg_v}')

    # Create a graphviz Digraph for PDF portrait
    dot_pdf_v = graphviz.Digraph(comment='Family Tree Portrait', format='pdf')
    dot_pdf_v.attr(rankdir='TB', dpi='600', size='8.27,11.69!')  # A4 portrait size in inches, no compression
    add_nodes_edges(dot_pdf_v, family_tree)
    output_pdf_v = 'family_tree_portrait.pdf'
    dot_pdf_v.render(filename='family_tree_portrait', cleanup=True)
    print(f'Family tree portrait PDF generated: {output_pdf_v}')

if __name__ == '__main__':
    family_tree = None
    with open('poparan.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    family_tree = parse_family_data(lines)
    main()
    print("\nFamily tree summary:")
    print_family_summary(family_tree)
    print("\nDetailed family relationships:")
    print_family_detailed(family_tree)
