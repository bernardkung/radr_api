const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  sequelize.define('submission', {
    date: {
      type: DataTypes.DATE,
      allowNull: false,
    },
  }, {
    timestamps: true,
    underscored: true,
  });
};
