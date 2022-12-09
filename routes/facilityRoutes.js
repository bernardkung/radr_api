// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});

// Import Models
const { models }    = require('../sequelize');


// INDEX
router.get("/", async (req, res)=>{
  const facilities = await models.facility.findAll();
  res.render('facilities/index', {facilities});
});

// NEW
router.get("/new", (req, res)=>{
  res.render('facilities/create');
})

// CREATE
router.post("/new", async (req, res)=>{
  const facility = await models.facility.create(req.body.facility);
  res.redirect(`/facilities/${facility.id}`);
})

// SHOW
router.get("/:id", async (req, res)=>{
  const facility = await models.facility.findByPk(req.params.id);
  res.render('facilities/show', {facility});
})

// EDIT
router.get("/:id/edit", async (req, res)=>{
  const facility = await models.facility.findByPk(req.params.id);
  res.render('facilities/update', {facility});
})

// UPDATE
router.put("/:id", async (req, res)=>{
  const facility = await models.facility.findByPk(req.params.id);
  await facility.update(req.body.facility)
  res.redirect(`/facilities/${facility.id}`);
})

// DESTROY
router.delete("/:id", async (req, res)=>{
  const facility = await models.facility.findByPk(req.params.id);
  await facility.destroy();
  res.redirect('/facilities');
})


module.exports = router;