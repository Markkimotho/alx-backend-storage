-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that
-- computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    	DECLARE total_score FLOAT;
    	DECLARE total_weight FLOAT;
    	DECLARE weighted_average FLOAT;

    	-- Calculate the total score and total weight for the user
    	SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    	INTO total_score, total_weight
    	FROM corrections
    	JOIN projects ON corrections.project_id = projects.id
    	WHERE corrections.user_id = user_id;

    	-- Calculate the weighted average
    	SET weighted_average = total_score / total_weight;

    	-- Update the user's average_score in the users table
    	UPDATE users
    	SET average_score = weighted_average
    	WHERE id = user_id;
END //

DELIMITER ;
