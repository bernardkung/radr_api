const {  DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  sequelize.define('decision', {
    decision: {
      type: DataTypes.ENUM(
        'FAVORABLE',
        'PARTIALLY FAVORABLE',
        'UNFAVORABLE',
        'OTHER',
      ),
      allowNull: false,
    },
    date: {
      type: DataTypes.DATE,
      allowNull: false,
    },
  }, {
    timestamps: true,
    underscored: true,
  });
};