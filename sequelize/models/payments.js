const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  sequelize.define('payment', {
    amount: {
      type: DataTypes.DECIMAL(8,2),
      allowNull: false
    },
    date: {
      type: DataTypes.DATEONLY,
      allowNull: false
    },
  }, {
    timestamps: true,
    underscored: true,
  });
};

