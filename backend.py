import pyodbc
from datetime import datetime

def create_connection():
    server = "localhost,1433"
    database = "instgram_db"
    username = "sa"
    password = "password"
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "TrustServerCertificate=yes"  # Disable SSL certificate validation
    )
    return pyodbc.connect(conn_str)


def test_connection():
    try:
        conn = create_connection()
        print("Connection successful!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        db_version = cursor.fetchone()
        print("SQL Server version:", db_version[0])

        cursor.execute("SELECT COUNT(*) FROM [user]")
        user_count = cursor.fetchone()[0]
        print(f"Number of users in database: {user_count}")
        
        cursor.close()
        conn.close()
        return True
    except pyodbc.Error as e:
        print("Connection failed!")
        print("Error:", str(e))
        return False

def create_user(fname, lname, profile_name, email, password, bio="", account_type="regular"):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO [user] (fname, lname, profile_name, email, password, bio, account_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (fname, lname, profile_name, email, password, bio, account_type))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def authenticate_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, fname, lname, profile_name, profile_pic_path,email, bio, account_type
        FROM [user]
        WHERE email = ? AND password = ?
    """, (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    user = {
        "user_id": user[0],
        "fname": user[1],
        "lname": user[2],
        "profile_name": user[3],
        "profile_pic_path": user[4],
        "email": user[5],
        "bio": user[6],
        "account_type": user[7]
    }
    return user
    
def display_personal_posts(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM post
        WHERE created_by_user_id = ?
    """, (user_id,))
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

def change_profile_pic(user_id, profile_pic_path):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE [user]
        SET profile_pic_path = ?
        WHERE user_id = ?
    """, (profile_pic_path, user_id))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def display_all_posts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM post
    """)
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

def get_comments(post_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * from comment
        WHERE post_id = ?
    """, (post_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments

def get_commenter_name(comment_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.fname, u.lname
        FROM comment c
        JOIN [user] u
        ON c.created_by_user_id = u.user_id
        WHERE c.id = ?
    """, (comment_id,))
    commenter = cursor.fetchone()
    cursor.close()
    conn.close()
    return f"{commenter[0]} {commenter[1]}"

def get_post_media(post_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM post_media
        WHERE post_id = ?
        """, (post_id,))
    media = cursor.fetchall()
    cursor.close()
    conn.close()
    return media

def get_post_media_effects(post_media_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ef.* FROM [effect] ef 
        JOIN [post_media_effect] pe
        ON pe.effect_id = ef.id
        JOIN [post_media] pm
        ON pm.post_media_id = pe.post_media_id
        WHERE pm.post_media_id = ?
    """, (post_media_id,))
    effects = cursor.fetchall()
    cursor.close()
    conn.close()
    return effects

def get_post_media_filter(post_media_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.filter_name FROM [filter] f 
        JOIN [post_media] pm
        ON pm.filter_id = f.id
        WHERE pm.post_media_id = ?
    """, (post_media_id,))
    filters = cursor.fetchall()
    cursor.close()
    conn.close()
    return filters

def get_number_reacts(post_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM reaction
        WHERE post_id = ?
    """, (post_id,))
    react_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return react_count

def create_reaction(user_id,post_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO [reaction] (user_id,post_id)
        VALUES (?,?)
    """, (user_id, post_id))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def create_comment(user_id, post_id, comment):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO comment (created_by_user_id, post_id, comment, created_datetime)
        VALUES (?, ?, ?, ?)
    """, (user_id, post_id, comment, datetime.now()))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def update_post(post_id, new_caption):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE post
        SET caption = ?
        WHERE post_id = ?
    """, (new_caption, post_id))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def delete_post(post_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM post
        WHERE post_id = ?
    """, (post_id,))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def show_effects():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM [effect]
    """)
    effects = cursor.fetchall()
    cursor.close()
    conn.close()
    return effects

def show_filters():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM [filter]
    """)
    filters = cursor.fetchall()
    cursor.close()
    conn.close()
    return filters

def create_post(created_by_user_id,created_datetime, caption, location, post_type):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO post (created_by_user_id, created_datetime, caption, location, post_type)
        VALUES (?, ?, ?, ?, ?)
    """, (created_by_user_id, created_datetime, caption, location, post_type))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()

    # get the lastly created post id
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 1 post_id 
        FROM [post]
        WHERE created_by_user_id = ? 
        ORDER BY created_datetime DESC
    """, (created_by_user_id, ))
    post_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return post_id

def create_post_media(post_id, media_file, filter_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO post_media (post_id, media_file, filter_id, longtude, latitude)
        VALUES (?, ?, ?, 1, 1)
    """, (post_id, media_file, filter_id))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def get_post_media_id(post_id, media_file):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT post_media_id FROM post_media
        WHERE post_id = ? AND media_file = ?
    """, (post_id, media_file))
    post_media_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return post_media_id

def post_effects_register(post_media_id, effect_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO post_media_effect (post_media_id, effect_id)
        VALUES (?, ?)
    """, (post_media_id, effect_id))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def save_post(post_id, user_id, saved_at):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO saved_post (user_id, post_id, saved_at)
        VALUES (?, ?, ?)
    """, (user_id, post_id, saved_at))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def get_saved_posts(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.* FROM post p
        JOIN saved_post sp
        ON p.post_id = sp.post_id
        WHERE sp.user_id = ?
    """, (user_id,))
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

def create_collection(user_id, collection_name, created_at):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO collection (user_id, collection_name, created_at)
        VALUES (?, ?, ?)
    """, (user_id, collection_name, created_at))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def add_post_to_collection(post_id, collection_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO collection_post (collection_id, post_id)
        VALUES (?, ?)
    """, (collection_id, post_id))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def get_collections(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM collection
        WHERE user_id = ?
    """, (user_id,))
    collections = cursor.fetchall()
    cursor.close()
    conn.close()
    return collections

def get_collection_posts(collection_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.* FROM post p
        JOIN collection_post cp
        ON p.post_id = cp.post_id
        WHERE cp.collection_id = ?
    """, (collection_id,))
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

def count_collection(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM collection
        WHERE user_id = ?
    """, (user_id,))
    collection_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return collection_count

def activate_business_account(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        update [user] 
        set account_type = 'business'
        where user_id = ?
    """, (user_id,))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def bussiness_account_add_info( user_id, business_name, category, website, business_email, contact_phone):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO business_account (user_id, business_name, category, website, contact_email, contact_phone)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, business_name, category, website, business_email, contact_phone))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def get_business_info(business_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM business_account
        WHERE user_id = ?
    """, (business_id,))
    business_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return business_info

def check_exist_in_bussiness_table(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM business_account
        WHERE user_id = ?
    """, (user_id,))
    business_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return business_count

def get_bussiness_id(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT business_id FROM business_account
        WHERE user_id = ?
    """, (user_id,))
    business_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return business_id

def create_product(business_id, product_name, price, description, available_stock):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO product (business_id, product_name, price, description, available_stock)
        VALUES (?, ?, ?, ?, ?)
    """, (business_id, product_name, price, description, available_stock))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def get_products(business_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM product
        WHERE business_id = ?
    """, (business_id,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

def ad_insights(ad_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM ad_insight
        WHERE ad_id = ?
    """, (ad_id,))
    insight = cursor.fetchone()
    cursor.close()
    conn.close()
    return insight

def get_ads(bussiness_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM advertisement
        WHERE created_by_user_id = ?
    """, (bussiness_id,))
    ads = cursor.fetchall()
    cursor.close()
    conn.close()
    return ads

def insert_advertisment(created_by_user_id, post_id, product_id, created_datetime, target_audience, start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO advertisement (created_by_user_id, post_id, product_id, created_datetime, target_audience, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (created_by_user_id, post_id, product_id, created_datetime, target_audience, start_date, end_date))
    conn.commit()
    row_count = cursor.rowcount > 0

    cursor.execute("""
                   SELECT ad_id FROM advertisement
                     WHERE created_by_user_id = ? AND post_id = ? AND product_id = ?
                     """, (created_by_user_id, post_id, product_id))
    ad_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return ad_id
    
def get_product_name(ad_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.product_name FROM product p
        JOIN advertisement a
        ON p.product_id = a.product_id
        WHERE a.ad_id = ?
    """, (ad_id,))
    product_name = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return product_name

def insert_ad_insight(ad_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ad_insight (ad_id, views_count, clicks_count, impressions, engagement_rate, cost_per_click, cost_per_mille)
        VALUES (?, 0, 0, 0, 0, 0, 0)
    """, (ad_id,))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM [user]
    """)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def follow(following_user_id, followed_user_id, created_at):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO follower (following_user_id, followed_user_id, created_at, status)
        VALUES (?, ?, ?, 'accepted')
    """, (following_user_id, followed_user_id, created_at))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def unfollow(following_user_id, followed_user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM follower
        WHERE following_user_id = ? AND followed_user_id = ?
    """, (following_user_id, followed_user_id))
    conn.commit()
    row_count = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return row_count

def get_followers(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.* FROM [user] u
        JOIN follower f
        ON u.user_id = f.following_user_id
        WHERE f.followed_user_id = ?
    """, (user_id,))
    followers = cursor.fetchall()
    cursor.close()
    conn.close()
    return followers

def get_following(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.* FROM [user] u
        JOIN follower f
        ON u.user_id = f.followed_user_id
        WHERE f.following_user_id = ?
    """, (user_id,))
    following = cursor.fetchall()
    cursor.close()
    conn.close()
    return following


def count_followers(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM follower
        WHERE followed_user_id = ?
    """, (user_id,))
    follower_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return follower_count

def count_following(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM follower
        WHERE following_user_id = ?
    """, (user_id,))
    following_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return following_count


def get_data_dictionary():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
        TABLE_NAME, 
        COLUMN_NAME, 
        DATA_TYPE, 
        CHARACTER_MAXIMUM_LENGTH, 
        IS_NULLABLE 
        FROM 
                INFORMATION_SCHEMA.COLUMNS 
        WHERE 
                TABLE_CATALOG = 'instgram_db' 
        ORDER BY 
                TABLE_NAME, 
                ORDINAL_POSITION;
    """)
    data_dict = cursor.fetchall()
    cursor.close()
    conn.close()
    return data_dict
    
