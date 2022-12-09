const express           = require('express')
const mongoose          = require('mongoose');
const Facility          = require('../models/facilities');


// Connect mongoose to mongo
const uri = `mongodb+srv://${process.env.DB_UID}:${process.env.DB_PWD}@tablum.zvip3.mongodb.net/radr?retryWrites=true&w=majority`
mongoose.connect(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(() => console.log("MongoDB connected."))
    .catch(err => console.log(err));

const facilities = [
    {
    	global_id: 111111,
    	facility_id: 1111,
    	facility_name: 'pine',
	    division: 'east',
	    operating_group: 'eastern',
	    region: 'easterly',
	    billing_group: 'east coast',
	    mac: 'inner',
    },
    {
    	global_id: 222222,
    	facility_id: 2222,
    	facility_name: 'oak',
	    division: 'east',
	    operating_group: 'eastern',
	    region: 'easterly',
	    billing_group: 'east coast',
	    mac: 'inner',
    },
    {
    	global_id: 333333,
    	facility_id: 3333,
    	facility_name: 'palm',
	    division: 'south',
	    operating_group: 'southern',
	    region: 'southerly',
	    billing_group: 'east coast',
	    mac: 'inner',
    },
    {
    	global_id: 444444,
    	facility_id: 4444,
    	facility_name: 'redwood',
	    division: 'west',
	    operating_group: 'western',
	    region: 'westerly',
	    billing_group: 'west coast',
	    mac: 'inner',
    },
    {
    	global_id: 555555,
    	facility_id: 5555,
    	facility_name: 'maple',
	    division: 'north',
	    operating_group: 'northern',
	    region: 'northerly',
	    billing_group: 'west coast',
	    mac: 'inner',
    },
];

const seedDB = async () => {
    await Facility.deleteMany({});
    for (let f = 0; f < facilities.length; f++) {
        const facility = new Facility(facilities[f]);
        await facility.save();
    }
}

seedDB();