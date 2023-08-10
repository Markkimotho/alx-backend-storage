-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that 
-- computes and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    	DECLARE user_id INT;
    	DECLARE total_score FLOAT;
    	DECLARE total_weight FLOAT;
    	DECLARE weighted_average FLOAT;
    
    	-- Declare cursor to iterate over user ids
    	DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    	DECLARE CONTINUE HANDLER FOR NOT FOUND SET @done = TRUE;
    
    	-- Open cursor
    	OPEN user_cursor;
    
    	-- Iterate over user ids
    	user_loop: LOOP
        	-- Fetch next user id
        	FETCH user_cursor INTO user_id;
        
        	-- Exit loop if no more users
        	IF @done THEN
        		LEAVE user_loop;
        	END IF;
        
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
END LOOP;
	-- Close cursor
    	CLOSE user_cursor;
    
END //

DELIMITER ;
