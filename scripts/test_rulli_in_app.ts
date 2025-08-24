// Test pour vérifier que les stats de Rulli sont bien chargées
import { getPlayerStatistics } from '../services/sportmonks';
import { omPlayersRealStats } from '../data/omPlayersCompleteStats';

async function testRulliStats() {
  console.log("Test des stats de Rulli après mise à jour");
  console.log("=" * 60);
  
  // ID de Rulli
  const rulliId = '186418';
  
  // Vérifier les données brutes
  console.log("\n1. Données brutes dans omPlayersRealStats:");
  const rulliData = omPlayersRealStats[186418];
  if (rulliData) {
    console.log(`Nom: ${rulliData.displayName}`);
    console.log(`Position: ${rulliData.position}`);
    console.log(`Numéro: ${rulliData.jersey}`);
    console.log(`Saisons disponibles:`);
    Object.keys(rulliData.stats).forEach(season => {
      const stats = rulliData.stats[season];
      if (stats) {
        console.log(`  - ${season}:`);
        console.log(`    Matchs: ${stats.appearences}`);
        console.log(`    Minutes: ${stats.minutes}`);
        console.log(`    Clean sheets: ${stats.clean_sheets}`);
        console.log(`    Buts encaissés: ${stats.goals_conceded}`);
      }
    });
  } else {
    console.log("❌ Rulli non trouvé dans les données");
  }
  
  // Tester la fonction getPlayerStatistics
  console.log("\n2. Test de getPlayerStatistics:");
  const stats = await getPlayerStatistics(rulliId, 'ligue1');
  
  console.log("\nSaison actuelle (2025/2026):");
  if (stats.current === null) {
    console.log("  NULL - Pas de données");
  } else {
    console.log(`  Matchs: ${stats.current.appearences}`);
    console.log(`  Minutes: ${stats.current.minutes}`);
    console.log(`  Clean sheets: ${stats.current.clean_sheets}`);
    console.log(`  Buts encaissés: ${stats.current.goals_conceded}`);
  }
  
  console.log("\nSaison 2024/2025:");
  if (stats.previous[0] === null) {
    console.log("  NULL - Pas de données");
  } else {
    console.log(`  Matchs: ${stats.previous[0].appearences}`);
    console.log(`  Minutes: ${stats.previous[0].minutes}`);
    console.log(`  Clean sheets: ${stats.previous[0].clean_sheets}`);
    console.log(`  Buts encaissés: ${stats.previous[0].goals_conceded}`);
  }
  
  console.log("\n✅ Test terminé - Les stats de Rulli devraient maintenant être différentes pour chaque saison");
}

testRulliStats().catch(console.error);