const { DataTypes } = require('sequelize');


// Define model
module.exports = (sequelize) => {
  sequelize.define('facility', {
    global_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    facility_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    facility_name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    division: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    operating_group: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    region: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    billing_group: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    mac: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  }, {
    timestamps: true,
    underscored: true,
  })
};