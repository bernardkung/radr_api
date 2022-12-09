// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});
const dayjs         = require('dayjs');
const currency      = require('currency.js');

// Import Models
const { models }    = require('../sequelize');

// Functions

// INDEX
router.get("/", async (req, res)=>{
  const submissions = await models.submission.findAll({})
  res.render('submissions/index', {submissions})
})

// NEW
router.get("/new", async (req, res)=>{
  const adrId = req.params.adrId
  const adr = await models.adr.findOne({ 
    where: { id: req.params.adrId }, 
    include: [{model: models.stage}],
  })
  const auditors = await models.auditor.findAll()
  res.render('submissions/create', {adrId, adr, auditors});
})

// CREATE
router.post("/new", async (req, res)=>{
  const adrId = req.params.adrId
  const submission = await models.submission.create({
    ...req.body.submission,
    adrId,
  })
  res.redirect(`/adrs/${adrId}`)
})

// SHOW
router.get("/:id", async (req, res)=>{
  const adrId = req.params.adrId
  const submissionId = req.params.id
  const submission = await models.submission.findOne({ 
    where: { id: req.params.id }, 
    include: [
      {
        model: models.stage,
        include: [models.adr]
      },
      {
        model: models.auditor,
      },
    ],
  })
  res.render('submissions/show', {submission, adrId})
})

// EDIT
router.get("/:id/edit", async (req, res)=>{
  const adrId = req.params.adrId
  const submissionId = req.params.id
  const submission = await models.submission.findOne({ 
    where: { id: submissionId }, 
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
      models.auditor,
    ],
  })
  const auditors = await models.auditor.findAll()
  console.log(submission)
  res.render('submissions/update', {submission, auditors, adrId, dayjs})
})

// UPDATE
router.put("/:id", async (req, res)=>{
  const submissionId = req.params.id
  const submission = await models.submission.findByPk(submissionId)
  await submission.update(req.body.submission)
  res.redirect(`/adrs/${req.params.adrId}`)
})

// DESTROY
router.delete("/:id", async (req, res)=>{
  const submissionId = req.params.id
  const submission = await models.submission.findByPk(submissionId)
  await submission.destroy()
  res.redirect(`/adrs/${req.params.adrId}`)
})


module.exports = router;