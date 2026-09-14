// index.js
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.get('/compute', (req, res) => {
  // Simulate lightweight CPU work
  let result = 0;
  for (let i = 0; i < 10000; i++) {
    result += Math.sqrt(i);
  }
  res.status(200).json({ result });
});

app.get('/data', (req, res) => {
  // Simulate data response
  const items = Array.from({ length: 100 }, (_, i) => ({
    id: i,
    value: `item-${i}`
  }));
  res.status(200).json({ items });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
