const Pool = require('pg').Pool

const pool = new Pool({
    host: 'adr-tracker-development.cdthwrcf9teg.us-east-1.rds.amazonaws.com',
    port: 5432,
    database: 'adrs',
    user: process.env.DB_UID,
    password: process.env.DB_PWD,
});

const getAdrs = (req, res) => {
  pool.query('SELECT * FROM adrs ORDER BY id ASC', (error, results) => {
    if (error) {
      throw error
    }
    res.render('createADR.ejs')
  })
}

const createAdr = (req, res) => {
  const {global_id, mrn, from_date, to_date, exp_reimb, 
    exp_reimb_80, active, mcr_status} = req.body

  pool.query(`
    INSERT INTO adrs (global_id, mrn, from_date, to_date, 
      expected_reimbursement, expected_reimbursement_80, 
      active, mcr_status) 
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
  `, [global_id, mrn, from_date, to_date, exp_reimb, 
    exp_reimb_80, active, mcr_status], (error, results) => {
    if (error) {
      throw error
    }
    res.status(201).send(`ADR added with ID: ${results.insertId}`)
  })
}

// const createAdr = (req, res) => {
//     const text = `INSERT INTO adrs(
//         global_id, mrn, 
//         from_date, to_date, 
//         expected_reimbursement, expected_reimbursement_80, 
//         active, mcr_status) 
//       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`
      
//   // const {global_id, mrn, from_date, to_date, exp_reimb, 
//   //   exp_reimb_80, active, mcr_status} = req.body
    
//   const values = req.body
//   pool
//     .query(text, values)
//     .then(res => {
//       res.render('createADR.ejs')
//     })
//     .catch(err=>console.error(err.stack))
// }


const getAdrById = (req, res) => {
  const id = parseInt(req.params.id)

  pool.query('SELECT * FROM adrs WHERE id = $1', [id], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}


const updateAdr = (req, res) => {
  const id = parseInt(req.params.id)
  const { name, email } = req.body

  pool.query(
    'UPDATE adrs SET name = $1, email = $2 WHERE id = $3',
    [name, email, id],
    (error, results) => {
      if (error) {
        throw error
      }
      res.status(200).send(`User modified with ID: ${id}`)
    }
  )
}

const deleteAdr = (req, res) => {
  const id = parseInt(req.params.id)

  pool.query('DELETE FROM adrs WHERE id = $1', [id], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).send(`User deleted with ID: ${id}`)
  })
}

module.exports = {
  getAdrs,
  getAdrById,
  createAdr,
  updateAdr,
  deleteAdr,
}