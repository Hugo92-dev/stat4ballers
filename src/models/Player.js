const mongoose = require('mongoose');

const playerSchema = new mongoose.Schema({
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
    firstName: String,
    lastName: String,
    displayName: String,
    image: String,
    dateOfBirth: Date,
    age: Number,
    height: Number,
    weight: Number,
    nationality: String,
    position: {
        type: String,
        enum: ['Goalkeeper', 'Defender', 'Midfielder', 'Forward', 'Unknown']
    },
    detailedPosition: String,
    jerseyNumber: Number,
    team: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Team'
    },
    currentSeason: String,
    statistics: {
        // General statistics
        rating: Number,
        appearances: Number,
        minutesPlayed: Number,
        captain: Number,
        goals: Number,
        assists: Number,
        redCards: Number,
        
        // Offensive creativity
        shotsTotal: Number,
        shotsOnTarget: Number,
        penalties: Number,
        hitWoodwork: Number,
        keyPasses: Number,
        bigChancesCreated: Number,
        accurateCrosses: Number,
        successfulDribbles: Number,
        
        // Defensive commitment
        yellowCards: Number,
        tackles: Number,
        ownGoals: Number,
        interceptions: Number,
        duelsWon: Number,
        aerialsWon: Number,
        dispossessed: Number,
        dribbledPast: Number,
        fouls: Number,
        foulsDrawn: Number,
        errorLeadToGoal: Number,
        
        // Goalkeeper specific
        saves: Number,
        savesInsideBox: Number,
        goalsConceded: Number,
        cleanSheets: Number
    },
    historicalStatistics: [{
        season: String,
        year: String,
        statistics: {
            type: Map,
            of: Number
        }
    }],
    lastUpdated: {
        type: Date,
        default: Date.now
    }
}, {
    timestamps: true
});

playerSchema.index({ sportmonksId: 1 });
playerSchema.index({ slug: 1 });
playerSchema.index({ team: 1 });
playerSchema.index({ position: 1 });
playerSchema.index({ 'statistics.rating': -1 });

// Method to check if player is a goalkeeper
playerSchema.methods.isGoalkeeper = function() {
    return this.position === 'Goalkeeper';
};

// Method to get radar chart data
playerSchema.methods.getRadarChartData = function() {
    const isGK = this.isGoalkeeper();
    
    if (isGK) {
        return {
            general: {
                rating: this.statistics.rating || 0,
                appearances: this.statistics.appearances || 0,
                minutesPlayed: this.statistics.minutesPlayed || 0,
                captain: this.statistics.captain || 0,
                redCards: this.statistics.redCards || 0
            },
            goalkeeper: {
                saves: this.statistics.saves || 0,
                savesInsideBox: this.statistics.savesInsideBox || 0,
                goalsConceded: this.statistics.goalsConceded || 0,
                cleanSheets: this.statistics.cleanSheets || 0
            }
        };
    } else {
        return {
            general: {
                rating: this.statistics.rating || 0,
                appearances: this.statistics.appearances || 0,
                minutesPlayed: this.statistics.minutesPlayed || 0,
                captain: this.statistics.captain || 0,
                goals: this.statistics.goals || 0,
                assists: this.statistics.assists || 0,
                redCards: this.statistics.redCards || 0
            },
            offensive: {
                shotsTotal: this.statistics.shotsTotal || 0,
                shotsOnTarget: this.statistics.shotsOnTarget || 0,
                penalties: this.statistics.penalties || 0,
                hitWoodwork: this.statistics.hitWoodwork || 0,
                keyPasses: this.statistics.keyPasses || 0,
                bigChancesCreated: this.statistics.bigChancesCreated || 0,
                accurateCrosses: this.statistics.accurateCrosses || 0,
                successfulDribbles: this.statistics.successfulDribbles || 0
            },
            defensive: {
                yellowCards: this.statistics.yellowCards || 0,
                tackles: this.statistics.tackles || 0,
                ownGoals: this.statistics.ownGoals || 0,
                interceptions: this.statistics.interceptions || 0,
                duelsWon: this.statistics.duelsWon || 0,
                aerialsWon: this.statistics.aerialsWon || 0,
                dispossessed: this.statistics.dispossessed || 0,
                dribbledPast: this.statistics.dribbledPast || 0,
                fouls: this.statistics.fouls || 0,
                foulsDrawn: this.statistics.foulsDrawn || 0,
                errorLeadToGoal: this.statistics.errorLeadToGoal || 0
            }
        };
    }
};

module.exports = mongoose.model('Player', playerSchema);