function createAssociations(sequelize) {
    const { 
        facility,
        patient,
        adr,
        stage,
        submission,
        decision,
        srn,
        payment,
        auditor,
    } = sequelize.models;
    
    // Define associations
    adr.belongsTo(facility);
    facility.hasMany(adr);
    
    adr.belongsTo(patient);
    patient.hasMany(adr);


    // STAGES :: submissions, decisions
    adr.hasMany(stage);
    stage.belongsTo(adr);
    
    stage.hasMany(submission);
    submission.belongsTo(stage);
    
    stage.hasMany(decision);
    decision.belongsTo(stage);

    // AUDITOR :: submissions
    auditor.hasMany(submission);
    submission.belongsTo(auditor);
    
    // SRNS :: payments
    adr.hasMany(srn);
    srn.belongsTo(adr);
    
    payment.belongsTo(srn);
    srn.hasMany(payment);
}

module.exports = { createAssociations };