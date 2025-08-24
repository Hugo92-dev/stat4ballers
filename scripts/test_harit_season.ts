// Test pour vérifier que la saison 2025/2026 d'Amine Harit est bien accessible
import { getPlayerStatistics } from '../services/sportmonks';
import { omPlayersRealStats } from '../data/omPlayersCompleteStats';

async function testHaritSeasons() {
  console.log("Test des saisons d'Amine Harit");
  console.log("=".repeat(60));
  
  // ID d'Amine Harit
  const haritId = 96691;
  
  // Vérifier les données brutes
  console.log("\n1. Données brutes dans omPlayersCompleteStats:");
  const haritData = omPlayersRealStats[haritId];
  if (haritData) {
    console.log(`Nom: ${haritData.displayName}`);
    console.log(`Numéro: ${haritData.jersey}`);
    console.log(`Saisons disponibles:`);
    Object.keys(haritData.stats).forEach(season => {
      const stats = haritData.stats[season];
      console.log(`  - ${season}: ${stats ? 'Données présentes' : 'NULL'}`);
      if (stats && stats.appearences !== undefined) {
        console.log(`    Matchs: ${stats.appearences}, Minutes: ${stats.minutes}`);
      }
    });
  } else {
    console.log("Joueur non trouvé dans les données");
  }
  
  // Tester la fonction getPlayerStatistics
  console.log("\n2. Test de getPlayerStatistics:");
  const stats = await getPlayerStatistics(haritId.toString(), 'ligue1');
  
  console.log("\nSaison actuelle (2025/2026):");
  if (stats.current === null) {
    console.log("  NULL - Pas de données");
  } else {
    console.log(`  Matchs: ${stats.current.appearences}`);
    console.log(`  Minutes: ${stats.current.minutes}`);
    console.log(`  Buts: ${stats.current.goals}`);
    console.log(`  Passes décisives: ${stats.current.assists}`);
  }
  
  console.log("\nSaisons précédentes:");
  stats.previous.forEach((season, index) => {
    const seasonName = index === 0 ? '2024/2025' : '2023/2024';
    if (season === null) {
      console.log(`  ${seasonName}: NULL - Pas de données`);
    } else {
      console.log(`  ${seasonName}:`);
      console.log(`    Matchs: ${season.appearences}`);
      console.log(`    Minutes: ${season.minutes}`);
      console.log(`    Buts: ${season.goals}`);
    }
  });
  
  console.log("\nStatistiques cumulées:");
  if (stats.cumulative === null) {
    console.log("  NULL - Pas de données");
  } else {
    console.log(`  Matchs: ${stats.cumulative.appearences}`);
    console.log(`  Minutes: ${stats.cumulative.minutes}`);
    console.log(`  Buts: ${stats.cumulative.goals}`);
  }
  
  // Vérifier que la saison 2025/2026 est bien créée avec des 0
  console.log("\n3. Vérification finale:");
  if (stats.current !== null) {
    console.log("✅ La saison 2025/2026 est bien disponible (même avec 0 match)");
    console.log(`   Elle affiche: ${stats.current.appearences} match(s), ${stats.current.minutes} minute(s)`);
  } else {
    console.log("❌ La saison 2025/2026 n'est pas disponible");
  }
}

testHaritSeasons().catch(console.error);