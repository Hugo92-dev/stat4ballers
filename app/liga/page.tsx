import LeaguePage from '@/components/LeaguePage';
import { ligaTeams } from '@/data/leagues';

export default function LigaPage() {
  return (
    <LeaguePage
      leagueId="liga"
      leagueName="Liga"
      leagueFlag="🇪🇸"
      teams={ligaTeams}
      gradient="from-red-500 to-orange-600"
    />
  );
}