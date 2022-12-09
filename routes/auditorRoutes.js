// Initialize
const express       = require('express');
const router        = express.Router({mergeParams: true});

// Import Models
const { models }    = require('../sequelize')

// INDEX
router.get("/", async (req, res)=>{
    const auditors = await models.auditor.findAll();
    res.render('auditors/index', {auditors});
  });

// NEW
router.get("/new", (req, res)=>{
    res.render('auditors/create')
})

// CREATE
router.post('/new', async (req, res)=>{
    const auditor = await models.auditor.create(req.body.auditor)
    res.redirect(`/auditors/`)
})

// SHOW
router.get('/:id', async (req, res)=>{
    const auditor = await models.auditor.findByPk(req.params.id)
    res.render('auditors/show', {auditor})
})

// EDIT
router.get('/:id/edit', async (req, res)=>{
    const auditor = await models.auditor.findByPk(req.params.id)
    res.render('auditors/update', {auditor})
})

// UPDATE
router.put(':/id', async (req, res)=>{
    const auditor = await models.auditor.findByPk(req.params.id)
    await auditor.update(req.body.auditor)
    res.redirect(`/auditors/${auditor.id}`)
})

// DESTROY
router.delete('/:id', async (req, res)=>{
    const auditor = await models.auditor.findByPk(req.params.id)
    await auditor.destroy()
    res.redirect('/auditors')
})


module.exports = router