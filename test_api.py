from fastapi import FastAPI, HTTPException, Header
import uvicorn
import pandas as pd

# Bikin instance untuk menangkap REST API (Fast API)
dewa = FastAPI()

# --reload = while True, akan terus dijalankan

# Endpoint Utama (API cuma bisa baca dictionary)
# @dewa.get("/") # Setara dengan 127:0.0.1:8000/ atau localhost:8000/
# def home():
#     return {"message": "Hello World! This is my first API",
#             "menu":{1:"/students",
#                      2:"/players",
#                      3:"/shopping_cart"}}



####################Load From JSON####################
students_data = {
    "Joni":{
        "shoe_size":44,
        "fav_color":"Black"
    },
    "Salsa":{
        "shoe_size":39,
        "fav_color":"White"
    },
    "Dewa":{
        "show_size":42,
        "fav_color":"Green"
    }

}

# Endpoint Students
@dewa.get("/students")
def students():
    return {"message":"Ini merupakan API untuk menampilkan, menambah, mengedit, dan menghapus data siswa",
            "menu":{
                1:"/data",
                2:"/find_students/{name}",
                3:"/add_students",
                4:"/update_student/{name}",
                5:"/delete_students/{name}"
            }}

# Endpoint menampilkan semua data
@dewa.get("/students/data")
def std_data():
    return students_data

# Endpoint menambah data siswa
@dewa.post("/students/add_student")
def add_std(student_data:dict):
    # Untuk menambahkan print pesan dalam terminal
    print(f"Student Data {student_data}")
    # Untuk menambahkan data dalam dictionary
    student_name = student_data["name"]
    student_shoe_size = student_data["shoe_size"]
    student_fav_color = student_data["fav_color"]
    student_data[student_name] = {
        "shoe_size":student_shoe_size,
        "fav_color":student_fav_color
    }

    # Menambahkan pesan dalam tampilan API
    return {"message":f"Student {student_name} succesfully added!"}


@dewa.get("/students/find_student/{name}")
def find_student(name:str):
    # Kondisional/Pengecekan Apakah nama siswa ada dalam data?
    if name in students_data.keys():
        return {name:students_data[name]}
    else:
        raise HTTPException(status_code=404, detail="Student Not Found!")


# Endpoint untuk update/edit data
@dewa.put("/students/update_student/{name}")
def put_std(name:str, student_data):
    # Kondisional/Pengecekan. Apakah nama siswa ada dalam data?
    if name not in students_data.keys():
        raise HTTPException(status_code=404, detail=f"Student {name} not found")
    else:
        # Assign variable value dari hasil slicing dictionary students_data dalam student_data
        students_data[name] = student_data
        # Menampilkan pesan dalam API
        return {"message":f"Students {name} has been updated"}


# Endpoint untuk hapus data siswa
@dewa.delete("/students/delete_student/{name}")
def del_std(name:str):
    if name in students_data.keys():
        # Hapus data siswa berdasarkan hasil slicing dictionary
        del students_data[name]
        return {"message":f"Student data {name} has been deleted!"}
    else:
        raise HTTPException(status_code=404, detail= f"Student {name} not found")

# HTTP hanya untuk method GET saja
# Swagger UI untuk dapat digunakan untuk selain GET


####################Load From CSV#####################
# Load data disimpan dalam variable horse
horse = pd.read_csv("horse_clean.csv")

# Endpoint home horse
@dewa.get("/") # Setara dengan 127:0.0.1:8000/ atau localhost:8000/
def home():
    return {"message": "Hello World! This is my first API",
            "menu":{1:"/horses",
                     2:"/players",
                     3:"/shopping_cart"}}

@dewa.get("/horses")
def kandang():
    return {"message":"Selamat datang di submenu perkudaan hewan paling keren!",
            "menu":{
                1:"Get all horses (/horses/data)",
                2:"Filter by surgery (/horses/surgery/{surge})",
                3:"Filter by outcome (/horses/outcome/{horse_outcome})",
                4:"Delete one of horse data by Unnamed: 0 *Sad :'( (/horses/del/{id})"
            }
            }

# Endpoint show horses data
@dewa.get("/horses/data")
def kuda():
    return horse.to_dict(orient="records")


# Endpoint filter by surgery
@dewa.get("/horses/surgery/{surgery_type}")
def operasi(surgery_type:str):
    # Menyimpan hasil slicing dalam variable baru, menggunakan bracket method
    horse_surgery = horse[horse["surgery"]==surgery_type]
    # Return hasil slicing
    return horse_surgery.to_dict(orient="records")


# Endpoint filter by outcome
@dewa.get("/horses/outcome/{outcome_type}")
def outcome(outcome_type:str):
    # Menyimpan hasil slicing dalam variable baru, menggunakan bracket method
    horse_outcome = horse[horse["outcome"]==outcome_type]
    # Return hasil slicing
    return horse_outcome.to_dict(orient="records")


# API Key (Password) --> (Buat menjadi variabel global)
API_KEY = "admin1234"

# Endpoint hapus data menggunakan akses api key
@dewa.delete("/horses/del/{id}")

def hapus(id:int, api_key:str=Header(None)): # Memasang API Key dalam Header dengan default value None
    # Menunjukan value API Key dalam terminal
    print(api_key)

    # Conditional pengecekan API Key
    if api_key == None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key masih kosong atau salah")
    # Kalau API Key bener
    else:
        # Pengecekan kondisi apakah id ada dalam kolom Unnamed: 0
        if id not in horse["Unnamed: 0"].values:
            raise HTTPException(status_code=404, detail=f"Horse with id {id} didnot found")
        # Kalau ketemu/ada
        else:
            horse.drop(horse[horse["Unnamed: 0"] == id].index, inplace=True)
            return {"message":f"Horse with id {id} is successfully deleted!"}





######################################################
######################################################
######################################################

cart = {"name": "shopping cart",
        "columns": ["prod_name", "price", "num_items"],
        "items": {}}


@dewa.get("/shopping_cart")
def root():
    return {"message": "Welcome to Toko H8 Shopping Cart! There are some features that you can explore",
            "menu": {1: "See shopping cart (/shopping_cart/cart)",
                     2: "Add item (/shopping_cart/add)",
                     3: "Edit shopping cart (/shopping_cart/edit/{id})",
                     4: "Delete item from shopping cart (/shopping_cart/del/{id})",
                     5: "Calculate total price (/shopping_cart/total)",
                     6: "Exit (/shopping_cart/exit)"}
            }


@dewa.get("/shopping_cart/cart")
def show():
    return cart


@dewa.post("/shopping_cart/add")
def add_item(added_item: dict):
    id = len(cart["items"].keys()) + 1
    cart["items"][id] = added_item
    return f"Item successfully added into your cart with ID {id}"


@dewa.put("/shopping_cart/edit/{id}")
def update_cart(id: int, updated_cart: dict):
    if id not in cart['items'].keys():
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    else:
        cart["items"][id].update(updated_cart)
        return {"message": f"Item with ID {id} has been updated successfully."}


@dewa.delete("/shopping_cart/del/{id}")
def remove_row(id: int):
    if id not in cart['items'].keys():
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    else:
        cart["items"].pop(id)
        return {"message": f"Item with ID {id} has been deleted successfully."}


@dewa.get("/shopping_cart/total")
def get_total():
    total_price = sum(item["price"] * item["num_items"] for item in cart["items"].values())
    return {"total_price": total_price}


@dewa.get("/shopping_cart/exit")
def exit():
    return {"message": "Thank you for using Toko H8 Shopping Cart! See you next time."}

if __name__ == "__main__":
    uvicorn.run("test_api:dewa", host="127.0.0.1", port=8000, reload=True)