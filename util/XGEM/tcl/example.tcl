
# To run this script, start jtclsh and type:
# % source all_supported_commands.tcl
# or run:
# jtclsh all_supported_commands.tcl
# from a DOS or Cygwin shell prompt


# Import the Anue XGEM Tcl library
package require anue::xgem

# Import all exported xgem commands into the local namespace
# This allows us to call commands with "open_conn" instead of
# "anue::xgem::open_conn"
namespace import anue::xgem::*



#######################################
# SETUP DEFAULTS
#######################################

# Indicates that any bad parameters passed to XGEM commands should halt
# execution of the script 
set_bound_chk -severity ERROR

# Turns on verbosity so descriptive information is displayed
set_default_verbose_mode -on

# Sets the default line to avoid having to pass it thru -line to each command
set_default_line -line 1

# Sets the default profile to avoid having to pass it thru -p to each command
set_default_profile -p 1



# Open a read-write connection, storing the connection reference in $my_conn
set my_conn [open_conn -ip 192.168.40.52 -access rw]

# Sets the default connection to avoid having to pass it thru -conn to each
# command
set_default_conn -conn $my_conn





#######################################
# CLASSIFIER
#######################################

# Filter all IP traffic on line 1 to or from a 192.168.*.* IP address into
# profile 1

# Set the name of profile 1 and enable the classifier
set_classifier -line 1 -p 1 -enable true -check_ip_version false \
        -name "Local IP Traffic"

# Clear any existing equations
set_classifier_equation -line 1 -p 1 -clear

# Add the filter for the source address
set_classifier_equation -line 1 -p 1 -append -protocol Ipv4 -field Src_Addr \
        -field_value 192.168..

# Add the filter for the destination address
set_classifier_equation -line 1 -p 1 -append -protocol Ipv4 -field Dest_Addr \
        -field_value 192.168..

# Call apply_profiles to apply the changes to the classifier
apply_profiles -line 1

# Now all traffic on line 1 to or from a 192.168.*.* IP address is flowing
# through profile 1






#######################################
# PROFILE IMPAIRMENTS
#######################################

# Set the delay on the default line and profile to 150 micro-seconds
set_profile_delay -delay 150 -unit us

# Drop 40% of packets on the default line and profile
set_profile_drop -enable true -distribution uniform -prob .4

# Modify the first 4 bytes of every 10 packets on the default line and profile
set_profile_modify -mod_engine 0 -enable true \
        -distribution periodic -select_cnt 1 -interval 10 \
        -starting_offset 0 -value 0xFE8080FE00000000 -mask 0xFFFFFFFF00000000

# Apply all changes to profiles on line 1
apply_profiles -line 1




#######################################
# STATISTICS
#######################################

# Show statistics every 4 seconds until 50,000 packets have been dropped on
# line 1, profile 1

# Fetch the stats, storing the returned associative array to 'ret'
array set ret [get_profile_stats -line 1 -p 1]

# Loop until the number of dropped packets exceeds 50,000
while {$ret(DROPPED_FRAMES_CUMULATIVE) < 50000} {
    # Delay 4 seconds
    after 4000
    # Refetch the stats
    array set ret [get_profile_stats -line 1 -p 1]
}


# Disconnect from the XGEM box
close_conn
