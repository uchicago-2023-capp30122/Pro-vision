import sys
import os
import dashboard_full.app as full_app
import dashboard_quick.app as quick_app
if sys.argv[1] == "quick":
    sys.path.append(os.path.abspath(os.path.join('Pro-vision', 'dashboard_quick')))
    quick_app.app.run_server(host='127.0.0.1', port='8090', debug = False)
elif sys.argv[1] == "full":
    sys.path.append(os.path.abspath(os.path.join('Pro-vision', 'dashboard_full')))
    full_app.app.run_server(host='127.0.0.1', port='8090', debug = False)
else:
    print("Please enter one argument only")
    sys.exit(1)