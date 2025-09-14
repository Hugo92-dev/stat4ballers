const mongoose = require('mongoose');

const leagueSchema = new mongoose.Schema({
    sportmonksId: {
        type: Number,
        required: true,
        unique: true
    },
    name: {
        type: String,
        required: true
    },
    slug: {
        type: String,
        required: true,
        unique: true
    },
    country: {
        type: String,
        required: true
    },
    logo: String,
    seasons: [{
        id: Number,
        name: String,
        year: String,
        isCurrent: Boolean
    }],
    teams: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Team'
    }],
    lastUpdated: {
        type: Date,
        default: Date.now
    }
}, {
    timestamps: true
});

leagueSchema.index({ sportmonksId: 1 });
leagueSchema.index({ slug: 1 });

module.exports = mongoose.model('League', leagueSchema);