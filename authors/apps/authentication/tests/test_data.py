valid_user = {
    "username" : "henryjones",
    "email" : "hjones@email.com",
    "password" : "T35tingi2E"
}
valid_user2 ={
    "username" : "peter",
    "email" : "peter@email.com",
    "password" : "Pass1234"
}
valid_user3 ={
    "username" : "sapiens",
    "email" : "sapiens@email.com",
    "password" : "Pass1234_"
}

valid_user4 ={
    "username" : "Anorld",
    "email" : "anorld@email.com",
    "password" : "Pass1234__"
}
user_with_existing_email = {
    "username": "peter",
    "email" : "hjones@email.com",
    "password" : "T35tingi2E"
}
user_with_existing_username = {
    "username" : "henryjones",
    "email": "peter@email.com",
    "password": "T35tingi2E"
}
user_without_password = {
    "username": "henryjones",
    "email": "hjones@email.com"
}
user_without_username = {
    "email": "hjones@email.com",
    "password": "T35tingi2E"
}
user_without_email = {
    "username" : "henryjones",
    "password": "T35tingi2E"
}
user_with_little_password = {
    "username": "peter2",
    "email": "peter@gmail.com",
    "password": "Enter"
}
user_with_short_username = {
                "username": "pet",
                "email": "peter@email.com",
                "password": "Password8"
        }
user_with_a_non_numeric_password = {
                "username": "peter",
                "email": "peter@email.com",
                "password": "Password"
        }
username_with_special_characters = {
                "username": "peter.",
                "email": "peter@email.com",
                "password": "Password9"
        }
message = "username should be atleast 4 characters long and shouldnt contain special characters"
invalid_email = {
                "username": "peter",
                "email": "peter@.com",
                "password": "Password1"
        }
user_data_2 = {
            "username": "nicksbro",
            "email": "nicholus@gmail.com",
            "password": "Enter1234"
            }
invalid_token = "icVpZnJlZCIsImV4cCI6MTU1ODY3"
expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJlaWZyZWQzM0BnbWFpbC5jb20iLCJleHAiOjE1NTQxOTYxMTd9.TAJa94Vvj7S_4nCDJqWGItbRBEsvpybM3Qc_Pp-NYwE"
profiles = '/api/profiles/'