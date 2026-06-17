var DataTypes = require("sequelize").DataTypes;
var _Descubridor = require("./Descubridor");
var _Dieta = require("./Dieta");
var _Dinosaurio = require("./Dinosaurio");
var _Dinosaurio_Descubridor = require("./Dinosaurio_Descubridor");
var _Dinosaurio_Habitat = require("./Dinosaurio_Habitat");
var _Habitat = require("./Habitat");
var _Periodo = require("./Periodo");

function initModels(sequelize) {
  var Descubridor = _Descubridor(sequelize, DataTypes);
  var Dieta = _Dieta(sequelize, DataTypes);
  var Dinosaurio = _Dinosaurio(sequelize, DataTypes);
  var Dinosaurio_Descubridor = _Dinosaurio_Descubridor(sequelize, DataTypes);
  var Dinosaurio_Habitat = _Dinosaurio_Habitat(sequelize, DataTypes);
  var Habitat = _Habitat(sequelize, DataTypes);
  var Periodo = _Periodo(sequelize, DataTypes);

  Dinosaurio_Descubridor.belongsTo(Descubridor, { as: "descubridor", foreignKey: "descubridor_id"});
  Descubridor.hasMany(Dinosaurio_Descubridor, { as: "Dinosaurio_Descubridors", foreignKey: "descubridor_id"});
  Dinosaurio.belongsTo(Dieta, { as: "dietum", foreignKey: "dieta_id"});
  Dieta.hasMany(Dinosaurio, { as: "Dinosaurios", foreignKey: "dieta_id"});
  Dinosaurio_Descubridor.belongsTo(Dinosaurio, { as: "dinosaurio", foreignKey: "dinosaurio_id"});
  Dinosaurio.hasMany(Dinosaurio_Descubridor, { as: "Dinosaurio_Descubridors", foreignKey: "dinosaurio_id"});
  Dinosaurio_Habitat.belongsTo(Dinosaurio, { as: "dinosaurio", foreignKey: "dinosaurio_id"});
  Dinosaurio.hasMany(Dinosaurio_Habitat, { as: "Dinosaurio_Habitats", foreignKey: "dinosaurio_id"});
  Dinosaurio_Habitat.belongsTo(Habitat, { as: "habitat", foreignKey: "habitat_id"});
  Habitat.hasMany(Dinosaurio_Habitat, { as: "Dinosaurio_Habitats", foreignKey: "habitat_id"});
  Dinosaurio.belongsTo(Periodo, { as: "periodo", foreignKey: "periodo_id"});
  Periodo.hasMany(Dinosaurio, { as: "Dinosaurios", foreignKey: "periodo_id"});

  return {
    Descubridor,
    Dieta,
    Dinosaurio,
    Dinosaurio_Descubridor,
    Dinosaurio_Habitat,
    Habitat,
    Periodo,
  };
}
module.exports = initModels;
module.exports.initModels = initModels;
module.exports.default = initModels;
