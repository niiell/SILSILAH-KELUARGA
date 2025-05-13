const express = require('express');
const fs = require('fs');
const { exec } = require('child_process');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// Path to poparan.txt
const poparanPath = path.join(__dirname, 'poparan.txt');

// GET endpoint to read poparan.txt
app.get('/api/poparan', (req, res) => {
  fs.readFile(poparanPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to read poparan.txt' });
    }
    res.json({ content: data });
  });
});

// POST endpoint to update poparan.txt
app.post('/api/poparan', (req, res) => {
  const { content } = req.body;
  if (typeof content !== 'string') {
    return res.status(400).json({ error: 'Invalid content' });
  }
  fs.writeFile(poparanPath, content, 'utf8', (err) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to write poparan.txt' });
    }
    res.json({ message: 'poparan.txt updated successfully' });
  });
});

// POST endpoint to run generate_family_tree.py
app.post('/api/generate', (req, res) => {
  exec('python generate_family_tree.py', (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: 'Failed to run generate_family_tree.py', details: stderr });
    }
    res.json({ message: 'Family tree generated successfully', output: stdout });
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
