select
	distinct pbp.batter_id as 'Batter ID',
    concat(pm.name_last, ', ' ,pm.name_first, ' ' ,pm.name_middle) as 'Batter Name',
    -- At Bats
    (COUNT(IF(
		pbp.event_type = "single"
        or pbp.event_type = "double"
        or pbp.event_type = "triple"
        or pbp.event_type = "home_run"
        or pbp.event_type = "batter_interference"
		or pbp.event_type = "field_out"
        or pbp.event_type = "field_error"
        or pbp.event_type = "fielders_choice"
        or pbp.event_type = "fielders_choice_out"
        or pbp.event_type = "force_out"
        or pbp.event_type = "grounded_into_double_play"
        or pbp.event_type = "strikeout"
        or pbp.event_type = "strikeout_double_play"
        or pbp.event_type = "strikeout_triple_play"
        or pbp.event_type = "triple_play"
        or pbp.event_type = "double_play"
        or pbp.event_type = "cs_double_play"
		
        , 1, NULL))) as 'AB',
-- BATTING AVERAGE
	-- Hits
    ROUND((COUNT(IF(
 		pbp.event_type = "single" 
         or pbp.event_type = "double" 
         or pbp.event_type = "triple" 
         or pbp.event_type = "home_run"
 		, 1, NULL))) / 
	-- At Bats
     (COUNT(IF(
		pbp.event_type = "single"
        or pbp.event_type = "double"
        or pbp.event_type = "triple"
        or pbp.event_type = "home_run"
        or pbp.event_type = "batter_interference"
		or pbp.event_type = "field_out"
        or pbp.event_type = "field_error"
        or pbp.event_type = "fielders_choice"
        or pbp.event_type = "fielders_choice_out"
        or pbp.event_type = "force_out"
        or pbp.event_type = "grounded_into_double_play"
        or pbp.event_type = "strikeout"
        or pbp.event_type = "strikeout_double_play"
        or pbp.event_type = "strikeout_triple_play"
        or pbp.event_type = "triple_play"
        or pbp.event_type = "double_play"
        or pbp.event_type = "cs_double_play"
         , 1, NULL))), 3) as 'BA',
	-- ON BASE PERCENTAGE
	-- Hits
	ROUND((COUNT(IF(
		pbp.event_type = "single"
        or pbp.event_type = "double"
        or pbp.event_type ="triple"
        or pbp.event_type = "home_run"
        , 1, NULL))+
	-- Walks
	COUNT(IF(
		pbp.event_type = "intent_walk"
        or pbp.event_type = "walk"
        , 1, NULL))+
	-- HBP
    COUNT(IF(pbp.event_type = "hit_by_pitch", 1, NULL))
	) / 
    -- At Bats
    ((COUNT(IF(
		pbp.event_type = "single"
        or pbp.event_type = "double"
        or pbp.event_type = "triple"
        or pbp.event_type = "home_run"
        or pbp.event_type = "batter_interference"
		or pbp.event_type = "field_out"
        or pbp.event_type = "field_error"
        or pbp.event_type = "fielders_choice"
        or pbp.event_type = "fielders_choice_out"
        or pbp.event_type = "force_out"
        or pbp.event_type = "grounded_into_double_play"
        or pbp.event_type = "strikeout"
        or pbp.event_type = "strikeout_double_play"
        or pbp.event_type = "strikeout_triple_play"
        or pbp.event_type = "triple_play"
        or pbp.event_type = "double_play"
        or pbp.event_type = "cs_double_play"
        , 1, NULL))) + 
	-- Walks
	COUNT(IF(pbp.event_type = "intent_walk" or pbp.event_type = "walk", 1, NULL)) + 
    -- Hit by Pitch
	COUNT(IF(pbp.event_type = "hit_by_pitch", 1, NULL)) + 
    -- Sac Fly
	COUNT(IF(pbp.event_type = "sac_fly" or pbp.event_type = "sac_bunt", 1, NULL))), 3) as OBP,

-- SLUGGING PERCENTAGE
ROUND(
	(COUNT(IF(pbp.event_type = "single", 1, NULL))
    +
    ((COUNT(IF(pbp.event_type = "double", 1, NULL))) * 2)
    +
    ((COUNT(IF(pbp.event_type = "triple", 1, NULL))) * 3)
    +
    ((COUNT(IF(pbp.event_type = "home_run", 1, NULL))) * 4) )
    /
    (COUNT(IF(
		pbp.event_type = "single"
        or pbp.event_type = "double"
        or pbp.event_type = "triple"
        or pbp.event_type = "home_run"
        or pbp.event_type = "batter_interference"
		or pbp.event_type = "field_out"
        or pbp.event_type = "field_error"
        or pbp.event_type = "fielders_choice"
        or pbp.event_type = "fielders_choice_out"
        or pbp.event_type = "force_out"
        or pbp.event_type = "grounded_into_double_play"
        or pbp.event_type = "strikeout"
        or pbp.event_type = "strikeout_double_play"
        or pbp.event_type = "strikeout_triple_play"
        or pbp.event_type = "triple_play"
        or pbp.event_type = "double_play"
        or pbp.event_type = "cs_double_play"
         , 1, NULL)))
, 3) as 'SLG'
from baseball.play_by_play pbp
JOIN baseball.player_master pm on pbp.batter_id = pm.player_id
WHERE pbp.game_id LIKE "2016%" AND pbp.game_type = "R"
GROUP BY pbp.batter_id