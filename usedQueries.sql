-- Select SQL Server version
SELECT @@VERSION;

-- Count the number of users in the database
SELECT COUNT(*) FROM [user];

-- Insert a new user into the user table
INSERT INTO [user] (fname, lname, profile_name, email, password, bio, account_type)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- Authenticate a user by email and password
SELECT user_id, fname, lname, profile_name, profile_pic_path, email, bio, account_type
FROM [user]
WHERE email = ? AND password = ?;

-- Select personal posts of a user
SELECT * FROM post
WHERE created_by_user_id = ?;

-- Update the profile picture of a user
UPDATE [user]
SET profile_pic_path = ?
WHERE user_id = ?;

-- Select all posts
SELECT * FROM post;

-- Select comments for a specific post
SELECT * FROM comment
WHERE post_id = ?;

-- Get the name of the commenter
SELECT u.fname, u.lname
FROM comment c
JOIN [user] u
ON c.created_by_user_id = u.user_id
WHERE c.id = ?;

-- Select media for a specific post
SELECT * FROM post_media
WHERE post_id = ?;

-- Select effects for a specific post media
SELECT ef.* FROM [effect] ef 
JOIN [post_media_effect] pe
ON pe.effect_id = ef.id
JOIN [post_media] pm
ON pm.post_media_id = pe.post_media_id
WHERE pm.post_media_id = ?;

-- Select filter for a specific post media
SELECT f.filter_name FROM [filter] f 
JOIN [post_media] pm
ON pm.filter_id = f.id
WHERE pm.post_media_id = ?;

-- Count the number of reactions for a specific post
SELECT COUNT(*) FROM reaction
WHERE post_id = ?;

-- Insert a new reaction for a post
INSERT INTO [reaction] (user_id, post_id)
VALUES (?, ?);

-- Insert a new comment for a post
INSERT INTO comment (created_by_user_id, post_id, comment, created_datetime)
VALUES (?, ?, ?, ?);

-- Update the caption of a post
UPDATE post
SET caption = ?
WHERE post_id = ?;

-- Delete a post
DELETE FROM post
WHERE post_id = ?;

-- Select all effects
SELECT * FROM [effect];

-- Select all filters
SELECT * FROM [filter];

-- Insert a new post
INSERT INTO post (created_by_user_id, created_datetime, caption, location, post_type)
VALUES (?, ?, ?, ?, ?);

-- Select the latest post id created by a user
SELECT TOP 1 post_id 
FROM [post]
WHERE created_by_user_id = ? 
ORDER BY created_datetime DESC;

-- Insert a new post media
INSERT INTO post_media (post_id, media_file, filter_id, longtude, latitude)
VALUES (?, ?, ?, 1, 1);

-- Select post media id for a specific post and media file
SELECT post_media_id FROM post_media
WHERE post_id = ? AND media_file = ?;

-- Insert a new post media effect
INSERT INTO post_media_effect (post_media_id, effect_id)
VALUES (?, ?);

-- Insert a new saved post
INSERT INTO saved_post (user_id, post_id, saved_at)
VALUES (?, ?, ?);

-- Select saved posts for a user
SELECT p.* FROM post p
JOIN saved_post sp
ON p.post_id = sp.post_id
WHERE sp.user_id = ?;

-- Insert a new collection
INSERT INTO collection (user_id, collection_name, created_at)
VALUES (?, ?, ?);

-- Insert a post into a collection
INSERT INTO collection_post (collection_id, post_id)
VALUES (?, ?);

-- Select collections for a user
SELECT * FROM collection
WHERE user_id = ?;

-- Select posts in a collection
SELECT p.* FROM post p
JOIN collection_post cp
ON p.post_id = cp.post_id
WHERE cp.collection_id = ?;

-- Count the number of collections for a user
SELECT COUNT(*) FROM collection
WHERE user_id = ?;

-- Update user account type to business
UPDATE [user] 
SET account_type = 'business'
WHERE user_id = ?;

-- Insert a new business account
INSERT INTO business_account (user_id, business_name, category, website, contact_email, contact_phone)
VALUES (?, ?, ?, ?, ?, ?);

-- Select business account information for a user
SELECT * FROM business_account
WHERE user_id = ?;

-- Count the number of business accounts for a user
SELECT COUNT(*) FROM business_account
WHERE user_id = ?;

-- Select business id for a user
SELECT business_id FROM business_account
WHERE user_id = ?;

-- Insert a new product
INSERT INTO product (business_id, product_name, price, description, available_stock)
VALUES (?, ?, ?, ?, ?);

-- Select products for a business
SELECT * FROM product
WHERE business_id = ?;

-- Select ad insights for an ad
SELECT * FROM ad_insight
WHERE ad_id = ?;

-- Select ads for a business
SELECT * FROM advertisement
WHERE created_by_user_id = ?;

-- Insert a new advertisement
INSERT INTO advertisement (created_by_user_id, post_id, product_id, created_datetime, target_audience, start_date, end_date)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- Select product name for an ad
SELECT p.product_name FROM product p
JOIN advertisement a
ON p.product_id = a.product_id
WHERE a.ad_id = ?;

-- Insert a new ad insight
INSERT INTO ad_insight (ad_id, views_count, clicks_count, impressions, engagement_rate, cost_per_click, cost_per_mille)
VALUES (?, 0, 0, 0, 0, 0, 0);

-- Select all users
SELECT * FROM [user];

-- Insert a new follower
INSERT INTO follower (following_user_id, followed_user_id, created_at, status)
VALUES (?, ?, ?, 'accepted');

-- Delete a follower
DELETE FROM follower
WHERE following_user_id = ? AND followed_user_id = ?;

-- Select followers for a user
SELECT u.* FROM [user] u
JOIN follower f
ON u.user_id = f.following_user_id
WHERE f.followed_user_id = ?;

-- Select users followed by a user
SELECT u.* FROM [user] u
JOIN follower f
ON u.user_id = f.followed_user_id
WHERE f.following_user_id = ?;

-- Count the number of followers for a user
SELECT COUNT(*) FROM follower
WHERE followed_user_id = ?;

-- Count the number of users followed by a user
SELECT COUNT(*) FROM follower
WHERE following_user_id = ?;