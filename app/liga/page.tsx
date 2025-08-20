import LeaguePage from '@/components/LeaguePage';
import { ligaTeams } from '@/data/ligaTeams';

export default function LigaPage() {
  return (
    <LeaguePage
      leagueId="liga"
      leagueName="La Liga"
      leagueFlag="🇪🇸"
      teams={ligaTeams}
      gradient="from-orange-600 to-orange-800"
    />
  );
}