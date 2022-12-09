// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});

// Import Models
const { models }    = require('../sequelize');


// INDEX
router.get("/", async (req, res)=>{
  try {
    const facilities = await models.facility.findAll()
    res.status(200).json({ facilities })
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
router.post("/new", async (req, res)=>{
  try {
    const facility = await models.facility.create(req.body.facility)
    res.status(201).end()
  } catch (err) {
    res.status(400).send(err)
  }
})

// SHOW
router.get("/:id", async (req, res)=>{
  try {
    const facility = await models.facility.findByPk(req.params.id)
    if (!facility) {
      res.status(404).end()
    } else {
      res.status(200).json({facility})
    }
  } catch (err) {
    res.status(400).send(err)
  }
})

// EDIT
router.get("/:id/edit", async (req, res)=>{
  try {
    const facility = await models.facility.findByPk(req.params.id)
    res.status(200).json({facility})
  } catch (err) {
    res.status(400).send(err)
  }
})

// UPDATE
router.put("/:id", async (req, res)=>{
  try {
    const facility = await models.facility.findByPk(req.params.id);
    await facility.update(req.body.facility)
    res.status(201).end()
  } catch (err) {
    res.status(400).send(err)
  }

})

// DESTROY
router.delete("/:id", async (req, res)=>{
  //
  try {
    const facility = await models.facility.findByPk(req.params.id)
    await facility.destroy()
    res.redirect('/facilities')
  } catch (err) {
    res.status(400).send(err)
  }
})


module.exports = router;