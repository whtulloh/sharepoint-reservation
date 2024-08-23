import os
import json
import office365
import datetime
import random
import sys
from datetime import datetime, timedelta
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.listitems.listitem import ListItem
from config import spo_base_url, spo_client_id, spo_client_secret, spo_file_names, spo_account_status, spo_checkin_days, spo_checkout_days

class SharePointService:
    def __init__(self):
        self.title = spo_file_names
        self.status_provisioned = spo_account_status

    def get_all_sharepoint_user(self):
        try:
            client_credentials = ClientCredential(spo_client_id, spo_client_secret)    
            ctx = ClientContext(spo_base_url).with_credentials(client_credentials)
            list_items = ctx.web.lists.get_by_title(self.title)
            
            include_fields = ["Title","LastName","UserName","AccountNumber","UserRegion","checkin","checkout","HotelName"]
            filter_text = "Status eq %27"+ self.status_provisioned +"%27"
            
            self.item = list_items.items.select(include_fields).filter(filter_text).paged(5000).get().execute_query()
            if len(self.item) == 0:
                sys.exit()
            
            return self.item
        except SystemExit:
            return "Error SharePoint API response: email not found"
        except:
            return "Error SharePoint API response: something went horribly wrong"

    def get_sharepoint_user(self, accNumber):
        try:
            client_credentials = ClientCredential(spo_client_id, spo_client_secret)    
            ctx = ClientContext(spo_base_url).with_credentials(client_credentials)
            list_items = ctx.web.lists.get_by_title(self.title)
            
            include_fields = ["Title","LastName","UserName","AccountNumber","UserRegion","checkin","checkout","HotelName"]
            filter_text = "AccountNumber eq %27"+ accNumber +"%27"
            
            self.item = list_items.items.select(include_fields).filter(filter_text).get().execute_query()
            if len(self.item) == 0:
                sys.exit()
            
            return self.item
        except SystemExit:
            #Account Number = Reservation Number
            return "Error SharePoint API response: Reservation Number not found"
        except:
            return "Error SharePoint API response: something went horribly wrong"
    
    def update_sharepoint_user(self, accNumber, demo):
        try:
            data = json.loads(demo)["data"]
            client_credentials = ClientCredential(spo_client_id, spo_client_secret)    
            ctx = ClientContext(spo_base_url).with_credentials(client_credentials)
            list_items = ctx.web.lists.get_by_title(self.title)

            filter_text = "AccountNumber eq %27"+ accNumber +"%27"
            
            items = list_items.items.filter(filter_text).get().execute_query()
            if len(items) == 0:
                sys.exit()

            self.item_to_update = items[0]
            if data['checkin']:
                self.item_to_update.set_property("checkin", f"{data['checkin']}").update().execute_query()
            if data['checkout']:
                self.item_to_update.set_property("checkout", f"{data['checkout']}").update().execute_query()
            if data['hotelname']:
                self.item_to_update.set_property("HotelName", f"{data['hotelname']}").update().execute_query()
            
            return True
        except SystemExit:
            #Account Number = Reservation Number
            return "Error SharePoint API response: Reservation Number not found"
        except:
            return "Error SharePoint API response: something went horribly wrong"

def get_all_user():
    try:
        spo = SharePointService()
        sp_user = spo.get_all_sharepoint_user()

        print(sp_user)

        if type(sp_user) != str:
            users = []

            for index, item in enumerate(sp_user):
                username = item.properties['UserName']
                accountnumber = item.properties['AccountNumber']
                checkin = item.properties['checkin']
                checkout = item.properties['checkout']
                hotelname = item.properties['HotelName']

                if not username:
                    return {'error': "get_all_user: username for "+email+" not found"}
                elif not checkin:
                    return {'error': "get_user: checkin for "+email+" not found"}
                elif not checkout:
                    return {'error': "get_user: checkout for "+email+" not found"}
                elif not hotelname:
                    return {'error': "get_user: hotelname for "+email+" not found"}
                elif not accountnumber:
                    return {'error': "get_user: accountnumber for "+email+" not found"}
                else:
                    newdata = {                       
                        "username": username,
                        "checkin" : checkin,
                        "checkout" : checkout,
                        "hotelname" : hotelname,
                        "accountnumber": accountnumber     
                    }
                    users.append(newdata)

            data = {'data' : users}
            return (data)

        else:
            sys.exit()
    except SystemExit:
        return {'error': sp_user}
    except Exception as e:
        return {'error': "Error generating get_all_user response: " + str(e)}

def get_user(accNumber):
    try:
        spo = SharePointService()
        sp_user = spo.get_sharepoint_user(accNumber)

        if type(sp_user) != str:

            for index, item in enumerate(sp_user):
                username = item.properties['UserName']
                checkin = item.properties['checkin']
                checkout = item.properties['checkout']
                hotelname = item.properties['HotelName']
            
            if not username:
                return {'error': "get_user: username for "+accNumber+" not found"}
            elif not checkin:
                return {'error': "get_user: checkin for "+accNumber+" not found"}
            elif not checkout:
                return {'error': "get_user: checkout for "+accNumber+" not found"}
            elif not hotelname:
                return {'error': "get_user: hotelname for "+accNumber+" not found"}
            else:
                data = {
                    "data" : {
                        "username": username,
                        "reservation_number": accNumber,
                        "checkin": checkin,
                        "checkout" : checkout,
                        "hotelname" : hotelname
                    }
                }
                return (data)

        else:
            sys.exit()
    except SystemExit:
        return {'error': sp_user}
    except Exception as e:
        return {'error': "Error generating get_user response: " + str(e)}

def generate_demo_reservation():
    try:
        # Check in date: this should be (current date + 5 days)
        # Check out date: (current date + 10 days)
        checkinDate = datetime.today() + timedelta(int(spo_checkin_days))
        checkoutDate = datetime.today() + timedelta(int(spo_checkout_days))

        data = {
            "data" : {
                "checkin" : checkinDate.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "checkout" : checkoutDate.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }

        return (data)
    except Exception as e:
        return {'error': "Error generating generate_demo_reservation response: " + str(e)}

def update_user(accNumber, request_data=""):
    try:
        if not request_data:
            data = generate_demo_reservation()
        else:
            req = json.loads(request_data)

            HotelName = ""
            checkinDate = ""
            checkoutDate = ""
            
            if 'checkin' in req:
                checkinDate = datetime.strptime(req["checkin"], "%Y-%m-%dT%H:%M:%SZ") 
                checkinDate = checkinDate.strftime("%Y-%m-%dT%H:%M:%SZ")
            if 'checkout' in req:
                checkoutDate = datetime.strptime(req["checkout"], "%Y-%m-%dT%H:%M:%SZ")
                checkoutDate = checkoutDate.strftime("%Y-%m-%dT%H:%M:%SZ")
            if 'hotelname' in req: 
                HotelName = req["hotelname"]

            data = {
                "data" : {
                    "checkin" : checkinDate,
                    "checkout" : checkoutDate,
                    "hotelname" : HotelName
                }
            }
        
        spo = SharePointService()
        sp_user = spo.update_sharepoint_user(accNumber, json.dumps(data))

        if type(sp_user) != str:
            data = {
                "data" : {
                    "reservation_number": accNumber,
                    "status" : "Update successfull",
                }
            }
            return (data)
        else:
            sys.exit()
    except SystemExit:
        return {'error': sp_user}
    except Exception as e:
        return {'error': "Error generating update_user response: " + str(e)}