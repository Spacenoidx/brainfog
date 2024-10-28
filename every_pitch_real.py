import statsapi

sched = statsapi.schedule(start_date='07/01/2024',end_date='07/31/2024')

print('The A\'s won %s games in 2024.' % sum(1 for x in statsapi.schedule(team=133,start_date='3/29/2018',end_date='9/30/2018') if x.get('winning_team','')=='Oakland Athletics'))
