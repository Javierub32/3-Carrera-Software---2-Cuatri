const Sequelize = require('sequelize');
const db = require("../config/database");
module.exports = function(sequelize, DataTypes) {
  return db.define('Dinosaurio', {
    id: {
      autoIncrement: true,
      type: DataTypes.INTEGER,
      allowNull: true,
      primaryKey: true
    },
    nombre: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    'tamaño_metros': {
      type: DataTypes.REAL,
      allowNull: true
    },
    peso_toneladas: {
      type: DataTypes.REAL,
      allowNull: true
    },
    periodo_id: {
      type: DataTypes.INTEGER,
      allowNull: true,
      references: {
        model: 'Periodo',
        key: 'id'
      }
    },
    dieta_id: {
      type: DataTypes.INTEGER,
      allowNull: true,
      references: {
        model: 'Dieta',
        key: 'id'
      }
    }
  }, {
    sequelize,
    tableName: 'Dinosaurio',
    timestamps: false
  });
};
