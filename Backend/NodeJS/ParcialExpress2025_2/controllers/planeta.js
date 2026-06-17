const initModels = require("../models/init-models");
const sequelize = require("sequelize");
const models = initModels(sequelize);
const { Op } = require("sequelize");

const controller = {};

controller.listarPlanetas = async function (req, res, next) {
    try {
		const planetas = await models.Planeta.findAll();
		const especies = await models.Especie.findAll();
		res.render("planeta", {planetas: planetas, especies: especies});
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.editarEspecie = async function (req, res, next) {
	try {
		const id = req.params.id;
		const especie = await models.Especie.findOne({
			where: { especie_id: id }
		})
		const familias = await models.Familia_Especie.findAll();
		const personajes = await models.Personaje.findAll();
		res.render("formEspecie", {especie: especie, familias: familias, personajes: personajes});
	} catch (error) {
		res.send("Se ha producido un error " + error);
	}
}

controller.guardarEspecie = async function (req, res, next) {
	try {
		const id = req.body.id;
		const especie = await models.Especie.findOne({
			where: { especie_id: id }
		})
		
		if (especie) {
			await especie.update({
				peso_medio: req.body.peso,
				esperanza_vida: req.body.esperanza,
				clasificacion: req.body.familia
			});
		}
		
        res.redirect('/');
	} catch (error) {
		res.send("Se ha producido un error " + error);
	}
}

controller.filtrarPlanetas = async function (req, res, next) {
	try {
		const diMayor = req.params.diMayor;
		const diMenor = req.params.diMenor;
		const planetas = await models.Planeta.findAll({
			where: {
				diametro: {
					[Op.gt]: diMenor,
            		[Op.lt]: diMayor
				}
			}
		});
		const especies = await models.Especie.findAll();
		res.render("planeta", {planetas: planetas, especies: especies});
	} catch (error) {
		res.send("Se ha producido un error " + error);
	}
}

module.exports = controller;