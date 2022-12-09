// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});
const dayjs         = require('dayjs');
const currency      = require('currency.js');

// Import Models
const { models }    = require('../sequelize');

const capitalize = string => string.replace(/\w\S*/g, (w) => (w.replace(/^\w/, (c) => c.toUpperCase())));
const prettifyString = string => capitalize(string.replace('_', ' ').toLowerCase());


function calculateNetPayment(adr){
  net_payment = 0
  if (adr.srns) {
    for (let srn of adr.srns) {
      if (srn.payments) {
        for (let payment of srn.payments) {
          net_payment += parseFloat(payment.amount)
        }
      }
    }
  }
  return net_payment
}

// INDEX
router.get("/", async (req, res)=>{
  try {  
    const adrs = await models.adr.findAll({
      include: [
        models.facility,
        models.patient,
        models.stage,
      ]
    })
    res.status(200).json({ adrs })
  } catch (err) {
    res.status(400).send(err)
  }

})


// NEW
router.get("/new", async (req, res)=>{
  try {
    // Get ID fields from both these tables as well, and embed in form
    const facilities  = await models.facility.findAll({attributes: ['id', 'global_id']})
    const patients    = await models.patient.findAll({attributes: ['id', 'mrn', 'first_name', 'last_name']})
    res.status(200).json({facilities, patients})
  } catch (err) {
    res.status(400).send(err)
  }
})


// CREATE
router.post("/new", async (req, res)=>{
  try {
    // Future error handling if there's no patient or facility
    const newAdr = {
      ...req.body.adr, 
      patientId: req.body.patient.id,
      facilityId: req.body.facility.id
    }
    const adr = await models.adr.create(newAdr);
    res.status(204)
  } catch (err) {
    res.status(400).send(err)
  }
})

// SHOW
router.get("/:id", async (req, res)=>{
  try {
    const adr = await models.adr.findOne({ 
      where: { id: req.params.id }, 
      include: [
        {
          model: models.stage,
          include: [
            {
              model: models.submission,
              include: [models.auditor],
            },
            models.decision,
          ]
        },
        {
          model: models.srn,
          include: [models.payment],
        },
        models.facility,
        models.patient,
      ],
    })
  
    // Calculated Fields
    adr.net_payment = calculateNetPayment(adr)
    adr.current_balance = adr.expected_reimbursement_80 - adr.net_payment
  
    res.status(200).json({adr})
  } catch (err) {
    res.status(400).send(err)
  }
})


// EDIT
router.get("/:id/edit", async (req, res)=>{
  try {
    const adr = await models.adr.findByPk(
      req.params.id, {
        include: [
          models.facility,
          models.patient,
        ]
      }
    )
    
    const facilities  = await models.facility.findAll({attributes: ['id', 'global_id']})
    const patients    = await models.patient.findAll({attributes: ['id', 'mrn', 'first_name', 'last_name']})
    
    res.status(200).json({adr, facilities, patients})
  } catch (err) {
    res.status(400).send(err)
  }
})


// UPDATE
router.put("/:id", async (req, res)=>{
  try {
    const adr = await models.adr.findByPk(req.params.id)
    adr.update(req.body.adr)
    await adr.save()
    res.status(204)
  } catch (err) {
    res.status(400).send(err)
  }

})


// DESTROY
router.delete("/:id", async (req, res)=>{
  try {
    const adr = await models.adr.findByPk(req.params.id)
    await adr.destroy()
    res.status(204)
  } catch (err) {
    res.status(400).send(err)
  }

})


// Export
module.exports = router;