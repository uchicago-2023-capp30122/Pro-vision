import sys
import os
if sys.argv[1] == "quick":
    from .dashboard_quick import app as quick_app
    sys.path.append(os.path.abspath(os.path.join('ProVision', 'dashboard_quick')))
    quick_app.app.run_server(host='127.0.0.1', port='4444', debug = False)
elif sys.argv[1] == "full":
    from .dashboard_full import app as full_app
    sys.path.append(os.path.abspath(os.path.join('ProVision', 'dashboard_full')))
    full_app.app.run_server(host='127.0.0.1', port='4444', debug = False)
else:
    print("Please enter one argument only")
    sys.exit(1)