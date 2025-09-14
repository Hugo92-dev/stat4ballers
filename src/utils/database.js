const fs = require('fs').promises;
const path = require('path');

class LocalDatabase {
    constructor() {
        this.dbPath = path.join(__dirname, '../../data/db');
        this.collections = {
            leagues: [],
            teams: [],
            players: []
        };
        this.initialized = false;
    }

    async init() {
        try {
            // Create data directory if it doesn't exist
            await fs.mkdir(this.dbPath, { recursive: true });
            
            // Load existing data
            await this.loadCollections();
            this.initialized = true;
            console.log('✅ Local database initialized');
        } catch (error) {
            console.error('Error initializing database:', error);
        }
    }

    async loadCollections() {
        for (const collection of Object.keys(this.collections)) {
            const filePath = path.join(this.dbPath, `${collection}.json`);
            try {
                const data = await fs.readFile(filePath, 'utf-8');
                this.collections[collection] = JSON.parse(data);
            } catch (error) {
                // File doesn't exist, create it
                await this.saveCollection(collection);
            }
        }
    }

    async saveCollection(collectionName) {
        const filePath = path.join(this.dbPath, `${collectionName}.json`);
        await fs.writeFile(
            filePath, 
            JSON.stringify(this.collections[collectionName], null, 2)
        );
    }

    async find(collection, query = {}) {
        const data = this.collections[collection] || [];
        if (Object.keys(query).length === 0) {
            return data;
        }
        
        return data.filter(item => {
            return Object.keys(query).every(key => {
                if (typeof query[key] === 'object' && query[key].$in) {
                    return query[key].$in.includes(item[key]);
                }
                return item[key] === query[key];
            });
        });
    }

    async findOne(collection, query) {
        const results = await this.find(collection, query);
        return results[0] || null;
    }

    async insertOne(collection, document) {
        if (!document.id) {
            document.id = Date.now().toString();
        }
        this.collections[collection].push(document);
        await this.saveCollection(collection);
        return document;
    }

    async updateOne(collection, query, update) {
        const index = this.collections[collection].findIndex(item => {
            return Object.keys(query).every(key => item[key] === query[key]);
        });
        
        if (index !== -1) {
            this.collections[collection][index] = {
                ...this.collections[collection][index],
                ...update,
                lastUpdated: new Date().toISOString()
            };
            await this.saveCollection(collection);
            return this.collections[collection][index];
        }
        return null;
    }

    async findOneAndUpdate(collection, query, update, options = {}) {
        let document = await this.findOne(collection, query);
        
        if (!document && options.upsert) {
            document = await this.insertOne(collection, { ...query, ...update });
        } else if (document) {
            document = await this.updateOne(collection, query, update);
        }
        
        return document;
    }
}

// Singleton instance
const database = new LocalDatabase();

// Mock Mongoose models for compatibility
class MockModel {
    constructor(collectionName, query = {}) {
        this.collection = collectionName;
        this.query = query;
        this.selectFields = null;
        this.populateFields = null;
        this.limitValue = null;
    }

    find(query = {}) {
        this.query = query;
        return this;
    }

    findOne(query) {
        this.query = query;
        return database.findOne(this.collection, query);
    }

    findOneAndUpdate(query, update, options) {
        return database.findOneAndUpdate(this.collection, query, update, options);
    }

    create(document) {
        return database.insertOne(this.collection, document);
    }

    save() {
        return database.insertOne(this.collection, this);
    }

    select(fields) {
        this.selectFields = fields;
        return this;
    }
    
    populate(fields) {
        this.populateFields = fields;
        return this;
    }
    
    lean() {
        return this;
    }
    
    limit(n) {
        this.limitValue = n;
        return this;
    }
    
    async exec() {
        let results = await database.find(this.collection, this.query);
        if (this.limitValue) {
            results = results.slice(0, this.limitValue);
        }
        return results;
    }
    
    then(resolve, reject) {
        return this.exec().then(resolve, reject);
    }
}

// Create model classes
class LeagueModel extends MockModel {
    constructor() {
        super('leagues');
    }
}

class TeamModel extends MockModel {
    constructor() {
        super('teams');
    }
}

class PlayerModel extends MockModel {
    constructor() {
        super('players');
    }
}

// Export mock models
module.exports = {
    database,
    League: new LeagueModel(),
    Team: new TeamModel(),
    Player: new PlayerModel(),
    init: () => database.init()
};