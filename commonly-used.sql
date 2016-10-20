SELECT distinct md.seasonID, md.homeSide, md.stadium, t.teamLongName
FROM fanfootball.stg_match_details as md
	INNER JOIN fanfootball.teams as t on md.homeSide = t.teamID
ORDER BY seasonID, stadium;

SELECT     *
FROM 	stg_player_stats
WHERE ps_playerID = 215170;

UPDATE stg_player_stats SET 
    ps_playerName = 'Didier N''Dong', 
    ps_playerURL = '/player/215170/didier-n''dong'
WHERE 
	ps_playerID = 215170;

SELECT * FROM fanfootball.stg_player_news
order by player_news_status, player_returndate, player_team, player_rowadded;

UPDATE fanfootball.stg_player_news
SET player_news_status = 0 
WHERE
	player_returndate <= '2016-10-16' 

DELETE from fanfootball.players 
where pl_seasonID = 2;

INSERT into fanfootball.players 
(pl_playerID, pl_playerTeam, pl_jerseyNo, pl_playerName, pl_playerURL, pl_seasonID) 
SELECT DISTINCT 
	ps.ps_playerID, 
	ps.ps_team,
    ps.ps_jerseyNo,
    ps.ps_playerName,
	ps.ps_playerURL,
    ps.ps_seasonID
FROM fanfootball.stg_player_stats as ps
WHERE ps.ps_seasonID = 2