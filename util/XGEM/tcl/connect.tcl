
# To run this script, start jtclsh and type:
# % source connect.tcl
# or run:
# jtclsh connect.tcl
# from a DOS or Cygwin shell prompt


# Import the Anue XGem Tcl library
package require anue::xgem

# Import all exported xgem commands into the local namespace
# This allows us to call commands with "open_conn" instead of
# "anue::xgem::open_conn"
namespace import anue::xgem::*


# Open a read-write connection, storing the connection reference in $my_conn
set my_conn [open_conn -ip 192.168.1.101 -access rw]
