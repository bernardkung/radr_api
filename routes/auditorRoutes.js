// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});

// Import Models
const { models }    = require('../sequelize')

// INDEX
router.get("/", async (req, res)=>{
  try {
      const auditors = await models.auditor.findAll()
      res.status(200).json({ auditors })
    } catch (err) {
      res.status(400).send(err)
    }
})

// NEW
router.get("/new", (req, res)=>{
  try {
    res.status(204).end()
  } catch (err) {
    res.status(400).send(err)
  }
})

// CREATE
router.post('/new', async (req, res)=>{
  try {
    const auditor = await models.auditor.create(req.body.auditor)
    res.status(201).end()
  } catch (err) {
    res.status(400).send(err)
  }
})

// SHOW
router.get('/:id', async (req, res)=>{
  try {
    const auditor = await models.auditor.findByPk(req.params.id)
    if (!auditor) {
      // If no auditor found
      res.status(404).send("no Auditor found under given ID")
    } else {
      res.status(200).json({auditor})
    }
  } catch (err) {
    res.status(400).send(err)
  }
})

// EDIT
router.get('/:id/edit', async (req, res)=>{
  try {
    const auditor = await models.auditor.findByPk(req.params.id)
    if (!auditor) {
      // If no auditor found
      res.sendStatus(404).send("no Auditor found under given ID")
    } else {
      res.status(200).json({ auditor })
    }
  } catch (err) {
    res.status(400).send(err)
  }
})

// UPDATE
router.put(':/id', async (req, res)=>{
  try {
    const auditor = await models.auditor.findByPk(req.params.id);
    if (!auditor) {
      // If no auditor found
      res.sendStatus(404).send("no Auditor found under given ID")
    } else {
      await auditor.update(req.body.auditor)
      res.status(201).end()
    }
  } catch (err) {
    res.status(400).send(err)
  }
})

// DESTROY
router.delete('/:id', async (req, res)=>{
  //
  try {
    const auditor = await models.auditor.findByPk(req.params.id)    
    if (!auditor) {
      // If no facility found
      res.status(404).send("no Auditor found under given ID")
    } else {
      // Destroy
      await auditor.destroy()
      res.status(201).end()
    }
  } catch (err) {
    res.status(400).send(err)
  }
})


module.exports = router