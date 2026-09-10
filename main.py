import pandas as pd

dataframe = pd.read_csv('hotels.csv', dtype={'id': str})

card_df = pd.read_csv('cards.csv', dtype=str).to_dict(orient='records')

secure_credit_card_df = pd.read_csv('card_security.csv', dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = dataframe.loc[dataframe["id"] == self.hotel_id , "name"].squeeze()

    def book(self):
        """ Book a hotel by changing its availability to no"""
        dataframe.loc[dataframe['id'] == self.hotel_id, 'available'] = 'no'
        dataframe.to_csv('hotels.csv', index=False)

    def availability(self):
        """ check hotel availability"""
        availability = dataframe.loc[dataframe['id'] == self.hotel_id, 'available'].squeeze()
        if availability == 'yes':
            return True
        else: 
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
         Thank you for your reservation!
         Hera are your booking data:
            Name: {self.customer_name}
            Hotel name: {self.hotel.name}
        """

        return content
    
class CreditCard:
    def __init__(self, card_number):
        self.number = card_number 

    def validate(self, expiration_date, cvc, holder_name):
        validate_data = {
            'number': self.number,
            'expiration': expiration_date,
            'cvc': cvc,
            'holder': holder_name }  

        if validate_data in card_df:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
       password = secure_credit_card_df.loc[secure_credit_card_df['number'] == self.number, 'password'].squeeze()
       if password == given_password:
           return True
       else:
           return False 


hotel_id = input("Enter the hotel id you want to book:")
hotel = Hotel(hotel_id)

if hotel.availability():
    credit_card = SecureCreditCard(card_number="1234567890123456")
    if credit_card.authenticate(given_password="mypass"):
        validate = credit_card.validate(expiration_date="12/26", cvc="123", holder_name="JOHN SMITH")
        if validate:
            customer_name = input("Enter your name:")
            ticket = ReservationTicket(customer_name, hotel)
            print(ticket.generate())
            hotel.book()
        else:
            print("Invalid credit card detials. Please check your card information and try again.")
    else:
        print("Authentication failed. Please check your password and try again.")        
else:
    print("Sorry, the hotel is not available for booking.")    
