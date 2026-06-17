const express = require("express");
const router = express.Router();

const clientesController = require('../controllers/planeta');

router.get("/", clientesController.listarPlanetas);
router.get("/especie/:id", clientesController.editarEspecie);
router.post("/guardarEspecie", clientesController.guardarEspecie);
router.get("/:diMenor/:diMayor", clientesController.filtrarPlanetas)

module.exports = router;
