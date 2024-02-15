#eixe skopo na kanei test den xrhsimopoihthike telika        
def receiveData(json_data):
    data_type = list(json_data.keys())[0] 
    match data_type:
        case "cred_sign_in":
            print(1)
        case "cred_sign_up":
            print(2)
        case "game_data":
            pass
        
data_to_server = {
    "cred_sign_in": {
        "username": "your_username",
        "password": "your_password"
    }
}            
receiveData(data_to_server)