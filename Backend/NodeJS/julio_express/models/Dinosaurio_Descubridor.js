const Sequelize = require('sequelize');
const db = require("../config/database");
module.exports = function(sequelize, DataTypes) {
  return db.define('Dinosaurio_Descubridor', {
    dinosaurio_id: {
      autoIncrement: false,
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Dinosaurio',
        key: 'id'
      },
      unique: true
    },
    descubridor_id: {
      autoIncrement: false,
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Descubridor',
        key: 'id'
      },
      unique: true
    }
  }, {
    sequelize,
    tableName: 'Dinosaurio_Descubridor',
    timestamps: false,
    indexes: [
      {
        name: "sqlite_autoindex_Dinosaurio_Descubridor_1",
        unique: true,
        fields: [
          { name: "dinosaurio_id" },
          { name: "descubridor_id" },
        ]
      },
    ]
  });
};
