const Sequelize = require('sequelize');
const db = require("../config/database");
module.exports = function(sequelize, DataTypes) {
  return db.define('Dinosaurio_Habitat', {
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
    habitat_id: {
      autoIncrement: false,
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Habitat',
        key: 'id'
      },
      unique: true
    }
  }, {
    sequelize,
    tableName: 'Dinosaurio_Habitat',
    timestamps: false,
    indexes: [
      {
        name: "sqlite_autoindex_Dinosaurio_Habitat_1",
        unique: true,
        fields: [
          { name: "dinosaurio_id" },
          { name: "habitat_id" },
        ]
      },
    ]
  });
};
