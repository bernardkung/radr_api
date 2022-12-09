const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  sequelize.define('stage', {
    stage: {
      type: DataTypes.ENUM('45', '120', '180', '180T', 'ALJ', 'ALJR'),
      allowNull: false,
    },
    notification_date: {
      type: DataTypes.DATE,
      allowNull: false,
    },
    due_date: {
      type: DataTypes.DATE,
      allowNull: false,
    },
    submitted: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
    },
    decided: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
    },
    active: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: true,
    },
  },{
    timestamps: true,
    underscored: true,
  })
}