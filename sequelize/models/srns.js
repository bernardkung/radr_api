const { Sequelize, DataTypes } = require('sequelize');
const sequelize = new Sequelize(`postgres://${process.env.DB_UID}:${process.env.DB_PWD}@radr.cdthwrcf9teg.us-east-1.rds.amazonaws.com:5432/adrs`)


module.exports = (sequelize) => {
  sequelize.define('srn', {
    srn: {
      type: DataTypes.STRING,
      allowNull: false
    },
  }, {
    timestamps: true,
    underscored: true,
  });
};
