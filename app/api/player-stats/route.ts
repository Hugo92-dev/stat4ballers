import { NextRequest, NextResponse } from 'next/server';
import { getPlayerStatistics, CURRENT_SEASONS } from '@/services/sportmonks';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const playerId = searchParams.get('playerId');
  const league = searchParams.get('league');

  if (!playerId || !league) {
    return NextResponse.json(
      { error: 'Missing playerId or league parameter' },
      { status: 400 }
    );
  }

  try {
    const stats = await getPlayerStatistics(
      parseInt(playerId), 
      league as keyof typeof CURRENT_SEASONS
    );
    
    return NextResponse.json(stats);
  } catch (error) {
    console.error('Error fetching player stats:', error);
    return NextResponse.json(
      { error: 'Failed to fetch player statistics' },
      { status: 500 }
    );
  }
}