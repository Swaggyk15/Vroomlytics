import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import joblib

#due to having previous issues with mapping of values, ai suggested I use reverse mappings
#and so for the prupose of the gui to function succesfully, the reversed maps had to be loaded in:
fuel_mapping = pd.read_csv('maps/fuel_mapping.csv').set_index('fuel_type')['fuel_encoded'].to_dict()
transmission_mapping = pd.read_csv('maps/transmission_mapping.csv').set_index('transmission')['transmission_encoded'].to_dict()

#similarly, I then loaded the cleaned data
data = pd.read_csv('cleaned_used_cars.csv')

#the model was then set to the price predictor model developed in the price_predictor.py file
model = joblib.load('price_model.pkl')

#mappings were then loaded for each field and the following code was given by ai:
brand_mapping = pd.read_csv('maps/brand_mapping.csv').set_index('original_brand')['brand_encoded'].to_dict()
model_mapping = pd.read_csv('maps/model_mapping.csv').set_index('original_model')['model_encoded'].to_dict()

#to dipslay model names, ai also generated code for displaying the reverse mappings:
model_mapping_reverse = {v: k for k, v in model_mapping.items()}

#I then loaded the fuel type and tranmsission mappings as I needed them for the gui
fuel_mapping_reverse = pd.read_csv('maps/fuel_mapping.csv').set_index('fuel_encoded')['fuel_type'].to_dict()
transmission_mapping_reverse = pd.read_csv('maps/transmission_mapping.csv').set_index('transmission_encoded')['transmission'].to_dict()


#Create a dictionary to dynamically update dropdowns based on model selection
#I wanted to have it so the liters, cylinders, fuel_type, and transmission automatically
#update when the user selects both a brand a model name (as they can be derived from just these two).
#Therefore, I used a dictionary to dynamically update dropdowns based on model selection.
model_details_dict = {}
#go throw each row
for _, row in data.iterrows():
    model_key = row['model']
    if model_key not in model_details_dict:
        #update liters, cylinder, fuel_type, and transmission based on model selected
        model_details_dict[model_key] = {
            'liters': set(),
            'cylinders': set(),
            'fuel_type': set(),
            'transmission': set()
        }
    #finally, ensure the dictionary saves these values for each row:
    model_details_dict[model_key]['liters'].add(row['liters'])
    model_details_dict[model_key]['cylinders'].add(row['cylinders'])
    model_details_dict[model_key]['fuel_type'].add(row['fuel_type'])
    model_details_dict[model_key]['transmission'].add(row['transmission'])


#to ensure that the saved disctioanry values could be used for dropdowns, I had to convert
#the sets to lists as the gui only allowed for lists to be used for the prupose of dropdowns
for key in model_details_dict:
    model_details_dict[key]['liters'] = list(model_details_dict[key]['liters'])
    model_details_dict[key]['cylinders'] = list(model_details_dict[key]['cylinders'])
    model_details_dict[key]['fuel_type'] = list(model_details_dict[key]['fuel_type'])
    model_details_dict[key]['transmission'] = list(model_details_dict[key]['transmission'])

#I then had to initialize the tkinter window so all the widgets can fit within in
root = tk.Tk()
root.title("Vroomlytics")
#this size is more than enough for all the widgets and also so the user can easily see the gui
root.geometry("450x700")

#I then created variables for the dropdowns and entries so that way they can be used for presenting
#and updating the information in dropdowns.
brand_var = tk.StringVar()
model_var = tk.StringVar()
liters_var = tk.StringVar()
cylinders_var = tk.StringVar()
fuel_var = tk.StringVar()
transmission_var = tk.StringVar()
year_entry_var = tk.StringVar()
mileage_entry_var = tk.StringVar()
accident_var = tk.StringVar()  
clean_title_var = tk.StringVar() 

#In order to make the gui easier to use, I initially had it where the user has to select their brand of car
#and then also select the model name (but they had to scroll through all model names of every brand).
#Evidently, this was very time consuming for the user, so I wanted to update the model name dropdown, 
#that way whenever the user selects the brand name, only the possible model names relate to that brand show
#up in the drop down (honestly was inspired by autotrader lol!).
#Due to this, as I had no experience with dropdowns and dynamically updating them with mappings, ai
#provided the following code:
def update_model_dropdown(*args):
    """Update the model dropdown based on the selected brand."""
    selected_brand = brand_var.get()
    if selected_brand:
        # Get the brand code using the brand mapping
        brand_code = brand_mapping.get(selected_brand)

        # Filter models directly from the dataset based on the selected brand
        filtered_models = data[data['brand'] == brand_code]['model'].unique()

        # Convert the numerical model codes to the original model names using the reverse mapping
        model_names = [model_mapping_reverse.get(model_code, str(model_code)) for model_code in filtered_models]
        model_combobox['values'] = model_names
        model_var.set('')  # Clear the current selection

#When I tested the gui at first, blanks and unkowns were left as 999 which I thought would confuse
#the user as for example, lets say they chose a model name that did not have data for cylinders it would 
#display as "Cylinders: 999" which would like very incorrect (having 999 cylinders would be crazy lol).
#So as a result, I made values with 999 display as "N/A" so the user knows that the value for that data is 
#not available within the used_cars.csv dataset
def format_value(value):
    return "N/A" if value == '999' else value

#Similar to the model update dropdown, this time around I wanted the gui to display the udpated
#information of the liters, cylinders, fuel type, and tranmission when the user selected the model.
#And so a result of studying how to do the update for the model, I was able to write some 
#of the following code, but did need assitance with fuel_menu and transmission_menu code which
#were generated by ai (I marked which lines they were):
def update_details_dropdown(*args):
    selected_model = model_var.get()
    
    #model names converted to numerical values, Ex: Ford = 14
    model_code = model_mapping.get(selected_model)
    
    #if model_code (the numerical value) is found within the dictioanry of all features, then we 
    #need to dynamically update the details/features pertaining to that specific car model
    if model_code in model_details_dict:
        details = model_details_dict[model_code]

        #liters dropwdown gets updated but had to be kept as a float, since they are commonly
        #represented as floats
        liters_menu['values'] = [format_value(f) for f in details['liters']]
        if details['liters']:
            liters_var.set(format_value(details['liters'][0]))

        #cylinders dropdown gets updated but had to be converted into int values
        cylinders_menu['values'] = [format_value(int(c)) for c in details['cylinders']]
        if details['cylinders']:
            cylinders_var.set(format_value(int(details['cylinders'][0])))

        #AI GENERATED: Update Fuel Type dropdown (convert to original strings using reverse mapping)
        fuel_menu['values'] = [format_value(fuel_mapping_reverse[int(f)]) for f in details['fuel_type'] if int(f) in fuel_mapping_reverse]
        if details['fuel_type']:
            fuel_var.set(format_value(fuel_mapping_reverse[int(details['fuel_type'][0])]))

        #AI GENERATED: Update Transmission dropdown (convert to original strings using reverse mapping)
        transmission_menu['values'] = [format_value(transmission_mapping_reverse[int(t)]) for t in details['transmission'] if int(t) in transmission_mapping_reverse]
        if details['transmission']:
            transmission_var.set(format_value(transmission_mapping_reverse[int(details['transmission'][0])]))
    else:
        #In the case that there were no details found, all dropdowns need to be cleared

        #Note: Although with my dataset this was not possible, I made sure to include it in case
        #I were to try this program with a larger and similar dataset in the future.
        liters_menu['values'] = []
        cylinders_menu['values'] = []
        fuel_menu['values'] = []
        transmission_menu['values'] = []
        liters_var.set('')
        cylinders_var.set('')
        fuel_var.set('')
        transmission_var.set('')



#again, here I developed a function to ensure that values of 999 or 999.0 showed up as "N/A"
#as not only did it look inaccurate, but it also have me issues during testing and so this step
#was necessary to avoid such issues. 
def format_value(value):
    if isinstance(value, str):
        return value
    return "N/A" if value == 999 or value == 999.0 else value


#When testing the gui at first, I realized that I had to maunually exit the program if I wanted to try
#the prediction on a differnet brand/car. I then decided to add a reset button to help clear everything
#and make it easier for the user to select another car without having to exit the program every time.
def reset_fields():
    
    #brand and model get reset to default 
    brand_var.set('')
    model_var.set('')

    #this line of my code was ai generated, as I did not know that I needed a combobox to then reset 
    #values back to their default:
    model_combobox['values'] = []
    
    #similaryly, so do the other features
    liters_var.set('')
    cylinders_var.set('')
    fuel_var.set('')
    transmission_var.set('')
    liters_menu['values'] = []
    cylinders_menu['values'] = []
    fuel_menu['values'] = []
    transmission_menu['values'] = []
    
    #year and mileage entry get resetted as well
    year_entry_var.set('')
    mileage_entry_var.set('')
    
    #similarly, so does the result_label since there is no prediction cost to display
    result_label.config(text="")


#I then needed to create a predict_price function so that way when a user clicks on the "Predict Price"
#button, it will then call this function to handle such predctions.
def predict_price():
    try:
        #if any features/details are missing, the model I created won't be able to predict as it needs
        #all information and so I added a quick check to make sure that this does not happen if the 
        #user were to try testing with missing information (Ex: user does not enter a year and tries to test)
        if not (brand_var.get() and model_var.get() and year_entry_var.get() and mileage_entry_var.get() and 
                accident_var.get() and clean_title_var.get()):
            messagebox.showerror("Error, please make sure all details have been entered!")
            return

        #I then had to create input handlers for all attributes to then connect them to their 
        #encoded labels (numerical values) via mapping.
        brand = brand_var.get()
        model_name = model_var.get()
        model_year = int(year_entry_var.get())
        mileage = int(mileage_entry_var.get())

        #for both liters and cylinders, I had to ensure that I handled the 999 cases and I developed
        #the following code:
        liters = liters_var.get()
        liters = 999.0 if liters == "N/A" else float(liters)
        
        cylinders = cylinders_var.get()
        cylinders = 999 if cylinders == "N/A" else int(cylinders)
        
        fuel_type = fuel_var.get()
        transmission = transmission_var.get()
        accident = accident_var.get()
        clean_title = clean_title_var.get()

        #so for this part, I had to each field back to their encoded values so the regression
        #model could then use the numerical data to then predict the price
        
        brand_encoded = brand_mapping.get(brand, -1)
        model_encoded = model_mapping.get(model_name, -1)
        fuel_encoded = fuel_mapping.get(fuel_type, -1) if fuel_type != "N/A" else 999

        #for the transmission encoding, the following code was generated:
        transmission_encoded = transmission_mapping.get(transmission, -1) if transmission != "N/A" else 999
        
        #similar to my conversion of when I cleaned the data in cleaner.py, I followed 
        #the same concept here:
        accident_encoded = 1 if accident == "At least 1" else 0
        clean_title_encoded = 1 if clean_title == "Yes" else 0
        

        #the following if statement was ai generated (ai suggested I include this in case I would 
        #like to try this program with a larger dataset in the future):
        # Check if any encoded value is invalid
        if brand_encoded == -1 or model_encoded == -1:
            messagebox.showerror("Error", "Invalid brand or model.")
            return

        #after receiving the encoded values, I then had to store the encoded information, and so
        #using a dictionary (input_data) was convenient for this. 
        input_data = pd.DataFrame({
            'brand': [brand_encoded],
            'model': [model_encoded],
            'model_year': [model_year],
            'mileage': [mileage],
            'fuel_type': [fuel_encoded],
            'liters': [liters],
            'cylinders': [cylinders],
            'transmission': [transmission_encoded],
            'accident': [accident_encoded],
            'clean_title': [clean_title_encoded]
        })

        #I then passed the model the encoded (numerical) data so it can predict the price
        price_prediction = model.predict(input_data)[0]
        result_label.config(text=f"Predicted price: ${price_prediction:,.2f}")

    #I also made sure to include erros in case the user were to enter in any information 
    #that cannot be encoded properly (Ex: say the user types in a string for the model year/mileage,
    #then an error message displays to let them know)
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))



#I wanted the gui to look nicer and so I implemented my own image (from the web) as the background
#Note: the "images" folder has the image I used
bg_image = Image.open("./images/purps.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
canvas = tk.Canvas(root, width=450, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

#using tkinter was differnet than when I used css as the display for widgets and buttons had to be on
#their own frame, and so I had to create a frame for the widgets.
frame = tk.Frame(canvas, bg='')
frame.place(relx=0.5, rely=0.5, anchor='center')

#I then had ai generate me a function that creates placeholder text so the user can see what 
#to enter in each field. Hence, the following function is ai generated:

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(foreground='grey')
    
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, 'end')
            entry.config(foreground='black')
    
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(foreground='grey')
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

#next, I had to create labels for all attributes/features and then add the widgets onto the center frame
#Note: I also made sure to include the updated values for each drop down, that way when the user selects the
#car brand, then the model dropdown gets updated -> and so the the other features after that!
ttk.Label(frame, text="Brand:").grid(row=0, column=0)
brand_combobox = ttk.Combobox(frame, textvariable=brand_var, values=list(brand_mapping.keys()))
brand_combobox.grid(row=0, column=1)
brand_combobox.bind("<<ComboboxSelected>>", update_model_dropdown)

ttk.Label(frame, text="Model:").grid(row=1, column=0)
model_combobox = ttk.Combobox(frame, textvariable=model_var)
model_combobox.grid(row=1, column=1)
model_combobox.bind("<<ComboboxSelected>>", update_details_dropdown)

ttk.Label(frame, text="Engine liters:").grid(row=2, column=0)
liters_menu = ttk.Combobox(frame, textvariable=liters_var)
liters_menu.grid(row=2, column=1)

ttk.Label(frame, text="Cylinders:").grid(row=3, column=0)
cylinders_menu = ttk.Combobox(frame, textvariable=cylinders_var)
cylinders_menu.grid(row=3, column=1)

ttk.Label(frame, text="Fuel type:").grid(row=4, column=0)
fuel_menu = ttk.Combobox(frame, textvariable=fuel_var)
fuel_menu.grid(row=4, column=1)

ttk.Label(frame, text="Transmission:").grid(row=5, column=0)
transmission_menu = ttk.Combobox(frame, textvariable=transmission_var)
transmission_menu.grid(row=5, column=1)

#no need for updates as the model year and mileage labels need the user to enter their own information:
year_label = ttk.Label(frame, text="Model year:")
year_label.grid(row=6, column=0)
year_entry = ttk.Entry(frame, textvariable=year_entry_var)
year_entry.grid(row=6, column=1)
#added a placeholder so the user knows exactly the format to enter in their information
add_placeholder(year_entry, "Ex: 2012")

mileage_label = ttk.Label(frame, text="Mileage:")
mileage_label.grid(row=7, column=0)
mileage_entry = ttk.Entry(frame, textvariable=mileage_entry_var)
mileage_entry.grid(row=7, column=1)
#similarly, added a placeholder for the proper mileage input
add_placeholder(mileage_entry, "Ex: 15000")

ttk.Label(frame, text="Accident history:").grid(row=8, column=0)
accident_menu = ttk.Combobox(frame, textvariable=accident_var, values=["None reported", "At least 1"])
accident_menu.grid(row=8, column=1)

ttk.Label(frame, text="Clean title:").grid(row=9, column=0)
clean_title_menu = ttk.Combobox(frame, textvariable=clean_title_var, values=["Yes", "No"])
clean_title_menu.grid(row=9, column=1)

predict_button = ttk.Button(frame, text="See predicted price", command=predict_price)
predict_button.grid(row=10, column=0, columnspan=2, pady=10)

reset_button = ttk.Button(frame, text="Reset", command=reset_fields)
reset_button.grid(row=11, column=0, columnspan=2, pady=10)

result_label = ttk.Label(frame, text="")
result_label.grid(row=12, column=0, columnspan=2)

root.mainloop()
