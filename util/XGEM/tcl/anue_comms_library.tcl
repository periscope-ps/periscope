#!c:\tcl\bin\tclsh.exe
######################################################################
#
#                         Anue Systems, Inc.
#                        www.anuesystems.com
#    Copyright (c) 2005-2009 Anue Systems, Inc.. All Rights Reserved.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#           THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE OF 
#                      ANUE SYSTEMS INC.
#
#      The copyright notice above does not evidence any actual 
#      or intended publication of such source code.
#   
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#   	               COMMS: TCL Support library
# 	            
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 	For questions contact:     <support@anuesystems.com>
#
#   Updated:     $Date: 2009-06-01 10:36:01 -0500 (Mon, 01 Jun 2009) $
#   Revision:    $Rev: 42000 $
#######################################################################

######################################################################
#  default target name to connect to. If DEFAULT_TARGET is non-empty,
#     this script library will automatically attempt a connection. 
#     Two examples of possible settings are also shown below.
#     default target should only be set here, if you are not using
#     another tcl library (ie hseries.tcl or mseries.tcl)
######################################################################
#set      DEFAULT_TARGET                ""
#set     DEFAULT_TARGET                COM4:
#set     DEFAULT_TARGET                192.168.40.98:2003:1

######################################################################
#          Communication control and debugging variables
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# COMM_POLL:          how often (in ms) to check for new characters
# COMM_WARN:          when (in ms) to print a warning message if no response
# COMM_TIMEOUT:       maximum amount of time (in ms) to wait for response
# COMM_VERBOSE_DEBUG: enable debugging. 0=no debug, 1=debugging
#
######################################################################
set 	 COMM_POLL           		1
set 	 COMM_WARN           		5000
set 	 COMM_TIMEOUT        		20000
set 	 COMM_HAVE_ADDRESSES 		1
set 	 COMM_VERBOSE_DEBUG  		0

set      TX_DEST_ADDR                   0xFF
set      TX_SRC_ADDR                    0x00
set      RX_DEST_ADDR                   0xFF
set      RX_SRC_ADDR                    0x00

global 	 CHASSISVARS
set      com_ser                        ""

######################################################################
# --------------------------------------------------------------------
# CRC support Routines
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : CRC_Reset 
# Parameters       : none (side effect, update global $crc)
# Return Value     : none
# Purpose          : initializes the CRC calculator
######################################################################
proc CRC_Reset {} {
    global crc
    set crc 0xFFFF
}

######################################################################
# Function Name    : CRC_DoBit
# Parameters       : bit (1/0)
# Return Value     : none (side effect, update global $crc
# Purpose          : adds one bit to the CRC calculation
######################################################################
proc CRC_DoBit {bit} {
    global crc
    set fb  [expr $crc  & 1   ]
    set fb  [expr $fb   ^ $bit]
    set crc [expr $crc >> 1   ]
    set crc [expr $crc ^ ($fb ? 0x8408 : 0) ]
}

######################################################################
# Function Name    : CRC_DoChar
# Parameters       : char (8 bits)
# Return Value     : none (side effect, upate global $crc)
# Purpose          : adds one character to the CRC calculation
######################################################################
proc CRC_DoChar {c} {
    set byte $c
    for {set i 0} {$i < 8 } {incr i} {
	CRC_DoBit [expr $byte & 1]   
	set byte [expr $byte >> 1] 
    }
}

######################################################################
# Function Name    : CRC_DoString
# Parameters       : string (arbitrary length)
# Return Value     : CRC value (16-bits, as a decimal string)
# Purpose          : Calculate the CRC for a string, and return it
######################################################################
proc CRC_DoString {str} {
    global crc
    CRC_Reset
    set tmpstr $str
    while {[string length $tmpstr] > 0} {
	set b [string range $tmpstr 0 1  ]
	set tmpstr  [string range $tmpstr 2 end]
	CRC_DoChar "0x$b"
    }
    return $crc
}

######################################################################
# Function Name    : CRC_CheckString
# Parameters       : string (arbitrary length)
# Return Value     : CRC value (16-bits, as a decimal string)
# Purpose          : Calculate the CRC for a string, and return it
######################################################################
proc CRC_CheckString {str} {
    global crc
    CRC_Reset
    set l [string length $str]
    if {$l < 8 } {
	return 0
    }
    set tmpstr [string range $str 0 [expr $l-5]]
    set rxcrc  "0x[string range $str [expr $l-4] end]"
    while {[string length $tmpstr] > 0} {
	set b [string range $tmpstr 0 1  ]
	set tmpstr  [string range $tmpstr 2 end]
	#puts "         CRC_DoChar \"0x$b\""
	CRC_DoChar "0x$b"
    }

    set crc [expr ([CRC_HiByte $crc]<<8) | ([CRC_LoByte $crc]<<0)]
    if {$rxcrc == $crc} {
	#puts [format "CRC GOOD: rxcrc=$rxcrc crc=0x%4.4X" $crc]
	return 1
    } else {
	#puts [format "CRC BAD:  rxcrc=$rxcrc crc=0x%4.4X" $crc]
	return 0
    }
}

######################################################################
# Function Name    : CRC_HiByte
# Parameters       : 16-bit crc value value
# Return Value     : 8 bit value decimal string
# Purpose          : extracts the high byte of the CRC value 
######################################################################
proc CRC_HiByte {crc} {
    return [expr (($crc >> 0) & 0xFF)^0xFF]
}

######################################################################
# Function Name    : CRC_LoByte
# Parameters       : 16-bit crc value value
# Return Value     : 8 bit value decimal string
# Purpose          : extracts the low byte of the CRC value 
######################################################################
proc CRC_LoByte {crc} {
    return [expr (($crc >> 8) & 0xFF)^0xFF]
}

######################################################################
# Function Name    : CRC_AppendToString
# Parameters       : string
# Return Value     : string (with CRC appended)
# Purpose          : appends a 16-bit crc to a string
######################################################################
proc CRC_AppendToString {str} {
    set crc [CRC_DoString $str]
    set outstr $str
    append outstr [format "%2.2X" [CRC_HiByte $crc]]
    append outstr [format "%2.2X" [CRC_LoByte $crc]]
    return $outstr
}

######################################################################
# Function Name    : CRC_ConvertStringtoHex 
# Parameters       : string value
# Return Value     : hexadecimal string
# Purpose          : 
######################################################################
proc CRC_ConvertStringToHex {str} {
    set hexstr {}
    set tmpstr $str
    while {[string length $tmpstr] > 0} {
	set b [string range $tmpstr 0 1  ]
	append hexstr "$b "
	set tmpstr  [string range $tmpstr 2 end]
    }
    return $hexstr
}

######################################################################
# Function Name    : CRC_NumListToString
# Parameters       : list of numbers (8-bit values)
# Return Value     : string of hex characters
# Purpose          : converts "ABCD" to "41424344"
######################################################################
proc CRC_NumListToString {args} {
    set str {}
    foreach  byte $args {
	append str [format "%2.2X" [expr $byte & 0xFF]]
    }
    return $str
}

######################################################################
# Function Name    :  target_prompt
# Parameters       :  none
# Return Value     :  none
# Purpose          :  Writes a prompt with the blade id ie Blade<1>% 
######################################################################
proc target_prompt {} {
    global TX_DEST_ADDR
    global CHASSISVARS
    
    if {[info exists CHASSISVARS(currid)]} {
	puts -nonewline "Blade<$CHASSISVARS(currid):$TX_DEST_ADDR>% "
    } else {
	puts -nonewline "Blade<$TX_DEST_ADDR>% "
    }
}

######################################################################
# Function Name    : set_target
# Parameters       : the blade id of the new target blade (ie 3)
# Return Value     : none
# Purpose          : Sets the blade id to be connected to
######################################################################
proc set_target {target} {
    global TX_DEST_ADDR
    global tcl_prompt1
    set tcl_prompt1 target_prompt
    if {[regexp  -nocase  {^(\w+):([0-9]+)$} $target tmp id b]} {
	set_chassis $id
	set TX_DEST_ADDR $b
    } else {
	set TX_DEST_ADDR $target
    }
    return ""
}

######################################################################
# Function Name    : blade
# Parameters       : blade number and command to execute
# Return Value     : none
# Purpose          : Execute any other command with a temporary
#                  :   blade selection
#####################################################################
proc blade {n args} {
    global TX_DEST_ADDR

    if {[regexp  -nocase  {^(\w+):([0-9]+)$} $n tmp id b]} {
	if {[llength $args] == 0} {
	    set_chassis $id
	    set_target  $b
	    return
	} else {
	    set cmd [concat chassis $id blade $b $args]
	    return [eval $cmd]
	}
    } 

    set old_dest $TX_DEST_ADDR

    if {([llength $n] > 1) && ([llength $args] != 0)} {
        foreach b $n {
            if {[llength $args] > 1} {
                if { [catch {uplevel 1 blade $b $args} ret] } {
                    puts stderr "ERROR: $ret"
                    set ret ""
                }
            } elseif {[llength $args] == 1} {
                set_target $b
                if { [catch {uplevel 1 [lindex $args 0]} ret] } {
                    puts stderr "ERROR: $ret"
                    set ret ""
                }
            }
        }
        set_target $old_dest
        return $ret
    }

    if {! [regexp  -nocase  {^[0-9]+$} $n] } {
	error "blade: ``$n'' is not a blade number"
    }

    if {[llength $args] == 0} {
	set_target $n
	return
    }
    set_target $n
    if { [catch {uplevel 1 $args} ret] } {
    	puts stderr "ERROR: $ret"
    	set ret ""
    }
    set_target $old_dest
    return $ret
}

######################################################################
# Function Name    : set_chassis
# Parameters       : chassis id (alphanumeric)
# Return Value     : none
# Purpose          : set the current chassis ID 
#####################################################################
proc set_chassis {id} {
    global com_ser
    global TX_DEST_ADDR
    global TX_SRC_ADDR
    global RX_DEST_ADDR
    global RX_SRC_ADDR
    global CHASSISVARS

    if {[regexp  -nocase  {:} $id] } {
	error "chassis: ``$id'' is not a valid chassis id"
    }

    if {[info exists CHASSISVARS(currid)]} {
	set currid $CHASSISVARS(currid)
    } else {
	set currid $id
    }

    if { $com_ser != "" } {
	set CHASSISVARS($currid:SOCK) $com_ser
	set CHASSISVARS($currid:TXDA) $TX_DEST_ADDR
	set CHASSISVARS($currid:TXSA) $TX_SRC_ADDR
	set CHASSISVARS($currid:RXDA) $RX_DEST_ADDR
	set CHASSISVARS($currid:RXSA) $RX_SRC_ADDR
    }

    if {[info exists CHASSISVARS($id:SOCK)]} {
	set com_ser	  $CHASSISVARS($id:SOCK) 
	set TX_DEST_ADDR  $CHASSISVARS($id:TXDA) 
	set TX_SRC_ADDR	  $CHASSISVARS($id:TXSA) 
	set RX_DEST_ADDR  $CHASSISVARS($id:RXDA) 
	set RX_SRC_ADDR   $CHASSISVARS($id:RXSA) 
    } else {
	set com_ser	  ""
	set TX_DEST_ADDR  0xFF
	set TX_SRC_ADDR	  0
	set RX_DEST_ADDR  0xFF
	set RX_SRC_ADDR   0
    }

    set CHASSISVARS(currid) $id
}

######################################################################
# Function Name    : chassis
# Parameters       : chassis id and command to execute
# Return Value     : return code from command that was executed
# Purpose          : Execute any other command with a temporary
#                  :   chassis selection
#####################################################################
proc chassis {id args} {
    global CHASSISVARS

    if {[regexp  -nocase  {:} $id] } {
	error "chassis: ``$id'' is not a valid chassis id"
    }

    if {[llength $args] == 0} {
	set_chassis $id
	return
    }

    if {[info exists CHASSISVARS(currid)]} {
	set old_id $CHASSISVARS(currid)
    } else {
	set old_id $id
    }
   
    set_chassis $id
    if { [catch {uplevel 1 $args} ret] } {
    	puts stderr "ERROR: $ret"
    	set ret ""
    }
    set_chassis $old_id
    return $ret
}

######################################################################
# Function Name    : BuildCommand
# Parameters       : Command number, length, and argument bytes
# Return Value     : command string
# Purpose          : Builds command string including CRC
######################################################################
proc BuildCommand {args} {
    global COMM_VERBOSE_DEBUG
    global COMM_HAVE_ADDRESSES  
    global TX_DEST_ADDR
    global TX_SRC_ADDR

    if {$COMM_HAVE_ADDRESSES} {
	set x [list $TX_DEST_ADDR $TX_SRC_ADDR]
    } else {
	set x [list ]
    }
    # Code added 4/24/06 to handle case if $args is a single list of numbers (cwebb)
    if {([llength $args] == 1) && ([llength [lindex $args 0]] > 1)} {
	set args [lindex $args 0]
    }
    set args [lreplace $args 1 1 [expr [llength $args] - 2]]
    set x [concat $x $args]
    set str [eval CRC_NumListToString $x]
    set cmd [CRC_AppendToString  $str]

    return "$cmd\r\n"
}


######################################################################
# --------------------------------------------------------------------
# Low level communication routines
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : open_com
# Parameters       : name (COM1: etc) rate (baud rate for COM port)
# Return Value     : none (side effect, sets global $com_ser)
# Purpose          : opens communication channel with target
######################################################################
proc open_com {com_name {rate 115200}} {
    global com_ser
    global COMM_VERBOSE_DEBUG
    if {! [catch {close_com} fid] } {
	puts "WARNING: Closing old connection: $com_ser"
	puts "         (waiting 1 second for connection to shutdown...)"
	after 1000
    }

    if [ regexp  -nocase  {^com[0-9]:$} $com_name ] {
	if {$COMM_VERBOSE_DEBUG} {
	    puts "INFO: Connecting to target on COM=$com_name"
	}
        if {[catch {set com_ser [open $com_name r+]} errmsg]} {
            puts "ERROR: $errmsg"
            return
        }
	fconfigure $com_ser -mode $rate,n,8,1 -blocking 0 -translation {auto auto}
	#fconfigure $com_ser -mode $rate,n,8,1 
    } elseif [regexp -nocase {^([a-z0-9_.]+):([0-9]+)$} $com_name \
		  tmp server port] {
	global TX_DEST_ADDR
	if {$TX_DEST_ADDR == 0xFF} {
	    puts "INFO: Using default blade number 1 in target."
	    set_target 1
	}
	if {$COMM_VERBOSE_DEBUG} {
	    puts "INFO: Connecting to target at SERVER=$server PORT=$port"
	}
        if {[catch {set com_ser [socket $server $port]} errmsg]} {
            puts "ERROR: $errmsg"
	    return
        }
	fconfigure $com_ser -buffering none -blocking 0 
    } elseif [regexp -nocase {^([a-z0-9_.]+):([0-9]+):([0-9]+)$} $com_name \
		  tmp server port blade] {
	set_target $blade
	if {$COMM_VERBOSE_DEBUG} {
	    puts "INFO: Connecting to target at SERVER=$server PORT=$port BLADE=$blade"
	}
        if {[catch {set com_ser [socket $server $port]} errmsg]} {
            puts "ERROR: $errmsg"
	    return
        }
	fconfigure $com_ser -buffering none -blocking 0 
    } else {
	puts "ERROR: Unrecognized communication port name  '$com_name'"
	puts "       Must be in the format of 'COM1:' or 'HOST:PORT'"
	return
    }
}

######################################################################
# Function Name    : close_com
# Parameters       : none
# Return Value     : none
# Purpose          : Closes communication channel with target 
######################################################################
proc close_com {} {
    global com_ser
    global TX_DEST_ADDR
    global TX_SRC_ADDR
    global RX_DEST_ADDR
    global RX_SRC_ADDR

    set TX_DEST_ADDR 0xFF
    set TX_SRC_ADDR  0x00
    set RX_DEST_ADDR 0x00
    set RX_SRC_ADDR  0x00

    close $com_ser
}

######################################################################
# Function Name    : flushin
# Parameters       : none
# Return Value     : 
# Purpose          : clear any unread input from $com_ser
######################################################################
proc flushin {} {
    global com_ser
    set l ""
    set rd ""
    if {[catch {set rd [read $com_ser] } err]} {
	set l ""
	set rd ""
	set errtype  [fconfigure $com_ser -lasterror]
	if {! [string compare -nocase $errtype "FRAME BREAK"]} {
	    puts "WARNING: FRAME/BREAK errs detected on serial line. This may mean that"
	    puts "         the target was restarted or reconnected......"
	} elseif {! [string compare -nocase $errtype "FRAME"]} {
	    puts "WARNING: FRAME errs detected on serial line. This may mean that"
	    puts "         the target was restarted or reconnected......"
	} elseif {! [string compare -nocase $errtype "BREAK"]} {
	    puts "WARNING: BREAK errs detected on serial line. This may mean that"
	    puts "         the target was restarted or reconnected......"
	} else {
	    puts "WARNING: $err\n\tAdditional Information: $errtype"
	}
	after 100
    } else {
	if {[string compare $rd ""] != 0} {
	    set l ""
	    regsub -all {[ \n\r]+} $rd " " l
	    regsub -all {[ \n\r]$} $l "" l
	    regsub -all {^[ \n\r]} $l "" l
	    set l [split $l]
	    puts "WARNING: Discarded/unexpected response(s) from target:"
	    foreach k $l {
		puts "\t $k"
	    }
	    puts ""
	}
    }
}

######################################################################
# Function Name    : re_sync
# Parameters       : none
# Return Value     : none
# Purpose          : resynchronizes comms with target by sending newline
######################################################################
proc re_sync {} {
    send_command "\n"
    after 100
}

######################################################################
# Function Name    : no_status
# Parameters       : none
# Return Value     : none
# Purpose          : print error messsage when comms totally fail
######################################################################
proc no_status {} {
    puts "ERROR: Unable to communcate with device.  Please check cable."
    puts "       Please connect cable and execute com_check."
}

######################################################################
# Function Name    : ping
# Parameters       : none
# Return Value     : none
# Purpose          : sends a NOP packet to get pong response
#                  :   which proves comms synchronization is OK
######################################################################
proc ping {} {
    send_command [BuildCommand 0x01 0x00]
}

######################################################################
# Function Name    : pong
# Parameters       : none
# Return Value     : list of two-char hex bytes returned from target
# Purpose          : gets command responses
######################################################################
proc pong {} {
    global COMM_POLL
    global COMM_TIMEOUT
    global COMM_WARN
    global COMM_VERBOSE_DEBUG
    global com_ser
    global COMM_HAVE_ADDRESSES
    global RX_DEST_ADDR
    global RX_SRC_ADDR
    set warn_flag 0

    set rd ""
    for {set i 0} {$i < $COMM_TIMEOUT} {incr i $COMM_POLL} {
	if {[catch {set rd [gets $com_ser] } err]} {
	    set rd ""
	    set errtype  [fconfigure $com_ser -lasterror]
	    if {! [string compare -nocase $errtype "FRAME BREAK"]} {
		puts "WARNING: FRAME/BREAK errs detected on serial line. This may mean that"
		puts "         the target was restarted or reconnected......"
	    } elseif {! [string compare -nocase $errtype "FRAME"]} {
		puts "WARNING: FRAME errs detected on serial line. This may mean that"
		puts "         the target was restarted or reconnected......"
	    } elseif {! [string compare -nocase $errtype "BREAK"]} {
		puts "WARNING: BREAK errs detected on serial line. This may mean that"
		puts "         the target was restarted or reconnected......"
	    } else {
		puts "WARNING: $err\n\tAdditional Information: $errtype"
	    }
	    after 10
	} else {
	    if {[string compare $rd ""] != 0} {
		#puts "got '$rd'"
		break;
	    }
	}

	if {($i > $COMM_WARN) && ($warn_flag == 0)} {
	    incr warn_flag
	    puts "WARNING: Slow response from target ... still trying"
	}
	after $COMM_POLL
    }

    if {$COMM_VERBOSE_DEBUG} {
	puts "INFO: Response data='$rd'"
	puts "INFO: Response time was $i ms"
	puts ""
    }

    if {[string length $rd] == 0} {
	set bytes {0 0}
	return $bytes
    }

    if {![CRC_CheckString $rd]} {
	puts "COMM ERROR: CRC error in RX packet '$rd'"
	set bytes {0 0}
	#puts "bytes='$bytes' (CRC BAD)"
	return $bytes
    }

    set bytes [CRC_ConvertStringToHex $rd]
    set l [llength $bytes]
    set bytes [lrange $bytes 0 [expr $l-3]]
    #puts "bytes='$bytes' l=$l"
    if {$COMM_HAVE_ADDRESSES} {
	set RX_DEST_ADDR "0x[lindex $bytes 0]"
	set RX_SRC_ADDR  "0x[lindex $bytes 1]"
	set bytes [lrange $bytes 2 end]
    }

    set exlen [expr [llength $bytes] - 2]
    set rxlen 0x[lindex $bytes 1]
    #puts "bytes='$bytes' exlen=$exlen rxlen=$rxlen"
    if {$rxlen != $exlen} {
	puts "COMM ERROR: RX packet has incorrect length (PKT='$rd')"
	puts "            rxlen=$rxlen exlen=$exlen"
	set bytes {0 0}
	return $bytes
	
    }

    #puts "bytes='$bytes'"
    return $bytes
}

######################################################################
# Function Name    : send_command
# Parameters       : send command to the target
# Return Value     : none
# Purpose          : 
######################################################################
proc send_command {cmd} {
    global COMM_VERBOSE_DEBUG
    global com_ser
    flushin
    if {$COMM_VERBOSE_DEBUG} {
	puts "----------------------------"
	puts "INFO: Sending CMD=$cmd"
    }
    after 1
    puts  -nonewline $com_ser $cmd
    flush $com_ser
}

######################################################################
# Function Name    : nack_msg
# Parameters       : response and a default_msg in case of a nack
#                  : with no error code or msg
# Return Value     : none
######################################################################
proc nack_msg {ret {default_msg "Invalid command."} } {
    if {! [string compare $ret ""]} {	no_status }

    if {[llength $ret] >= 3} {
        # Received at least a 3-byte response.

        if {"0x[lindex $ret 0]" == 0xC7} {
            # Received a NACK.
            set code "0x[lindex $ret 3]"

            if {$code == 0x0B} {
                # Received a NACK due to Network Playback in progress.
                puts "ERROR: Unable to perform requested operation."
                puts "       Cannot make impairment changes to this profile" 
                puts "       while network playback is playing on this profile."
            } elseif {$code == 0x0D} {
                # Received a NACK due to Network Playback in progress.
                puts "ERROR: Unable to perform requested operation."
                puts "       Cannot make classifier changes" 
                puts "       while network playback is playing."
            } elseif {$code == 0x0C} {
                # Received a NACK due to Logging in progress.
                puts "ERROR: Unable to perform requested operation."
                puts "       Cannot make the requested change"
                puts "       while logging is in progress."
            } elseif {$code == 0x0E} {
                # Received a NACK due to in wrong opmode.
                puts "ERROR: Unable to perform requested operation."
                puts "       The emulator is not in GEM mode."
            } elseif {$code == 0x0A} {
                set msg {}
                foreach a [lrange $ret 4 end] {
                    lappend msg [format %c "0x$a"]
                }
                puts -nonewline "ERROR: "
                puts [join $msg ""]
            } else {
                puts "ERROR: $default_msg"
            }
        }
    }
}

######################################################################
# Function Name    : pong_check
# Parameters       : none
# Return Value     : none
# Purpose          : checks for response, if none, prints error
######################################################################
proc pong_check {} {

    nack_msg [pong]

    return ""
}

######################################################################
# Function Name    : parse_read_value
# Parameters       : none
# Return Value     : hex byte returned from command
# Purpose          : extracts return value from ack messages
######################################################################
proc parse_read_value {} {
    set retn_val [pong]
    if {[string compare $retn_val ""] == 0} {
	no_status
	return 0
    } else  {
	set read_val [lindex [split $retn_val] 3]
	return "0x$read_val"
    }
}

######################################################################
# Function Name    : is_nack
# Parameters       : pkt is the reply packet we got back
# Return Value     : 1 if the packet is a NACK, 0 if it is not.
# Purpose          : Determine if a response packet is a NACK.
######################################################################
proc is_nack {pkt} {

    if {"0x[lindex $pkt 0]" == 0xC7} {
        return 1
    }

    return 0
}

######################################################################
# Function Name    : print_error_on_nack
# Parameters       : pkt is the reply packet we got back
#                    if packet is a NACK, we print out error_string
# Return Value     : 1 if the packet is a NACK, 0 if it is not.
# Purpose          : Print a message if we get a NACK.
######################################################################
proc print_error_on_nack {pkt error_string} {
    if {[is_nack $pkt] == 1} {
        puts "ERROR: $error_string"
        return 1
    }

    return 0
}

######################################################################
# --------------------------------------------------------------------
# Comm establishment and checking routines
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : est_com
# Parameters       : target name (COM1: or host.domain.com:7200)
# Return Value     : none (side effect, set global $com_ser)
# Purpose          : establishes communication with target & 
#                  :   checks communication integrity.
######################################################################
proc est_com {com_name {baud 115200}} {

    global TX_DEST_ADDR
    global TX_SRC_ADDR
    global RX_DEST_ADDR
    global RX_SRC_ADDR

    open_com $com_name $baud
    #
    # Ensure that mspd is sync'd and alive
    #
    set trial_count 4
    while {$trial_count >= 0} {
	ping
        set response [pong]
	if {[string match -nocase "01*" $response] ||
            [string match -nocase "C6*" $response]} {
	    if {$TX_SRC_ADDR == 0} {
		if {$RX_DEST_ADDR != 0} {
		    set TX_SRC_ADDR $RX_DEST_ADDR
		}
	    }
	    if {$TX_DEST_ADDR == 0xFF} {
		set TX_DEST_ADDR $RX_SRC_ADDR
	    }

            if {! [string compare -nocase $response "01 02 02 00"]} {
                set boardtype "Mauna Kea"
            } elseif {! [string compare -nocase $response "01 02 03 00"]} {
                set boardtype "Mauna Loa"
            } elseif {! [string compare -nocase $response "01 02 41 00"]} {
                set boardtype "Niihau"
            } elseif {! [string compare -nocase $response "01 02 82 A0"]} {
                set boardtype "Kauai"
            } elseif {! [string compare -nocase $response "01 02 81 A0"]} {
                set boardtype "Hawaii"
            } elseif {! [string compare -nocase $response "01 02 F3 0A"]} {
                set boardtype "Kona"
            } else {
                set boardtype "<UNKNOWN>"
            }
            break
        } else {
	    puts "WARNING: Communication with target on $com_name failed.\n"
	    if {$trial_count > 0} {
		puts "INFO: Attempting to resynchronize \[$trial_count attempt(s) left]\n"
	    }
	    set trial_count [expr $trial_count - 1]
	    re_sync
	}
    }

    if {$trial_count <= 1} {
	puts "ERROR: Unable to communicate with equipment on $com_name"
	puts "        Please check the cable and re-start the program"
	return 0
    } else {
	puts "INFO: Successfully connected to target on $com_name"
	puts "INFO: Target has identified itself as a $boardtype"
	return 1
    }
}

######################################################################
# Function Name    : com_check
# Parameters       : none
# Return Value     : none
# Purpose          : Checks communication to target
######################################################################
proc com_check {} {
    set trial_count 3
    while {$trial_count >= 0} {
	ping
        set response [pong]
	if {[string match -nocase "01*" $response] ||
	    [string match -nocase "C6*" $response]} {
	    puts "INFO: Succesfully communicated with device."
	    return
	}
	set trial_count [expr $trial_count - 1]
    }
    no_status
}


