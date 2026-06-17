const initModels = require("../models/init-models");
const sequelize = require("sequelize");
const models = initModels(sequelize);

const controller = {};

// Listar clientes /////////////////////////////////////////////////////////////////////////////////////////////////////
controller.listarPeliculas = async function (req, res, next) {
    try {
        await models.Pelicula
            .findAll()
            .then(async (data) => {

                //res.json(data);
                res.render("peliculas", {peliculas: data});
            });
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.ordenarPeliculas = async function (req, res, next) {
    try {
        const orden = req.query.by;

        const peliculas = await models.Pelicula.findAll({
            order: [
                [orden, 'ASC']
            ]
        })

        res.render("peliculas", { peliculas: peliculas });
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.buscarFrases = async function (req, res, next) {
    try {
        const id = req.params.id;

        const pelicula = await models.Pelicula.findOne({
            where: {
                pelicula_id: id
            },
            include: [
                {
                    model: models.Frase_Celebre,
                    as: "Frase_Celebres",
                    include: [
                        {
                            model: models.Personaje,
                            as: "personaje_Personaje",
                        }
                    ]
                }
            ]
        })
        //res.json(peliculas)
        res.render("frases", { pelicula: pelicula });
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.nuevaFrase = async function (req, res, next) {
    try {
        const id = req.params.id;

        const personajes = await models.Personaje.findAll({});

        //res.json(personajes);
        res.render("formFrase", { personajes: personajes, id: id });
    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

controller.guardarFrase = async function (req, res, next) {
    try {
        const idPelicula = req.body.id;
        const frase = req.body.frase;
        const personajeId = req.body.personaje;

        await models.Frase_Celebre.create({
            frase: frase,
            personaje: personajeId,
            pelicula: idPelicula
        });

        res.redirect('/frases/' + idPelicula);

    } catch (error) {
        res.send("Se ha producido un error " + error);
    }
};

module.exports = controller;