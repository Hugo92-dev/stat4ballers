import LeaguePage from '@/components/LeaguePage';
import { premierLeagueTeams } from '@/data/premierLeagueTeams';

export default function PremierLeaguePage() {
  return (
    <LeaguePage
      leagueId="premier-league"
      leagueName="Premier League"
      leagueFlag="🏴󠁧󠁢󠁥󠁮󠁧󠁿"
      teams={premierLeagueTeams}
      gradient="from-purple-600 to-purple-800"
    />
  );
}