
################################### LIBRARY ###################################

import streamlit as st
from database import conn, userAuth
import pandas as pd
import streamlit_authenticator as stauth
from datetime import date

################################### PAGE CONFIG ###################################
st.set_page_config(page_title="Fadly's Food Diary", page_icon=":bar_chart:", layout="wide")
#hiding footer and hamburger menu~
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# --- USER AUTHENTICATION ---
users = userAuth.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
passwords = [user["password"] for user in users]

credentials = {"usernames":{}}
        
for uname,name,pwd in zip(usernames,names,passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})


authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")



################################### KEY FUNCTIONS #########################


utc_today = date.today()
today = utc_today.strftime("%m-%d-%Y")

def main_data():
    all_data = pd.json_normalize(conn.get_all_data())
    all_data = all_data.drop('key', axis=1)
    column_names = ['Day', 'Name', 'TimeOfDay', 'Meal', 'Calories', 'Notes']
    all_data=all_data[column_names]
    data = pd.DataFrame(all_data)
    return data


def show_user():
    user_list = pd.json_normalize(userAuth.fetch_all_users())
    user_list = user_list.drop('password', axis=1)
    final_user_list = user_list.rename(columns={'key':'User Name', 'name': 'Name'})
    return pd.DataFrame(final_user_list)
    
def user_list():
    user_list = pd.json_normalize(userAuth.fetch_all_users())
    list_user = user_list.drop('password', axis=1)
    list_user = list_user['key']
    return list_user.values.tolist()



    #### Form ####




#################################### FRONT END ####################################

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")


if authentication_status:


    home, admin = st.tabs(['Home', 'Admin'])

    with home:

        MEAL_TIME = ['','Breakfast', 'Lunch', 'Dinner', 'Snack']



        authenticator.logout("Logout", "sidebar")
        st.sidebar.title(f"Welcome {name}")
        st.title(f"{name}'s Food Diary :ramen:")




        data = main_data()
        user_data = data.loc[data['Name'] == f'{name}']
        st.subheader("View Food Dairy based on time of day")
        if len(user_data) > 0:
            st.table(user_data)
        else:
            st.warning("""It looks like you don't have any food logged yet """)






        with st.expander ("View Meal based on Meal Time"):

            meal_time = st.selectbox(label="Select Meal Time", options=MEAL_TIME)
            view_button = st.button('View')
            if view_button:
                view_data = main_data()
                get_meal = view_data[(view_data['TimeOfDay'] == meal_time) & (view_data['Name'] == name)]
                st.write(get_meal)

        with st.expander("Food Log"):

            with st.form(key="Data-Input", clear_on_submit=True):
                meal = st.text_input("Meal")
                time_of_day = st.selectbox("Select Meal Time", options=MEAL_TIME)
                calories = st.number_input("Enter Calories")
                notes = st.text_area("Notes")
                save_button = st.form_submit_button(label="Save Data")

                if save_button :
                    try:
                        st.spinner()
                        with st.spinner("Saving data to database :rocket :rocket :rocket :rocket"):
                            ## do post API to save data to Deta
                            conn.insert_data(time_of_day=time_of_day, meal=meal, calories=calories, notes=notes, name=name)

                            st.success("Data has been saved!")
                    except Exception as e:
                        st.error(e)
                        print(e)


    with admin:
        admin_password = st.text_input(label='Enter password')
        if admin_password == 'admin':
            with st.expander("View all user!"):
                st.table(show_user())
            with st.expander('Delete User'):
                del_user = st.text_input(label='User to delete', placeholder='Enter the name of user to delete')
                if del_user != '':
                    delete_button = st.button(key='delete-user', label='Delete User')
                    if delete_button:
                        userAuth.delete_user(username=del_user)
                        st.success(f'{del_user} is deleted from user list')
            
            with st.expander('Add New User'):
                with st.form(key='add_user', clear_on_submit=True):

                    u_name = st.text_input('Username')
                    nama = st.text_input('Full Name')
                    secrets = st.text_input('Password')
                    
                    save_user = st.form_submit_button('Save User')
                    
                    if save_user:
                        user_name_test=[u_name]
                        names=[nama]
                        passwords=[secrets]
                        hashed_passwords = stauth.Hasher(passwords).generate() 

                        
                        for (username, name, hash_password) in zip(user_name_test, names, hashed_passwords):
                            userAuth.insert_user(username, name, hash_password)
                            st.success(f'{u_name} has been added')

            with st.expander('Update User'):
                user_data_final = user_list()
                user_data_final.insert(0,'')

                select_user = st.selectbox(label='Select User', options=user_data_final)
                if select_user != '':
                    update = st.text_input('Update Name')
                    if update != '':
                        updates = {"name": update,
                                    "password": pwd}
                        userAuth.update_user(username=select_user, updates=updates)
                        st.success(f'{select_user} data has been updated')



             
        if admin_password != 'admin':
            st.info('Please enter the correct password')

            

    