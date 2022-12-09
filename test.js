const Pool = require('pg').Pool

const pool = new Pool({
    host: 'adr-tracker-development.cdthwrcf9teg.us-east-1.rds.amazonaws.com',
    port: 5432,
    database: 'adrs',
    user: process.env.DB_UID,
    password: process.env.DB_PWD,
});


const createAdr = (req, res) => {
    const text = `INSERT INTO adrs(
        global_id, mrn, 
        from_date, to_date, 
        expected_reimbursement, expected_reimbursement_80, 
        active, mcr_status) 
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`
      
  // const {global_id, mrn, from_date, to_date, exp_reimb, 
  //   exp_reimb_80, active, mcr_status} = req.body
    
  const values = req.body
  pool
    .query(text, values)
    .then(res => {
      res.render('createADR.ejs')
    })
    .catch(err=>console.error(err.stack))
}





module.exports = {
  getAdrs,
  getAdrById,
  createAdr,
  updateAdr,
  deleteAdr,
}