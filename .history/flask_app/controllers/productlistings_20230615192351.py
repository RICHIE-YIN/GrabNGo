from flask_app import app, render_template, redirect, session, request
from flask_app.models.productlisting import ProductListing

@app.route('/listings')
def listings():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('show_all_listings.html', listings = ProductListing.get_all())

@app.route('/listings/new')
def new_listing():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('create_listing.html')

@app.route('/listings/create', methods=['POST'])
def create_listing():
    if 'user_id' not in session:
        return redirect('/logout')
    if not ProductListing.validate_listing(request.form):
        return redirect('/listings/new')

    image_data = None
    if 'images' in request.files:
        image_file = request.files['images']
        if image_file.filename:
            image_data = image_file.read()

    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "price": float(request.form['price']),
        "itemcondition": request.form['itemcondition'],
        "category": request.form['category'],
        "location": request.form['location'],
        "zip": request.form['zip'],
        "city": request.form['city'],
        "state": request.form['state'],
        "status": "active",
        "user_id": session['user_id']
    }

    new_listing_id = ProductListing.save(data, image_data)
    return redirect(f'/listings/{new_listing_id}')


@app.route('/listings/<int:id>')
def show_listing(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': id}
    return render_template("view_one_listing.html", listing = ProductListing.get_one(data))

@app.route("/listings/<int:id>/edit")
def edit_listing(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': id}
    return render_template("edit_listing.html", listing = ProductListing.get_one(data))

@app.route('/listings/user/<int:user_id>')
def user_listings(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    listings = ProductListing.get_by_user(user_id)
    return render_template('user_listings.html', listings=listings)

@app.route('/listings/update', methods=["POST"])
def update_listing():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not ProductListing.validate_listing(request.form):
        return redirect(f"/listings/edit/{request.form['id']}")

    image_data = None
    if 'images' in request.files:
        image_file = request.files['images']
        if image_file.filename:
            image_data = image_file.read()

    data = {
        "id": request.form['id'],
        "title": request.form['title'],
        "description": request.form['description'],
        "price": float(request.form['price']),
        "itemcondition": request.form['itemcondition'],
        "category": request.form['category'],
        "location": request.form['location'],
        "zip": request.form['zip'],
        "city": request.form['city'],
        "state": request.form['state'],
        "status": request.form['status'],
    }

    ProductListing.update(data, image_data)
    return redirect(f'/listings/{request.form["id"]}')

@app.route('/listings/<int:id>/delete')
def delete_listing(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {'id': id}
    ProductListing.delete(data)
    return redirect('/listings')

@app.route('/listings/<int:id>/mark_as_sold')
def mark_item_as_sold(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': id}
    ProductListing.mark_as_sold(data)
    return redirect(f'/listings/{id}/select_buyer')
