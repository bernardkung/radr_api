// Initialize
const express       = require('express')
const router        = express.Router({mergeParams: true})
const dayjs         = require('dayjs')

// Import Models
const { models }    = require('../sequelize')

// Functions

// INDEX

// NEW
router.get("/new", (req, res)=>{
  const adrId = req.params.adrId
  res.render('srns/create', {adrId})
})


// CREATE
router.post("/new", async (req, res)=>{
  const adrId = req.params.adrId
  const srn = await models.srn.create({
    ...req.body.srn,
    adrId,
  })
  res.redirect(`/adrs/${adrId}`)
})


// SHOW
router.get("/:id", async (req, res)=>{
  const adrId = req.params.adrId
  const srnId = req.params.id
  const srn = await models.srn.findByPk(srnId)
  res.render('srns/show', {srn, adrId})
})


// EDIT
router.get("/:id/edit", async (req, res)=>{
  const adrId = req.params.adrId
  const srnId = req.params.id
  const srn = await models.srn.findByPk(srnId)
  res.render('srns/update', {srn, adrId})
})


// UPDATE
router.put("/:id", async (req, res)=>{
  const srnId = req.params.id
  const srn = await models.srn.findByPk(srnId)
  await srn.update(req.body.srn)
  res.redirect(`/adrs/${req.params.adrId}`)
})


// DESTROY
router.delete("/:id", async (req, res)=>{
  const srnId = req.params.id
  const srn = await models.srn.findByPk(srnId)
  await srn.destroy()
  res.redirect(`/adrs/${req.params.adrId}`)
})


module.exports = router;