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
invalid_token = "icVpZnJlZCIsImV4cCI6MTU1ODY3"
expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJlaWZyZWQzM0BnbWFpbC5jb20iLCJleHAiOjE1NTQxOTYxMTd9.TAJa94Vvj7S_4nCDJqWGItbRBEsvpybM3Qc_Pp-NYwE"
