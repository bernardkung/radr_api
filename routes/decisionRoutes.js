// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});
const dayjs         = require('dayjs');
const currency      = require('currency.js');

// Import Models
const { models }    = require('../sequelize');

// Functions
const capitalize = string => string.replace(/\w\S*/g, (w) => (w.replace(/^\w/, (c) => c.toUpperCase())));
const prettifyString = string => capitalize(string.replace('_', ' ').toLowerCase());

// INDEX

// NEW
router.get("/new", async (req, res)=>{
  const adrId = req.params.adrId
  const adr = await models.adr.findOne({ 
    where: { id: req.params.adrId }, 
    include: [{model: models.stage}],
  });
  const decisionValues = models.decision.rawAttributes.decision.values
  res.render('decisions/create', {adrId, adr, decisionValues, prettifyString});
})

// CREATE
router.post("/new", async (req, res)=>{
  const adrId = req.params.adrId
  const adr = await models.adr.findByPk(adrId)
  const decision = await models.decision.create({
    ...req.body.decision,
    adrId,
  })
  res.redirect(`/adrs/${adrId}`);
})

// SHOW
router.get("/:id", async (req, res)=>{
  const adrId = req.params.adrId;
  const decision = await models.decision.findOne({ 
    where: { id: req.params.id }, 
    include: [
      {
        model: models.stage,
        include: [models.adr]
      },
    ],
  })
  res.render('decisions/show',  {decision, adrId, dayjs})
})

// EDIT
router.get("/:id/edit", async (req, res)=>{
  const adrId = req.params.adrId;
  const decision = await models.decision.findOne({ 
    where: { id: req.params.id }, 
    // Include parent stage
    include: [
      {
        model: models.stage,
        // Include parent adr with all child stages
        include: [
          {
            model: models.adr,
            include: [models.stage]
          }
        ]
      },
    ],
  })
  const stageValues = models.stage.rawAttributes.stage.values
  const decisionValues = models.stage.rawAttributes.stage.values
  res.render('decisions/update', {decision, stageValues, decisionValues, adrId, dayjs})
})

// UPDATE
router.put("/:id", async (req, res)=>{
  const decision = await models.decision.findByPk(req.params.id)
  await decision.update(req.body.decision)
  res.redirect(`/adrs/${req.params.adrId}`);
})

// DESTROY
router.delete("/:id", async (req, res)=>{
  const decision = await models.decision.findByPk(req.params.id)
  await decision.destroy()
  res.redirect(`/adrs/${req.params.adrId}`)
})





module.exports = router;