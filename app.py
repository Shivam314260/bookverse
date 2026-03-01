from flask import Flask, request , Response ,session, url_for,redirect,render_template


app = Flask(__name__)

# ✅ Use SECRET_KEY from Vercel environment
app.secret_key = os.environ.get("SECRET_KEY")


# ✅ Universal DB Connection (Neon / Vercel)
def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route("/selfhelp")
def selfhelp():
    conn = get_db_connection()
    cur = conn.cursor()

    search = request.args.get("search")
    sort = request.args.get("sort")

    query = """
        SELECT book_id, title, author, price, image_url
        FROM books
        WHERE category_id = 2
    """

    params = []

    # 🔎 Search filter
    if search:
        query += " AND title ILIKE %s"
        params.append(f"%{search}%")

    # 🔄 Sorting
    if sort == "low":
        query += " ORDER BY price ASC"
    elif sort == "high":
        query += " ORDER BY price DESC"
    elif sort == "latest":
        query += " ORDER BY book_id DESC"

    cur.execute(query, params)
    books = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("selfhelp.html", books=books)

@app.route("/finance")
def finance():
    conn = get_db_connection()
    cur = conn.cursor()

    search = request.args.get("search")
    sort = request.args.get("sort")

    query = """
        SELECT book_id, title, author, price, image_url
        FROM books
        WHERE category_id = 3
    """

    params = []

    # 🔎 Search filter
    if search:
        query += " AND title ILIKE %s"
        params.append(f"%{search}%")

    # 🔄 Sorting
    if sort == "low":
        query += " ORDER BY price ASC"
    elif sort == "high":
        query += " ORDER BY price DESC"
    elif sort == "latest":
        query += " ORDER BY book_id DESC"

    cur.execute(query, params)
    books = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("finance.html", books=books)

@app.route("/business")
def business():
    conn = get_db_connection()
    cur = conn.cursor()

    search = request.args.get("search")
    sort = request.args.get("sort")

    query = """
        SELECT book_id, title, author, price, image_url
        FROM books
        WHERE category_id = 4
    """

    params = []

    # 🔎 Search filter
    if search:
        query += " AND title ILIKE %s"
        params.append(f"%{search}%")

    # 🔄 Sorting
    if sort == "low":
        query += " ORDER BY price ASC"
    elif sort == "high":
        query += " ORDER BY price DESC"
    elif sort == "latest":
        query += " ORDER BY book_id DESC"

    cur.execute(query, params)
    books = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("business.html", books=books)




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()   # 🔥 ADD THIS
        cur = conn.cursor()

        cur.execute("""
            SELECT user_id, full_name 
            FROM users 
            WHERE email = %s AND password_hash = %s
        """, (email, password))

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect("/")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")




@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()   # 🔥 ADD THIS
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (full_name, email, password_hash)
            VALUES (%s, %s, %s)
        """, (full_name, email, password))

        conn.commit()
        cur.close()
        conn.close()   # 🔥 CLOSE CONNECTION

        return redirect("/login")

    return render_template("signup.html")



@app.route("/description/<int:book_id>")
def description(book_id):

    conn = get_db_connection()
    cur = conn.cursor()

    # 📘 Get selected book
    cur.execute("""
        SELECT book_id, title, author, description, price, image_url
        FROM books
        WHERE book_id = %s
    """, (book_id,))

    book = cur.fetchone()

    if not book:
        cur.close()
        conn.close()
        return "Book not found", 404

    author_name = book[2]

    # 📚 Get other books by same author
    cur.execute("""
        SELECT book_id, title, image_url
        FROM books
        WHERE author = %s
        AND book_id != %s
    """, (author_name, book_id))

    other_books = cur.fetchall()

    # 📖 Get reviews for this book
    cur.execute("""
        SELECT r.rating, r.comment, u.full_name, r.created_at
        FROM reviews r
        JOIN users u ON r.user_id = u.user_id
        WHERE r.book_id = %s
        ORDER BY r.created_at DESC
    """, (book_id,))

    reviews = cur.fetchall()


    cur.close()
    conn.close()

    return render_template(
    "description.html",
    book=book,
    other_books=other_books,
    reviews=reviews
)





from flask import session, redirect

@app.route("/checkout/<int:book_id>")
def checkout(book_id):

    # 🔐 Check if user logged in
    if "user_id" not in session:
        return redirect("/login")

    quantity = int(request.args.get("qty", 1))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT book_id, title, price
        FROM books
        WHERE book_id = %s
    """, (book_id,))

    book = cur.fetchone()

    if not book:
        return "Book not found"

    total = book[2] * quantity

    cur.close()
    conn.close()

    return render_template(
        "checkout.html",
        book=book,
        quantity=quantity,
        total=total
    )




@app.route('/order_status')
def order_status():
    return render_template('order_status.html')


import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="bookverse",
        user="postgres",
        password="root"
    )
    return conn


@app.route("/adventure")
def adventure():
    conn = get_db_connection()
    cur = conn.cursor()

    search = request.args.get("search")
    sort = request.args.get("sort")

    query = """
        SELECT book_id, title, author, price, image_url
        FROM books
        WHERE category_id = 1
    """

    params = []

    # 🔎 Search filter
    if search:
        query += " AND title ILIKE %s"
        params.append(f"%{search}%")

    # 🔄 Sorting
    if sort == "low":
        query += " ORDER BY price ASC"
    elif sort == "high":
        query += " ORDER BY price DESC"
    elif sort == "latest":
        query += " ORDER BY book_id DESC"

    cur.execute(query, params)
    books = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("adventure.html", books=books)


@app.route("/biography")
def biography():
    conn = get_db_connection()
    cur = conn.cursor()

    search = request.args.get("search")
    sort = request.args.get("sort")

    query = """
        SELECT book_id, title, author, price, image_url
        FROM books
        WHERE category_id = 5
    """

    params = []

    # 🔎 Search filter
    if search:
        query += " AND title ILIKE %s"
        params.append(f"%{search}%")

    # 🔄 Sorting
    if sort == "low":
        query += " ORDER BY price ASC"
    elif sort == "high":
        query += " ORDER BY price DESC"
    elif sort == "latest":
        query += " ORDER BY book_id DESC"

    cur.execute(query, params)
    books = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("biography.html", books=books)


@app.route("/logout")
def logout():
    session.clear()   # removes everything from session
    return redirect("/")


@app.route("/add_review/<int:book_id>", methods=["POST"])
def add_review(book_id):

    if "user_id" not in session:
        return redirect("/login")

    rating = request.form["rating"]
    comment = request.form["comment"]
    user_id = session["user_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reviews (user_id, book_id, rating, comment)
        VALUES (%s, %s, %s, %s)
    """, (user_id, book_id, rating, comment))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("description", book_id=book_id))


@app.route("/preview/<int:book_id>")
def preview_book(book_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT title, preview_file
        FROM books
        WHERE book_id = %s
    """, (book_id,))

    book = cur.fetchone()

    cur.close()
    conn.close()

    if not book:
        return "Preview not found"

    return render_template(
        "preview.html",
        title=book[0],
        preview_file=book[1]
    )


@app.route('/payment', methods=['POST'])
def payment():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    city = request.form['city']
    pincode = request.form['pincode']
    payment_method = request.form['paymentmethod']
    book_id = request.form['book_id']
    quantity = request.form['quantity']
    total_amount = request.form['total_amount']

    conn = psycopg2.connect(
        host="localhost",
        database="bookverse",
        user="postgres",
        password="root"
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders
        (user_id, book_id, full_name, phone, email, address, city, pincode,
         payment_method, quantity, total_amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING order_id;
    """, (user_id, book_id, fullname, phone, email,
          address, city, pincode,
          payment_method, quantity, total_amount))

    order_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('receipt', order_id=order_id))



@app.route('/receipt/<int:order_id>')
def receipt(order_id):

    conn = psycopg2.connect(
        host="localhost",
        database="bookverse",
        user="postgres",
        password="root"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT o.order_id, o.full_name, o.phone, o.email,
               o.address, o.city, o.pincode,
               o.payment_method, o.quantity, o.total_amount,
               b.title
        FROM orders o
        JOIN books b ON o.book_id = b.book_id
        WHERE o.order_id = %s;
    """, (order_id,))

    order = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("receipt.html", order=order)
















