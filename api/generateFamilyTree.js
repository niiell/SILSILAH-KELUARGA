const { exec } = require('child_process');
const graphviz = require('graphviz');
const fs = require('fs');
const path = require('path');

function parseFamilyData(lines) {
  const familyTree = {};
  const stack = [{ node: familyTree, indent: -1 }];

  lines.forEach(line => {
    const stripped = line.trimStart();
    if (!stripped) return;
    const indent = line.length - stripped.length;

    while (stack.length && indent <= stack[stack.length - 1].indent) {
      stack.pop();
    }

    const parent = stack[stack.length - 1].node;
    const name = stripped.replace(/^-+\s*/, '').trim();
    parent[name] = {};
    stack.push({ node: parent[name], indent });
  });

  return familyTree;
}

function addNodesEdges(graph, familyDict, parent = null) {
  Object.entries(familyDict).forEach(([member, children]) => {
    const label = member.replace('(✞)', '†');
    graph.addNode(label);
    if (parent) {
      graph.addEdge(parent, label);
    }
    addNodesEdges(graph, children, label);
  });
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { content } = req.body;
  if (typeof content !== 'string') {
    res.status(400).json({ error: 'Invalid content' });
    return;
  }

  try {
    const lines = content.split('\n');
    const familyTree = parseFamilyData(lines);

    const g = graphviz.digraph('FamilyTree');
    g.setGraphVizPath('/usr/local/bin'); // Adjust path if needed

    addNodesEdges(g, familyTree);

    const outputPath = path.join('/tmp', `family_tree_${Date.now()}.png`);
    g.output('png', outputPath, (code, stdout, stderr) => {
      if (code !== 0) {
        res.status(500).json({ error: 'Graphviz generation failed', details: stderr });
        return;
      }
      const image = fs.readFileSync(outputPath);
      res.setHeader('Content-Type', 'image/png');
      res.send(image);
      fs.unlinkSync(outputPath);
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
