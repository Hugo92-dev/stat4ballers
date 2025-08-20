import LeaguePage from '@/components/LeaguePage';
import { serieATeams } from '@/data/serieATeams';

export default function SerieAPage() {
  return (
    <LeaguePage
      leagueId="serie-a"
      leagueName="Serie A"
      leagueFlag="🇮🇹"
      teams={serieATeams}
      gradient="from-green-600 to-green-800"
    />
  );
}