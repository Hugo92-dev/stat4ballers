const mongoose = require('mongoose');

const teamSchema = new mongoose.Schema({
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
        required: true
    },
    shortName: String,
    logo: String,
    venue: {
        name: String,
        capacity: Number,
        city: String
    },
    league: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'League'
    },
    coach: {
        name: String,
        nationality: String,
        image: String
    },
    founded: Number,
    statistics: {
        season: String,
        rating: Number,
        gamesPlayed: Number,
        averagePointsPerGame: Number,
        averagePlayerAge: Number,
        teamWins: Number,
        teamDraws: Number,
        teamLost: Number,
        goalsScored: Number,
        goalsConceded: Number,
        cleanSheets: Number,
        redCards: Number,
        highestRatedPlayer: {
            name: String,
            rating: Number
        }
    },
    players: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Player'
    }],
    lastUpdated: {
        type: Date,
        default: Date.now
    }
}, {
    timestamps: true
});

teamSchema.index({ sportmonksId: 1 });
teamSchema.index({ slug: 1 });
teamSchema.index({ league: 1 });

module.exports = mongoose.model('Team', teamSchema);