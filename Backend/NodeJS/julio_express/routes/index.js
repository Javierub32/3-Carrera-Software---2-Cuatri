const express = require("express");
const router = express.Router();

const dinosaurioController = require('../controllers/dinosaurio');

router.get("/", dinosaurioController.listarDinosaurios);
router.get("/editarDinosaurio", dinosaurioController.editarDinosaurio);

module.exports = router;
