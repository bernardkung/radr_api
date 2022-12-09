const { DataTypes } = require('sequelize');


module.exports = (sequelize) => {
  sequelize.define('adr', {
    from_date: {
      type: DataTypes.DATE,
      allowNull: false
    },
    to_date: {
      type: DataTypes.DATE,
      allowNull: false
    },
    // Facility information is brought over in association file
    // Patient information is brough over in association file
    expected_reimbursement: {
    type: DataTypes.DECIMAL(8,2),
    allowNull: false
    },
    expected_reimbursement_80: {
      type: DataTypes.VIRTUAL,
      get() {
        return `${this.expected_reimbursement*0.8}`
      }
    },
    active: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
    },
    mcr_status: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        isIn: [['paid_in_full', 'partially_denied', 'denied', 'other']]
      }
    },
  }, {
    timestamps: true,
    underscored: true,
  })
};