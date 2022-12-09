const express           = require('express')
const path              = require('path')
const methodOverride    = require('method-override')
const dayjs             = require('dayjs')
const sequelize         = require('./sequelize')
const dotenv            = require('dotenv').config()

// Import Routes
const adrRoutes         = require('./routes/adrRoutes')
const facilityRoutes    = require('./routes/facilityRoutes')
const patientRoutes     = require('./routes/patientRoutes')
const auditorRoutes     = require('./routes/auditorRoutes')
const srnRoutes         = require('./routes/srnRoutes')
const paymentRoutes     = require('./routes/paymentRoutes')
const stageRoutes       = require('./routes/stageRoutes')
const submissionRoutes  = require('./routes/submissionRoutes')
const decisionRoutes    = require('./routes/decisionRoutes')


// const db = require('./db');

async function syncDatabase() {
  // See radr-data project for seeding fake data
  console.log('Syncing models to database...')
  try {
    await sequelize.sync({ force: true });
    console.log("Sync completed successfully")
  } catch (err) {
    console.error('Sync failed:', err)
  }
}

async function assertDatabaseConnection() {
  console.log('Checking database connection...')
  try {
    await sequelize.authenticate()
    console.log("Database connection successfully established.")
    return true
  } catch (err) {
    console.error('Unable to connect to the database:', err)
    return false
  }
}



// Configure app
const app = express()
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname + '/views')) // set views folder location
app.use(express.static(__dirname + '/public')) // add public directory
app.use(express.urlencoded({ extended: true })) // built-in bodyparser
app.use(methodOverride('_method')) // allows custom methods

// Configure routes
app.use('/facilities', facilityRoutes)
app.use('/patients', patientRoutes)
app.use('/auditors', auditorRoutes)
app.use('/adrs', adrRoutes)
app.use('/adrs/:adrId/stages', stageRoutes)
app.use('/adrs/:adrId/submissions', submissionRoutes)
app.use('/adrs/:adrId/decisions', decisionRoutes)
app.use('/adrs/:adrId/srns', srnRoutes)
app.use('/adrs/:adrId/payments', paymentRoutes)


// Temporary Routes
app.get("/", (req, res)=>{
  res.render("index");
})

app.get("/login", (req, res)=>{
  res.render("login");
})


// INDEX ROUTES
app.get("/srns", async (req, res)=>{
  const srns = await sequelize.models.srn.findAll({});
  res.render('srns/index', {srns, dayjs});
});

app.get("/stages", async (req, res)=>{
  const stages = await sequelize.models.stage.findAll({});
  res.render('stages/index', {stages, dayjs});
});

app.get("/payments", async (req, res)=>{
  const payments = await sequelize.models.payment.findAll({});
  res.render('payments/index', {payments, dayjs});
});

app.get("/decisions", async (req, res)=>{
  const decisions = await sequelize.models.decision.findAll({});
  res.render('decisions/index', {decisions, dayjs});
});

app.get("/submissions", async (req, res)=>{
  const submissions = await sequelize.models.submission.findAll({});
  res.render('submissions/index', {submissions, dayjs});
});

app.get("/facilities", async (req, res)=>{
  const stages = await sequelize.models.stage.findAll({});
  res.render('facilities/index', {stages, dayjs});
});

app.get("/patients", async (req, res)=>{
  const stages = await sequelize.models.stage.findAll({});
  res.render('patients/index', {stages, dayjs});
});

app.get("/auditors", async (req, res)=>{
  const stages = await sequelize.models.stage.findAll({});
  res.render('auditors/index', {stages, dayjs});
});


async function init() {
  console.log('Starting Express app...')
  if (assertDatabaseConnection){
    
    //// See sequelize folder for:
    ////    index.js for configuring sequelize
    ////    model and association files
    //// See radr_data project for seeding facilities/patients
    //// Uncomment these two lines to re-sync database
    // syncDatabase()
    //   .then(res=>console.log(res))
    
    // App Listen
    app.listen(process.env.PORT, process.env.IP, () => {
      console.log(`The server has started on ${process.env.IP}:${process.env.PORT}`);
    })
  }
}

init();