const {  DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  sequelize.define('auditor', {
    auditor: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  }, {
    timestamps: true,
    underscored: true,
  });
};