// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});
const dayjs         = require('dayjs');
const currency      = require('currency.js');

// Import Models
const { models }    = require('../sequelize');

// Functions

// INDEX

// NEW
router.get("/new", async (req, res)=>{
  const adrId = req.params.adrId
  const adr = await models.adr.findByPk(
    adrId, {
      include: [models.srn]
    }
  )
  res.render('payments/create', {adrId, adr});
})

// CREATE
router.post("/new", async (req, res)=>{
  const adrId = req.params.adrId
  const payment = await models.payment.create({
    ...req.body.payment,
    adrId,
  })
  res.redirect(`/adrs/${adrId}`)
})

// SHOW
router.get("/:id", async (req, res)=>{
  const adrId = req.params.adrId
  const paymentId = req.params.id
  const payment = await models.payment.findOne({ 
    where: { id: req.params.id }, 
    include: [
      {
        model: models.srn,
        include: [models.adr]
      },
    ],
  })
  res.render('payments/show', {payment, adrId, dayjs})
})

// EDIT
router.get("/:id/edit", async (req, res)=>{
  const adrId = req.params.adrId
  const paymentId = req.params.id
  const payment = await models.payment.findOne({
    where: { id: paymentId },
    // Include parent srn
    include: [
      {
        model: models.srn,
        // Include parent adr with all child stages
        include: [
          {
            model: models.adr,
            include: [models.srn]
          }
        ]
      }
    ]
  })
  res.render(`payments/update`, {payment, adrId, dayjs});
})

// UPDATE
router.put("/:id", async (req, res)=>{
  const paymentId = req.params.id
  const payment = await models.payment.findByPk(paymentId)
  await payment.update(req.body.payment)
  res.redirect(`/adrs/${req.params.adrId}`);
})

// DESTROY
router.delete("/:id", async (req, res)=>{
  const paymentId = req.params.id
  const payment = await models.payment.findByPk(paymentId)
  await payment.destroy()
  res.redirect(`/adrs/${req.params.adrId}`);
})


module.exports = router;