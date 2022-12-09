
const express       = require('express')
const router        = express.Router({mergeParams: true})
const { models }    = require('../sequelize')


// INDEX
router.get("/", async (req, res)=>{
  try {
    const patients = await models.patient.findAll({})
    res.status(200).json({ patients })
  } catch (err) {
    res.status(404).send(err)
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
router.post("/new", async (req, res)=>{
  try {
    const patient = await models.patient.create(req.body.patient)
    res.status(201).end()
  } catch (err) {
    res.status(400).send(err)
  }
})

// SHOW
router.get("/:id", async (req, res)=>{
  try {
    const patient = await models.patient.findByPk(req.params.id)
    if (!patient) {
      res.sendStatus(404).send("no Patient found under given ID")
    } else {
      res.status(200).json({ patient })
    }
  } catch (err) {
    res.status(400).send(err)
  }
})

// EDIT
router.get("/:id/edit", async (req, res)=>{
  try {
    const patient = await models.patient.findByPk(req.params.id)
    if (!patient) {
      res.sendStatus(404).send("no Patient found under given ID")
    } else {
      res.status(200).json({ patient })
    }
  } catch (err) {
    res.status(400).send(err)
  }
})

// UPDATE
router.put("/:id", async (req, res)=>{
  try {
    const patient = await models.patient.findByPk(req.params.id)
    if (!patient) {
      res.status(404).send("no Patient found under given ID")
    } else {
      await patient.update(req.body.patient)
      res.status(201).end()
    }
  } catch (err) {
    res.status(400).send(err)
  }
})

// DESTROY
router.delete("/:id", async (req, res)=>{
  try {
    const patient = await models.patient.findByPk(req.params.id)
    if (!patient) {
      res.status(404).send("no Patient found under given ID")
    } else {
      await patient.destroy()
      res.status(201).end()
    }

  } catch (err) {
    res.status(404).send(err)
  }
})


module.exports = router