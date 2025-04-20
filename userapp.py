import streamlit as st
from PIL import Image
import backend
import ast
import datetime


def boxstyle(post_type):
    color = ""
    post_type_text = ''
    if post_type == 1:
        color = "#f0f8f0"
        post_type_text = 'story'
    elif post_type == 2:
        color = "#f8f0f0"
        post_type_text = 'post'
    elif post_type == 3:
        color = "#f0f0f8"
        post_type_text = 'reel'
    elif post_type == 4:
        color = "#f8f0f8"
        post_type_text = 'ad'
    
    box_style = """
    <div style="border-radius: 10px; padding: 20px; margin: 20px 0; background-color: """ + color + """; 
        border: 2px solid #0056d6;color: #000000;">
        <p style="font-size: 20px; font-weight: bold;">This is a """+ post_type_text +"""</p>
        <p style="font-size: 16px;">You can add more text here.</p>
    </div>
    """
    return box_style


def receive_data():
    with open('dummy.txt', 'r') as f:
        data = f.read()
    return data

def modify_data(data):
    with open('dummy.txt', 'w') as f:
        f.write(str(data))


# Mock data
data = receive_data()
user_profile = ast.literal_eval(data)


# Function to display user profile
def display_user_profile():
    if user_profile["profile_pic_path"]:
        st.image(Image.open(user_profile["profile_pic_path"]), width=150)
    else:
        st.write("No image provided")
    st.write(f"**{user_profile['fname']} {user_profile['lname']}**")
    st.write(user_profile["bio"])
    st.write(f"**Email:** {user_profile['email']}")
    # Change Profile Picture
    st.write("### Change Profile Picture")
    new_profile_pic = st.file_uploader("Upload a new profile picture", type=["png", "jpg", "jpeg"])
    if new_profile_pic is not None:
        backend.change_profile_pic(user_profile["user_id"], new_profile_pic.name)
        st.success("Profile picture updated successfully!")
    # Business Account Option
    if user_profile.get("account_type") != "business":
        if st.sidebar.button("Switch to Business Account Mode"):
            backend.activate_business_account(user_profile["user_id"])
            user_profile["account_type"] = "business"
            modify_data(user_profile)
            st.sidebar.success("You are now in Business Account Mode")
    else:
        st.sidebar.write("You are in Business Account Mode")

    st.write('---')


# Function to display posts
def display_posts(posts):
    for post in posts:
        # Display the post with media, effects, and filters
        media_files = backend.get_post_media(post[0]) # Assuming this holds media file paths (e.g., images, videos)
        post_type = post[5]
        color = ""
        post_type_text = ''
        if post_type == 1:
            color = "#feba6f"
            post_type_text = 'story'
        elif post_type == 2:
            color = "##6dbfb8"
            post_type_text = 'post'
        elif post_type == 3:
            color = "#f0f0f8"
            post_type_text = 'reel'
        elif post_type == 4:
            color = "#272731"
            post_type_text = 'ad'
            if post[5] == 1:
                post_type = "Story"


        # Post content box with caption and media
        post_box = f"""
        <div style='border: 2px solid #e0e0e0; background-color: {color}; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='color: #ffffff ;'>{post[3]}</h3>
            <p style="font-size: 20px; color: #2e4053;font-weight: bold;">This is a {post_type_text}</p>
            <p style='font-size: 12px; color: #7d8799;'>Created at: {post[2].strftime('%Y-%m-%d %H:%M:%S')}</p>
        """

        # Adding media files with effects and filters
        for media in media_files: 
            effects = backend.get_post_media_effects(media[0])
            fltr = media[2]
            try:
                st.image(Image.open(media[3]))
            except FileNotFoundError:
                st.write("File not available now")
            media_box = f"""
            <div style='margin-top: 10px;'>
                <p style='font-size: 12px; color: #7d8799;'>Effects: {str(effects)} | Filter: {fltr} Filter Name: {backend.get_post_media_filter(media[0])}</p>
            </div>
            """
            st.markdown(media_box, unsafe_allow_html=True)

        post_box += f"""
        <div style='margin-top: 10px;'>
            <p style='color: #7d8799;'> post id: {post[0]}</p>
            <p style='color: #ffffff;'>Likes: {backend.get_number_reacts(post[0])}</p>
        </div>
        </div>
        """
            
        st.markdown(post_box, unsafe_allow_html=True)

       

        # Display comments
        st.write("Comments:")
        comments = backend.get_comments(post[0])  # Assuming each comment has 'username' and 'content'

        for comment in comments:
            user = backend.get_commenter_name(comment[0])
            content = comment[4]
            comment_box = f"""
            <div style='border: 1px solid #d0d3d4; background-color: #1c2833; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <strong style='color: #ffffff;'>{user}</strong>:<br>
                <span style='margin-left: 15px;'>{content}</span>
            </div>
            """
            st.markdown(comment_box, unsafe_allow_html=True)
        
        # Separator between posts
        st.write("---")


def create_post(is_business_account=False):
    st.title("Create a Post")

    # Caption input
    caption = st.text_area("Enter your caption", placeholder="Write something...")

    # Media selection - using file_uploader for multiple files
    media_files = st.file_uploader("Upload media files (at least one required)", 
                                   accept_multiple_files=True, type=["png", "jpg", "jpeg", "mp4"])
    
    if not media_files:
        st.warning("Please upload at least one media file.")

    else:
        media_data = []
        filter_dict = {filter.filter_name: filter.id for filter in backend.show_filters()}
        effect_dict = {effect.effect_name: effect.id for effect in backend.show_effects()}
        filter_choices = [filter.filter_name for filter in  backend.show_filters()]
        effects_choices = [effect.effect_name for effect in backend.show_effects()]
        for media in media_files:
            st.write(f"Settings for {media.name}")
            
            # Filter selection for each media
            filter_choice = st.selectbox(f"Choose a filter for {media.name}", 
                                         options=filter_choices)

            # Effect selection for each media
            effects_choice = st.multiselect(f"Choose effects for {media.name} (Multiple allowed)", 
                                            options=effects_choices)

            media_data.append({"media_name": media.name, "filter": filter_dict[filter_choice], "effects": [effect_dict[ec]for ec in effects_choice]})

    # Post type selection
    post_type_dict = {"post": 2, "reel": 3, "story": 1, "ad": 4}
    if not is_business_account:
        post_type = st.selectbox("Select the type of post", options=["post", "reel", "story"])
    elif is_business_account:
        post_type = st.selectbox("Select the type of post", 
                                 options=["post", "reel", "story", "ad"])

    # Post location input
    if post_type == "ad":
        products = backend.get_products(backend.get_bussiness_id(user_profile["user_id"]))
        product_choices = {product.product_name: product.product_id for product in products}
        selected_product = st.selectbox("Select a product to advertise", options=list(product_choices.keys()))
        target_audience = st.text_area("Target Audience")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

    location = st.text_input("Enter the location of the post", placeholder="Location")

    # Button to publish the post
    if st.button("Publish Post"):
        if not media_files:
            st.error("You must upload at least one media file.")
        else:
            st.success("Post published successfully!")
            time_created = datetime.datetime.now()

            if post_type == "ad":
                caption += f"\nAd for {selected_product} - {caption}\nTarget Audience: {target_audience}\nStart Date: {start_date}\nEnd Date: {end_date}"
                # insert_advertisment(created_by_user_id, post_id, product_id, created_datetime, target_audience, start_date, end_date):
                pid = backend.create_post(user_profile["user_id"], created_datetime=time_created, caption=caption,location=location ,post_type=post_type_dict[post_type])
                aid = backend.insert_advertisment(user_profile["user_id"], pid, product_choices[selected_product], time_created, target_audience, start_date, end_date)
                backend.insert_ad_insight(aid)
            else:
                pid = backend.create_post(user_profile["user_id"], created_datetime=time_created, caption=caption,location=location ,post_type=post_type_dict[post_type])

            for media in media_data:
                backend.create_post_media(pid, media["media_name"], media["filter"])
                mid = backend.get_post_media_id(pid, media["media_name"])
                for media_effect in media["effects"]:
                    backend.post_effects_register(mid, media_effect)


def collection_view():
    st.write("### Collections")

    # Create a new collection
    new_collection_name = st.text_input("Enter the name of the new collection")
    if st.button("Create Collection"):
        backend.create_collection(user_profile["user_id"], new_collection_name, datetime.datetime.now())
        st.success("Collection created successfully!")

    # Separator
    st.markdown("---")

    # Add a post to a collection
    if backend.count_collection(user_profile["user_id"]) == 0:
        st.warning("No collections available. Please create a collection first.")
        return
    else:
        post_id_to_add = st.number_input("Enter Post ID to Add to Collection", min_value=1, step=1)
        collection_name = st.text_input("Enter the name of the collection to add the post")
        if st.button("Add Post to Collection"):
            backend.add_post_to_collection(post_id_to_add,collection_name)
            st.success("Post added to collection successfully!")

    # Separator
    st.markdown("---")
    st.markdown("# Your Collections")
    for collection in backend.get_collections(user_profile["user_id"]):
        st.markdown(f"## {collection.collection_name} ({collection.collection_id})")
        for post in backend.get_collection_posts(collection.collection_id):
            post_box = f"""
            <div style='border: 2px solid #e0e0e0; background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <h4 style='color: #2e4053;'>Caption: {post.caption}</h4>
                <p style='font-size: 12px; color: #7d8799;'>Post Id: {post.post_id}</p>
            </div>
            """
            st.markdown(post_box, unsafe_allow_html=True)

def add_business_account_insights():
    st.write("### Business Account Insights")
    st.write("### Add Business Account Information")

    business_name = st.text_input("Business Name")
    category = st.text_input("Category")
    website = st.text_input("Website")
    business_email = st.text_input("Business Email")
    contact_phone = st.text_input("Contact Phone")

    if st.button("Add Business Info"):
        if business_name and category and website and business_email and contact_phone:
            success = backend.bussiness_account_add_info(user_profile["user_id"], business_name, category, website, business_email, contact_phone)
            if success:
                st.success("Business information added successfully!")
            else:
                st.error("Failed to add business information.")
        else:
            st.error("Please fill in all fields.")


# Streamlit app layout
st.title("Your feed")

# User Profile Section
st.sidebar.title("User Profile")
display_user_profile()

# React button
st.sidebar.title("Engage with Posts")

# Like a post
post_id_to_like = st.sidebar.number_input("Enter Post ID to Like", min_value=1, step=1)
if st.sidebar.button("Like Post"):
    backend.create_reaction(user_profile["user_id"], post_id_to_like)
    st.sidebar.success("Post liked successfully!")

# Add a comment
post_id_to_comment = st.sidebar.number_input("Enter Post ID to Comment", min_value=1, step=1, key="comment_post_id")
new_comment = st.sidebar.text_area("Add a comment:", key="new_comment")
if st.sidebar.button("Submit Comment"):
    backend.create_comment(user_profile["user_id"], post_id_to_comment, new_comment)
    st.sidebar.success("Comment added successfully!")

# Update a post
post_id_to_update = st.sidebar.number_input("Enter Post ID to Update", min_value=1, step=1, key="update_post_id")
updated_content = st.sidebar.text_area("Update post content:", key="updated_content")
if st.sidebar.button("Update Post"):
    backend.update_post(post_id_to_update, updated_content)
    st.sidebar.success("Post updated successfully!")

# Delete a post
post_id_to_delete = st.sidebar.number_input("Enter Post ID to Delete", min_value=1, step=1, key="delete_post_id")
if st.sidebar.button("Delete Post"):
    backend.delete_post(post_id_to_delete)
    st.sidebar.success("Post deleted successfully!")

# Save a post
post_id_to_save = st.sidebar.number_input("Enter Post ID to Save", min_value=1, step=1, key="save_post_id")
if st.sidebar.button("Save Post"):
    backend.save_post(post_id_to_save, user_profile["user_id"],datetime.datetime.now())
    st.sidebar.success("Post saved successfully!")



# User Sections
st.sidebar.title("Account Sections")
section = st.sidebar.radio("# Sections", ["Personal Posts", "All Posts", "Create Post", "Saved Posts", "Collections","Business Account Insights", "Products", "Advertisements", "Explore people"])

if section == "Personal Posts":
    st.header("Personal Posts")
    display_posts(backend.display_personal_posts(user_profile["user_id"]))
elif section == "All Posts":
    st.header("All Posts")
    display_posts(backend.display_all_posts())
elif section == "Create Post":
    create_post(user_profile.get("account_type") == "business")
elif section == "Saved Posts":
    st.header("Saved Posts")
    display_posts(backend.get_saved_posts(user_profile["user_id"]))
elif section == "Collections":
    collection_view()
# Additional sections for business accounts
if user_profile.get("account_type") == "business":
    if section == "Business Account Insights":
        st.header("Business Account Insights")
        if not (backend.check_exist_in_bussiness_table(user_profile["user_id"])):
            add_business_account_insights()
        else:
            insights = backend.get_business_info(user_profile["user_id"])
            st.write("### Business Information")
            st.markdown(f"**Business Name:** {insights.business_name}")
            st.markdown(f"**Category:** {insights.category}")
            st.markdown(f"**Website:** [{insights.website}]({insights.website})")
            st.markdown(f"**Business Email:** {insights.contact_email}")
            st.markdown(f"**Contact Phone:** {insights.contact_phone}")
        
    elif section == "Products":
        st.header("Products")
        def create_product():
            st.write("### Create a Product")

            product_name = st.text_input("Product Name")
            product_description = st.text_area("Product Description")
            product_price = st.number_input("Product Price", min_value=0.0, step=0.01)
            available_stock = st.number_input("Available Stock", min_value=0, step=1)

            if st.button("Add Product"):
                if product_name and product_description and product_price:
                    success = backend.create_product(backend.get_bussiness_id(user_profile["user_id"]), product_name, product_price, product_description, available_stock)
                    if success:
                        st.success("Product added successfully!")
                    else:
                        st.error("Failed to add product.")
                else:
                    st.error("Please fill in all fields and upload an image.")

        def list_products():
            st.write("### Your Products")
            products = backend.get_products(backend.get_bussiness_id(user_profile["user_id"]))
            if not products:
                st.write("No products found.")
            else:
                for product in products:
                    st.markdown(f"**Product Name:** {product.product_name}")
                    st.markdown(f"**Description:** {product.description}")
                    st.markdown(f"**Price:** ${product.price}")
                    st.markdown(f"**Available Stock:** ${product.available_stock}")
                    st.markdown("---")

        create_product()
        list_products()
    
    elif section == "Advertisements":
        def display_advertisements():
            st.write("### Advertisements")

            ads = backend.get_ads(backend.get_bussiness_id(user_profile["user_id"]))
            if not ads:
                st.write("No advertisements found.")
            else:
                for ad in ads:
                    st.markdown(f"### Ad ID: {ad.ad_id}")
                    st.markdown(f"**Product Name:** {backend.get_product_name(ad.ad_id)}")
                    st.markdown(f"**Created At:** {ad.created_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.markdown(f"**Target_audience :** {ad.target_audience}")
                    st.markdown(f"**Start - End dates :** {ad.start_date} - {ad.end_date}")

                    # Display insights
                    insights = backend.ad_insights(ad.ad_id)
                    st.markdown("#### Insights")
                    st.markdown(f"**Views Count:** {insights.views_count}")
                    st.markdown(f"**Clicks Count:** {insights.clicks_count}")
                    st.markdown(f"**Impressions:** {insights.impressions}")
                    st.markdown(f"**Engagement Rate:** {insights.engagement_rate}%")
                    st.markdown(f"**Cost Per Click:** ${insights.cost_per_click}")
                    st.markdown(f"**Cost Per Mille:** ${insights.cost_per_mille}")
                    st.markdown("---")

        display_advertisements()

if section == "Explore people":

    def display_people(people):
        for person in people:
            if person.user_id != user_profile["user_id"]:
                col1, col2, col3 = st.columns([1, 3, 6])
                with col1:
                    if person.profile_pic_path:
                        st.image(Image.open(person.profile_pic_path), width=50)
                    else:
                        st.write("No profile pic")
                with col2:
                    st.markdown(f"### {person.fname} {person.lname}")
                with col3:
                    st.markdown(f"**Bio:** {person.bio}")
                    st.markdown(f"**Email:** {person.email}")
                    st.markdown(f"User id: {person.user_id}")
                st.markdown("---")


    # box to follow a user using user_id
    user_id_to_follow = st.number_input("Enter User ID to Follow", min_value=1, step=1)
    if st.button("Follow User"):
        backend.follow(user_profile["user_id"], user_id_to_follow, datetime.datetime.now())
        st.success("User followed successfully!")
    
    # box to unfollow a user using user_id
    user_id_to_unfollow = st.number_input("Enter User ID to Unfollow", min_value=1, step=1)
    if st.button("Unfollow User"):
        backend.unfollow(user_profile["user_id"], user_id_to_unfollow)
        st.success("User unfollowed successfully!")

    # radio to show followers or following
    show_followers = st.radio("Show Followers or Following", ["Followers", "Following"])
    if show_followers == "Followers":
        st.write("### Followers")
        
        if backend.count_followers(user_profile["user_id"]) == 0:
            st.write("No followers yet.")
        else:
            people = backend.get_followers(user_profile["user_id"])
            display_people(people)
    else:
        st.write("### Following")
        if backend.count_following(user_profile["user_id"]) == 0:
            st.write("Not following anyone yet.")
        else:
            people = backend.get_following(user_profile["user_id"])
            display_people(people)

    st.write('---')
    st.header("Explore People")

    people = backend.get_all_users()
    display_people(people)