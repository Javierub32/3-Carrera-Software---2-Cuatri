const express = require("express");
const router = express.Router();

const cochesController = require('../controllers/coches');

router.get("/", cochesController.listarMarcas);
router.post("/buscarServicios", cochesController.buscarServicios);
router.get("/verMarca", cochesController.verMarca);
router.get("/verVehiculo", cochesController.verCoche);
router.post("/guardarVehiculo", cochesController.guardarVehiculo);


module.exports = router;
