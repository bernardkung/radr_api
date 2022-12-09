// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});
const dayjs         = require('dayjs');

// Import Models
const { models }    = require('../sequelize');

// INDEX
router.get("/", async (req, res)=>{
  const stages = await models.stage.find({})
  res.render('stages/index', {stages})
});

// NEW
router.get("/new", (req, res)=>{
  const adrId = req.params.adrId
  const stages = models.stage.rawAttributes.stage.values
  res.render('stages/create', {adrId, stages})
})

// CREATE
router.post("/new", async (req, res)=>{
  const adrId = req.params.adrId
  const stage = await models.stage.create({
    ...req.body.stage,
    adrId,
  });
  res.redirect(`/adrs/${adrId}`)
})

// SHOW
router.get("/:id", async (req, res)=>{
  const adrId = req.params.adrId
  const stageId = req.params.id
  const stage = await models.stage.findByPk(stageId)
  res.render('stages/show', {stage, adrId})
})

// EDIT
router.get("/:id/edit", async (req, res)=>{
  const adrId = req.params.adrId
  const stageId = req.params.id
  const stage = await models.stage.findByPk(stageId)
  const stageValues = models.stage.rawAttributes.stage.values
  res.render('stages/update', {stage, adrId, stageValues, dayjs})
})

// UPDATE
router.put("/:id", async (req, res)=>{
  const stageId = req.params.id
  const stage = await models.stage.findByPk(stageId)
  await stage.update(req.body.stage)
  res.redirect(`/adrs/${req.params.adrId}`)
})

// DESTROY
router.delete("/:id", async (req, res)=>{
  const stageId = req.params.id
  const stage = await models.stage.findByPk(stageId)
  await stage.destroy()
  res.redirect(`/adrs/${req.params.adrId}`)
})


module.exports = router;