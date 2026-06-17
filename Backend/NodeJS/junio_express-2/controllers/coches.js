const initModels = require("../models/init-models");
const sequelize = require("sequelize");
const models = initModels(sequelize);
const { Op } = require("sequelize");

const controller = {};

controller.listarMarcas = async function (req, res, next) {
    try {
        const marcas = await models.marca.findAll({});

        res.render("marcas", {marcas: marcas, coches: null, marcaSeleccionada: null});
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.buscarServicios = async function (req, res, next) {
    try {
        const idMarca = req.body.marca;
        const idsCoches = req.body.coches;

        const marcas = await models.marca.findAll({});
        const coches = await models.vehiculo.findAll({
            where: {
                id_marca: idMarca
            }
        })

        if (idsCoches != null) {
            const servicios = await models.servicio.findAll({
                where: {
                    id_vehiculo: {
                        [Op.or]: idsCoches
                    }
                }
            })
            res.render("servicios", {servicios: servicios, marca: idMarca});
        }

        res.render("marcas", {marcas: marcas, coches: coches, marcaSeleccionada: idMarca});

    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.verMarca = async function (req, res, next) {
    try {
        const marca = await models.marca.findOne({
            where: {
                id_marca: req.query.id
            }
        });

        res.render("marca", {marca: marca});
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.verCoche = async function (req, res, next) {
    try {
        const coche = await models.vehiculo.findOne({
            where: {
                id_vehiculo: req.query.id
            }
        });

        const propietarios = await models.propietario.findAll({});

        const propietariosSelec = await models.vehiculo_propietario.findAll({
            where: { id_vehiculo: req.query.id },
            include: {
                model: models.propietario,
                as: "id_propietario_propietario"
            }
        })
        //res.json(propietariosSelec);

        res.render("vehiculo", {coche: coche, propietariosSelec: propietariosSelec, propietarios: propietarios});
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.guardarVehiculo = async function (req, res, next) {
    try {
        const id = req.body.id;
        const modelo = req.body.modelo;
        const anyo = req.body.anyo;
        const propietarios = req.body.propietarios;

        let idsPropietarios = [];
        if (propietarios) {
            idsPropietarios = Array.isArray(propietarios) ? propietarios : [propietarios];
        }

        const vehiculo = await models.vehiculo.findOne({
            where: {
                id_vehiculo: id
            }
        });

        // Actualizamos los datos del vehiculo
        await vehiculo.update({
                modelo: modelo,
                anio: anyo
        });

        // Destruimos las relaciones anteriores
        await models.vehiculo_propietario.destroy({
            where: { id_vehiculo: id }
        })


        // Creamos una relacion por cada coche montado
        idsPropietarios.forEach(async (idP) => {
            await models.vehiculo_propietario.create({
                id_vehiculo: id,
                id_propietario: idP
            })
        })


        res.redirect('/verVehiculo?id=' + id);

    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

module.exports = controller;