const mongoose = require('mongoose');

const CoeffSchema = new mongoose.Schema({
    weight_coeff: {
        type: mongoose.Types.Decimal128,
        required: true
    },
    distance_coeff: {
        type: mongoose.Types.Decimal128,
    }
});
const Coeffs = mongoose.model('Coeffs', CoeffSchema);

module.exports = Coeffs;