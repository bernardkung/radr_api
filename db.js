const { Sequelize } = require('sequelize');
const db = new Sequelize(
    `postgres://${process.env.DB_UID}:${process.env.DB_PWD}@radr.cdthwrcf9teg.us-east-1.rds.amazonaws.com:5432/adrs`
)
module.exports = db

