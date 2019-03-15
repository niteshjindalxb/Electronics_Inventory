from Inventory import app
from .views import *


def set_urls():
    # app.add_url_rule('/', 'home', view_func=views.home, methods = ['GET', 'POST'])
    # app.add_url_rule('/login/', 'login', view_func=views.login, methods = ['GET', 'POST'])
    app.add_url_rule('/', 'home', view_func=home)
    app.add_url_rule('/login/', 'login', view_func=login)
    app.add_url_rule('/logout/', 'logout', view_func=logout)
    app.add_url_rule('/dashboard/', 'dashboard', view_func=dashboard)
    app.add_url_rule('/issue/', 'issue', view_func=issue)
    app.add_url_rule('/renew/', 'renew', view_func=renew)
    app.add_url_rule('/return_item/', 'return_item', view_func=return_item)
    app.add_url_rule('/account/', 'account', view_func=account)
    app.add_url_rule('/show_list/', 'show_list', view_func=show_list)
    app.add_url_rule('/admin/', 'admin', view_func=admin)


# Main function
if __name__ == "__main__":
    load_data()

    app.run(debug=True)