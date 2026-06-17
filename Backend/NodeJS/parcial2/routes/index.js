const express = require("express");
const router = express.Router();

const peliculasController = require('../controllers/peliculas');

router.get("/", peliculasController.listarPeliculas);
router.get("/ordenar", peliculasController.ordenarPeliculas);
router.get("/frases/:id", peliculasController.buscarFrases);
router.get("/nuevaFrase/:id", peliculasController.nuevaFrase);
router.post("/guardarFrase", peliculasController.guardarFrase);


module.exports = router;
