const initModels = require("../models/init-models");
const sequelize = require("sequelize");
const models = initModels(sequelize);

const controller = {};

controller.listarDinosaurios = async function (req, res, next) {
    try {
        const dinosaurios = await models.Dinosaurio.findAll({
            include: {
                model: models.Dieta,
                as: 'dietum'
            }
        });
        //res.json(dinosaurios);
        res.render('dinosaurios', {dinosaurios: dinosaurios, idEditando: null, dietas: null});
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.editarDinosaurio = async function (req, res, next) {
    try {
        const id = req.query.id;

        const dinosaurios = await models.Dinosaurio.findAll({
            include: {
                model: models.Dieta,
                as: 'dietum'
            }
        });
        const dietas = await models.Dieta.findAll();
        //res.json(dinosaurios);
        res.render('dinosaurios', {dinosaurios: dinosaurios, idEditando: id, dietas: dietas});
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

module.exports = controller;