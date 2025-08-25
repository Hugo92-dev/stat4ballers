import LeaguePage from '@/components/LeaguePage';
import { ligue1Teams } from '@/data/ligue1Teams';

export default function Ligue1Page() {
  return (
    <LeaguePage
      leagueId="ligue1"
      leagueName="Ligue 1"
      leagueFlag="🇫🇷"
      teams={ligue1Teams}
      gradient="from-blue-600 to-blue-800"
    />
  );
}