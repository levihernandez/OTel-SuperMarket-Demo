import os
import sys
from inventory_management import app as inventory_app
from order_processing import app as order_app

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'inventory':
        inventory_app.app.run(debug=True, host='0.0.0.0', port=8081)
        sys.exit()
    elif len(sys.argv) > 1 and sys.argv[1] == 'order':
        order_app.app.run(debug=True, host='0.0.0.0', port=8082)
        sys.exit()

    # If no argument was provided, start all apps
    inventory_app.app.run(debug=True, host='0.0.0.0')
    order_app.app.run(debug=True, host='0.0.0.0')
