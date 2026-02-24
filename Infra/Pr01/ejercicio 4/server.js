const express = require('express');
const app = express();
const PORT = 3000;

app.get('/api/info', (req, res) => {
  res.json({
    nombre: 'docker-node-api',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    mensaje: 'API funcionando en Docker'
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Servidor escuchando en puerto ${PORT}`);
});
