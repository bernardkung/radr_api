const { DataTypes } = require('sequelize');


module.exports = (sequelize) => {
  sequelize.define('patient', {
    mrn: {
      type: DataTypes.INTEGER,
      allowNull: false
    },
    last_name: {
      type: DataTypes.STRING,
      allowNull: false
    },
    first_name: {
      type: DataTypes.STRING,
      allowNull: false
    },
  },{
    timestamps: true,
    underscored: true,
  })
};