
const { Sequelize } = require('sequelize');
const { createAssociations } = require('./associations');
const dotenv = require('dotenv').config();

const sequelize = new Sequelize(
    `postgres://${process.env.DB_UID}:${process.env.DB_PWD}@${process.env.DB_ADDRESS}`,
    {
        logging: true
    }
);

// Define models
const modelDefiners = [
    require('./models/facilities'),
    require('./models/patients'),
    require('./models/auditors'),
    require('./models/adrs'),
    require('./models/stages'),
    require('./models/submissions'),
    require('./models/decisions'),
    require('./models/srns'),
    require('./models/payments'),
];

for (const modelDefiner of modelDefiners) {
    modelDefiner(sequelize);
}

// Add associations
createAssociations(sequelize);


// Export sequelize connection
module.exports = sequelize;