import os
from calculation_engine import calculate_portfolio
from portfolio_data import get_portfolio_stocks, get_user_portfolios
from flask import Flask, render_template, request, session, flash
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)


def get_user_datastore() -> dict:
    data = pd.read_csv("relational_database/user_metadata.csv")
    data.set_index("user_id", inplace=True)
    return data.to_dict("index")


user_datastore = get_user_datastore()


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html', name=session.get("name"))


@app.route('/login', methods=['POST'])
def do_login():
    provided_username = request.form['username']
    provided_password = request.form['password']
    for user_id, metadata in user_datastore.items():
        username = metadata["username"]
        password = metadata["password"]
        if username == provided_username and password == provided_password:
            session['logged_in'] = True
            session["user_id"] = user_id
            session["username"] = username
            session["name"] = metadata["name"]
            session["email"] = metadata["email"]
        else:
            flash('wrong password!')
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route("/get_portfolio_by_id/<portfolio_id>", methods=["GET"])
def get_portfolio_by_id(portfolio_id: int):
    portfolio_id = int(portfolio_id)
    user_portfolio = get_portfolio_stocks(portfolio_id)
    result = calculate_portfolio(user_portfolio)
    return result


@app.route("/get_portfolio_list", methods=["GET"])
def get_portfolio_list() -> str:
    portfolios = get_user_portfolios(session.get("user_id"))
    http_functions = ""
    for portfolio_id in portfolios:
        http_functions += f'<form action=/get_portfolio_by_id/{portfolio_id}"><input type="submit" value={portfolio_id} class="btn btn-primary btn-large btn-block" style="display: inline-block;"></form>'

    return render_template('portfolio.html', http_functions=http_functions)


if __name__ == "__main__":
    app.config["SECRET_KEY"] = os.urandom(12)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
