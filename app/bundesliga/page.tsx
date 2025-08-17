import LeaguePage from '@/components/LeaguePage';
import { bundesligaTeams } from '@/data/leagues';

export default function BundesligaPage() {
  return (
    <LeaguePage
      leagueId="bundesliga"
      leagueName="Bundesliga"
      leagueFlag="🇩🇪"
      teams={bundesligaTeams}
      gradient="from-gray-700 to-gray-900"
    />
  );
}