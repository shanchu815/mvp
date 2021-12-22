from flask import Flask, request, render_template, jsonify, redirect, url_for
from model import connect_to_db
import crud
# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'W33d1sl33t1845!'

@app.route('/')
def start_here():
    """Home page."""

    return render_template("homepage.html")

@app.route("/disclaimer")
def show_disclaimer():
    """Shows the disclaimer."""

    return render_template("disclaimer.html")

@app.route("/calculator")
def calculate():
    """Shows the protein calculator page."""

    return render_template("calculator.html")

@app.route("/fillout")
def fill_out():
    """Shows the fillout form"""

    return render_template("fillout.html")

@app.route("/save-list", methods = ['POST'])
def save_choices():
    """Saves the chosen form options as a new food object"""

    product_name = request.form.get("product_name")
    descriptor = request.form.get("descriptor")
    ingredient_name = request.form.get("ingredient_name")
    grain = request.form.get("grains")
    additive = request.form.get("additives")
    protein = request.form.get("proteins")
    preservative = request.form.get("preservatives")

    new_food = crud.create_food(product_name)
    ingredient_type = crud.get_ingredient_by_combo(ingredient_name, descriptor)
    grain_type = crud.get_grain_by_id(grain)
    additive_type = crud.get_additive_by_id(additive)
    protein_type = crud.get_protein_by_id(protein)
    preservative_type = crud.get_preservative_by_id(preservative)

    new_food_ingredient = crud.create_food_ingredient(new_food, ingredient_type, 
                                                    grain_type, additive_type, 
                                                    protein_type, preservative_type)

    return redirect(url_for('/results/') + new_food.food_id)

@app.route('/results/<food_id>')
def show_result(food_id):
    """Displays the choices as a result page"""
    
    if food_id not in db.pet_food:
        return "Invalid id"
    else:
        return render_template("results.html", ingredients = db.pet_food[food_id])
#ask Sean how do i call the pet_food db here

if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads"
    # our web app if we change the code.
    app.run(debug=True, host="0.0.0.0")
