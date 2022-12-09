
const express       = require('express');
const router        = express.Router({mergeParams: true});
const { models }    = require('../sequelize');


// INDEX
router.get("/", async (req, res)=>{
  const patients = await models.patient.findAll({});
  res.render('patients/index', {patients});
});

// NEW
router.get("/new", (req, res)=>{
  res.render('patients/create');
})

// CREATE
router.post("/new", async (req, res)=>{
  const patient = await models.patient.create(req.body.patient);
  res.redirect(`/patients/${patient.id}`);
})

// SHOW
router.get("/:id", async (req, res)=>{
  const patient = await models.patient.findByPk(req.params.id);
  res.render('patients/show', {patient});
})

// EDIT
router.get("/:id/edit", async (req, res)=>{
  const patient = await models.patient.findByPk(req.params.id);
  res.render('patients/update', {patient});
})

// UPDATE
router.put("/:id", async (req, res)=>{
  const patient = await models.patient.findByPk(req.params.id);
  await patient.update(req.body.patient)
  res.redirect(`/patients/${patient.id}`);
})

// DESTROY
router.delete("/:id", async (req, res)=>{
  const patient = await models.patient.findByPk(req.params.id);
  await patient.destroy();
  res.redirect('/patients');
})


module.exports = router;