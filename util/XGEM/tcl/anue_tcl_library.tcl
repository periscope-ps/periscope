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
#   	              Anue TCL Support library
# 	            
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 	For questions contact:     <support@anuesystems.com>
#
#   Updated:     $Date: 2009-06-04 14:45:56 -0500 (Thu, 04 Jun 2009) $
#   Revision:    $Rev: 42139 $
#######################################################################

if {$tcl_version < 8.4} {
   error "ERROR: The Anue TCL libraries require TCL version 8.4 or greater"
}

source anue_comms_library.tcl

set tcl_precision 17

######################################################################
#  definitions for delay functions
######################################################################
set      OTU1_BITS_PER_NS              [expr {0.01944*128.0*255.0/238.0}]
set      OTU2_BITS_PER_NS              [expr {0.01944*512.0*255.0/237.0}]
set      OC192_BITS_PER_NS             [expr {0.01944*512.0}]
set      OC48_BITS_PER_NS              [expr {0.01944*128.0}]
set      OC12_BITS_PER_NS              [expr {0.01944*32} ]
set      OC3_BITS_PER_NS               [expr {0.01944*8}  ]
set      GE_BITS_PER_NS                [expr {1.25}       ]
set      GEM100M_BITS_PER_NS           [expr {.100}       ]
set      GEM10M_BITS_PER_NS            [expr {.010}       ]
set      GEM_BITS_PER_NS               [expr {1.00}       ]
set      FC1X_BITS_PER_NS              [expr {1.0625}     ]
set      FC2X_BITS_PER_NS              [expr {2.125}      ]
set      FC4X_BITS_PER_NS              [expr {4.25}       ]
set      FC8X_BITS_PER_NS              [expr {8.5}        ]
set      FC10X_BITS_PER_NS             [expr {10.0*(66.0/64.0)*1.02}]
set      FC10X_FEC11317_BITS_PER_NS    [expr {10.0*(66.0/64.0)*1.02*(255/237.0)}]        
set      FC10X_FEC11270_BITS_PER_NS    [expr {10.0*(66.0/64.0)*1.02*(255/238.0)}]        
set      XGELAN_BITS_PER_NS            [expr {10.0*(66.0/64.0)}]
set      XGELAN_11049_BITS_PER_NS      [expr {10.0*(66.0/64.0)*(255.0/238.0)}]
set      XGELAN_11096_BITS_PER_NS      [expr {10.0*(66.0/64.0)*(255.0/237.0)}]

set      CPRI_O24_BITS_PER_NS          [expr {0.1536*16}]
set      CPRI_O12_BITS_PER_NS          [expr {0.1536*8 }]
set      CPRI_O6_BITS_PER_NS           [expr {0.1536*4 }]

######################################################################
#  definitions of constants for operating mode and bit rate
######################################################################
set     MODE_NULL                   0x00
set     MODE_DG                     0x11
set     MODE_PD                     0x12
set     MODE_GE                     0x13
set     MODE_FC                     0x14
set     MODE_HSDG                   0x11; # Symbol Deprecated
set     MODE_HSPD                   0x12; # Symbol Deprecated
set     MODE_HSGE                   0x13; # Symbol Deprecated
set     MODE_HSFC                   0x14; # Symbol Deprecated
set     MODE_GEM                    0x23
set     MODE_XGEM                   0x25
set     MODE_CPRI                   0x22

set     MODE_STRING($MODE_NULL)     "NULL"
set     MODE_STRING($MODE_DG)       "DG"
set     MODE_STRING($MODE_PD)       "PD"
set     MODE_STRING($MODE_GE)       "GE"
set     MODE_STRING($MODE_FC)       "FC"
set     MODE_STRING($MODE_GEM)      "GEM"
set     MODE_STRING($MODE_XGEM)     "XGEM"
set     MODE_STRING($MODE_CPRI)     "CPRI"

set     BITRATE_NULL                0x00
set     BITRATE_OC3                 0x02
set     BITRATE_OC12                0x03
set     BITRATE_OC48                0x04
set     BITRATE_OC192               0x09
set     BITRATE_GE                  0x05
set     BITRATE_XGELAN              0x0B
set     BITRATE_XGELAN_D            0x15
set     BITRATE_XGELAN_CX4          0x16
set     BITRATE_XGELAN_11049FEC     0x13
set     BITRATE_XGELAN_11096FEC     0x10
set     BITRATE_XGEWAN              0x0E
set     BITRATE_XGEWAN_FEC          0x12
set     BITRATE_FC1X                0x07
set     BITRATE_FC2X                0x08
set     BITRATE_FC4X                0x0D
set     BITRATE_FC8X                0x14
set     BITRATE_FC10X               0x0C
set     BITRATE_FC10X_FEC11317      0x11
set     BITRATE_FC10X_FEC11270      0x28
set     BITRATE_OTU1                0x0F
set     BITRATE_OTU2                0x0A
set     BITRATE_GE1GC               0x23
set     BITRATE_GE100M              0x24
set     BITRATE_GE10M               0x25
set     BITRATE_GE1GFS              0x26
set     BITRATE_GE1GFD              0x27
set     BITRATE_CPRI_O24            0x22
set     BITRATE_CPRI_O12            0x21
set     BITRATE_CPRI_O6             0x20

set     BITRATE_STRING($BITRATE_NULL)               "NULL"
set     BITRATE_STRING($BITRATE_OC3)                "OC-3 / STM-1"
set     BITRATE_STRING($BITRATE_OC12)               "OC-12 / STM-4"
set     BITRATE_STRING($BITRATE_OC48)               "OC-48 / STM-16"
set     BITRATE_STRING($BITRATE_OC192)              "OC-192 / STM-64"
set     BITRATE_STRING($BITRATE_GE)                 "GE"
set     BITRATE_STRING($BITRATE_XGELAN)             "10G-LAN (unpaired)"
set     BITRATE_STRING($BITRATE_XGELAN_D)           "10G-LAN (paired)"
set     BITRATE_STRING($BITRATE_XGELAN_CX4)         "10G-LAN (CX-4)"
set     BITRATE_STRING($BITRATE_XGELAN_11049FEC)    "GE10-Lan w/FEC (11.049)"
set     BITRATE_STRING($BITRATE_XGELAN_11096FEC)    "GE10-Lan w/FEC (11.096)"
set     BITRATE_STRING($BITRATE_XGEWAN)             "GE10-Wan"
set     BITRATE_STRING($BITRATE_XGEWAN_FEC)         "GE10-Wan w/FEC"
set     BITRATE_STRING($BITRATE_FC1X)               "FC-1x"
set     BITRATE_STRING($BITRATE_FC2X)               "FC-2x"
set     BITRATE_STRING($BITRATE_FC4X)               "FC-4x"
set     BITRATE_STRING($BITRATE_FC8X)               "FC-8x"
set     BITRATE_STRING($BITRATE_FC10X)              "FC-10x"
set     BITRATE_STRING($BITRATE_FC10X_FEC11317)     "FC-10x w/FEC \[11.317G\]"
set     BITRATE_STRING($BITRATE_FC10X_FEC11270)     "FC-10x w/FEC \[11.270G\]"
set     BITRATE_STRING($BITRATE_OTU1)               "OTU-1"
set     BITRATE_STRING($BITRATE_OTU2)               "OTU-2"
set     BITRATE_STRING($BITRATE_GE1GC)              "1G-Copper"
set     BITRATE_STRING($BITRATE_GE100M)             "100M-Copper"
set     BITRATE_STRING($BITRATE_GE10M)              "10M-Copper"
set     BITRATE_STRING($BITRATE_GE1GFS)             "1G-Fiber (unpaired)"
set     BITRATE_STRING($BITRATE_GE1GFD)             "1G-Fiber (paired)"
set     BITRATE_STRING($BITRATE_CPRI_O24)           "CPRI-24"
set     BITRATE_STRING($BITRATE_CPRI_O12)           "CPRI-12"
set     BITRATE_STRING($BITRATE_CPRI_O6)            "CPRI-6"

######################################################################
# Conversion factors for length/time units change
######################################################################
set      FIBER_VELOCITY_FACTOR         [expr {1/1.498962}]
set      SPEED_OF_LIGHT_METERS_PER_NS  [expr {0.2997924} ]

######################################################################
# Delay modes
######################################################################
set      DELAY_MODE_STATIC          1
set      DELAY_MODE_PPM             2
set      DELAY_MODE_TARGET_DELAY    3

######################################################################
#  definitions of constant values for BER settings & calculations
######################################################################
set 	 BER_MAX_INTERVAL 	       [expr {(65536.0 * 65536.0 * 65535.0 * 4.0)}]

set      BER_TYPE(NONE)                0
set      BER_TYPE(1BIT)                1  
set      BER_TYPE(BURST)               2   
set      BER_TYPE(BURST_INVERT)        3    
set      BER_TYPE(BURST_PRBS)          4    
set      BER_TYPE(BURST_ONES)          5    
set      BER_TYPE(BURST_ZEROES)        6    

set      BER_TYPE(0)                   "None"
set      BER_TYPE(1)                   "1Bit"
set      BER_TYPE(2)                   "Burst"
set      BER_TYPE(3)                   "BurstInvert"
set      BER_TYPE(4)                   "BurstPRBS"
set      BER_TYPE(5)                   "BurstOnes"
set      BER_TYPE(6)                   "BurstZeroes"

######################################################################
#  definitions of constant values statistical distributions
######################################################################
set      STAT_DISTRIB(PERIODIC)        1
set      STAT_DISTRIB(POISSON)         2
set      STAT_DISTRIB(GAUSSIAN)        3
set      STAT_DISTRIB(UNIFORM)         4
set      STAT_DISTRIB(ONESHOT)         5

set      STAT_DISTRIB(1)               "periodic"
set      STAT_DISTRIB(2)               "poisson"
set      STAT_DISTRIB(3)               "gaussian"
set      STAT_DISTRIB(4)               "uniform"
set      STAT_DISTRIB(5)               "oneshot"

######################################################################
#  definitions of constant values for Jitter PDVs (for simple_jitter)
######################################################################
set      JITTER_PDV(NONE)              1
set      JITTER_PDV(GAUSSIAN)          2
set      JITTER_PDV(UNIFORM)           3
set      JITTER_PDV(INTERNET)          4

######################################################################
#  definitions of constant values for bitrate & buffersize
#  (for basic_bwlimit)
######################################################################
set 	 BASIC_BWLIMIT_BITRATE(OC3)       1  
set 	 BASIC_BWLIMIT_BITRATE(DS3)       2 
set 	 BASIC_BWLIMIT_BITRATE(E3)        3 
set 	 BASIC_BWLIMIT_BITRATE(4Mb)       4 
set 	 BASIC_BWLIMIT_BITRATE(E1)        5 
set 	 BASIC_BWLIMIT_BITRATE(DS1)       6 
set 	 BASIC_BWLIMIT_BITRATE(768kb)     7 
set 	 BASIC_BWLIMIT_BITRATE(384kb)     8 
set 	 BASIC_BWLIMIT_BITRATE(144kb)     9 
set 	 BASIC_BWLIMIT_BITRATE(128kb)     10 
set 	 BASIC_BWLIMIT_BITRATE(64kb)      11

set 	 BASIC_BWLIMIT_BUFSIZE(1MB)       1 
set 	 BASIC_BWLIMIT_BUFSIZE(512kB)     2 
set 	 BASIC_BWLIMIT_BUFSIZE(256kB)     3 
set 	 BASIC_BWLIMIT_BUFSIZE(128kB)     4 
set 	 BASIC_BWLIMIT_BUFSIZE(64kB)      5 
set 	 BASIC_BWLIMIT_BUFSIZE(32kB)      6 
set 	 BASIC_BWLIMIT_BUFSIZE(16kB)      7 
set 	 BASIC_BWLIMIT_BUFSIZE(8kB)       8 

######################################################################
#  definitions of constant values for packet drop routines
######################################################################
set      PKTDROP_REPLACEBY(REPEAT)     2
set      PKTDROP_REPLACEBY(IDLE)       1

set      PKTDROP_REPLACEBY(0)          "repeat"
set      PKTDROP_REPLACEBY(1)          "idle"

######################################################################
#  definitions of constant values for packet drop routines
######################################################################
set      PKTCORRUPT_BL_RAND            0
set      PKTCORRUPT_BL_FIXED           1

######################################################################
#  GEM filter codes 
######################################################################
set      FP_MAC_SRC0                   0
set      FP_MAC_SRC1                   1
set      FP_MAC_SRC2                   2
set      FP_MAC_SRC3                   3
set      FP_MAC_SRC4                   4
set      FP_MAC_SRC5                   5

set      FP_MAC_DST0                   6
set      FP_MAC_DST1                   7
set      FP_MAC_DST2                   8
set      FP_MAC_DST3                   9
set      FP_MAC_DST4                   10
set      FP_MAC_DST5                   11

set      FP_MAC_LENTYPE                12

set      FP_IP_SRC0                    13
set      FP_IP_SRC1                    14
set      FP_IP_SRC2                    15
set      FP_IP_SRC3                    16

set      FP_IP_DST0                    17
set      FP_IP_DST1                    18
set      FP_IP_DST2                    19
set      FP_IP_DST3                    20

set      FP_IP_DSCP                    21
set      FP_IP_PROTOCOL                22

set      FP_PORT_SRC                   23
set      FP_PORT_DST                   24

set      FP_VLANID                     25
set      FP_PRIO                       26

set      FP_QINQ_VLANID                27
set      FP_QINQ_PRIO                  28

set      FP_CUSTOM_BYTE                29

set      FP_NAME                       30

set      FP_IP_SRC_MASK                31
set      FP_IP_DST_MASK                32

set      FP_CUSTOM_VALUE               33

set      FP_IP6_SRC0                   35
set      FP_IP6_SRC1                   36
set      FP_IP6_SRC2                   37
set      FP_IP6_SRC3                   38
set      FP_IP6_SRC4                   39
set      FP_IP6_SRC5                   40
set      FP_IP6_SRC6                   41
set      FP_IP6_SRC7                   42
set      FP_IP6_SRC8                   43
set      FP_IP6_SRC9                   44
set      FP_IP6_SRC10                  45
set      FP_IP6_SRC11                  46
set      FP_IP6_SRC12                  47
set      FP_IP6_SRC13                  48
set      FP_IP6_SRC14                  49
set      FP_IP6_SRC15                  50

set      FP_IP6_DST0                   51
set      FP_IP6_DST1                   52
set      FP_IP6_DST2                   53
set      FP_IP6_DST3                   54
set      FP_IP6_DST4                   55
set      FP_IP6_DST5                   56
set      FP_IP6_DST6                   57
set      FP_IP6_DST7                   58
set      FP_IP6_DST8                   59
set      FP_IP6_DST9                   60
set      FP_IP6_DST10                  61
set      FP_IP6_DST11                  62
set      FP_IP6_DST12                  63
set      FP_IP6_DST13                  64
set      FP_IP6_DST14                  65
set      FP_IP6_DST15                  66

set      FP_CHECK_IP_VERSION           67

set      FP_MPLS_LABEL1                68
set      FP_MPLS_LABEL2                69

set      FP_INGRESS_PORT               70
set      FP_EGRESS_PORT                71

set      FP_NXTHOP_IP0                 72
set      FP_NXTHOP_IP1                 73
set      FP_NXTHOP_IP2                 74
set      FP_NXTHOP_IP3                 75

set      FP_TPID                       76
set      FP_QINQ_TPID                  77

set      FP_IP6_2_SRC0                 78
set      FP_IP6_2_SRC1                 79
set      FP_IP6_2_SRC2                 80
set      FP_IP6_2_SRC3                 81
set      FP_IP6_2_SRC4                 82
set      FP_IP6_2_SRC5                 83
set      FP_IP6_2_SRC6                 84
set      FP_IP6_2_SRC7                 85

set      FP_IP6_2_DST0                 86
set      FP_IP6_2_DST1                 87
set      FP_IP6_2_DST2                 88
set      FP_IP6_2_DST3                 89
set      FP_IP6_2_DST4                 90
set      FP_IP6_2_DST5                 91
set      FP_IP6_2_DST6                 92
set      FP_IP6_2_DST7                 93

######################################################################
#  definitions for use with GEM's accumulate and burst feature
######################################################################
set      ACCUM_MODE(COUNT_ONLY)        1
set      ACCUM_MODE(TIMEOUT_ONLY)      2
set      ACCUM_MODE(COUNT_OR_TIMEOUT)  0
set      ACCUM_MODE(COUNT_AND_TIMEOUT) 3

######################################################################
# Definitions of units for status display (
######################################################################
set 	 LCD_DISPLAY_UNITS_TIME     	0x1
set 	 LCD_DISPLAY_UNITS_LENGTH   	0x2
set 	 LCD_DISPLAY_UNITS_BITS     	0x3            
set      LCD_DISPLAY_UNITS_BYTES        0x3

set  	 LCD_DISPLAY_UNITS(ms) 	   	$LCD_DISPLAY_UNITS_TIME
set  	 LCD_DISPLAY_UNITS(us) 	   	$LCD_DISPLAY_UNITS_TIME
set  	 LCD_DISPLAY_UNITS(ns) 	   	$LCD_DISPLAY_UNITS_TIME
set  	 LCD_DISPLAY_UNITS(km) 	   	$LCD_DISPLAY_UNITS_LENGTH
set  	 LCD_DISPLAY_UNITS(m)  	   	$LCD_DISPLAY_UNITS_LENGTH
set  	 LCD_DISPLAY_UNITS(meters) 	$LCD_DISPLAY_UNITS_LENGTH
set  	 LCD_DISPLAY_UNITS(bytes)  	$LCD_DISPLAY_UNITS_BITS
set  	 LCD_DISPLAY_UNITS(B)      	$LCD_DISPLAY_UNITS_BITS
set  	 LCD_DISPLAY_UNITS(bits)   	$LCD_DISPLAY_UNITS_BITS
set  	 LCD_DISPLAY_UNITS(b)      	$LCD_DISPLAY_UNITS_BITS

######################################################################
# Definitions of laser control modes
######################################################################
set 	 LASERCTL_NORM        	        0      
set 	 LASERCTL_LASEROFF      	1
set 	 LASERCTL_LOS            	1
set 	 LASERCTL_LASERON       	2
set 	 LASERCTL_LOF           	2
set 	 LASERCTL_SQUELCH       	4

######################################################################
# Definitions for OH capture
######################################################################
set      HSPD_TOH       0
set      HSPD_POH       1

set      HSPD_MAX_BUFFER_SIZE   127

set      HSPD_MAX_NUM_BUFFERS     3
set      HSPD_MAX_NUM_TRIGGERS    3

set      HSPD_OH_CAPTURE_EVERY_FRAME_MODE         0
set      HSPD_OH_CAPTURE_TRANSITIONAL_TIMING_MODE 1

set      HSPD_MANUAL_TRIGGER_MODE 0

######################################################################
# Definitions of POH byte codes
######################################################################
set      POH_BYTE_J1    1
set      POH_BYTE_B3    2
set      POH_BYTE_C2    3
set      POH_BYTE_G1    4
set      POH_BYTE_F2    5
set      POH_BYTE_H4    6
set      POH_BYTE_Z3    7
set      POH_BYTE_Z4    8
set      POH_BYTE_Z5    9

######################################################################
# Definitions of TOH byte codes
######################################################################
set      TOH_BYTE_A1        1
set      TOH_BYTE_A2        2
set      TOH_BYTE_A3        3
set      TOH_BYTE_B1        4
set      TOH_BYTE_E1        5
set      TOH_BYTE_F1        6
set      TOH_BYTE_D1        7
set      TOH_BYTE_D2        8
set      TOH_BYTE_D3        9
set      TOH_BYTE_H1       10
set      TOH_BYTE_H2       11
set      TOH_BYTE_H3       12
set      TOH_BYTE_B2       13
set      TOH_BYTE_K1       14
set      TOH_BYTE_K2       15
set      TOH_BYTE_D4       16
set      TOH_BYTE_D5       17
set      TOH_BYTE_D6       18
set      TOH_BYTE_D7       19
set      TOH_BYTE_D8       20
set      TOH_BYTE_D9       21
set      TOH_BYTE_D10      22
set      TOH_BYTE_D11      23
set      TOH_BYTE_D12      24
set      TOH_BYTE_S1_Z1    25
set      TOH_BYTE_Z1       25
set      TOH_BYTE_S1       25
set      TOH_BYTE_M0_M1_Z2 26
set      TOH_BYTE_M0       26
set      TOH_BYTE_M1       26
set      TOH_BYTE_Z2       26
set      TOH_BYTE_E2       27

######################################################################
# GEM-specific Definitions
######################################################################
set      GEM_MAX_PROFILES  16
set      GEM_MAX_OFFSET    2000

set      GEM_REF_BITS_T1   0
set      GEM_REF_PRS_E1    1
set      GEM_REF_EXT_10MHZ 2
set      GEM_REF_INT_10MHZ 3
set      GEM_REF_LINE      4

set array LSTAT_CACHE
set array PSTAT_CACHE


######################################################################
# --------------------------------------------------------------------
# Miscellaneous Utility Commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : reboot_lcd
# Parameters       : none
# Return Value     : none
# Purpose          : Reboots the LCD. Not really useful to end users
######################################################################
proc reboot_lcd {} {
    send_command [BuildCommand 0x04 0x0]
    pong_check
}

######################################################################
# Function Name    : set_lcd_contrast
# Parameters       : contrast_value (0-31)
# Return Value     : none
# Purpose          : Sets contrast of LCD, default is 16
######################################################################
proc set_lcd_contrast {contrast_value} {
    send_command [BuildCommand 0x06 0x01 $contrast_value]
    pong_check
}

######################################################################
# Function Name    : set_lcd_backlight
# Parameters       : backlight_value (0-100)
# Return Value     : none
# Purpose          : Sets backlight setting (percentage) default is 100
######################################################################
proc set_lcd_backlight {backlight_value} {
    send_command [BuildCommand 0x07 0x01 $backlight_value]
    pong_check
}


######################################################################
# --------------------------------------------------------------------
# Get/Set operating mode
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_device_mode
# Parameters       : mode bitrate
# Example          : set_device_mode $MODE_GEM $BITRATE_GE1GC
# Purpose          : Change the operating mode of the emulator.
######################################################################
proc set_device_mode {mode bitrate} {
    global MODE_STRING
    global BITRATE_STRING

    global TX_DEST_ADDR
    global COMM_WARN
    global COMM_TIMEOUT

    set ms "Unknown"
    set bs "Unknown"

	if {[info exists MODE_STRING($mode)]} {
	    set ms $MODE_STRING($mode)
	}
	if {[info exists BITRATE_STRING($bitrate)]} {
	    set bs $BITRATE_STRING($bitrate)
	}

    set blade $TX_DEST_ADDR
    set_target 1

    set valid_mode 0

    foreach available_mode [get_operating_mode_table_as_list] {
        if {($mode == [lindex $available_mode 0]) && \
            ($bitrate == [lindex $available_mode 1])} \
        {
            set valid_mode 1
            break
        }
    }

    if {!$valid_mode} {
        puts "ERROR:  Invalid operating mode for this device:  $ms/$bs"
        get_operating_mode_table
        set_target $blade
        return
    }

    puts -nonewline "Changing operating mode for this device to $ms/$bs... "
    flush stdout

    set old_warn $COMM_WARN
    set COMM_WARN 60000
    set_target 0

    send_command [BuildCommand 0x20 2 $mode $bitrate]
    pong_check

    set_target $blade
    set COMM_WARN $old_warn

    puts "done."
}


######################################################################
# Function Name    : get_device_mode
# Parameters       : none
# Return Value     : returns the current device mode
# Purpose          : 
######################################################################
proc get_device_mode {} {
    global MODE_STRING
    global BITRATE_STRING

    puts "Current Mode:"
    set current_mode [get_operating_mode]
    set m "0x[lindex $current_mode 0]"
    set b "0x[lindex $current_mode 1]"

    if { [info exists MODE_STRING($m) ] } {
        set ms $MODE_STRING($m)
        set mc [get_symbol_from_mode $m]
    } else {
        set ms "Unknown"
        set mc ""
    }

    if { [info exists BITRATE_STRING($b) ] } {
        set bs $BITRATE_STRING($b)
        set bc [get_symbol_from_bitrate $b]
    } else {
        set bs "Unknown"
        set bc ""
    }

    puts [format "%-35s%s" "  $ms/$bs" "($mc $bc)"]
}

######################################################################
# Function Name    : set_operating_mode
# Parameters       : mode bitrate autosense
# Return Value     : none
# Purpose          : 
######################################################################
proc set_operating_mode {mode bitrate {autosense 0}} {
    global MODE_GEM
    global MODE_XGEM

    if {{$mode == $MODE_GEM} || {$mode == $MODE_XGEM}} {
        puts "For GEM & XGEM devices, please use the set_device_mode TCL"
        puts "function to change the operating mode and bitrate of the device."
        return
    }

    puts "This function is deprecated."
    puts "Please use set_device_mode in the future."

    send_command [BuildCommand 0x20 0x03 $mode $bitrate $autosense]
    pong_check
}

######################################################################
# Function Name    : get_operating_mode
# Parameters       : none
# Return Value     : returns the operating mode tuple
# Purpose          : 
######################################################################
proc get_operating_mode {} {
    send_command [BuildCommand 0x21 0x00]
    return [lrange [pong] 2 4]
}

######################################################################
# Function Name    : get_operating_bitrate
# Parameters       : none
# Return Value     : returns the operating bitrate
# Purpose          : allows the scripts to handle multiple rates
######################################################################
proc get_operating_bitrate {} {
    return [lindex [get_operating_mode] 1]
}

######################################################################
# Function Name    : get_config_option
# Parameters       : option : option to get status for
# Return Value     : returns the option value
# Purpose          : allows the scripts to handle configuration options
######################################################################
proc get_config_option {option} {
    send_command [BuildCommand 0xEF 0x00]

	set ret [lrange [pong] 2 end]
	set slen [llength $ret]
	set ret_val 0

	for {set j 0} {$j < $slen} {incr j} {
		set itm "0x[lindex $ret $j]"

		if {$itm == $option} {
			switch $itm {
				0xF0 {set ret_val 2}
				0xF4 {set ret_val 4}
				0xF2 {set ret_val 1}
				0xF6 {
					incr j
					set ret_val [lindex $ret $j]
				}
				0xF8 {set ret_val 1}
				0xFA {set ret_val 1}
				0xFC {set ret_val 1}
				0xEE {set ret_val 1}
				0xEC {set ret_val 1}

				default {set ret_val -1}
			}
		}
	}

    return $ret_val
}

######################################################################
# Function Name    : get_operating_mode_table
# Parameters       : none
# Return Value     : returns the operating mode table
# Purpose          : 
######################################################################
proc get_operating_mode_table {} {
    global MODE_STRING
    global BITRATE_STRING

    puts "Modes Available:"
    foreach available_mode [get_operating_mode_table_as_list] {
        set m [lindex $available_mode 0]
        set b [lindex $available_mode 1]

        if { [info exists MODE_STRING($m) ] } {
            set ms $MODE_STRING($m)
            set mc [get_symbol_from_mode $m]
        } else {
            set ms "Unknown"
            set mc ""
        }

        if { [info exists BITRATE_STRING($b) ] } {
            set bs $BITRATE_STRING($b)
            set bc [get_symbol_from_bitrate $b]
        } else {
            set bs "Unknown"
            set bc ""
        }

        puts [format "%-35s%s" "  $ms/$bs" "($mc $bc)"]
    }
}

######################################################################
# Function Name    : get_operating_mode_table_as_list
#                  :
# Purpose          : *** INTERNAL USE ONLY ***
######################################################################
proc get_operating_mode_table_as_list {} {

    send_command [BuildCommand 0x23 0x00]
    set ret [pong]
    set tab {}
    set n   "0x[lindex $ret 1]"
    for {set j 0} {$j < $n} {incr j 2} {
        set m "0x[lindex $ret [expr $j+2]]"
        set b "0x[lindex $ret [expr $j+3]]"
        lappend tab [list $m $b]
    }
    return $tab
}

######################################################################
# Function Name    : get_symbol_from_mode
#                  :
# Purpose          : *** INTERNAL USE ONLY ***
######################################################################
proc get_symbol_from_mode {mode} {
    global MODE_NULL
    global MODE_DG
    global MODE_PD
    global MODE_GE
    global MODE_FC
    global MODE_GEM
    global MODE_XGEM
    global MODE_CPRI

    switch $mode "
        $MODE_NULL {set name MODE_NULL}
        $MODE_DG   {set name MODE_DG  }
        $MODE_PD   {set name MODE_PD  }
        $MODE_GE   {set name MODE_GE  }
        $MODE_FC   {set name MODE_FC  }
        $MODE_GEM  {set name MODE_GEM }
        $MODE_XGEM {set name MODE_XGEM}
        $MODE_CPRI {set name MODE_CPRI}
        default    {return \"Unknown\"  }
    "
    return "\$$name"
}

######################################################################
# Function Name    : get_symbol_from_bitrate
#                  :
# Purpose          : *** INTERNAL USE ONLY ***
######################################################################
proc get_symbol_from_bitrate {bitrate} {
    global BITRATE_NULL
    global BITRATE_OC3
    global BITRATE_OC12
    global BITRATE_OC48
    global BITRATE_OC192
    global BITRATE_GE
    global BITRATE_XGELAN
    global BITRATE_XGELAN_D
    global BITRATE_XGELAN_CX4
    global BITRATE_XGELAN_11049FEC
    global BITRATE_XGELAN_11096FEC
    global BITRATE_XGEWAN
    global BITRATE_XGEWAN_FEC
    global BITRATE_FC1X
    global BITRATE_FC2X
    global BITRATE_FC4X
    global BITRATE_FC8X
    global BITRATE_FC10X
    global BITRATE_FC10X_FEC11317
    global BITRATE_FC10X_FEC11270
    global BITRATE_OTU1
    global BITRATE_OTU2
    global BITRATE_GE1GC
    global BITRATE_GE100M
    global BITRATE_GE10M
    global BITRATE_GE1GFS
    global BITRATE_GE1GFD
    global BITRATE_CPRI_O24
    global BITRATE_CPRI_O12
    global BITRATE_CPRI_O6

    switch $bitrate "
        $BITRATE_NULL               {set name BITRATE_NULL}
        $BITRATE_OC3                {set name BITRATE_OC3}
        $BITRATE_OC12               {set name BITRATE_OC12}
        $BITRATE_OC48               {set name BITRATE_OC48}
        $BITRATE_OC192              {set name BITRATE_OC192}
        $BITRATE_GE                 {set name BITRATE_GE}
        $BITRATE_XGELAN             {set name BITRATE_XGELAN}
        $BITRATE_XGELAN_D           {set name BITRATE_XGELAN_D}
        $BITRATE_XGELAN_CX4         {set name BITRATE_XGELAN_CX4}
        $BITRATE_XGELAN_11049FEC    {set name BITRATE_XGELAN_11049FEC}
        $BITRATE_XGELAN_11096FEC    {set name BITRATE_XGELAN_11096FEC}
        $BITRATE_XGEWAN             {set name BITRATE_XGELAN_11096FEC}
        $BITRATE_XGEWAN_FEC         {set name BITRATE_XGEWAN_FEC}
        $BITRATE_FC1X               {set name BITRATE_FC1X}
        $BITRATE_FC2X               {set name BITRATE_FC2X}
        $BITRATE_FC4X               {set name BITRATE_FC4X}
        $BITRATE_FC8X               {set name BITRATE_FC8X}
        $BITRATE_FC10X              {set name BITRATE_FC10X}
        $BITRATE_FC10X_FEC11317     {set name BITRATE_FC10X_FEC11317}
        $BITRATE_FC10X_FEC11270     {set name BITRATE_FC10X_FEC11270}
        $BITRATE_OTU1               {set name BITRATE_OTU1}
        $BITRATE_OTU2               {set name BITRATE_OTU2}
        $BITRATE_GE1GC              {set name BITRATE_GE1GC}
        $BITRATE_GE100M             {set name BITRATE_GE100M}
        $BITRATE_GE10M              {set name BITRATE_GE10M}
        $BITRATE_GE1GFS             {set name BITRATE_GE1GFS}
        $BITRATE_GE1GFD             {set name BITRATE_GE1GFD}
        $BITRATE_CPRI_O24           {set name BITRATE_CPRI_O24}
        $BITRATE_CPRI_O12           {set name BITRATE_CPRI_O12}
        $BITRATE_CPRI_O6            {set name BITRATE_CPRI_O6}
        default                     {return \"Unknown\"   }
    "
    return "\$$name"
}

######################################################################
# Get version info
######################################################################
proc hex_text_2_string {arg_list} {
  set new_str ""

  foreach tmp_char $arg_list {
    set new_str $new_str[format "%c" "0x$tmp_char"]
  }
  return $new_str
}

proc get_all_version_info {} {

    send_command [BuildCommand 0x28 0x0]

    set  ret_list [pong]

    set model_name  [hex_text_2_string [lrange $ret_list 2 21]]

    set  pcb_type    "[lindex $ret_list 22]"
    set  pcb_version "[lindex $ret_list 23]"

    set serial_num  [hex_text_2_string [lrange $ret_list 24 43]]
    set pcb_bornon  [hex_text_2_string [lrange $ret_list 44 63]]
    

    set  t1 [lindex $ret_list 65] 
    set  t2 [lindex $ret_list 64] 
    set  fpga_compiter [expr 16 * int(0x$t1) + int(0x$t2)]
    set  fpga_chourmin [format "%d:%02d" "0x[lindex $ret_list 67]" \
                                       "0x[lindex $ret_list 66]" ]
    set  t1 [lindex $ret_list 69] 
    set  t2 [lindex $ret_list 68] 
    set  fpga_cyear [expr 256 * int(0x$t1) + int(0x$t2)]
    set  fpga_cmonthday [format "%.2d/%.2d" "0x[lindex $ret_list 71]" \
                                      "0x[lindex $ret_list 70]" ]
    set  fpga_type [format "%d" "0x[lindex $ret_list 72]" ]
    set  fpga_version   [format "%d" "0x[lindex $ret_list 73]" ]

    set avr_version  [hex_text_2_string [lrange $ret_list 74 93]]
    set avr_date     [hex_text_2_string [lrange $ret_list 94 113]]

    set  cfb_version [lindex $ret_list 114] 


    puts "------ Controller Software ------"
    puts "Model name      : $model_name"
    puts "PCB Type        : 0x$pcb_type"
    puts "PCB Version     : 0x$pcb_version"
    puts "PCB Serial #    : $serial_num"
    puts "PCB Born on Date: $pcb_bornon"
    puts "FPGA Type       : 0x$fpga_type"
    puts "FPGA Version    : 0x$fpga_version"
    puts "FPGA Date       : $fpga_cyear/$fpga_cmonthday ($fpga_chourmin) - $fpga_compiter"
    puts "SW Version      : $avr_version"
    puts "SW Date         : $avr_date"
    puts "CFB Version     : 0x$cfb_version"
}

######################################################################
# --------------------------------------------------------------------
# Delay commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_delay
#                  : 
# Parameters       : delayval units
#                  : 
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  : 
# Return Value     : none
#                  : 
# Purpose          : set the delay
######################################################################
proc set_delay {del {units "ms"}} {
    global LCD_DISPLAY_UNITS

    set del [expr $del * 1.0]

    if {$del < 0.0} {
	set del 0.0
    }

    puts "set_delay $del $units"

    set del [delay_convert $del $units "bits"]


    if { [info exists LCD_DISPLAY_UNITS($units) ] } {
	set_delay_units $LCD_DISPLAY_UNITS($units)
    }

    if {$del > 1099511627775.0} {
	set del 1099511627775.0
    }

    set del [expr floor($del+0.5)]
    for {set i 0} {$i<5} {incr i } {
	set b($i)  [expr int(fmod($del,256.0))]
	set del    [expr ($del / 256.0) ]
    }

    send_command [BuildCommand 0xD0 0x5  $b(4) $b(3) $b(2) $b(1) $b(0)]
    pong_check
}

######################################################################
# Function Name    : get_delay
#                  : 
# Parameters       : units
#                  : 
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  : 
# Return Value     : numeric delay value in the selected units
#                  : 
# Purpose          : Get the delay setting
######################################################################
proc get_delay {{units "ms"}} {
    send_command [BuildCommand 0xD1 0x0]
    set b [lrange [pong] 2 6]
    #puts "b=$b"
    set del 0.0
    for {set i 0} {$i<5} {incr i } {
	set del [expr $del * 256.0 ]
	set del [expr $del + "0x[lindex $b $i]"]
    }
    #puts "del=$del"
    set del [delay_convert $del "bits" $units]
    #puts "  =>$del"

    return $del
}


# --------------------------------------------------------------------
# Get/Set current delay units
# --------------------------------------------------------------------

######################################################################
# Function Name    : set_delay_units
# Parameters       : $type (0=TIME, 1=LENGTH, 2=BITS)
# Return Value     : none
# Purpose          : Sets the type of units displayed in LCD status
######################################################################
proc set_delay_units {type} {
    send_command  [BuildCommand 0xD2 0x01 $type]
    print_error_on_nack [pong] "Invalid command."
}

######################################################################
# Function Name    : get_delay_units
# Parameters       : 
# Return Value     : $type (0=TIME, 1=LENGTH, 2=BITS)
# Purpose          : Gets the type of units displayed in LCD status
######################################################################
proc get_delay_units {} {
    send_command [BuildCommand 0xD3 0x00]
    return [parse_read_value]
}



######################################################################
# --------------------------------------------------------------------
# Target ppm commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_target_ppm
#                  :
# Parameters       : ppm value
#                  :
# Return Value     : none
#                  :
# Purpose          : set the ppm
######################################################################
proc set_target_ppm {ppm} {
    global LCD_DISPLAY_UNITS

    if {$ppm < -2000.0} {
        set ppm -2000.0
    }
    if {$ppm > 2000.0} {
        set ppm 2000.0
    }

    puts "set_target_ppm $ppm"

    set ppm [expr int(floor(($ppm*10.0)+0.5))]

    for {set i 0} {$i<2} {incr i } {
        set b($i)  [expr $ppm % 256]
        set ppm    [expr ($ppm / 256) ]
    }
    send_command [BuildCommand 0x14 0x2  $b(1) $b(0)]

    pong_check
}

######################################################################
# Function Name    : get_target_ppm
#                  :
# Parameters       : units
#                  :
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  :
# Return Value     : numeric ppm value in the selected units
#                  :
# Purpose          : Get the ppm setting
######################################################################
proc get_target_ppm {} {
    send_command [BuildCommand 0x15 0x0]
    set b [lrange [pong] 2 3]

    set ppm 0.0
    for {set i 0} {$i<2} {incr i } {
        set ppm [expr $ppm * 256.0 ]
        set ppm [expr $ppm + "0x[lindex $b $i]"]
    }

    if {$ppm > 32767.0} {
        set ppm [expr $ppm-65536.0]
    }

    set ppm [expr $ppm / 10.0]

    return $ppm
}

######################################################################
# Function Name    : get_true_delay
#                  :
# Parameters       : units
#                  :
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  :
# Return Value     : numeric delay value in the selected units
#                  :
# Purpose          : Get the current true amount of delay
######################################################################
proc get_true_delay {{units "ms"}} {
    send_command [BuildCommand 0x17 0x0]
    set b [lrange [pong] 2 6]

    set del 0.0
    for {set i 0} {$i<5} {incr i } {
        set del [expr $del * 256.0 ]
        set del [expr $del + "0x0[lindex $b $i]"]
    }

    set del [delay_convert $del "bits" $units]

    return $del
}

######################################################################
# Function Name    : get_true_ppm
#                  :
# Parameters       : units
#                  :
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  :
# Return Value     : numeric ppm value in the selected units
#                  :
# Purpose          : Get the current true ppm offset
######################################################################
proc get_true_ppm {} {
    send_command [BuildCommand 0x18 0x0]
    set b [lrange [pong] 2 3]

    set ppm 0.0
    for {set i 0} {$i<2} {incr i } {
        set ppm [expr $ppm * 256.0 ]
        set ppm [expr $ppm + "0x[lindex $b $i]"]
    }

    if {$ppm > 32767.0} {
        set ppm [expr $ppm-65536.0]
    }

    set ppm [expr $ppm / 10.0]

    return $ppm
}




######################################################################
# --------------------------------------------------------------------
# BER commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_BER <value> <options>
#                  : 
# Parameters       : <value> is the desired BER (e.g. 1.5E-9)
#                  : 
#                  : <options> can be one or more of the following:
#                  : 
#                  : Error Type options
#                  : 
#                  :      -burst=<n>        - inserts a burst of N consecutive errors
#                  :      -burst=<n>:PRBS   - replaces with x^23 PRBS for n consecutive bits
#                  :      -burst=<n>:ONES   - replaces with n consecutive ones
#                  :      -burst=<n>:ZEROES - replaces with n consecutive zeroes
#                  :     
#                  : Statistical distribution of error event times:
#                  : 
#                  :      -periodic        - non-random (fixed) error insertion
#                  :      -poisson         - generated poisson distributed errs
#                  :      -gaussian:stdev_pct - generates gaussian distributed errs
#                  :      -uniform         - generates uniformly distributed errs
#                  : 
#                  : For poisson, gaussian and uniform, the mean error rate
#                  : is given by <value>. For gaussian distributions, the
#                  : standard deviation is specified by stdev_pct as 
#                  : a percentage of themean time between error events 
#                  : (e.g. for BER=1e-3 and stdev_pct=10%, a six sigma 
#                  : interval would be from 0.77E-3 to 1.43E-3 
#                  : (1/1000+300 to 1/1000-300)
#                  : 
# Return Value     : none
#                  : 
# Purpose          : Sets the BER to be inserted 
######################################################################
proc set_BER {args} {
    global BER_MAX_INTERVAL
    global BER_TYPE
    global STAT_DISTRIB

    set ber_type       $BER_TYPE(1BIT)
    set ber_burstlen   0x1
    set ber_distrib    $STAT_DISTRIB(PERIODIC)
    set ber_stdev      30.00
    set ber_interval   0
    set ber_value      "xxxx"

    set cmderrflag     0

    # ----------------------------------------------------------------
    # Parse the command options
    # ----------------------------------------------------------------
    foreach a $args {
	if {[regexp -nocase {^([-+.E0-9]+)$} $a tmp ber_value]} {
	    # peachy, check value below
	} \
	elseif {[regexp -nocase {^-1bit$} $a]} {
	    set ber_type $BER_TYPE(1BIT)
	} \
	elseif {[regexp -nocase {^-burst=([0-9]+)$} $a tmp ber_burstlen]} {
	    set ber_type $BER_TYPE(BURST_INVERT)
	} \
	elseif {[regexp -nocase {^-burst=([0-9]+):PRBS$} $a tmp ber_burstlen]} {
	    set ber_type $BER_TYPE(BURST_PRBS)
	} \
	elseif {[regexp -nocase {^-burst=([0-9]+):ONES$} $a tmp ber_burstlen]} {
	    set ber_type $BER_TYPE(BURST_ONES)
	} \
	elseif {[regexp -nocase {^-burst=([0-9]+):ZEROES$} $a tmp ber_burstlen]} {
	    set ber_type $BER_TYPE(BURST_ZEROES)
	} \
	elseif {[regexp -nocase {^-periodic$} $a ]} {
	    set ber_distrib $STAT_DISTRIB(PERIODIC)
	} \
	elseif {[regexp -nocase {^-poisson$} $a ]} {
	    set ber_distrib $STAT_DISTRIB(POISSON)
	} \
	elseif {[regexp -nocase {^-gaussian:([0-9.]+)%?$} $a tmp ber_stdev]} {
	    set ber_distrib $STAT_DISTRIB(GAUSSIAN)
	} \
	elseif {[regexp -nocase {^-uniform$} $a ]} {
	    set ber_distrib $STAT_DISTRIB(UNIFORM)
	} \
	else {
	    puts "ERROR: set_BER: bad argument '$a'."
	    incr cmderrflag
	}
    }

    # ----------------------------------------------------------------
    # If there were command errors, print usage message
    # ----------------------------------------------------------------
    if {[string compare $ber_value "xxxx"] == 0} {
	puts "ERROR: set_BER: Missing BER <value>"
	incr cmderrflag
    }

    if {$ber_value < 0} {
	puts "ERROR: set_BER: Bad BER value $ber_value"
	return
    }

    if {$cmderrflag} {
	puts ""
	puts "usage: set_BER <value>  "
	puts ""
	puts "set_BER <value> <options>"
	puts ""
	puts "<value> is the desired BER (e.g. 1.5E-9)"
	puts "Specifying a <value> of 0 turns off errors"
	puts ""
	puts "<options> can be one or more of the following:"
	puts ""
	puts "Error Type options"
	puts ""
	puts "     -1bit            - inserts single bit errors"
	puts "     -burst=<n>       - inserts n consecutive errors"
	puts "     -burst=<n>:PRBS  - replace with n consecutive PRBS23 bits"
	puts "     -burst=<n>:ONES  - replace with n consecutive ones"
	puts "     -burst=<n>:ZEROE - replace with n consecutive zeroes"
	puts ""
	puts "Statistical distribution of error event times:"
	puts ""
	puts "     -periodic        - non-random (fixed) error insertion"
	puts "     -poisson         - generated poisson distributed errs"
	puts "     -gaussian:stdev_pct - generates gaussian distributed errs"
	puts "     -uniform         - generates uniformly distributed errs"
	puts ""
	puts "For poisson, gaussian and uniform, the mean error rate"
	puts "is given by <value>. For gaussian distributions, the"
	puts "standard deviation is specified as a percentage of the"
	puts "mean time between error events (e.g. for BER=1e-3 "
	puts "and stdev_pct=10%, a six sigma interval would be"
	puts "from 0.77E-3 to 1.43E-3 (1/1000+300 to 1/1000-300)"
	puts ""
	puts ""
	return
    }


    # ----------------------------------------------------------------
    # if BER value is 0, set type to None
    # ----------------------------------------------------------------
    if {$ber_value  == 0} {
	set ber_type $BER_TYPE(NONE)
    }

    # ----------------------------------------------------------------
    # Convert BER rate to an interval
    # ----------------------------------------------------------------
    set ber_interval [BER_rate2interval $ber_value]

    # ----------------------------------------------------------------
    # break down ber_interval into 5 bytes 
    # ----------------------------------------------------------------
    set divisor   [expr {256.0 * 256.0 * 256.0 * 256.0 * 256.0 * 256.0 * 256.0}]
    for {set i 0} {$i<8} {incr i} {
	set tmp            [expr {$ber_interval / $divisor}]
	set ltmp           [expr {int($tmp)}]
	set berbyte($i)    $ltmp
	set ber_interval   [expr {$ber_interval - ($ltmp * $divisor)}]
	set divisor        [expr {$divisor / 256.0}]
    }

    # ----------------------------------------------------------------
    # break down ber_burstlen into 4 bytes 
    # ----------------------------------------------------------------
    set tmp $ber_burstlen
    for {set i 3} {$i>=0} {incr i -1} {
	set burstbyte($i)   [expr ($tmp & 0xFF)]
	set tmp             [expr ($tmp >> 8)]
    }

    # ----------------------------------------------------------------
    # break down ber_stdev into 2 bytes 
    # ----------------------------------------------------------------
    set tmp [expr round($ber_stdev * 100)]
    for {set i 1} {$i>=0} {incr i -1} {
	set stdevbyte($i)  [expr ($tmp & 0xFF)]
	set tmp            [expr ($tmp >> 8)]
    }

    # ----------------------------------------------------------------
    # Now send the command
    # ----------------------------------------------------------------
    send_command [BuildCommand 0xD4 16  $ber_type \
                                        $burstbyte(0) $burstbyte(1) $burstbyte(2) $burstbyte(3) \
		                        $ber_distrib \
		                        $stdevbyte(0) $stdevbyte(1) \
		                        $berbyte(0) $berbyte(1) $berbyte(2) $berbyte(3) \
		                        $berbyte(4) $berbyte(5) $berbyte(6) $berbyte(7) ]

    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    pong_check
}


######################################################################
# Function Name    : get_BER
# Parameters       : none
# Return Value     : Current bit error rate settings for target
# Purpose          : See discussion above for set_BER for a detailed
#                  :   description of possible return values.
######################################################################
proc get_BER {args} {
    global BER_TYPE
    global STAT_DISTRIB

    send_command [BuildCommand 0xD5 0]
    set ret [lrange [pong] 2 17]

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set type [expr "0x[lindex $ret 0]" + 0]
    if {$type == 0} {
	return "0"
    }

    # ------------------------------------------------------------
    # Get rate 
    # ------------------------------------------------------------
    set berreg(7) "0x[lindex $ret 8  ]"
    set berreg(6) "0x[lindex $ret 9  ]"
    set berreg(5) "0x[lindex $ret 10 ]"
    set berreg(4) "0x[lindex $ret 11 ]"
    set berreg(3) "0x[lindex $ret 12 ]"
    set berreg(2) "0x[lindex $ret 13 ]"
    set berreg(1) "0x[lindex $ret 14 ]"
    set berreg(0) "0x[lindex $ret 15 ]"
    
    set ber_interval 0.0
    for {set i 7} {$i>=0} {incr i -1} {
	set ber_interval  [expr {$ber_interval * 256.0 }]
	set ber_interval  [expr {$ber_interval + $berreg($i)}]
    }
    
    set ber  [BER_interval2rate $ber_interval]
    set berstr [format "%9.2e" $ber]

    # ------------------------------------------------------------
    # Shortcut if no errors
    # ------------------------------------------------------------
    if {$ber == 0} {
	return $berstr
    }

    # ------------------------------------------------------------
    # Convert received type into a string
    # ------------------------------------------------------------
    set type [expr "0x[lindex $ret 0]" + 0]
    # if {[info exists BER_TYPE($type) ] } {
    #	 set berstr "$berstr -$BER_TYPE($type)"
    # } 
    #
    # if {[string compare $BER_TYPE($type) "None"] == 0} {
    # 	set berstr "0"
    # 	return $berstr
    # }

    # ------------------------------------------------------------
    # Get burstlen
    # ------------------------------------------------------------
    set ber_burstlen 1
    if {$type >= 2} {
	set ber_burstlen 0
	for {set i 1} {$i<=4} {incr i} {
	    set ber_burstlen [expr $ber_burstlen << 8]
	    set tmp "0x[lindex $ret $i]"
	    set ber_burstlen [expr $ber_burstlen | $tmp]
	}
	set ber_burstlen [format "%d" $ber_burstlen]
	set berstr "$berstr -burst=$ber_burstlen"

	if {$type == 3} {
	    set berstr "$berstr"
	}
	if {$type == 4} {
	    set berstr "$berstr:PRBS"
	}
	if {$type == 5} {
	    set berstr "$berstr:Ones"
	}
	if {$type == 6} {
	    set berstr "$berstr:Zeroes"
	}
    }
    # ------------------------------------------------------------
    # Get distrib
    # ------------------------------------------------------------
    set tmp [expr "0x[lindex $ret 5]" + 0]
    if { [info exists STAT_DISTRIB($tmp) ] } {
	set ber_distrib "-$STAT_DISTRIB($tmp)"
	set berstr "$berstr $ber_distrib"
    } 

    # ------------------------------------------------------------
    # Get stdev
    # ------------------------------------------------------------
    if {[string compare $ber_distrib "-gaussian"] == 0} {
	set ber_stdev 0
	for {set i 6} {$i<=7} {incr i} {
	    set ber_stdev [expr $ber_stdev << 8]
	    set tmp "0x[lindex $ret $i]"
	    set ber_stdev [expr $ber_stdev | $tmp]
	}
	set ber_stdev [format "%.2f%%" [expr $ber_stdev / 100.0]]
	set berstr "$berstr:$ber_stdev"
    }
	
    # ------------------------------------------------------------
    # uncomment to see return value
    # ------------------------------------------------------------
    return $berstr
}

######################################################################
# Function Name    : set_BER_oneshot
# Parameters       : none
# Return Value     : 
# Purpose          : 
######################################################################
proc set_BER_oneshot {} {
    send_command [BuildCommand 0xD6 0x00]
    pong_check
}



######################################################################
# --------------------------------------------------------------------
# Packet Dropping  commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_packet_drop <value> <options>
#                  : 
# Parameters       : <value> is the desired packet drop rate (e.g. 10
#                  : which means that 1/10 packets will be dropped)
#                  : Specifying a <value> of 0 turns off errors
#                  : 
#                  : <value> can be in the range 1-65536
#                  : 
#                  : <options> can be one or more of the following:
#                  : 
#                  : Error Type options (only for HSFC modes)
#                  : 
#                  :      -replace_by_repeat - replaces dropped packets 
#                  :                           by repeating the codeword
#                  :                           just before SOP. This is 
#                  :                           the desired behavior for 
#                  :                           FC-AL applications
#                  :     
#                  :      -replace_with_idle - replaces dropped packets
#                  :                           with idle control words
#                  :     
#                  : Statistical distribution of packet dropping:
#                  : 
#                  :      -periodic        - non-random (fixed) packet dropping
#                  :      -poisson         - poisson distributed packet dropping
#                  :      -gaussian:<stdev_pct> - gaussian distributed dropping
#                  :      -uniform         - uniformly distributed (random)
#                  : 
#                  : For poisson, gaussian and uniform, the mean drop rate
#                  : is given by <value>. For gaussian distributions, the
#                  : standard deviation is specified as a percentage of the
#                  : mean time between error events (e.g. for packet_drop=100
#                  : and stdev_pct=10%, a six sigma interval would be
#                  : from 0.70 to 1.30 (100-30 to 100+30))
#                  : 
# Return Value     : none
#                  : 
# Purpose          : Sets the packet_drop to be inserted 
######################################################################
proc set_packet_drop {args} {
    global STAT_DISTRIB
    global PKTDROP_REPLACEBY

    set pktdrop_enable      1
    set pktdrop_replaceby   $PKTDROP_REPLACEBY(IDLE)
    set pktdrop_distrib     $STAT_DISTRIB(PERIODIC)
    set pktdrop_stdev       30.00
    set pktdrop_interval    "xxx"

    set cmderrflag   0

    # ----------------------------------------------------------------
    # Parse the command options
    # ----------------------------------------------------------------
    foreach a $args {
	if {[regexp -nocase {^([-+.E0-9]+)$} $a tmp pktdrop_interval]} {
	    # peachy, check interval below
	} \
	elseif {[regexp -nocase {^-enable$} $a]} {
	    set pktdrop_enable 1
	} \
	elseif {[regexp -nocase {^-disable$} $a]} {
	    set pktdrop_enable 0
	} \
	elseif {[regexp -nocase {^-replace_by_repeat$} $a]} {
	    set pktdrop_replaceby $PKTDROP_REPLACEBY(REPEAT)
	} \
	elseif {[regexp -nocase {^-replace_with_idle$} $a]} {
	    set pktdrop_replaceby $PKTDROP_REPLACEBY(IDLE)
	} \
	elseif {[regexp -nocase {^-periodic$} $a ]} {
	    set pktdrop_distrib $STAT_DISTRIB(PERIODIC)
	} \
	elseif {[regexp -nocase {^-poisson$} $a ]} {
	    set pktdrop_distrib $STAT_DISTRIB(POISSON)
	} \
	elseif {[regexp -nocase {^-gaussian:([0-9.]+)%?$} $a tmp pktdrop_stdev]} {
	    set pktdrop_distrib $STAT_DISTRIB(GAUSSIAN)
	} \
	elseif {[regexp -nocase {^-uniform$} $a ]} {
	    set pktdrop_distrib $STAT_DISTRIB(UNIFORM)
	} \
	else {
	    puts "ERROR: set_packet_drop: bad argument '$a'."
	    incr cmderrflag
	}
    }

    # ----------------------------------------------------------------
    # If there were command errors, print usage message
    # ----------------------------------------------------------------
    if {[string compare $pktdrop_interval "xxx"] == 0} {
	puts "ERROR: set_packet_drop: Missing packet drop interval (1/N) <value>"
	incr cmderrflag
    }

    if {$pktdrop_interval < 0} {
	puts "ERROR: set_packet_drop: Bad PKTDROP value $pktdrop_interval"
	return
    }
    if {$pktdrop_interval > 65535} {
        puts "WARNING: set_packet_drop: Setting PKTDROP value to 65535"
        set pktdrop_interval 65535
    }

    if {$cmderrflag} {
	puts "set_packet_drop <value> <options>"
	puts ""
	puts "<value> is the desired packet drop rate (e.g. 10"
	puts "which means that 1/10 packets will be dropped)"
	puts "Specifying a <value> of 0 turns off errors"
	puts ""
	puts "<options> can be one or more of the following:"
	puts ""
	puts "Error Type options (only for HSFC modes)"
	puts ""
	puts "     -replace_by_repeat - replaces dropped packets "
	puts "                          by repeating the codeword"
	puts "                          just before SOP. This is "
	puts "                          the desired behavior for "
	puts "                          FC-AL applications"
	puts "    "
	puts "     -replace_with_idle - replaces dropped packets"
	puts "                          with idle control words"
	puts "    "
	puts "Statistical distribution of packet dropping:"
	puts ""
	puts "     -periodic        - non-random (fixed) packet dropping"
	puts "     -poisson         - poisson distributed packet dropping"
	puts "     -gaussian:stdev_pct - gaussian distributed dropping"
	puts "     -uniform         - uniformly distributed (random)"
	puts ""
	puts "For poisson, gaussian and uniform, the mean drop rate"
	puts "is given by <value>. For gaussian distributions, the"
	puts "standard deviation is specified as a percentage of the"
	puts "mean time between error events (e.g. for packet_drop=100"
	puts "and stdev_pct=10%, a six sigma interval would be"
	puts "from 0.70 to 1.30 (100-30 to 100+30))"
	puts ""
	puts ""
	return
    }

    # ----------------------------------------------------------------
    # if value is 0, set type to None
    # ----------------------------------------------------------------
    if {$pktdrop_interval  == 0} {
	set pktdrop_enable 0
    }

    # ----------------------------------------------------------------
    # break down interval into 2 bytes 
    # ----------------------------------------------------------------
    set tmp $pktdrop_interval
    for {set i 1} {$i>=0} {incr i -1} {
	set intvbyte($i)   [expr ($tmp & 0xFF)]
	set tmp            [expr ($tmp >> 8)]
    }

    # ----------------------------------------------------------------
    # break down pktdrop_stdev into 2 bytes 
    # ----------------------------------------------------------------
    set tmp [expr round($pktdrop_stdev * 100)]
    for {set i 1} {$i>=0} {incr i -1} {
	set stdevbyte($i)  [expr ($tmp & 0xFF)]
	set tmp            [expr ($tmp >> 8)]
    }

    # ----------------------------------------------------------------
    # Now send the command
    # ----------------------------------------------------------------
    send_command [BuildCommand 0xD8 7   $pktdrop_enable \
                                        $pktdrop_replaceby \
		                        $pktdrop_distrib \
		                        $stdevbyte(0) $stdevbyte(1) \
		                        $intvbyte(0) $intvbyte(1) ]
    
    # ----------------------------------------------------------------
    # Wait for computation
    # ----------------------------------------------------------------
    if {$pktdrop_distrib != 1} {
	puts "Computing random numbers .......";
	after 4000
    }
    after 1000

    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    pong_check
}


######################################################################
# Function Name    : get_packet_drop
# Parameters       : none
# Return Value     : Current bit error rate settings for target
# Purpose          : See discussion above for set_BER for a detailed
#                  :   description of possible return values.
######################################################################
proc get_packet_drop {args} {
    global PKTDROP_TYPE
    global STAT_DISTRIB

    send_command [BuildCommand 0xD9 0]
    set ret [lrange [pong] 2 8]

    # ------------------------------------------------------------
    # Get rate 
    # ------------------------------------------------------------
    set pktdrop_interval 0
    for {set i 5} {$i<=6} {incr i} {
	set pktdrop_interval [expr $pktdrop_interval << 8]
	set tmp "0x[lindex $ret $i]"
	set pktdrop_interval [expr $pktdrop_interval | $tmp]
    }
    set pktdropstr "$pktdrop_interval"

    # ------------------------------------------------------------
    # If disabled return quickly
    # ------------------------------------------------------------
    if { $pktdrop_interval == 0 } {
	return 0
    } 

    set tmp [expr "0x[lindex $ret 0]" + 0]
    if { $tmp == 0 } {
	return 0
    } 

    # ------------------------------------------------------------
    # Get distrib
    # ------------------------------------------------------------
    set tmp [expr "0x[lindex $ret 2]" + 0]
    if { [info exists STAT_DISTRIB($tmp) ] } {
	set pktdrop_distrib "-$STAT_DISTRIB($tmp)"
	set pktdropstr "$pktdropstr $pktdrop_distrib"
    } else {
	set pktdrop_distrib ""
    }
    

    # ------------------------------------------------------------
    # Get stdev
    # ------------------------------------------------------------
    if {[string compare $pktdrop_distrib "-gaussian"] == 0} {
	set pktdrop_stdev 0
	for {set i 3} {$i<=4} {incr i} {
	    set pktdrop_stdev [expr $pktdrop_stdev << 8]
	    set tmp "0x[lindex $ret $i]"
	    set pktdrop_stdev [expr $pktdrop_stdev | $tmp]
	}
	set pktdrop_stdev [format "%.2f%%" [expr $pktdrop_stdev / 100.0]]
	set pktdropstr "$pktdropstr:$pktdrop_stdev"
    }
	
    # ------------------------------------------------------------
    # uncomment to see return value
    # ------------------------------------------------------------
    return $pktdropstr
}


######################################################################
# --------------------------------------------------------------------
# Get/Set laser_control modes
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_laserctl_mode
# Parameters       : mode
# Return Value     : none
# Purpose          : sets the laser mode (norm,1,0,squelch)
######################################################################
proc set_laserctl_mode {mode} {
    send_command [BuildCommand 0xDA 0x01 $mode]
    pong_check
}

######################################################################
# Function Name    : get_laserctl_mode
# Parameters       : none
# Return Value     : returns the laserctl mode
# Purpose          : allows the scripts to handle multiple rates
######################################################################
proc get_laserctl_mode {} {
    send_command [BuildCommand 0xDB 0x00]
    return [parse_read_value]
}


######################################################################
# Function Name    : clear_all_alarms
# Parameters       : none
# Return Value     : clears overflow/underflow status
# Purpose          : 
######################################################################
proc clear_all_alarms {} {
    send_command [BuildCommand 0xE4 0x0]
    print_error_on_nack [pong] "Unable to clear alarms."
}

######################################################################
# Function Name    : get_all_alarms
# Parameters       : none
# Return Value     : returns the overflow/underflow status
# Purpose          : 
######################################################################
proc get_all_alarms {} {
    send_command [BuildCommand 0xE5 0x0]
    set ret [lrange [pong] 2 end]

    set b1 "0x[lindex $ret 0]"
    set b2 "0x[lindex $ret 1]"
    set ret [expr ($b1<<8) + $b2]

    set color(0) "GREEN"
    set color(1) "YELLOW"
    set color(2) "RED"

    puts [format "Optics    = %s" $color([expr ($ret>>14)&0x3])]
    puts [format "LOS       = %s" $color([expr ($ret>>12)&0x3])]
    puts [format "LOL       = %s" $color([expr ($ret>>10)&0x3])]
    puts [format "FIFO      = %s" $color([expr ($ret>> 8)&0x3])]
    puts [format "Aligner   = %s" $color([expr ($ret>> 6)&0x3])]
    puts [format "OOF       = %s" $color([expr ($ret>> 4)&0x3])]
    puts [format "Disparity = %s" $color([expr ($ret>> 2)&0x3])]
    puts [format "Codeword  = %s" $color([expr ($ret>> 0)&0x3])]
}

######################################################################
# Function Name    : clear_all_statistics
# Parameters       : none
# Return Value     : clears all HSGE statistics
# Purpose          :  (only for HSGE/GigE mode)
######################################################################
proc clear_all_statistics {} {
    send_command [BuildCommand 0xE6 0x0]
    pong_check
}

######################################################################
# Function Name    : list_to_flt
# Parameters       : a list of hexadecimal byte values
# Return Value     : value of the bytes interpreted big-endian
# Purpose          : Utility function for converting returned values
######################################################################
proc list_to_flt {args} {
    set tot 0.0
    foreach byte [split [lindex $args 0] " " ] {
	set b [expr "0x$byte" + 0]
	set tot [expr $tot * 256.0]
	set tot [expr $tot + $b]
    }
    return $tot
}

######################################################################
# Function Name    : get_all_statistics
# Parameters       : none
# Return Value     : prints all HSGE statistics
# Purpose          :  (only for HSGE/GigE mode)
######################################################################
set hsge_elapsed_seconds 0
set hsge_packet_rx       0
set hsge_packet_drop     0
set hsge_byte_rx         0
set hsge_disparity_err   0
set hsge_codeword_err    0
set hsge_bad_idle        0
set hsge_bad_ipg         0

proc get_all_statistics {} {
    send_command [BuildCommand 0xE7 0x0]
    set ret [lrange [pong] 2 end]

    global hsge_elapsed_seconds
    global hsge_packet_rx      
    global hsge_packet_drop    
    global hsge_byte_rx        
    global hsge_disparity_err  
    global hsge_codeword_err   
    global hsge_bad_idle       
    global hsge_bad_ipg        
    
    set new_elapsed_seconds [list_to_flt [lrange $ret  0  7]]
    set new_packet_rx       [list_to_flt [lrange $ret  8 15]]
    set new_packet_drop     [list_to_flt [lrange $ret 16 23]]
    set new_byte_rx         [list_to_flt [lrange $ret 24 31]]
    set new_disparity_err   [list_to_flt [lrange $ret 32 35]]
    set new_codeword_err    [list_to_flt [lrange $ret 36 39]]
    set new_bad_idle        [list_to_flt [lrange $ret 40 43]]
    set new_bad_ipg         [list_to_flt [lrange $ret 44 47]]

    set inc_elapsed_seconds [expr $new_elapsed_seconds - $hsge_elapsed_seconds ]
    set inc_packet_rx       [expr $new_packet_rx       - $hsge_packet_rx       ]
    set inc_packet_drop     [expr $new_packet_drop     - $hsge_packet_drop     ]
    set inc_byte_rx         [expr $new_byte_rx         - $hsge_byte_rx         ]
    set inc_disparity_err   [expr $new_disparity_err   - $hsge_disparity_err   ]
    set inc_codeword_err    [expr $new_codeword_err    - $hsge_codeword_err    ]
    set inc_bad_idle        [expr $new_bad_idle        - $hsge_bad_idle        ]
    set inc_bad_ipg         [expr $new_bad_ipg         - $hsge_bad_ipg         ]

    set max_bitrate 1000000000

    if {$inc_elapsed_seconds > 0} {
	set inc_bitrate [expr 8.0 * $inc_byte_rx / $inc_elapsed_seconds]
	puts "============================================================"
	puts "Incremental statistics"
	puts "------------------------------------------------------------"
	puts [format "elapsed_seconds = %15.0f" $inc_elapsed_seconds ]
	puts [format "packet_rx       = %15.0f    (%15.0f per sec)" $inc_packet_rx     [expr $inc_packet_rx    /$inc_elapsed_seconds] ]
	puts [format "packet_drop     = %15.0f    (%15.0f per sec)" $inc_packet_drop   [expr $inc_packet_drop  /$inc_elapsed_seconds]]
	puts [format "byte_rx         = %15.0f    (%15.0f per sec)" $inc_byte_rx       [expr $inc_byte_rx      /$inc_elapsed_seconds]]
	puts [format "disparity_err   = %15.0f    (%15.0f per sec)" $inc_disparity_err [expr $inc_disparity_err/$inc_elapsed_seconds]]
	puts [format "codeword_err    = %15.0f    (%15.0f per sec)" $inc_codeword_err  [expr $inc_codeword_err /$inc_elapsed_seconds]]
	puts [format "bad_idle        = %15.0f    (%15.0f per sec)" $inc_bad_idle      [expr $inc_bad_idle     /$inc_elapsed_seconds]]
	puts [format "bad_ipg         = %15.0f    (%15.0f per sec)" $inc_bad_ipg       [expr $inc_bad_ipg      /$inc_elapsed_seconds]]
	puts [format "bitrate           %5.2f%%   (%15.0f bps)" [expr 100.0*$inc_bitrate/$max_bitrate] $inc_bitrate ]
	puts ""
    }

    set hsge_elapsed_seconds $new_elapsed_seconds 
    set hsge_packet_rx       $new_packet_rx       
    set hsge_packet_drop     $new_packet_drop     
    set hsge_byte_rx         $new_byte_rx         
    set hsge_disparity_err   $new_disparity_err   
    set hsge_codeword_err    $new_codeword_err    
    set hsge_bad_idle        $new_bad_idle        
    set hsge_bad_ipg         $new_bad_ipg         

    set bitrate [expr 8.0 * $hsge_byte_rx / $hsge_elapsed_seconds]

    puts "============================================================"
    puts "Total statistics"
    puts "------------------------------------------------------------"
    puts [format "elapsed_seconds = %15.0f" $hsge_elapsed_seconds ]
    puts [format "packet_rx       = %15.0f    (%15.1f per sec)" $hsge_packet_rx     [expr $hsge_packet_rx    /$hsge_elapsed_seconds]]
    puts [format "packet_drop     = %15.0f    (%15.1f per sec)" $hsge_packet_drop   [expr $hsge_packet_drop  /$hsge_elapsed_seconds]]
    puts [format "byte_rx         = %15.0f    (%15.1f per sec)" $hsge_byte_rx       [expr $hsge_byte_rx      /$hsge_elapsed_seconds]]
    puts [format "disparity_err   = %15.0f    (%15.1f per sec)" $hsge_disparity_err [expr $hsge_disparity_err/$hsge_elapsed_seconds]]
    puts [format "codeword_err    = %15.0f    (%15.1f per sec)" $hsge_codeword_err  [expr $hsge_codeword_err /$hsge_elapsed_seconds]]
    puts [format "bad_idle        = %15.0f    (%15.1f per sec)" $hsge_bad_idle      [expr $hsge_bad_idle     /$hsge_elapsed_seconds]]
    puts [format "bad_ipg         = %15.0f    (%15.1f per sec)" $hsge_bad_ipg       [expr $hsge_bad_ipg      /$hsge_elapsed_seconds]]
    puts [format "bitrate         = %5.2f%%   (%15.0f bps)" [expr 100.0*$bitrate/$max_bitrate] $bitrate ]

    puts ""
}


######################################################################
# Function Name    : get_all_settings
# Return Value     : none
# Purpose          : prints all of the current settings
######################################################################
proc get_all_settings {} {
    global BER_TYPE
    global PKTDROP_TYPE
    global STAT_DISTRIB
    global PKTDROP_REPLACEBY

    send_command [BuildCommand 0xE1 0x0]
    set ret [pong]

    puts "-----------------------------------"
    puts "Operating Mode=<[lindex $ret 2],[lindex $ret 3],[lindex $ret 4]>"

    puts "- - - - - - - - - - - - - - - - - -"
    puts "DelMode:          <[lindex $ret 25]>"
    puts "Delay:            [list_to_flt [lrange $ret 5 12]] bits"
    puts "TargPPM:          [list_to_flt [lrange $ret 13 14]]"

    puts "- - - - - - - - - - - - - - - - - -"
    set type [expr 0x[lindex $ret 26] + 0]
    if {[info exists BER_TYPE($type) ] } {
	puts "BERType:          $BER_TYPE($type)"
    } else {
	puts "BERType:          <$type>"
    }

    set ber [BER_interval2rate [list_to_flt [lrange $ret 17 24]]]
    puts "BER:              [format "%8.2e" $ber]"
    puts "BurstLen:         [list_to_flt [lrange $ret 29 32]]"

    set tmp  [expr 0x[lindex $ret 27] + 0]
    if { [info exists STAT_DISTRIB($tmp) ] } {
	puts "Distrib:          $STAT_DISTRIB($tmp)"
    } else {
	puts "Distrib:          <$tmp>"
    }
    puts "StDev:            [expr [list_to_flt [lrange $ret 15 16]]/100]%"

    puts "- - - - - - - - - - - - - - - - - -"
    set tmp [expr 0x[lindex $ret 33] + 0]
    puts "PktDropEnable:    $tmp"

    set tmp [expr 0x[lindex $ret 34] + 0]
    if { [info exists PKTDROP_REPLACEBY($tmp) ] } {
	puts "ReplaceBy:        $PKTDROP_REPLACEBY($tmp)"
    } else {
	puts "ReplaceBy:        <$tmp>"
    }
    
    set tmp  [expr 0x[lindex $ret 35] + 0]
    if { [info exists STAT_DISTRIB($tmp) ] } {
	puts "Distrib:          $STAT_DISTRIB($tmp)"
    } else {
	puts "Distrib:          <$tmp>"
    }
    puts "StDev:            [expr [list_to_flt [lrange $ret 36 37]]/100]%"
    puts "Drop:             1/[expr [list_to_flt [lrange $ret 38 39]]]"

    puts "- - - - - - - - - - - - - - - - - -"
    puts "LaserCtl:         [lindex $ret 28]"
    puts "-----------------------------------"
}

######################################################################
# Function Name    : get_all_status
# Return Value     : none
# Purpose          : prints current status
######################################################################
proc get_all_status {} {
    display_all_status 0
}

######################################################################
# Function Name    : pd_get_all_status
# Return Value     : none
# Purpose          : prints current PD status
######################################################################
proc pd_get_all_status {} {
    display_all_status 1
}

######################################################################
# Function Name    : display_all_status
# Parameter        : is_pd (1 if we're printing PD status, 0 if not)
# Return Value     : none
# Purpose          : prints all of the current statistics (alarms)
######################################################################
proc display_all_status {{is_pd 0}} {
    send_command [BuildCommand 0xE3 0x0]
    set ret [pong]

    puts "-----------------------------------"
    if {!$is_pd} {
        puts "Delay:            [list_to_flt [lrange $ret 2 9]] bits"
        puts "PPM:              [list_to_flt [lrange $ret 10 11]]"
    }
    set tmp [lindex $ret 12]
    puts "Status Flags:     <0x$tmp>"
    set tmp [expr 0x$tmp + 0]
    if {$tmp & (1<<6)} {
	puts "                  <OPTICS MISSING/NOT READY>"
    }
    if {$tmp & (1<<5)} {
	puts "                  <LASER ON>"
    } else {
	puts "                  <LASER OFF>"
    }
    if {$tmp & (1<<4)} {
	puts "                  <LOS>"
    }
    if {$tmp & (1<<3)} {
	puts "                  <RxLOL>"
    }
    if {$tmp & (1<<2)} {
	puts "                  <TxLOL>"
    }
    if {$tmp & (1<<1)} {
	puts "                  <OVERFLOW>"
    }
    if {$tmp & (1<<0)} {
	puts "                  <UNDERFLOW>"
    }
    puts "FPGA Temp:        [format "%-d C" 0x[lindex $ret 13]]"
    if {$tmp & (1<<6)} {
        puts "XFP  Temp:        N/A"
    } else {
        puts "XFP  Temp:        [format "%-d C" 0x[lindex $ret 14]]"
    }
    puts "-----------------------------------"
}




######################################################################
# --------------------------------------------------------------------
# Delay Conversion Commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : delay_ns2bits
# Parameters       : value in ns
# Return Value     : value in bits
# Purpose          : Converts delay in ns units to bits
######################################################################
proc delay_ns2bits {ns} {
    global FC10X_BITS_PER_NS
    global FC10X_FEC11317_BITS_PER_NS
    global FC10X_FEC11270_BITS_PER_NS 
    global XGELAN_BITS_PER_NS
    global XGELAN_11049_BITS_PER_NS
    global XGELAN_11096_BITS_PER_NS
    global OTU1_BITS_PER_NS
    global OTU2_BITS_PER_NS
    global OC192_BITS_PER_NS
    global OC48_BITS_PER_NS
    global OC12_BITS_PER_NS
    global OC3_BITS_PER_NS
    global GE_BITS_PER_NS
    global GEM100M_BITS_PER_NS
    global GEM10M_BITS_PER_NS
    global GEM_BITS_PER_NS
    global FC1X_BITS_PER_NS
    global FC2X_BITS_PER_NS
    global FC4X_BITS_PER_NS
    global FC8X_BITS_PER_NS

    global CPRI_O24_BITS_PER_NS
    global CPRI_O12_BITS_PER_NS
    global CPRI_O6_BITS_PER_NS
    
    global BITRATE_OC3
    global BITRATE_OC12
    global BITRATE_OC48
    global BITRATE_GE
    global BITRATE_FC1X
    global BITRATE_FC2X
    global BITRATE_FC4X
    global BITRATE_FC8X
    global BITRATE_OC192
    global BITRATE_OTU1
    global BITRATE_OTU2
    global BITRATE_XGELAN
    global BITRATE_XGELAN_11049FEC
    global BITRATE_XGELAN_11096FEC
    global BITRATE_XGEWAN
    global BITRATE_XGEWAN_FEC
    global BITRATE_FC10X
    global BITRATE_FC10X_FEC11317
    global BITRATE_FC10X_FEC11270
    global BITRATE_GE100M
    global BITRATE_GE10M

    global BITRATE_CPRI_O24
    global BITRATE_CPRI_O12
    global BITRATE_CPRI_O6
    
    global MODE_GEM

    set operating_mode [get_operating_mode]

    set opmode  "0x[lindex $operating_mode 0]"
    set bitrate "0x[lindex $operating_mode 1]"
    if {$bitrate == $BITRATE_FC10X} {
	return  [expr {floor (($ns * $FC10X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC10X_FEC11317} {
	return  [expr {floor (($ns * $FC10X_FEC11317_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC10X_FEC11270} {
	return  [expr {floor (($ns * $FC10X_FEC11270_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGELAN} {
	return  [expr {floor (($ns * $XGELAN_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGELAN_11049FEC} {
	return  [expr {floor (($ns * $XGELAN_11049_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGELAN_11096FEC} {
	return  [expr {floor (($ns * $XGELAN_11096_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OTU1} {
	return  [expr {floor (($ns * $OTU1_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OTU2} {
	return  [expr {floor (($ns * $OTU2_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OC192} {
	return  [expr {floor (($ns * $OC192_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGEWAN} {
	return  [expr {floor (($ns * $OC192_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGEWAN_FEC} {
	return  [expr {floor (($ns * $OTU2_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OC48} {
	return  [expr {floor (($ns * $OC48_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OC12} {
	return  [expr {floor (($ns * $OC12_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OC3} {
	return  [expr {floor (($ns * $OC3_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_GE && $opmode != $MODE_GEM} {
	return  [expr {floor (($ns * $GE_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_GE100M && $opmode == $MODE_GEM} {
	return  [expr {floor (($ns * $GEM100M_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_GE10M && $opmode == $MODE_GEM} {
	return  [expr {floor (($ns * $GEM10M_BITS_PER_NS)+0.5)}]
    } elseif {$opmode == $MODE_GEM} {
	return  [expr {floor (($ns * $GEM_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC1X} {
	return  [expr {floor (($ns * $FC1X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC2X} {
	return  [expr {floor (($ns * $FC2X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC4X} {
	return  [expr {floor (($ns * $FC4X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC8X} {
	return  [expr {floor (($ns * $FC8X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_CPRI_O24} {
	return  [expr {floor (($ns * $CPRI_O24_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_CPRI_O12} {
	return  [expr {floor (($ns * $CPRI_O12_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_CPRI_O6} {
	return  [expr {floor (($ns * $CPRI_O6_BITS_PER_NS)+0.5)}]
    } else {
	puts "WARNING: target returned invalid code for bit rate"
	return  [expr {floor (($ns * $OC48_BITS_PER_NS)+0.5)}]
    }
    
}

######################################################################
# Function Name    : delay_bits2ns
# Parameters       : value in bits
# Return Value     : value in ns
# Purpose          : Converts delay in bits units to ns
######################################################################
proc delay_bits2ns {bits} {
    global FC10X_BITS_PER_NS
    global FC10X_FEC11317_BITS_PER_NS
    global FC10X_FEC11270_BITS_PER_NS 
    global XGELAN_BITS_PER_NS
    global XGELAN_11049_BITS_PER_NS
    global XGELAN_11096_BITS_PER_NS
    global OTU1_BITS_PER_NS
    global OTU2_BITS_PER_NS
    global OC192_BITS_PER_NS
    global OC48_BITS_PER_NS
    global OC12_BITS_PER_NS
    global OC3_BITS_PER_NS
    global GE_BITS_PER_NS
    global GEM100M_BITS_PER_NS
    global GEM10M_BITS_PER_NS
    global GEM_BITS_PER_NS
    global FC1X_BITS_PER_NS
    global FC2X_BITS_PER_NS
    global FC4X_BITS_PER_NS
    global FC8X_BITS_PER_NS

    global CPRI_O24_BITS_PER_NS
    global CPRI_O12_BITS_PER_NS
    global CPRI_O6_BITS_PER_NS
    
    global BITRATE_OC3
    global BITRATE_OC12
    global BITRATE_OC48
    global BITRATE_GE
    global BITRATE_FC1X
    global BITRATE_FC2X
    global BITRATE_FC4X
    global BITRATE_FC8X
    global BITRATE_OC192
    global BITRATE_OTU1
    global BITRATE_OTU2
    global BITRATE_XGELAN
    global BITRATE_XGELAN_11049FEC
    global BITRATE_XGELAN_11096FEC
    global BITRATE_XGEWAN
    global BITRATE_XGEWAN_FEC
    global BITRATE_FC10X
    global BITRATE_FC10X_FEC11317
    global BITRATE_FC10X_FEC11270
    global BITRATE_GE100M
    global BITRATE_GE10M

    global BITRATE_CPRI_O24
    global BITRATE_CPRI_O12
    global BITRATE_CPRI_O6
    
    global MODE_GEM

    set operating_mode [get_operating_mode]

    set opmode  "0x[lindex $operating_mode 0]"
    set bitrate "0x[lindex $operating_mode 1]"

    if {$bitrate == $BITRATE_FC10X} {
	return  [expr {floor (($bits/$FC10X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC10X_FEC11317} {
	return  [expr {floor (($bits/$FC10X_FEC11317_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC10X_FEC11270} {
	return  [expr {floor (($bits/$FC10X_FEC11270_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGELAN} {
	return  [expr {floor (($bits/$XGELAN_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGELAN_11049FEC} {
	return  [expr {floor (($bits/$XGELAN_11049_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGELAN_11096FEC} {
	return  [expr {floor (($bits/$XGELAN_11096_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OTU1} {
	return  [expr {floor (($bits/$OTU1_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OTU2} {
	return  [expr {floor (($bits/$OTU2_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGEWAN} {
	return  [expr {floor (($bits/$OC192_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_XGEWAN_FEC} {
	return  [expr {floor (($bits/$OTU2_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OC192} {
	return  [expr {floor (($bits/$OC192_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OC48} {
	return  [expr {floor (($bits/$OC48_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OC12} {
	return  [expr {floor (($bits/$OC12_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_OC3} {
	return  [expr {floor (($bits/$OC3_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_GE && $opmode != $MODE_GEM} {
	return  [expr {floor (($bits/$GE_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_GE100M && $opmode == $MODE_GEM} {
	return  [expr {floor (($bits/$GEM100M_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_GE10M && $opmode == $MODE_GEM} {
	return  [expr {floor (($bits/$GEM10M_BITS_PER_NS)+0.5)}]
    } elseif {$opmode == $MODE_GEM} {
	return  [expr {floor (($bits/$GEM_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC1X} {
	return  [expr {floor (($bits/$FC1X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC2X} {
	return  [expr {floor (($bits/$FC2X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC4X} {
	return  [expr {floor (($bits/$FC4X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_FC8X} {
	return  [expr {floor (($bits/$FC8X_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_CPRI_O24} {
	return  [expr {floor (($bits / $CPRI_O24_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_CPRI_O12} {
	return  [expr {floor (($bits / $CPRI_O12_BITS_PER_NS)+0.5)}]
    } elseif {$bitrate == $BITRATE_CPRI_O6} {
	return  [expr {floor (($bits / $CPRI_O6_BITS_PER_NS)+0.5)}]
    } else {
	puts "WARNING: target returned invalid code for bit rate"
	return  [expr {floor (($bits/$OC48_BITS_PER_NS)+0.5)}]
    }
}

######################################################################
# Function Name    : delay_meters2ns
# Parameters       : value in meters
# Return Value     : value in ns
# Purpose          : Converts delay in meters units to ns
######################################################################
proc delay_meters2ns {meters} {
    global FIBER_VELOCITY_FACTOR
    global SPEED_OF_LIGHT_METERS_PER_NS
    return [expr {$meters/($FIBER_VELOCITY_FACTOR * $SPEED_OF_LIGHT_METERS_PER_NS)}]
}

######################################################################
# Function Name    : delay_ns2meters
# Parameters       : value in ns
# Return Value     : value in meters
# Purpose          : Converts delay in ns units to meters
######################################################################
proc delay_ns2meters {ns} {
    global FIBER_VELOCITY_FACTOR
    global SPEED_OF_LIGHT_METERS_PER_NS
    return [expr {$FIBER_VELOCITY_FACTOR * $SPEED_OF_LIGHT_METERS_PER_NS * $ns}]
}

######################################################################
# Function Name    : delay_convert
# Parameters       : del old_units new_units
# Return Value     : converted delay value
# Purpose          : Converts delay in any units to any other units
######################################################################
proc delay_convert {del old_units new_units} {

    # ------------------------------------------------------------
   if {! [string compare -nocase $old_units "ms"] } {
	set del [expr $del * 1000000.0]
	set del [delay_ns2bits $del]
    } \
    elseif {! [string compare -nocase $old_units "us"] } {
        set del [expr $del * 1000.0]
        set del [delay_ns2bits $del]
    } \
    elseif {! [string compare -nocase $old_units "ns"] } {
        set del [delay_ns2bits $del]
    } \
    elseif {! [string compare -nocase $old_units "km"] } {
        set del [expr $del * 1000.0]
        set del [delay_meters2ns $del]
        set del [delay_ns2bits $del]
    } \
    elseif {! [string compare -nocase $old_units "meters"] } {
        set del [delay_meters2ns $del]
        set del [delay_ns2bits $del]
    } \
    elseif {! [string compare -nocase $old_units "m"] } {
        set del [delay_meters2ns $del]
        set del [delay_ns2bits $del]
    } \
    elseif {! [string compare -nocase $old_units "bits"] } {
        # nop
    } \
    elseif {! [string compare $old_units "b"] } {
        # nop
    } \
    elseif {! [string compare -nocase $old_units "bytes"] } {
        set del [expr $del * 8.0]
    } \
    elseif {! [string compare $old_units "B"] } {
        set del [expr $del * 8.0]
    } \
    elseif {! [string compare -nocase $old_units "words"] } {
        set del [expr $del * 16.0]
    } \
    else {
        puts "ERROR: Unrecognized units: '$old_units': need ms,us,ns,km,m,meters,bits,b,bytes,B"
        return 0
    }

    # ------------------------------------------------------------
    if {! [string compare -nocase $new_units "ms"] } {
	set del [delay_bits2ns $del]
	set del [expr $del / 1000000.0]
	set del [format "%-11.7f" $del]
    } \
    elseif {! [string compare -nocase $new_units "us"] } {
        set del [delay_bits2ns $del]
        set del [expr $del / 1000.0]
        set del [format "%-11.4f" $del]
    } \
    elseif {! [string compare -nocase $new_units "ns"] } {
        set del [delay_bits2ns $del]
        set del [format "%-11.1f" $del]
    } \
    elseif {! [string compare -nocase $new_units "km"] } {
        set del [delay_bits2ns $del]
        set del [delay_ns2meters $del]
        set del [expr $del / 1000.0]
        set del [format "%-11.3f" $del]
    } \
    elseif {! [string compare -nocase $new_units "meters"] } {
        set del [delay_bits2ns $del]
        set del [delay_ns2meters $del]
        set del [format "%-11.0f" $del]
    } \
    elseif {! [string compare -nocase $new_units "m"] } {
        set del [delay_bits2ns $del]
        set del [delay_ns2meters $del]
        set del [format "%-11.0f" $del]
    } \
    elseif {! [string compare -nocase $new_units "bits"] } {
        # nop
    } \
    elseif {! [string compare $new_units "b"] } {
        # nop
    } \
    elseif {! [string compare -nocase $new_units "bytes"] } {
        set del [expr $del / 8.0]
        set del [format "%-11.1f" $del]
    } \
    elseif {! [string compare $new_units "B"] } {
        set del [expr $del / 8.0]
        set del [format "%-11.1f" $del]
    } \
    elseif {! [string compare -nocase $new_units "words"] } {
        set del [expr $del / 16.0]
        set del [format "%-11.1f" $del]
    } \
    else {
        puts "ERROR: Unrecognized units: '$new_units': need ms,us,ns,km,m,meters,bits,b,bytes,B"
        return 0
    }
    
    return $del
}


######################################################################
# --------------------------------------------------------------------
# BER Rate to interval conversions
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : BER_rate2interval
# Parameters       : ber, bits_per_count
# Return Value     : interval
# Purpose          : convert bit error rate to interval
######################################################################
proc BER_rate2interval {ber} {
    global BER_MAX_INTERVAL
    
    if {$ber == 0.0} {
	return 0.0
    } elseif {$ber < 0.0} {
	return 0.0
    }
    
    set interval [expr 1.0/($ber)]
    
    if {$interval > $BER_MAX_INTERVAL} {
	set interval $BER_MAX_INTERVAL
    } elseif {$interval <= 1.0} { 
	return 1.0
    }
    return $interval
}

######################################################################
# Function Name    : BER_interval2rate
# Parameters       : interval bits_per_count
# Return Value     : rate
# Purpose          : convert bit error rate to interval
######################################################################
proc BER_interval2rate {interval} {
    global BER_MAX_INTERVAL
    
    if {$interval > $BER_MAX_INTERVAL} {
	set interval $BER_MAX_INTERVAL
    } elseif {$interval <= 1.0} { 
	return 0
    }
    
    set ber [expr 1.0/($interval)]
    
    if {$ber == 0.0} {
	return 0.0
    } elseif {$ber < 0.0} {
	return 0.0
    }
    
    return $ber
}

######################################################################
#  definitions of constant values for BER settings & calculations
######################################################################
set 	 HSPD_BER_BITS_PER_CNT 	       32
set 	 HSPD_BER_MAX_INTERVAL 	       [expr {(65536.0 * 65536.0 * 256.0)-1.0}]

######################################################################
#  definitions of predefined payload structure types
######################################################################
set 	 PAYLOAD_STRUCTURE_STS192C	6
set 	 PAYLOAD_STRUCTURE_STS48C	0
set 	 PAYLOAD_STRUCTURE_STS12C	1
set 	 PAYLOAD_STRUCTURE_STS3C	2
set 	 PAYLOAD_STRUCTURE_STS1		3

######################################################################
# Definitions of expected concat values
######################################################################
set 	 EXCONC_LOP   			0                 
set 	 EXCONC_AIS   			1
set 	 EXCONC_NORM  			2
set 	 EXCONC_CONC  			3

set      EXCONC_OC192_STS192C [list $EXCONC_NORM \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			       \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC \
			     	    $EXCONC_CONC ]

set      EXCONC_OC192_STS48C [list $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC ]

set      EXCONC_OC192_STS12C [list $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC ]

set      EXCONC_OC192_STS3C  [list $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC \
			     	   $EXCONC_NORM \
			     	   $EXCONC_CONC \
			     	   $EXCONC_CONC ]

set      EXCONC_OC192_STS1   [list $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			      \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM \
			     	   $EXCONC_NORM ]

set      EXCONC_OC48_STS48C [list $EXCONC_NORM \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC \
			     	  $EXCONC_CONC ]

set      EXCONC_OC48_STS12C [list $EXCONC_NORM \
			     	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
 \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
 \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
 \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC ]

set      EXCONC_OC48_STS3C  [list $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
 \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
 \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
 \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC ]

set      EXCONC_OC48_STS1  [list  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
 \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
 \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
 \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM ]

set      EXCONC_OC12_STS12C [list $EXCONC_NORM \
			     	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC ]

set      EXCONC_OC12_STS3C  [list $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC \
		             	  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC ]

set      EXCONC_OC12_STS1  [list  $EXCONC_NORM \
		                  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM \
		            	  $EXCONC_NORM ]

set      EXCONC_OC3_STS3C  [list  $EXCONC_NORM \
		             	  $EXCONC_CONC \
		             	  $EXCONC_CONC ]

set      EXCONC_OC3_STS1  [list   $EXCONC_NORM \
		                  $EXCONC_NORM \
		            	  $EXCONC_NORM ]



######################################################################
# --------------------------------------------------------------------
# Get/Set operating mode tuple (mode,bitrate,autosense)
# --------------------------------------------------------------------
######################################################################


######################################################################
# --------------------------------------------------------------------
# Set/get delay  and payload structure routines
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_payload_structure
#                  : 
# Parameters       : payload structure, which has values as follows:
#                  :     $PAYLOAD_STRUCTURE_STS192C	6
#                  :     $PAYLOAD_STRUCTURE_STS48C	0
#                  :     $PAYLOAD_STRUCTURE_STS12C	1
#                  :     $PAYLOAD_STRUCTURE_STS3C	2
#                  :     $PAYLOAD_STRUCTURE_STS1	3
#                  : 
# Return Value     : None
#                  : 
# Purpose          : Set the payload structure
######################################################################
proc set_payload_structure {structure} {
    send_command [BuildCommand 0xC0 0x1 [expr $structure & 7]]
    pong_check
}


######################################################################
# Function Name    : get_payload_structure
#                  : 
# Return Value     : payload structure, which has values as follows:
#                  :     $PAYLOAD_STRUCTURE_STS192C	6
#                  :     $PAYLOAD_STRUCTURE_STS48C	0
#                  :     $PAYLOAD_STRUCTURE_STS12C	1
#                  :     $PAYLOAD_STRUCTURE_STS3C	2
#                  :     $PAYLOAD_STRUCTURE_STS1	3
#                  : 
# Purpose          : Get the current payload structure
######################################################################
proc get_payload_structure {} {
    send_command [BuildCommand 0xC1 0x0]
    return [parse_read_value]
}

######################################################################
# Function Name    : set_exconc_track
#                  : 
# Parameters       : track (0 or 1)
#                  : 
# Return Value     : None
#                  : 
# Purpose          : enables or disables the behavior of the exconc
#                  : to track the recieved conc.
######################################################################
proc set_exconc_track {track} {
    if {($track != 0) && ($track != 1)} {
	puts "ERROR: set_exconc_track argument ($track) must be 0 or 1"
	return
    }

    send_command [BuildCommand 0xC4 0x1 $track]
    pong_check
}

######################################################################
# Function Name    : get_exconc_track
#                  : 
# Return Value     : status of whether expected concat tracks Rx conc
#                  : 
# Purpose          : Get the current payload structure
######################################################################
proc get_exconc_track {} {
    send_command [BuildCommand 0xC5 0x0]
    return [parse_read_value]
}





######################################################################
# Function Name    : set_path_delay
#                  : 
# Parameters       : ts, del, units
#                  : For concatenated payloads, set delay for the 
#                  : first (Norm) STS of the group. Concatenated
#                  :   timeslots will automatically follow. Valid
#                  :   values for ts are as follows:
#                  :      - for STS-48c:  ts=1      
#                  :      - for STS-12c:  ts=1,13,25,37
#                  :      - for STS-3c:   ts=1,4,7,10,13,16,19,22,25,28,...,46
#                  :      - for STS-1:    1<=ts<=48
#                  :      - for mixed payloads: ts must be the first (NORM) 
#                  :                        timeslot
#                  : 
#                  : del   is a numeric value
#                  : 
#                  : units is one of ms,us,ns,km,meters,m,b,bytes
#                  :   if units is omitted, "ms" is the default
#                  : 
# Return Value     : none
#                  : 
# Purpose          : Set the delay of a timeslot
#                  : 
# Note             : We say that delay is measured in "bytes" 
#                  :  but it is actually more correct to say that
#                  :  delay setting is in units of SONET/SDH pointer
#                  :  position, so that one unit of delay is nominally
#                  :  equal to the transmission time of one byte of
#                  :  data at an STS-1/STM-0 rate, which is 154.32ns
#                  :  (8/51.84MHz).
#                  :
#                  : The above paragraph is true for small delay values,
#                  :  in particular when the delay does not move the
#                  :  J1 byte of the payload past a row boundary.
#                  :  However, for large delay values there is a
#                  :  slight difference between the actual time delay
#                  :  and the simplistic conversion factor (154.32ns)
#                  :  described above. This difference is due to the
#                  :  TOH (transport overhead bytes) that are added to
#                  :  each row of the payload to create an STS-1
#                  :  frame.  There are 27 TOH bytes and 783 payload
#                  :  bytes in a frame, making the total number of
#                  :  bytes in an STS-1 frame equal to 810 (27+783).
#                  :
#                  : Therefore, the aggregate delay per pointer position
#                  :  is actually 154.32ns multiplied by the ratio of
#                  :  total bytes/payload bytes (810/783), which gives
#                  :  a conversion factor of 159.64ns.  For small
#                  :  values of delay, the ~5ns difference is not
#                  :  appreciable; it is only 3.4%. But for large
#                  :  delay values, like a whole frame, the difference
#                  :  is noticeable because the simplistic conversion
#                  :  doesn't result in "nice" round time values that most
#                  :  users expect. For example there are exactly 8
#                  :  SONET/SDH frames per millisecond so it is
#                  :  preferable for a delay of 6264 (8 * 783) "bytes"
#                  :  to be equal to exactly 1 ms.
#                  :
######################################################################
proc set_path_delay {ts del {units "ms"}} {
    global LCD_DISPLAY_UNITS_TIME     	
    global LCD_DISPLAY_UNITS_LENGTH   	
    global LCD_DISPLAY_UNITS_BYTES     	

    set  LCD_DISPLAY_UNITS(ms) 	   $LCD_DISPLAY_UNITS_TIME
    set  LCD_DISPLAY_UNITS(us) 	   $LCD_DISPLAY_UNITS_TIME
    set  LCD_DISPLAY_UNITS(ns) 	   $LCD_DISPLAY_UNITS_TIME
    set  LCD_DISPLAY_UNITS(km) 	   $LCD_DISPLAY_UNITS_LENGTH
    set  LCD_DISPLAY_UNITS(m)  	   $LCD_DISPLAY_UNITS_LENGTH
    set  LCD_DISPLAY_UNITS(meters) $LCD_DISPLAY_UNITS_LENGTH
    set  LCD_DISPLAY_UNITS(bytes)  $LCD_DISPLAY_UNITS_BYTES
    set  LCD_DISPLAY_UNITS(b)      $LCD_DISPLAY_UNITS_BYTES

    puts "set_path_delay $ts $del $units"

    set del [pd_delay_convert $del $units "bytes"]
    if { [info exists LCD_DISPLAY_UNITS($units) ] } {
	set_lcd_display_units $LCD_DISPLAY_UNITS($units)
    }

    set H  [expr ($del>>16) & 0xFF]
    set M  [expr ($del>>8)  & 0xFF]
    set L  [expr ($del>>0)  & 0xFF]

    set ts [expr $ts & 0xFF]

    send_command [BuildCommand 0xC6 0x4 $ts $H $M $L]
    pong_check
}

######################################################################
# Function Name    : set_all_path_delays
#                  : 
# Return Value     : none
#                  : 
# Purpose          : This function is identical to set_path_delay, except
#                  :  it sets the specified delay on EVERY path.
#                  : 
#                  :
######################################################################
proc set_all_path_delays {del {units "ms"}} {
    global LCD_DISPLAY_UNITS_TIME     	
    global LCD_DISPLAY_UNITS_LENGTH   	
    global LCD_DISPLAY_UNITS_BYTES     	

    set  LCD_DISPLAY_UNITS(ms) 	   $LCD_DISPLAY_UNITS_TIME
    set  LCD_DISPLAY_UNITS(us) 	   $LCD_DISPLAY_UNITS_TIME
    set  LCD_DISPLAY_UNITS(ns) 	   $LCD_DISPLAY_UNITS_TIME
    set  LCD_DISPLAY_UNITS(km) 	   $LCD_DISPLAY_UNITS_LENGTH
    set  LCD_DISPLAY_UNITS(m)  	   $LCD_DISPLAY_UNITS_LENGTH
    set  LCD_DISPLAY_UNITS(meters) $LCD_DISPLAY_UNITS_LENGTH
    set  LCD_DISPLAY_UNITS(bytes)  $LCD_DISPLAY_UNITS_BYTES
    set  LCD_DISPLAY_UNITS(b)      $LCD_DISPLAY_UNITS_BYTES

    puts "set_all_path_delays $del $units"

    set del [pd_delay_convert $del $units "bytes"]
    if { [info exists LCD_DISPLAY_UNITS($units) ] } {
	set_lcd_display_units $LCD_DISPLAY_UNITS($units)
    }

    set H  [expr ($del>>16) & 0xFF]
    set M  [expr ($del>>8)  & 0xFF]
    set L  [expr ($del>>0)  & 0xFF]

    send_command [BuildCommand 0xA7 0x3 $H $M $L]
    pong_check
}

######################################################################
# Function Name    : get_path_delay
#                  : 
# Parameters       : ts (1<=ts<=48)
#                  : 
#                  : For concatenated payloads, get delay for the 
#                  :   first (Norm) STS of the group. The Concatenated
#                  :   timeslots will automatically follow. Valid
#                  :   values for ts are as follows:
#                  :      - for STS-48c:  ts=1      
#                  :      - for STS-12c:  ts=1,13,25,37
#                  :      - for STS-3c:   ts=1,4,7,10,13,16,19,22,25,28,...,46
#                  :      - for STS-1:    1<=ts<=48
#                  : 
#                  : units is one of ms,us,ns,km,meters,m,b,bytes
#                  :   if units is omitted, "ms" is the default
#                  : 
# Return Value     : numeric delay value in the selected units
#                  : 
# Purpose          : Get the delay of a tsannel
#                  : 
# Note:            : See discussion under set_path_delay/get_path_delay for
#                  :  a detailed description of time and distance units
######################################################################
proc get_path_delay {ts {units "ms"}} {
    set ts [expr $ts & 0xFF]

    send_command [BuildCommand 0xC7 0x1 $ts]
    set ret [lrange [pong] 2 4]
    set ret [format "0x%2.2X%2.2X%2.2X" "0x[lindex $ret 0]" \
                                        "0x[lindex $ret 1]" \
                                        "0x[lindex $ret 2]" ]
    set del [expr 0 + $ret]

    set del [pd_delay_convert $del "bytes" $units]

    return $del
}

######################################################################
# Function Name    : delay_ms2bytes
# Parameters       : value in ms
# Return Value     : value in bytes
# Purpose          : Converts delay in ms units to bytes
# Note:            : See discussion under set_path_delay/get_path_delay for
#                  :  additional information on this conversion
######################################################################
proc delay_ms2bytes {ms} {
    return [expr round ($ms * 1691280.0/270.0)]
}

######################################################################
# Function Name    : delay_bytes2ms
# Parameters       : value in bytes
# Return Value     : value in ms
# Purpose          : Converts delay in bytes to ms units 
# Note:            : See discussion under set_path_delay/get_path_delay for
#                  :  additional information on this conversion
######################################################################
proc delay_bytes2ms {bytes} {
    return [expr ($bytes * 270.0)/1691280.0]
}

######################################################################
# Function Name    : set_lcd_display_units
# Parameters       : $type (0=TIME, 1=LENGTH, 2=BITS)
# Return Value     : none
# Purpose          : Sets the type of units displayed in LCD status
######################################################################
proc set_lcd_display_units {type} {
    send_command [BuildCommand 0xD2 0x01 $type]
    pong_check
}

######################################################################
# Function Name    : pd_delay_convert
# Parameters       : del old_units new_units
# Return Value     : converted delay value
# Purpose          : Converts delay in any units to any other units
######################################################################
proc pd_delay_convert {del old_units new_units} {

    # ------------------------------------------------------------
    if {! [string compare -nocase $old_units "ms"] } {
	set del [delay_ms2bytes $del]
    } \
    elseif {! [string compare -nocase $old_units "us"] } {
	set del [expr $del / 1000.0]
	set del [delay_ms2bytes $del]
    } \
    elseif {! [string compare -nocase $old_units "ns"] } {
	set del [expr $del / 1000000.0]
	set del [delay_ms2bytes $del]
    } \
    elseif {! [string compare -nocase $old_units "km"] } {
	set del [expr $del * 1000.0]
	set del [delay_meters2ns $del]
	set del [expr $del / 1000000.0]
	set del [delay_ms2bytes $del]
    } \
    elseif {! [string compare -nocase $old_units "meters"] } {
	set del [delay_meters2ns $del]
	set del [expr $del / 1000000.0]
	set del [delay_ms2bytes $del]
    } \
    elseif {! [string compare -nocase $old_units "m"] } {
	set del [delay_meters2ns $del]
	set del [expr $del / 1000000.0]
	set del [delay_ms2bytes $del]
    } \
    elseif {! [string compare -nocase $old_units "bytes"] } {
	# nop
    } \
    elseif {! [string compare -nocase $old_units "b"] } {
	# nop
    } \
    else {
	puts "ERROR: Unrecognized units: '$old_units': need ms,us,ns,km,m,meters,b,bytes"
	return 0
    }

    # ------------------------------------------------------------
    if {! [string compare -nocase $new_units "ms"] } {
	set del [format "%-9.5f" [delay_bytes2ms $del]]
    } \
    elseif {! [string compare -nocase $new_units "us"] } {
	set del [delay_bytes2ms $del]
	set del [expr $del * 1000]
	set del [format "%-9.2f" $del]
    } \
    elseif {! [string compare -nocase $new_units "ns"] } {
	set del [delay_bytes2ms $del]
	set del [expr $del * 1000000.0]
	set del [format "%-10.0f" $del]
    } \
    elseif {! [string compare -nocase $new_units "km"] } {
	set del [delay_bytes2ms $del]
	set del [expr $del * 1000000.0]
	set del [delay_ns2meters $del]
	set del [expr $del / 1000.0]
	set del [format "%-9.3f" $del]
    } \
    elseif {! [string compare -nocase $new_units "meters"] } {
	set del [delay_bytes2ms $del]
	set del [expr $del * 1000000.0]
	set del [delay_ns2meters $del]
	set del [format "%-9.0f" $del]
    } \
    elseif {! [string compare -nocase $new_units "m"] } {
	set del [delay_bytes2ms $del]
	set del [expr $del * 1000000.0]
	set del [delay_ns2meters $del]
	set del [format "%-9.0f" $del]
    } \
    elseif {! [string compare -nocase $new_units "bytes"] } {
	# nop
    } \
    elseif {! [string compare -nocase $new_units "b"] } {
	# nop
    } \
    else {
	puts "ERROR: Unrecognized units: '$new_units': need ms,us,ns,km,m,meters,b,bytes"
	return 0
    }

    return $del
}



######################################################################
# Function Name    : force_inc
#                  : 
# Description      : Forces increments on a timeslot with a given
#                  :   repeat count and spacing
#                  : 
# Parameters       : ts, repeat, interval
#                  : 
#                  : ts        (1<=ts<=48)
#                  : repeat    (0<=repeat<=65535)
#                  : interval  (0<=interval<=65535)
#                  : 
#                  : For concatenated payloads, force increments for the 
#                  :   first (Norm) STS of the group. The Concatenated
#                  :   timeslots will automatically follow. Valid
#                  :   values for ts are as follows:
#                  :      - for STS-48c:  ts=1      
#                  :      - for STS-12c:  ts=1,13,25,37
#                  :      - for STS-3c:   ts=1,4,7,10,13,16,19,22,25,28,...,46
#                  :      - for STS-1:    1<=ts<=48
#                  : 
# Return Value     : None
#                  : 
######################################################################
proc force_inc {ts repeat interval} {
    puts "INC TS\#$ts INTERVAL=$interval REPEAT=$repeat"

    set rH  [expr ($repeat>>8) 	 & 0xFF]
    set rL  [expr ($repeat>>0) 	 & 0xFF]
    set iH  [expr ($interval>>8) & 0xFF]
    set iL  [expr ($interval>>0) & 0xFF]

    set ts  [expr $ts & 0xFF]

    send_command [BuildCommand 0xC8 10 $ts 1 $rH $rL $iH $iL 0 0 0 0]
    pong_check
    
}

######################################################################
# Function Name    : force_dec
#                  : 
# Description      : Forces decrements on a timeslot with a given
#                  :   repeat count and spacing
#                  : 
# Parameters       : ts, repeat, interval
#                  : 
#                  : ts        (1<=ts<=48)
#                  : repeat    (0<=repeat<=65535)
#                  : interval  (0<=interval<=65535)
#                  : 
#                  : For concatenated payloads, force decrements for the 
#                  :   first (Norm) STS of the group. The Concatenated
#                  :   timeslots will automatically follow. Valid
#                  :   values for ts are as follows:
#                  :      - for STS-48c:  ts=1      
#                  :      - for STS-12c:  ts=1,13,25,37
#                  :      - for STS-3c:   ts=1,4,7,10,13,16,19,22,25,28,...,46
#                  :      - for STS-1:    1<=ts<=48
#                  : 
# Return Value     : None
#                  : 
######################################################################
proc force_dec {ts repeat interval} {
    puts "DEC TS\#$ts INTERVAL=$interval REPEAT=$repeat"

    set rH  [expr ($repeat>>8) 	 & 0xFF]
    set rL  [expr ($repeat>>0) 	 & 0xFF]
    set iH  [expr ($interval>>8) & 0xFF]
    set iL  [expr ($interval>>0) & 0xFF]

    set ts  [expr $ts & 0xFF]

    send_command [BuildCommand 0xC8 10 $ts 2 0 0 0 0 $rH $rL $iH $iL]
    pong_check
    
}

######################################################################
# Function Name    : incdec_op_pending
# Parameters       : ts (1 to 192)
# Return Value     : 0=none, 1=inc, -1=dec
# Purpose          : determine whether an inc or dec operation is 
#                  : pending for a given channel
######################################################################
proc incdec_op_pending {ts} {
    set ts     [expr $ts    & 0xFF]
    if {$ts == 0xFF} {
	send_command [BuildCommand 0xC9 1 $ts]
	set ret [lrange [pong] 2 193]
	foreach s $ret {
	    set r  "0x$s"
	    if {$r == 0xFF} {
		set r -1
	    } elseif {$r == 0x00} {
		set r 0
	    } elseif {$r == 0x01} {
		set r 1
	    }
	    lappend stat $r
	}
	return $stat
    } elseif {($ts>=1) && ($ts<=192)} {
	send_command [BuildCommand 0xC9 1 $ts]
	set stat [lrange [pong] 3 3]
	set tmp [expr "0x[lindex $stat 0]" ]
	if {$tmp == 0xFF} {
	    set tmp -1
	} elseif {$tmp == 0x00} {
	    set tmp 0
	} elseif {$tmp == 0x01} {
	    set tmp 1
	}
	return $stat
    } else {
	puts "ERROR: incdec_op_pending: bad ts, must be 1-192 or 0xFF (255)"
    }
}

######################################################################
# Function Name    : wait_for_incdec_to_finish
# Parameters       : ts (1 to 192)
#                  : verbose {0,1,2} [optional, default is 0]
#                  : poll    N       [optional, default is 250 milliseconds]
# Return Value     : 0=none, 1=inc, -1=dec
# Purpose          : determine whether an inc or dec operation is 
#                  : pending for a given channel
######################################################################
proc wait_for_incdec_to_finish {ch {verbose 0} {poll 250}} {
    set tmp 0
    set t [time {
	          while {1} {
		      set tmp [incdec_op_pending $ch]
		      if {$verbose>1} {
			  puts "incdec_is_pending($ch) -> $tmp"
		      }
		      if {!$tmp} {
			  break
		      }
		      after $poll
		  }
                }
	   ]
    set t [lindex $t 0]
    set t [expr $t/1000000.0]
    if {$verbose} {
	puts "INFO: Waited $t seconds (for incdec on $ch to complete)"
    }
    return $t
}


######################################################################
# --------------------------------------------------------------------
# RX Path status commands
# --------------------------------------------------------------------
######################################################################


######################################################################
# Function Name    : get_rx_path_status
#                  : 
# Parameters       : ts           (1<=x<=192)
#                  : stickyaction (1<=x<=3)
#                  : stickyclrmask (0 -> 0xFFFF)
#                  : 
# Return Value     : status bit
#                  : 
# Purpose          : Get the received path status for a given channel or channels
#                  : 
######################################################################
proc get_rx_path_status {{ts 0xFF} {stickyaction 0} {stickyclrmask 0xFF}} {
    set ptrstatestr {{LOP } {AIS } NORM CONC}

    set ts      	[expr $ts           & 0xFF]
    set stickyaction    [expr $stickyaction & 0xFF]
    set stickyclrmask   [expr $stickyclrmask& 0xFF]

    if {$ts == 0xFF} {
	send_command [BuildCommand 0xB5 3 \
		      $ts \
		      $stickyaction \
		      $stickyclrmask]

	set stat [lrange [pong] 0 193]
	for {set i 1} {$i<=192} {incr i} {
	    set tmp [expr "0x[lindex $stat [expr $i + 1]]"]
	    set rxptrstate    [expr ($tmp>>0) & 0x3]
	    set rxptrstatestr [lindex $ptrstatestr $rxptrstate]
	    set exptrstate    [expr ($tmp>>2) & 0x3]
	    set exptrstatestr [lindex $ptrstatestr $exptrstate]
	    puts [format "ch\[%2d]=0x%4.4X  \[Rx=$rxptrstatestr] \[Ex=$exptrstatestr]" $i $tmp]
	}
    } elseif {($ts>=1) && ($ts<=192)} {
	send_command [BuildCommand 0xB5 3 \
		      $ts \
		      $stickyaction \
		      $stickyclrmask]
	set stat [lrange [pong] 2 2]
	set tmp [expr "0x[lindex $stat 0]"]
	set rxptrstate    [expr $tmp & 0x3]
	set rxptrstatestr [lindex $ptrstatestr $rxptrstate]
	set exptrstate    [expr $tmp & 0x3]
	set exptrstatestr [lindex $ptrstatestr $exptrstate]
	puts [format "ch\[%2d]=0x%4.4X  \[Rx=$rxptrstatestr] \[Ex=$exptrstatestr]" $ts $tmp]
    } else {
	puts "ERROR: get_rx_path_status: bad ts, must be 1-192 or 255"
    }
}


######################################################################
# --------------------------------------------------------------------
# Expected Concat commands
# --------------------------------------------------------------------
######################################################################


######################################################################
# Function Name    : get_expected_concat
#                  : 
# Parameters       : ts           (1<=x<=192, 0xFF)
#                  : 
# Return Value     : expected concat, either single value or list of 192 values
#                  : 
# Purpose          : Get the expected concatenation for a given channel or channels
#                  : 
######################################################################
proc get_expected_concat {{ts 0xFF}} {
    if {$ts == 0xFF} {
	send_command [BuildCommand 0xC3 1 $ts]
	set stat [lrange [pong] 2 193]
	return $stat
    } elseif {($ts>=1) && ($ts<=192)} {
	send_command [BuildCommand 0xC3 1 $ts]
	set stat [lrange [pong] 2 2]
	set tmp [expr "0x[lindex $stat 0]" ]
	return $stat
    } else {
	puts "ERROR: get_expected_concat: bad ts, must be 1-192 or 255"
    }
}

######################################################################
# Function Name    : set_expected_concat
#                  : 
# Parameters       : 192x expected concat values
#                  : 
# Return Value     : none
#                  : 
# Purpose          : Set the expected concatenation map
#                  : 
######################################################################
proc set_expected_concat {args} {
    if {[llength $args] == 1} {
	set args [lindex $args 0]
    }

    if {([llength $args] != 192) && \
        ([llength $args] != 48) && \
        ([llength $args] != 12) && \
        ([llength $args] !=  3)} {
	puts "ERROR: set_expected_concat: must supply 192/48/12/3 expected concat values"
	return 1
    }

    set x  [concat 0xC2 [llength $args] $args]
    send_command [eval "BuildCommand $x"]

    set ret_val [parse_read_value]
    return $ret_val
}



######################################################################
# --------------------------------------------------------------------
# Sense LOS/LOF/LOL/B1
# --------------------------------------------------------------------
######################################################################


######################################################################
# Function Name    : get_rx_line_status
#                  : 
# Parameters       : stickyaction (1<=x<=3)
#                  : stickyclrmask (0 -> 0xFFFF)
#                  : 
# Return Value     : status bit
#                  : 
# Purpose          : Get the received path status for a given channel or channels
#                  : 
######################################################################
proc get_rx_line_status {{stickyaction 0} {stickyclrmask 0xFF}} {
    set stickyaction    [expr $stickyaction & 0xFF]
    set stickyclrmask   [expr $stickyclrmask& 0xFF]

    send_command [BuildCommand 0xB4 2 \
		               $stickyaction \
			       $stickyclrmask]

    set stat [lrange [pong] 2 2]
    set tmp [expr "0x[lindex $stat 0]"]

    set los [expr ($tmp>>0) & 0x1]
    set lol [expr ($tmp>>1) & 0x1]
    set lof [expr ($tmp>>2) & 0x1]
    set b1  [expr ($tmp>>3) & 0x1]
    set abs [expr ($tmp>>4) & 0x1]

    
    puts [format "LineStatus=0x%4.4X: LOS=%d LOL=%d LOF=%d B1=%d NO_OPTICS=%d"\
                               $tmp $los $lol $lof $b1 $abs]
}



######################################################################
# --------------------------------------------------------------------
# Path AIS/UNEQ Commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_path_AIS
# Parameters       : ts value
# Return Value     : none
# Purpose          : Sets the Path layer AIS
######################################################################
proc set_path_AIS {ts value} {
    set ts     [expr $ts    & 0xFF]
    set value  [expr $value & 0x01]
    puts "set_path_AIS $ts $value"
    send_command [BuildCommand 0xCA 2 $ts $value]
    pong_check
}

######################################################################
# Function Name    : get_path_AIS
# Parameters       : ts 
# Return Value     : AIS status
# Purpose          : Query Path layer AIS status for a timeslot
######################################################################
proc get_path_AIS {ts} {
    set ts     [expr $ts    & 0xFF]
    send_command [BuildCommand 0xCB 1 $ts]
    set ret_val [parse_read_value]
    return $ret_val
}
######################################################################
# Function Name    : set_path_UNEQ
# Parameters       : ts value
# Return Value     : none
# Purpose          : Sets the Path layer UNEQ
######################################################################
proc set_path_UNEQ {ts value} {
    set ts     [expr $ts    & 0xFF]
    set value  [expr $value & 0x01]
    puts "set_path_UNEQ $ts $value"
    send_command [BuildCommand 0xCC 2 $ts $value]
    pong_check
}

######################################################################
# Function Name    : get_path_UNEQ
# Parameters       : ts 
# Return Value     : UNEQ status
# Purpose          : Query Path layer UNEQ status for a timeslot
######################################################################
proc get_path_UNEQ {ts} {
    set ts     [expr $ts    & 0xFF]
    send_command [BuildCommand 0xCD 1 $ts]
    set ret_val [parse_read_value]
    return $ret_val
}


######################################################################
# Function Name    : set_path_UNEQ_C2
# Parameters       : mode
# Return Value     : none
# Purpose          : sets the laser mode (norm,1,0,squelch)
######################################################################
proc set_path_UNEQ_C2 {mode} {
    send_command [BuildCommand 0xCE 0x01 $mode]
    pong_check
}

######################################################################
# Function Name    : get_path_UNEQ_C2
# Parameters       : none
# Return Value     : returns the laserctl mode
# Purpose          : allows the scripts to handle multiple rates
######################################################################
proc get_path_UNEQ_C2 {} {
    send_command [BuildCommand 0xCF 0x00]
    return [parse_read_value]
}



######################################################################
# --------------------------------------------------------------------
# BER Rate to interval conversions
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : pd_BER_rate2interval
# Parameters       : ber, bits_per_count
# Return Value     : interval
# Purpose          : convert bit error rate to interval
######################################################################
proc pd_BER_rate2interval {ber bits_per_cnt} {
    global HSPD_BER_MAX_INTERVAL

    if {$ber == 0.0} {
	return 0.0
    } elseif {$ber < 0.0} {
	return 0.0
    }

    set interval [expr 1.0/($bits_per_cnt * $ber)]

    if {$interval > $HSPD_BER_MAX_INTERVAL} {
	set interval $HSPD_BER_MAX_INTERVAL
    } elseif {$interval <= 1.0} { 
	return 1.0
    }
    return $interval
}

######################################################################
# Function Name    : pd_BER_interval2rate
# Parameters       : interval bits_per_count
# Return Value     : rate
# Purpose          : convert bit error rate to interval
######################################################################
proc pd_BER_interval2rate {interval bits_per_cnt} {
    global HSPD_BER_MAX_INTERVAL

    if {$interval > $HSPD_BER_MAX_INTERVAL} {
	set interval $HSPD_BER_MAX_INTERVAL
    } elseif {$interval <= 1.0} { 
	return 0
    }

    set ber [expr 1.0/($bits_per_cnt * $interval)]

    if {$ber == 0.0} {
	return 0.0
    } elseif {$ber < 0.0} {
	return 0.0
    }

    return $ber
}

######################################################################
# --------------------------------------------------------------------
# Line BER Commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_line_BER
# Parameters       : BER value (e.g. 4.5e-6)
# Return Value     : none
# Purpose          : Sets the Line layer BER to be inserted 
#                  :   if value is nonzero, also turns on BER insertion
######################################################################
proc set_line_BER {value} {
    global HSPD_BER_MAX_INTERVAL
    global HSPD_BER_BITS_PER_CNT

    puts "set_line_BER $value"

    if {$value == 0} {
	set berreg(4)  0
	set berreg(3)  0
	set berreg(2)  0
	set berreg(1)  0
	set berreg(0)  0
    } else {
	set interval  [pd_BER_rate2interval $value 1]
	set divisor   [expr {256.0 * 256.0 * 256.0 * 256.0}]
	for {set i 4} {$i>=0} {incr i -1} {
	    set tmp        [expr {$interval / $divisor}]
	    set ltmp       [expr {int($tmp)}]
	    set berreg($i) $ltmp
	    set interval   [expr {$interval - ($ltmp * $divisor)}]
	    set divisor    [expr {$divisor / 256.0}]
	}
    }

#    puts [format "FPGA=%2.2X.%2.2X.%2.2X.%2.2X.%2.2X" \
\#    	  $berreg(4) $berreg(3) $berreg(2) $berreg(1) $berreg(0)]

    send_command [BuildCommand 0xB2 5 $berreg(4) $berreg(3) $berreg(2) $berreg(1) $berreg(0)]
    after 50
    pong_check
}

######################################################################
# Function Name    : get_line_BER
# Parameters       : none
# Return Value     : Bit error rate value ins %9.2e format
# Purpose          : Returns the current BER setting, or zero if
#                  :  BER insertoin is not enabled
######################################################################
proc get_line_BER {} {
    global HSPD_BER_MAX_INTERVAL
    global HSPD_BER_BITS_PER_CNT

    send_command [BuildCommand 0xB3 0x0]
    after 50
    set ret [lrange [pong] 2 6]

#    puts [format "0x%2.2X%2.2X%2.2X%2.2X%2.2X" "0x[lindex $ret 0]" "0x[lindex $ret 1]" "0x[lindex $ret 2]" "0x[lindex $ret 3]" "0x[lindex $ret 4]" ]

    set berreg(0) "0x[lindex $ret 4 ]"
    set berreg(1) "0x[lindex $ret 3 ]"
    set berreg(2) "0x[lindex $ret 2 ]"
    set berreg(3) "0x[lindex $ret 1 ]"
    set berreg(4) "0x[lindex $ret 0 ]"

    set interval 0.0

    for {set i 4} {$i>=0} {incr i -1} {
	set interval  [expr {$interval * 256.0 }]
	set interval  [expr {$interval + $berreg($i)}]
    }

    set ber  [pd_BER_interval2rate $interval 1]

    set berstr [format "%9.2e" $ber]

    # ------------------------------------------------------------
    # uncomment to see return value
    # ------------------------------------------------------------
    #puts "BERSTR=$berstr"
    return $berstr

}

######################################################################
# --------------------------------------------------------------------
# Path BER Commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : set_path_BER
# Parameters       : ts, BER value (e.g. 4.5e-6)
# Return Value     : none
# Purpose          : Sets the Path layer BER to be inserted 
#                  :   if value is nonzero, also turns on BER insertion
######################################################################
proc set_path_BER {ts value} {
    puts "set_path_BER $ts $value"

    set interval [pd_BER_rate2interval $value 1]

    set divisor   [expr {256.0 * 256.0 * 256.0 * 256.0}]
    for {set i 4} {$i>=0} {incr i -1} {
	set tmp        [expr {$interval / $divisor}]
	set ltmp       [expr {int($tmp)}]
	set berreg($i) $ltmp
	set interval   [expr {$interval - ($ltmp * $divisor)}]
	set divisor    [expr {$divisor / 256.0}]
    }

    set ts [expr $ts & 0xFF]

    send_command [BuildCommand 0xB0 6 $ts $berreg(4) $berreg(3) $berreg(2) $berreg(1) $berreg(0) ]
    pong_check
}

######################################################################
# Function Name    : set_all_path_BERs
# Parameters       : BER value (e.g. 4.5e-6)
# Return Value     : none
# Purpose          : Idential to set_path_BER, except it sets the
#                  :  specified BER on EVERY path.
######################################################################
proc set_all_path_BERs {value} {
    puts "set_all_path_BERs $value"

    set interval [pd_BER_rate2interval $value 1]

    set divisor   [expr {256.0 * 256.0 * 256.0 * 256.0}]
    for {set i 4} {$i>=0} {incr i -1} {
	set tmp        [expr {$interval / $divisor}]
	set ltmp       [expr {int($tmp)}]
	set berreg($i) $ltmp
	set interval   [expr {$interval - ($ltmp * $divisor)}]
	set divisor    [expr {$divisor / 256.0}]
    }

    send_command [BuildCommand 0xA8 5 $berreg(4) $berreg(3) $berreg(2) $berreg(1) $berreg(0) ]
    pong_check
}

######################################################################
# Function Name    : get_path_BER
# Parameters       : none
# Return Value     : Bit error rate value ins %9.2e format
# Purpose          : Returns the current BER setting, or zero if
#                  :  BER insertoin is not enabled
######################################################################
proc get_path_BER {ts} {
    set ts [expr $ts & 0xFF]

    send_command [BuildCommand 0xB1 1 $ts]
    set ret [lrange [pong] 2 6]

    #puts [format "READ=0x%2.2X%2.2X%2.2X%2.2X%2.2X" \
	"0x[lindex $ret 0]" \
	"0x[lindex $ret 1]" \
	"0x[lindex $ret 2]" \
	"0x[lindex $ret 3]" \
	"0x[lindex $ret 4]" ]

    set berreg(0) "0x[lindex $ret 4 ]"
    set berreg(1) "0x[lindex $ret 3 ]"
    set berreg(2) "0x[lindex $ret 2 ]"
    set berreg(3) "0x[lindex $ret 1 ]"
    set berreg(4) "0x[lindex $ret 0 ]"

    set interval 0.0

    for {set i 4} {$i>=0} {incr i -1} {
	set interval  [expr {$interval * 256.0 }]
	set interval  [expr {$interval + $berreg($i)}]
    }

    set ber  [pd_BER_interval2rate $interval 1]

    set berstr [format "%9.2e" $ber]

    # ------------------------------------------------------------
    # uncomment to see return value
    # ------------------------------------------------------------
    #puts "BERSTR=$berstr"
    return $berstr
}

######################################################################
# Function Name    : set_oh_capture_trigger
# Parameters       : trig_num: which trigger number to set
#                    ch: which channel to watch for this trigger
#                    oh_byte: which byte to watch
#                    oh_byte_val: the value to trigger on the oh_byte
# Return Value     : None
# Purpose          : Set up an OH capture trigger.
######################################################################
proc set_oh_capture_trigger {oh trig_num ch oh_byte oh_byte_val} {
    global HSPD_MAX_NUM_TRIGGERS

    if {$trig_num > $HSPD_MAX_NUM_TRIGGERS || $trig_num < 1} {
	puts "ERROR: Invalid trigger number: $trig_num."
	puts "ERROR: Specify a trigger number 1 thru $HSPD_MAX_NUM_TRIGGERS."
        return
    }

    if {$ch < 1 || $ch > 192} {
	puts "ERROR: Invalid channel number: $ch."
	puts "ERROR: Must specify channel 1-192."
        return
    }

    send_command [BuildCommand 0xA0 5 $oh $trig_num $ch $oh_byte $oh_byte_val]
    print_error_on_nack [pong] "Unable to configure trigger; invalid parameter."
}

######################################################################
# Function Name    : set_toh_capture_trigger
# Parameters       : trig_num: which trigger number to set (1-3)
#                    ch: which channel to watch for this trigger
#                    toh_byte: which byte to watch
#                    toh_byte_value: the value to trigger on the toh_byte
# Return Value     : None
# Purpose          : Set up a TOH capture trigger.
######################################################################
proc set_toh_capture_trigger {trig_num ch toh_byte toh_byte_value} {
    global HSPD_TOH

    if {$toh_byte < 1 || $toh_byte > 27} {
	puts "ERROR: Invalid toh byte: $toh_byte."
	puts "ERROR: Must specify one of the following TOH bytes:"
        puts "         \$TOH_BYTE_A1         (or 1)"
        puts "         \$TOH_BYTE_A2         (or 2)"
        puts "         \$TOH_BYTE_A3         (or 3)"
        puts "         \$TOH_BYTE_B1         (or 4)"
        puts "         \$TOH_BYTE_E1         (or 5)"
        puts "         \$TOH_BYTE_F1         (or 6)"
        puts "         \$TOH_BYTE_D1         (or 7)"
        puts "         \$TOH_BYTE_D2         (or 8)"
        puts "         \$TOH_BYTE_D3         (or 9)"
        puts "         \$TOH_BYTE_H1         (or 10)"
        puts "         \$TOH_BYTE_H2         (or 11)"
        puts "         \$TOH_BYTE_H3         (or 12)"
        puts "         \$TOH_BYTE_B2         (or 13)"
        puts "         \$TOH_BYTE_K1         (or 14)"
        puts "         \$TOH_BYTE_K2         (or 15)"
        puts "         \$TOH_BYTE_D4         (or 16)"
        puts "         \$TOH_BYTE_D5         (or 17)"
        puts "         \$TOH_BYTE_D6         (or 18)"
        puts "         \$TOH_BYTE_D7         (or 19)"
        puts "         \$TOH_BYTE_D8         (or 20)"
        puts "         \$TOH_BYTE_D9         (or 21)"
        puts "         \$TOH_BYTE_D10        (or 22)"
        puts "         \$TOH_BYTE_D11        (or 23)"
        puts "         \$TOH_BYTE_D12        (or 24)"
        puts "         \$TOH_BYTE_S1_Z1      (or 25)"
        puts "         \$TOH_BYTE_M0_M1_Z2   (or 26)"
        puts "         \$TOH_BYTE_E2         (or 27)"
        return
    }

    set_oh_capture_trigger $HSPD_TOH $trig_num $ch $toh_byte $toh_byte_value
}

######################################################################
# Function Name    : set_poh_capture_trigger
# Parameters       : trig_num: which trigger number to set (1-3)
#                    ch: which channel to watch for this trigger
#                    poh_byte: which byte to watch
#                    poh_byte_value: the value to trigger on the poh_byte
# Return Value     : None
# Purpose          : Set up a POH capture trigger.
######################################################################
proc set_poh_capture_trigger {trig_num ch poh_byte poh_byte_value} {
    global HSPD_POH

    if {$poh_byte < 1 || $poh_byte > 9} {
	puts "ERROR: Invalid poh byte: $poh_byte."
	puts "ERROR: Must specify one of the following POH bytes:"
        puts "         \$POH_BYTE_J1    (or 1)"
        puts "         \$POH_BYTE_B3    (or 2)"
        puts "         \$POH_BYTE_C2    (or 3)"
        puts "         \$POH_BYTE_G1    (or 4)"
        puts "         \$POH_BYTE_F2    (or 5)"
        puts "         \$POH_BYTE_H4    (or 6)"
        puts "         \$POH_BYTE_Z3    (or 7)"
        puts "         \$POH_BYTE_Z4    (or 8)"
        puts "         \$POH_BYTE_Z5    (or 9)"
        return
    }

    set_oh_capture_trigger $HSPD_POH $trig_num $ch $poh_byte $poh_byte_value
}

######################################################################
# Function Name    : get_oh_capture_trigger
# Parameters       : trig_num: which trigger number to get (1-3)
# Return Value     : The current settings of the trigger requested
# Purpose          : Set up a OH capture trigger.
######################################################################
proc get_oh_capture_trigger {oh trig_num} {
    global      HSPD_POH
    global      HSPD_TOH
    global      HSPD_MAX_NUM_TRIGGERS

    global      POH_BYTE_J1
    global      POH_BYTE_B3
    global      POH_BYTE_C2
    global      POH_BYTE_G1
    global      POH_BYTE_F2
    global      POH_BYTE_H4
    global      POH_BYTE_Z3
    global      POH_BYTE_Z4
    global      POH_BYTE_Z5
    global      TOH_BYTE_A1
    global      TOH_BYTE_A2
    global      TOH_BYTE_A3
    global      TOH_BYTE_B1
    global      TOH_BYTE_E1
    global      TOH_BYTE_F1
    global      TOH_BYTE_D1
    global      TOH_BYTE_D2
    global      TOH_BYTE_D3
    global      TOH_BYTE_H1
    global      TOH_BYTE_H2
    global      TOH_BYTE_H3
    global      TOH_BYTE_B2
    global      TOH_BYTE_K1
    global      TOH_BYTE_K2
    global      TOH_BYTE_D4
    global      TOH_BYTE_D5
    global      TOH_BYTE_D6
    global      TOH_BYTE_D7
    global      TOH_BYTE_D8
    global      TOH_BYTE_D9
    global      TOH_BYTE_D10
    global      TOH_BYTE_D11
    global      TOH_BYTE_D12
    global      TOH_BYTE_S1_Z1
    global      TOH_BYTE_M0_M1_Z2
    global      TOH_BYTE_E2

    if {$trig_num > $HSPD_MAX_NUM_TRIGGERS || $trig_num < 1} {
	puts "ERROR: Invalid trigger number: $trig_num."
	puts "ERROR: Specify a trigger number 1 thru $HSPD_MAX_NUM_TRIGGERS."
        return
    }

    send_command [BuildCommand 0xA1 2 $oh $trig_num]
    set ret [pong]

    if {[print_error_on_nack $ret "Invalid parameter to get_oh_capture_trigger."] == 1} {
        return
    }

    set oh [lindex $ret 2]
    set ch [expr 0 + "0x[lindex $ret 4]"]
    set oh_byte [lindex $ret 5]
    set oh_byte_value "0x[lindex $ret 6]"
    set byte "???"

    puts "Trigger #$trig_num: "

    if {$oh == $HSPD_POH} {
        if {$oh_byte == $POH_BYTE_J1} {
            set byte "J1"
        } elseif {$oh_byte == $POH_BYTE_B3} {
            set byte "B3"
        } elseif {$oh_byte == $POH_BYTE_C2} {
            set byte "C2"
        } elseif {$oh_byte == $POH_BYTE_G1} {
            set byte "G1"
        } elseif {$oh_byte == $POH_BYTE_F2} {
            set byte "F2"
        } elseif {$oh_byte == $POH_BYTE_H4} {
            set byte "H4"
        } elseif {$oh_byte == $POH_BYTE_Z3} {
            set byte "Z3"
        } elseif {$oh_byte == $POH_BYTE_Z4} {
            set byte "Z4"
        } elseif {$oh_byte == $POH_BYTE_Z5} {
            set byte "Z5"
        }
    }

    if {$oh == $HSPD_TOH} {
        if {$oh_byte == $TOH_BYTE_A1} {
            set byte "A1"
        } elseif {$oh_byte == $TOH_BYTE_A2} {
            set byte "A2"
        } elseif {$oh_byte == $TOH_BYTE_A3} {
            set byte "A2"
        } elseif {$oh_byte == $TOH_BYTE_B1} {
            set byte "B1"
        } elseif {$oh_byte == $TOH_BYTE_E1} {
            set byte "E1"
        } elseif {$oh_byte == $TOH_BYTE_F1} {
            set byte "F1"
        } elseif {$oh_byte == $TOH_BYTE_D1} {
            set byte "D1"
        } elseif {$oh_byte == $TOH_BYTE_D2} {
            set byte "D2"
        } elseif {$oh_byte == $TOH_BYTE_D3} {
            set byte "D3"
        } elseif {$oh_byte == $TOH_BYTE_H1} {
            set byte "H1"
        } elseif {$oh_byte == $TOH_BYTE_H2} {
            set byte "H2"
        } elseif {$oh_byte == $TOH_BYTE_H3} {
            set byte "H3"
        } elseif {$oh_byte == $TOH_BYTE_B2} {
            set byte "B2"
        } elseif {$oh_byte == $TOH_BYTE_K1} {
            set byte "K1"
        } elseif {$oh_byte == $TOH_BYTE_K2} {
            set byte "K2"
        } elseif {$oh_byte == $TOH_BYTE_D4} {
            set byte "D4"
        } elseif {$oh_byte == $TOH_BYTE_D5} {
            set byte "D5"
        } elseif {$oh_byte == $TOH_BYTE_D6} {
            set byte "D6"
        } elseif {$oh_byte == $TOH_BYTE_D7} {
            set byte "D7"
        } elseif {$oh_byte == $TOH_BYTE_D8} {
            set byte "D8"
        } elseif {$oh_byte == $TOH_BYTE_D9} {
            set byte "D9"
        } elseif {$oh_byte == $TOH_BYTE_D10} {
            set byte "D10"
        } elseif {$oh_byte == $TOH_BYTE_D11} {
            set byte "D11"
        } elseif {$oh_byte == $TOH_BYTE_D12} {
            set byte "D12"
        } elseif {$oh_byte == $TOH_BYTE_S1_Z1} {
            set byte "S1/Z1"
        } elseif {$oh_byte == $TOH_BYTE_M0_M1_Z2} {
            set byte "M0/M1/Z2"
        } elseif {$oh_byte == $TOH_BYTE_E2} {
            set byte "E2"
        }
    }

    puts "    Watching the $byte Byte on Channel $ch for value $oh_byte_value."
}

######################################################################
# Function Name    : get_poh_capture_trigger
# Parameters       : trig_num: which trigger number to get (1-3)
# Return Value     : The current settings of the trigger requested
# Purpose          : Set up a POH capture trigger.
######################################################################
proc get_poh_capture_trigger {trig_num} {
    global HSPD_POH

    get_oh_capture_trigger $HSPD_POH $trig_num
}

######################################################################
# Function Name    : get_toh_capture_trigger
# Parameters       : trig_num: which trigger number to get (1-3)
# Return Value     : The current settings of the trigger requested
# Purpose          : Set up a TOH capture trigger.
######################################################################
proc get_toh_capture_trigger {trig_num} {
    global HSPD_TOH

    get_oh_capture_trigger $HSPD_TOH $trig_num
}

######################################################################
# Function Name    : set_oh_capture_buffer_cfg
# Parameters       : buf_num: which buffer to configure (1-3)
#                    ch: which channel to capture from for this buffer
#                    oh_byte: which byte to capture
#                    threshold: number of bytes to capture before the triggers
#                               can be armed
#                    size: total size of the buffer in bytes
# Return Value     : None
# Purpose          : Set up a POH capture trigger.
######################################################################
proc set_oh_capture_buffer_cfg {oh buf_num ch oh_byte threshold size} {
    global HSPD_POH
    global HSPD_TOH

    global HSPD_MAX_NUM_BUFFERS
    global HSPD_MAX_BUFFER_SIZE

    if {$buf_num > $HSPD_MAX_NUM_BUFFERS || $buf_num < 1} {
        puts "ERROR: Invalid buffer: $buf_num."
        puts "ERROR: Specify a buffer number 1 thru $HSPD_MAX_NUM_BUFFERS."
        return
    }

    if {$ch < 1 || $ch > 192} {
        puts "ERROR: Invalid channel number: $ch."
        puts "ERROR: Must specify channel 1-192."
        return
    }

    if {$size <= 0 || $size > $HSPD_MAX_BUFFER_SIZE} {
        puts "ERROR: Fifo size specified is invalid."
        puts "ERROR: Must specify size <= $HSPD_MAX_BUFFER_SIZE and > 0."
        return
    }

    if {$threshold < 0 || $threshold > $HSPD_MAX_BUFFER_SIZE} {
        puts "ERROR: Threshold specified is invalid."
        puts "ERROR: Must specify size <= $HSPD_MAX_BUFFER_SIZE."
        return
    }

    if {$threshold > $size} {
        puts "ERROR: Threshold specified is larger than max size specified."
        return
    }

    if {$oh == $HSPD_POH} {
        if {$oh_byte < 1 || $oh_byte > 9} {
            puts "ERROR: Invalid oh byte: $oh_byte."
            puts "ERROR: Must specify one of the following POH bytes:"
            puts "         \$POH_BYTE_J1    (or 1)"
            puts "         \$POH_BYTE_B3    (or 2)"
            puts "         \$POH_BYTE_C2    (or 3)"
            puts "         \$POH_BYTE_G1    (or 4)"
            puts "         \$POH_BYTE_F2    (or 5)"
            puts "         \$POH_BYTE_H4    (or 6)"
            puts "         \$POH_BYTE_Z3    (or 7)"
            puts "         \$POH_BYTE_Z4    (or 8)"
            puts "         \$POH_BYTE_Z5    (or 9)"
            return
        }
    }

    if {$oh == $HSPD_POH} {
        if {$oh_byte < 1 || $oh_byte > 27} {
            puts "ERROR: Invalid oh byte: $oh_byte."
            puts "ERROR: Must specify one of the following TOH bytes:"
            puts "         \$TOH_BYTE_A1         (or 1)"
            puts "         \$TOH_BYTE_A2         (or 2)"
            puts "         \$TOH_BYTE_A3         (or 3)"
            puts "         \$TOH_BYTE_B1         (or 4)"
            puts "         \$TOH_BYTE_E1         (or 5)"
            puts "         \$TOH_BYTE_F1         (or 6)"
            puts "         \$TOH_BYTE_D1         (or 7)"
            puts "         \$TOH_BYTE_D2         (or 8)"
            puts "         \$TOH_BYTE_D3         (or 9)"
            puts "         \$TOH_BYTE_H1         (or 10)"
            puts "         \$TOH_BYTE_H2         (or 11)"
            puts "         \$TOH_BYTE_H3         (or 12)"
            puts "         \$TOH_BYTE_B2         (or 13)"
            puts "         \$TOH_BYTE_K1         (or 14)"
            puts "         \$TOH_BYTE_K2         (or 15)"
            puts "         \$TOH_BYTE_D4         (or 16)"
            puts "         \$TOH_BYTE_D5         (or 17)"
            puts "         \$TOH_BYTE_D6         (or 18)"
            puts "         \$TOH_BYTE_D7         (or 19)"
            puts "         \$TOH_BYTE_D8         (or 20)"
            puts "         \$TOH_BYTE_D9         (or 21)"
            puts "         \$TOH_BYTE_D10        (or 22)"
            puts "         \$TOH_BYTE_D11        (or 23)"
            puts "         \$TOH_BYTE_D12        (or 24)"
            puts "         \$TOH_BYTE_S1_Z1      (or 25)"
            puts "         \$TOH_BYTE_M0_M1_Z2   (or 26)"
            puts "         \$TOH_BYTE_E2         (or 27)"
            return
        }
    }

    set tmp $threshold
    for {set i 1} {$i>=0} {incr i -1} {
	set threshbyte($i)  [expr ($tmp & 0xFF)]
	set tmp             [expr ($tmp >> 8)]
    }

    set tmp $size
    for {set i 1} {$i>=0} {incr i -1} {
	set sizebyte($i)  [expr ($tmp & 0xFF)]
	set tmp           [expr ($tmp >> 8)]
    }

    send_command [BuildCommand 0xA2 8 $oh $buf_num $ch $oh_byte \
                  $threshbyte(0) $threshbyte(1) $sizebyte(0) $sizebyte(1)]
    print_error_on_nack [pong] "Unable to configure buffer; invalid parameter."
}

######################################################################
# Function Name    : set_poh_capture_buffer_cfg
# Parameters       : buf_num: which buffer to configure (1-3)
#                    ch: which channel to capture from for this buffer
#                    poh_byte: which byte to capture
#                    threshold: number of bytes to capture before the triggers
#                               can be armed
#                    size: total size of the buffer in bytes (max=128)
# Return Value     : None
# Purpose          : Set up a POH capture trigger.
######################################################################
proc set_poh_capture_buffer_cfg {buf_num ch poh_byte threshold size} {
    global HSPD_POH

    puts "set_poh_capture_buffer_cfg $buf_num $ch $poh_byte $threshold $size"
    set_oh_capture_buffer_cfg $HSPD_POH $buf_num $ch $poh_byte $threshold $size
}

######################################################################
# Function Name    : set_toh_capture_buffer_cfg
# Parameters       : buf_num: which buffer to configure (1-3)
#                    ch: which channel to capture from for this buffer
#                    toh_byte: which byte to capture
#                    threshold: number of bytes to capture before the triggers
#                               can be armed
#                    size: total size of the buffer in bytes (max=128)
# Return Value     : None
# Purpose          : Set up a POH capture trigger.
######################################################################
proc set_toh_capture_buffer_cfg {buf_num ch toh_byte threshold size} {
    global HSPD_TOH

    set_oh_capture_buffer_cfg $HSPD_TOH $buf_num $ch $toh_byte $threshold $size
}

######################################################################
# Function Name    : get_oh_capture_buffer_cfg
# Parameters       : buf_num: which buffer to get configuration of
# Return Value     : Specified buffer's configuration information.
######################################################################
proc get_oh_capture_buffer_cfg {oh buf_num} {
    global      HSPD_MAX_NUM_BUFFERS
    global      HSPD_POH
    global      HSPD_TOH

    global      POH_BYTE_J1
    global      POH_BYTE_B3
    global      POH_BYTE_C2
    global      POH_BYTE_G1
    global      POH_BYTE_F2
    global      POH_BYTE_H4
    global      POH_BYTE_Z3
    global      POH_BYTE_Z4
    global      POH_BYTE_Z5

    global      TOH_BYTE_A1
    global      TOH_BYTE_A2
    global      TOH_BYTE_A3
    global      TOH_BYTE_B1
    global      TOH_BYTE_E1
    global      TOH_BYTE_F1
    global      TOH_BYTE_D1
    global      TOH_BYTE_D2
    global      TOH_BYTE_D3
    global      TOH_BYTE_H1
    global      TOH_BYTE_H2
    global      TOH_BYTE_H3
    global      TOH_BYTE_B2
    global      TOH_BYTE_K1
    global      TOH_BYTE_K2
    global      TOH_BYTE_D4
    global      TOH_BYTE_D5
    global      TOH_BYTE_D6
    global      TOH_BYTE_D7
    global      TOH_BYTE_D8
    global      TOH_BYTE_D9
    global      TOH_BYTE_D10
    global      TOH_BYTE_D11
    global      TOH_BYTE_D12
    global      TOH_BYTE_S1_Z1
    global      TOH_BYTE_M0_M1_Z2
    global      TOH_BYTE_E2

    if {$buf_num > $HSPD_MAX_NUM_BUFFERS || $buf_num < 1} {
	puts "ERROR: Invalid buffer: $buf_num."
	puts "ERROR: Must specify buffer 1 thru $HSPD_MAX_NUM_BUFFERS."
        return
    }

    send_command [BuildCommand 0xA3 2 $oh $buf_num]
    set ret [pong]

    if {[print_error_on_nack $ret "Invalid parameter to get_oh_capture_buffer_cfg."] == 1} {
        return
    }

    set oh         [lindex $ret 2]
    set ch         [expr 0 + "0x[lindex $ret 4]"]
    set oh_byte    [lindex $ret 5]
    set msb_thresh "0x[lindex $ret 6]"
    set lsb_thresh "0x[lindex $ret 7]"
    set msb_size   "0x[lindex $ret 8]"
    set lsb_size   "0x[lindex $ret 9]"

    set threshold [expr ($msb_thresh << 8)]
    set threshold [expr ($threshold | $lsb_thresh)]

    set size      [expr ($msb_size << 8)]
    set size      [expr ($size | $lsb_size)]

    if {$oh == $HSPD_POH} {
        if {$oh_byte == $POH_BYTE_J1} {
            set byte "J1"
        } elseif {$oh_byte == $POH_BYTE_B3} {
            set byte "B3"
        } elseif {$oh_byte == $POH_BYTE_C2} {
            set byte "C2"
        } elseif {$oh_byte == $POH_BYTE_G1} {
            set byte "G1"
        } elseif {$oh_byte == $POH_BYTE_F2} {
            set byte "F2"
        } elseif {$oh_byte == $POH_BYTE_H4} {
            set byte "H4"
        } elseif {$oh_byte == $POH_BYTE_Z3} {
            set byte "Z3"
        } elseif {$oh_byte == $POH_BYTE_Z4} {
            set byte "Z4"
        } elseif {$oh_byte == $POH_BYTE_Z5} {
            set byte "Z5"
        } else {
            set byte "??"
        }
    }

    if {$oh == $HSPD_TOH} {
        if {$oh_byte == $TOH_BYTE_A1} {
            set byte "A1"
        } elseif {$oh_byte == $TOH_BYTE_A2} {
            set byte "A2"
        } elseif {$oh_byte == $TOH_BYTE_A3} {
            set byte "A2"
        } elseif {$oh_byte == $TOH_BYTE_B1} {
            set byte "B1"
        } elseif {$oh_byte == $TOH_BYTE_E1} {
            set byte "E1"
        } elseif {$oh_byte == $TOH_BYTE_F1} {
            set byte "F1"
        } elseif {$oh_byte == $TOH_BYTE_D1} {
            set byte "D1"
        } elseif {$oh_byte == $TOH_BYTE_D2} {
            set byte "D2"
        } elseif {$oh_byte == $TOH_BYTE_D3} {
            set byte "D3"
        } elseif {$oh_byte == $TOH_BYTE_H1} {
            set byte "H1"
        } elseif {$oh_byte == $TOH_BYTE_H2} {
            set byte "H2"
        } elseif {$oh_byte == $TOH_BYTE_H3} {
            set byte "H3"
        } elseif {$oh_byte == $TOH_BYTE_B2} {
            set byte "B2"
        } elseif {$oh_byte == $TOH_BYTE_K1} {
            set byte "K1"
        } elseif {$oh_byte == $TOH_BYTE_K2} {
            set byte "K2"
        } elseif {$oh_byte == $TOH_BYTE_D4} {
            set byte "D4"
        } elseif {$oh_byte == $TOH_BYTE_D5} {
            set byte "D5"
        } elseif {$oh_byte == $TOH_BYTE_D6} {
            set byte "D6"
        } elseif {$oh_byte == $TOH_BYTE_D7} {
            set byte "D7"
        } elseif {$oh_byte == $TOH_BYTE_D8} {
            set byte "D8"
        } elseif {$oh_byte == $TOH_BYTE_D9} {
            set byte "D9"
        } elseif {$oh_byte == $TOH_BYTE_D10} {
            set byte "D10"
        } elseif {$oh_byte == $TOH_BYTE_D11} {
            set byte "D11"
        } elseif {$oh_byte == $TOH_BYTE_D12} {
            set byte "D12"
        } elseif {$oh_byte == $TOH_BYTE_S1_Z1} {
            set byte "S1/Z1"
        } elseif {$oh_byte == $TOH_BYTE_M0_M1_Z2} {
            set byte "M0/M1/Z2"
        } elseif {$oh_byte == $TOH_BYTE_E2} {
            set byte "E2"
        }
    }

    puts "Buffer #$buf_num:"
    puts "  Capturing $byte Byte in Channel #$ch."
    puts "  Threshold:  $threshold"
    puts "  Size:  $size"
}

######################################################################
# Function Name    : get_poh_capture_buffer_cfg
# Parameters       : buf_num: which buffer to get configuration of
# Return Value     : Specified buffer's configuration information.
######################################################################
proc get_poh_capture_buffer_cfg {buf_num} {
    global HSPD_POH

    get_oh_capture_buffer_cfg $HSPD_POH $buf_num
}

######################################################################
# Function Name    : get_toh_capture_buffer_cfg
# Parameters       : buf_num: which buffer to get configuration of
# Return Value     : Specified buffer's configuration information.
######################################################################
proc get_toh_capture_buffer_cfg {buf_num} {
    global HSPD_TOH

    get_oh_capture_buffer_cfg $HSPD_TOH $buf_num
}

######################################################################
# Function Name    : start_oh_capture
# Parameters       : oh is either $HSPD_TOH or $HSPD_POH
#                    mode is either HSPD_OH_CAPTURE_EVERY_FRAME_MODE or
#                                   HSPD_OH_CAPTURE_TRANSITIONAL_TIMING_MODE
#                    num_triggers is the number of triggers to arm (1-3)
#                    use_buffers is a list of which buffers to use
#                        (valid buffer numbers are 1-3)
# Return Value     : None.
# Purpose          : Start a capture session.
######################################################################
proc start_oh_capture {oh mode num_triggers use_buffers} {
    global HSPD_POH
    global HSPD_TOH
    global HSPD_MAX_NUM_BUFFERS
    global HSPD_MAX_NUM_TRIGGERS
    global HSPD_OH_CAPTURE_EVERY_FRAME_MODE
    global HSPD_OH_CAPTURE_TRANSITIONAL_TIMING_MODE

    if {$num_triggers > $HSPD_MAX_NUM_TRIGGERS || $num_triggers < 0} {
	puts "ERROR: Invalid number of triggers!"
	puts -nonewline "ERROR: Specify number of triggers to use "
        puts " (0-$HSPD_MAX_NUM_TRIGGERS)"
        return
    }

    if {$mode != $HSPD_OH_CAPTURE_EVERY_FRAME_MODE &&
        $mode != $HSPD_OH_CAPTURE_TRANSITIONAL_TIMING_MODE} {
	puts "ERROR: Invalid capture mode specified!"
	puts -nonewline "ERROR: Please specify either "
        puts -nonewline "\$HSPD_OH_CAPTURE_EVERY_FRAME_MODE or "
        puts -nonewline "\$HSPD_OH_CAPTURE_TRANSITIONAL_TIMING_MODE."
        return
    }

    if {[llength $use_buffers] == 0} {
	puts "ERROR: Invalid buffer specification!"
        puts -nonewline "ERROR: Please specify a list of "
        puts "buffer numbers 1-$HSPD_MAX_NUM_BUFFERS to enable."
        return
    }

    set use_buffers_mask 0
    foreach i $use_buffers {
        if {$i < 1 || $i > $HSPD_MAX_NUM_BUFFERS} {
            puts "ERROR: Invalid buffer number: $i"
            puts -nonewline "ERROR: Please specify a list of "
            puts "buffer numbers 1-$HSPD_MAX_NUM_BUFFERS to enable."
            return
        }
        set use_buffers_mask [expr $use_buffers_mask | (1 << ($i - 1))]
    }

    send_command [BuildCommand 0xA4 5 $oh 1 $mode $num_triggers $use_buffers_mask]
    print_error_on_nack [pong] "Invalid parameter to start_oh_capture."
}

######################################################################
# Function Name    : start_poh_capture
# Parameters       : mode is either HSPD_OH_CAPTURE_EVERY_FRAME_MODE or
#                                   HSPD_OH_CAPTURE_TRANSITIONAL_TIMING_MODE
#                    num_triggers is the number of triggers to arm (0-3)
#                    use_buffers is a mask of which buffers to enable.  e.g.,
#                    1: use buffer #1 only
#                    2: use buffer #2 only
#                    3: use buffers #1 & #2
#                    4: use buffer #3 only
#                    5: use buffers #1 & #3
#                    6: use buffers #2 & #3
#                    7: use buffers #1, #2 and #3
# Return Value     : None.
# Purpose          : Start a capture session.
######################################################################
proc start_poh_capture {mode num_triggers use_buffers} {
    global HSPD_POH

    start_oh_capture $HSPD_POH $mode $num_triggers $use_buffers
}

######################################################################
# Function Name    : start_toh_capture
# Parameters       : mode is either HSPD_OH_CAPTURE_EVERY_FRAME_MODE or
#                                   HSPD_OH_CAPTURE_TRANSITIONAL_TIMING_MODE
#                    num_triggers is the number of triggers to arm (1-3)
#                    use_buffers is a mask of which buffers to enable.  e.g.,
#                    1: use buffer #1 only
#                    2: use buffer #2 only
#                    3: use buffers #1 & #2
#                    4: use buffer #3 only
#                    5: use buffers #1 & #3
#                    6: use buffers #2 & #3
#                    7: use buffers #1, #2 and #3
# Return Value     : None.
# Purpose          : Start a capture session.
######################################################################
proc start_toh_capture {mode num_triggers use_buffers} {
    global HSPD_TOH

    start_oh_capture $HSPD_TOH $mode $num_triggers $use_buffers
}

######################################################################
# Function Name    : stop_oh_capture
# Parameters       : None.
# Return Value     : None.
# Purpose          : Stop a capture session.
######################################################################
proc stop_oh_capture {oh} {

    send_command [BuildCommand 0xA4 2 $oh 0]

    if {[is_nack [pong]] == 0} {
        puts "OH capture stopped."
    } else {
        puts "ERROR: Couldn't stop OH capture!"
    }
}

######################################################################
# Function Name    : stop_poh_capture
# Parameters       : None.
# Return Value     : None.
# Purpose          : Stop a capture session.
######################################################################
proc stop_poh_capture {} {
    global HSPD_POH

    stop_oh_capture $HSPD_POH

    send_command [BuildCommand 0xA4 2 $HSPD_POH 0]

    if {[is_nack [pong]] == 0} {
        puts "POH capture stopped."
    } else {
        puts "ERROR: Couldn't stop POH capture!"
    }
}

######################################################################
# Function Name    : stop_toh_capture
# Parameters       : None.
# Return Value     : None.
# Purpose          : Stop a capture session.
######################################################################
proc stop_toh_capture {} {
    global HSPD_TOH

    stop_oh_capture $HSPD_TOH

    send_command [BuildCommand 0xA4 2 $HSPD_TOH 0]

    if {[is_nack [pong]] == 0} {
        puts "TOH capture stopped."
    }
    else {
        puts "ERROR: Couldn't stop TOH capture!"
    }
}

######################################################################
# Function Name    : get_oh_capture_status
# Parameters       : oh is either HSPD_POH or HSPD_TOH
# Return Value     : Tells whether the capture is complete, and
#                    all buffers have been filled.
######################################################################
proc get_oh_capture_status {oh} {
    global HSPD_POH
    global HSPD_TOH

    send_command [BuildCommand 0xA5 1 $oh]
    set ret [pong]

    if {[is_nack $ret] == 1} {
        puts "Invalid parameter to get_oh_capture_status."
        return
    }
    
    set ohstr ???

    if {$oh == $HSPD_POH} {
        set ohstr POH
    } elseif {$oh == $HSPD_TOH} {
        set ohstr TOH
    }

    set oh [lindex $ret 2]
    set bufs_full [lindex $ret 3]
    set enabled [lindex $ret 4]
    set triggers [lindex $ret 5]
    set num_fired [lindex $ret 6]
    set abort [lindex $ret 7]
    if {$enabled == 1} {
        if {$bufs_full == 1} {
            puts "$ohstr capture is enabled; all bufs have been filled."
            if {$abort == 1} {
                puts "($ohstr capture was unable to complete normally.)"
            }
            return 1
        } else {
            puts "$ohstr capture is enabled; bufs are not yet full."
        }
    } else {
        puts "$ohstr capture is currently disabled."
    }
    puts "Currently configured to use $triggers triggers."
    puts "($num_fired triggers have fired so far.)"
    return 0
}

######################################################################
# Function Name    : get_poh_capture_status
# Parameters       : None.
# Return Value     : Tells whether the capture is complete, and
#                    all buffers have been filled.
######################################################################
proc get_poh_capture_status {} {
    global HSPD_POH

    return [get_oh_capture_status $HSPD_POH]
}

######################################################################
# Function Name    : get_toh_capture_status
# Parameters       : None.
# Return Value     : Tells whether the capture is complete, and
#                    all buffers have been filled.
######################################################################
proc get_toh_capture_status {} {
    global HSPD_TOH

    return [get_oh_capture_status $HSPD_TOH]
}

######################################################################
# Function Name    : is_oh_capture_complete
# Parameters       : None.
# Return Value     : 1 if capture is complete; 0 if not.
######################################################################
proc is_oh_capture_complete {oh} {

    send_command [BuildCommand 0xA5 1 $oh]
    set ret [pong]

    if {[print_error_on_nack $ret "Nack for is_oh_capture_complete."] == 1} {
        return
    }
    
    set bufs_full [lindex $ret 3]
    set enabled [lindex $ret 4]
    if {$enabled == 1} {
        if {$bufs_full == 1} {
            return 1
        }
    }
    return 0
}

######################################################################
# Function Name    : is_poh_capture_complete
# Parameters       : None.
# Return Value     : 1 if capture is complete; 0 if not.
######################################################################
proc is_poh_capture_complete {} {
    global HSPD_POH

    return [is_oh_capture_complete $HSPD_POH]
}

######################################################################
# Function Name    : is_toh_capture_complete
# Parameters       : None.
# Return Value     : 1 if capture is complete; 0 if not.
######################################################################
proc is_toh_capture_complete {} {
    global HSPD_TOH

    return [is_oh_capture_complete $HSPD_TOH]
}

######################################################################
# Function Name    : did_oh_capture_abnormally_abort
# Parameters       : None.
# Return Value     : 1 if capture abnormally aborted; 0 if not.
######################################################################
proc did_oh_capture_abnormally_abort {oh} {

    send_command [BuildCommand 0xA5 1 $oh]
    set ret [pong]

    if {[is_nack $ret] == 1} {
        puts "Nack for did_oh_capture_abnormally_abort."
        return 0
    }
    
    return [lindex $ret 7]
}

######################################################################
# Function Name    : did_poh_capture_abnormally_abort
# Parameters       : None.
# Return Value     : 1 if capture is complete; 0 if not.
######################################################################
proc did_poh_capture_abnormally_abort {} {
    global HSPD_POH

    return [did_oh_capture_abnormally_abort $HSPD_POH]
}

######################################################################
# Function Name    : did_toh_capture_abnormally_abort
# Parameters       : None.
# Return Value     : 1 if capture is complete; 0 if not.
######################################################################
proc did_toh_capture_abnormally_abort {} {
    global HSPD_TOH

    return [did_oh_capture_abnormally_abort $HSPD_TOH]
}

######################################################################
# Function Name    : show_oh_capture_data
# Parameters       : oh is either HSPD_TOH or HSPD_POH
#                    buf_num is the buffer number to read
# Return Value     : None.
# Purpose          : Retrieve all of the captured OH data
#                    from the specified TOH or POH buffer
######################################################################
proc show_oh_capture_data {oh buf_num} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0
    send_command [BuildCommand 0xAB 3 $oh $blade $buf_num]
    set ret [pong]

    if {[print_error_on_nack $ret "Invalid parameter to show_oh_capture_data."] == 1} {
        set_target $blade
        return
    }


    set b1 "0x[lindex $ret 5]"
    set b2 "0x[lindex $ret 6]"
    set total_entries [expr ($b1 << 8) + $b2]

    set results {}

    set pkt_num 1
    set got_pkt_num [lindex $ret 8]

    if {$pkt_num != $got_pkt_num} {
        puts "ERROR:  Received out-of-order packet!"
        puts "ERROR:  Expected #$pkt_num, got #$got_pkt_num."
        set_target $blade
        return
    }
    incr pkt_num

    puts "Count\tPrePost\tValue"

    while {1} {
        set entries [expr 0 + "0x[lindex $ret 7]"]
        set index 9

        for {set i 0} {$i<$entries} {incr i} {
            set b1 "0x[lindex $ret $index]"
            incr index
            set b2 "0x[lindex $ret $index]"
            incr index
            set count [expr ($b1 << 8) + $b2]

            set trigger [lindex $ret $index]
            incr index
            if {$trigger == 1} {
                set trigger_word POST
            } elseif {$trigger == 0} {
                set trigger_word PRE
            } else {
                set trigger_word ???
            }

            set byte_val [lindex $ret $index]
            incr index

            puts "$count\t$trigger_word\t0x$byte_val"
            set element {}
            lappend element $count
            lappend element $trigger_word 
            lappend element "0x$byte_val"
            set results [lappend results $element]
            #puts "element is $element"
        }

        set total_entries [expr $total_entries - $entries]

        if {$total_entries <= 0} {
            break;
        }

        set ret [pong]
        if {[print_error_on_nack $ret "Subsequent packet error."] == 1} {
            set_target $blade
            return
        }

        set got_pkt_num [lindex $ret 8]
        if {$pkt_num != $got_pkt_num} {
            puts "ERROR:  Received out-of-order packet!"
            puts "ERROR:  Expected #$pkt_num, got $got_pkt_num."
            set_target $blade
            return
        }
        incr pkt_num

    }

    set_target $blade
    return $results
}

######################################################################
# Function Name    : show_poh_capture_data
# Parameters       : buf_num is the buffer number to read
# Purpose          : Retrieve all of the captured data
#                    from the specified POH buffer
######################################################################
proc show_poh_capture_data {buf_num} {
    global HSPD_POH

    show_oh_capture_data $HSPD_POH $buf_num
}

######################################################################
# Function Name    : show_toh_capture_data
# Parameters       : blade is the blade number
#                    buf_num is the buffer number to read
# Purpose          : Retrieve all of the captured data
#                    from the specified TOH buffer
######################################################################
proc show_toh_capture_data {buf_num} {
    global HSPD_TOH

    show_oh_capture_data $HSPD_TOH $buf_num
}

######################################################################
# --------------------------------------------------------------------
# Configuration Commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : save_config
# Parameters       : none
# Return Value     : none
# Purpose          : Saves current configuration to EE
######################################################################
proc save_config {} {
    send_command [BuildCommand 0x30 0x01 0x01]

    after 3000
    set ret_val [parse_read_value]
    if {$ret_val != 0xFF} {
	puts "INFO: Successfully saved configuration."
    } else {
	puts "ERROR: could not save configuratiuon."
    }
}

######################################################################
# Function Name    : erase_config
# Parameters       : reg number
# Return Value     : none
# Purpose          : Erase all config information from the EE prom
######################################################################
proc erase_config {} {
    send_command [BuildCommand 0x33 0x01 0x01]

    after 3000
    set ret_val [parse_read_value]
    if {$ret_val != 0xFF} {
	puts "INFO: Configuration erased."
    } else {
	puts "ERROR: could not erase configuratiuon."
    }
}

######################################################################
# Function Name    : restore_config
# Parameters       : none
# Return Value     : none
# Purpose          : Loads saved configuration from EE
######################################################################
proc restore_config {} {
    send_command [BuildCommand 0x31 0x01 0x01]

    after 250
    set ret_val [parse_read_value]
    if {$ret_val != 0xFF} {
	puts "INFO: Successfully restored configuration."
    } else {
	puts "ERROR: could not restore configuratiuon."
    }
}

######################################################################
# Function Name    : factory_default
# Parameters       : none
# Return Value     : none
# Purpose          : loads the factory default configuration
#                  :  (must then use save_config to save back to EE)
######################################################################
proc factory_default {} {
    send_command [BuildCommand 0x32 0x00]

    after 150
    set ret_val [parse_read_value]
    if {$ret_val != 0xFF} {
	puts "INFO: Successfully restored factory defaults."
    } else {
	puts "ERROR: could not restore factory defaults."
    }
}


######################################################################
# --------------------------------------------------------------------
# Miscellaneous Utility Commands
# --------------------------------------------------------------------
######################################################################

######################################################################
# Function Name    : display_enabled
# Parameters       : int
# Return Value     : "Enabled" or "Disabled"
######################################################################
proc display_enabled {enabled} {
    if {$enabled == 0} {
        return "Disabled"
    } else {
        return "Enabled"
    }
}

######################################################################
# Function Name    : get_rnd
# Parameters       : type mult
# Return Value     : status
# Purpose          : 
######################################################################
proc get_rnd {type mult} {
    send_command [BuildCommand 0xF0 2 $type $mult ]
    set ret [lrange [pong] 2 5]
    set ret [format "0x%2.2X%2.2X%2.2X%2.2X" "0x[lindex $ret 0]" \
                                             "0x[lindex $ret 1]" \
                                             "0x[lindex $ret 2]" \
                                             "0x[lindex $ret 3]" ]
    set ret [expr 0 + $ret]
    return $ret
}

######################################################################
# Function Name    : list_from_value
# Parameters       : a value
# Return Value     : a list containing each byte of the value, MSB first
# Purpose          : *** INTERNAL USE ONLY ***
######################################################################
proc list_from_value {v n} {
    set l [list]

    for {set i [expr $n - 1]} {$i >= 0} {incr i -1} {
        lappend l [expr (int($v) >> ($i * 8)) & 0xFF]
    }

    return $l
}

######################################################################
# Function Name    : value_from_array
# Parameters       : array chars in hex
# Return Value     : a number
# Purpose          : 
######################################################################
proc value_from_array {b} {
    set len [llength $b]
    
    if {$len == 4} {
        set val "0x[lindex $b 0][lindex $b 1][lindex $b 2][lindex $b 3]"
    } elseif {$len == 2} {
        set val "0x[lindex $b 0][lindex $b 1]"
    } elseif {$len == 1} {
        set val "0x[lindex $b 0]"
    } elseif {$len > 4} {
        set val 0.0
        for {set i 0} {$i<$len} {incr i } {
            set val [expr $val * 256.0 ]
            set val [expr $val + "0x[lindex $b $i]"]
        }
        return $val
    }

    return [expr $val + 0]
}

######################################################################
# Function Name    : gem_set_delay
#                  : 
# Parameters       : profile delayval units
#                  : 
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  : 
#                  : args:
#                  : -no_commit:  don't commit the delay
#                  :           use gem_load_impairments to commit
#                  :
# Return Value     : none
#                  : 
# Purpose          : Set the delay for a particular network profile.
######################################################################
proc gem_set_delay {profile del {units "ms"} {commit_arg "-commit"}} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set del [expr $del * 1.0]

    if {$del < 0.0} {
        set del 0.0
    }

    set commit 1

    if {[regexp -nocase {^-no_commit$} $commit_arg tmp]} {
        set commit 0
    } elseif {[regexp -nocase {^-commit$} $commit_arg tmp]} {
        set commit 1
    } else {
        puts "ERROR:  Invalid argument '$commit_arg'."
        return
    }

    puts "gem_set_delay $profile $del $units"

    set del [delay_convert $del $units "words"]

    set del [expr floor($del+0.5)]
    for {set i 0} {$i<5} {incr i } {
        set b($i)  [expr int(fmod($del,256.0))]
        set del    [expr ($del / 256.0) ]
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x34 0x8 $blade $profile \
                                        $b(4) $b(3) $b(2) $b(1) $b(0) $commit]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_get_delay
#                  : 
# Parameters       : profile units
#                  : 
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  : 
# Return Value     : numeric delay value in the selected units
#                  : 
# Purpose          : Get the delay setting for a particular network profile.
######################################################################
proc gem_get_delay {profile {units "ms"}} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x35 0x2 $blade $profile]

    set b [lrange [pong] 4 8]

    set_target $blade

    set del 0.0
    for {set i 0} {$i<5} {incr i } {
        set del [expr $del * 256.0 ]
        set del [expr $del + "0x[lindex $b $i]"]
    }

    set del [delay_convert $del "words" $units]

    return $del
}



######################################################################
# Function Name    : gem_set_basic_jitter
#                  : 
# Parameters       : profile shape dmin davg dmax unix
#                  : 
#                  : shape: 1 - no jitter (impulse, uses davg only)
#                  :        2 - gaussian  (uses dmin and dmax only)
#                  :        3 - uniform   (uses dmin and dmax only)
#                  :        4 - internet  (long tailed, uses dmin and dmax only)
#                  : 
#                  : dmin/davg/dmax are in the specified units
#                  : 
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  :
# Purpose          : Set up basic jitter
######################################################################
proc gem_set_basic_jitter {profile shape dmin davg dmax {units "ms"}} {
    global JITTER_PDV
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_set_basic_jitter $profile $shape $dmin $davg $dmax $units"

    set dmin [expr $dmin * 1.0]
    set davg [expr $davg * 1.0]
    set dmax [expr $dmax * 1.0]

    if {$dmin < 0.0} {
        set dmin 0.0
    }
    if {$davg < 0.0} {
        set davg 0.0
    }
    if {$dmax < 0.0} {
        set dmax 0.0
    }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Calculate a few helpful values
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    set range [expr ($dmax - $dmin)]
    set mid   [expr ($dmax + $dmin)/2.0]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Make sure that they'll be OK.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    if {$shape != 1} {
	if {$range == 0} {
	    set range 0.01
	}
	if {$dmin == 0 && $mid == 0} {	
	    set dmax 0.2
	    set davg 0.1
	}
    }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Map the basic setting into advanced parameters
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    set delay_min $dmin
    set delay_max $dmax

    if {$shape == $JITTER_PDV(NONE)} { 
	set delay     $davg
	set delta_min [expr $davg / 100.0]
	set delta_max [expr $davg / 100.0]
	set spread    1.0
    } elseif {$shape == $JITTER_PDV(GAUSSIAN)} {
	set delay      $mid
	set delta_min [expr $range / 6.0]
	set delta_max [expr $range / 6.0]
	set spread    1.58
    } elseif {$shape == $JITTER_PDV(UNIFORM)} {
	set delay     [expr $dmin + $range/1000.0]
	set delta_min [expr $range / 100.0]
	set delta_max [expr $range * 100.0]
	set spread    0.1
    } elseif {$shape == $JITTER_PDV(INTERNET)} {
	set delay     [expr $dmin + $range/10.0]
	set delta_min [expr $range / 100.0]
	set delta_max [expr $range * 0.9]
	set spread    1.25
    }  else {
	puts "ERROR: gem_set_basic_jitter: shape=$shape is invalid. Must be 1-4\n"
	return
    }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # 1)Set the delay, 2)jitter parameters, and 3)enable&select all packets
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    gem_set_jitter_cfg 	$profile  $delay_min $delay_max $delta_min $delta_max $units $spread
    gem_set_delay      	$profile  $delay $units
    if {($shape > 1) && ($shape <= 4)} {
	gem_enable_jitter  	$profile  $STAT_DISTRIB(PERIODIC) 1 1
    } else {
	gem_disable_jitter  	$profile
    }
}

######################################################################
# Function Name    : gem_set_jitter_cfg
#                  : 
# Parameters       : profile delay_min delay_max delta_min delta_max
#                  : 
#                  : delay_min/delay_max/delta_min/delta_max
#                  :     are in the specified units
#                  : 
#                  : units is one of ms,us,ns,km,meters,m,bits,b,bytes,B
#                  :   if units is omitted, "ms" is the default
#                  :
# Purpose          : Set up the jitter configuration parameters.
######################################################################
proc gem_set_jitter_cfg {profile delay_min delay_max delta_min delta_max {units "ms"} {spread 1.0}} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_set_jitter_cfg $profile $delay_min $delay_max $delta_min $delta_max $units"

    set delta_min [expr $delta_min * 1.0]
    set delta_max [expr $delta_max * 1.0]
    set delay_min [expr $delay_min * 1.0]
    set delay_max [expr $delay_max * 1.0]
    set spread    [expr $spread    * 1.0]

    if {$delta_min < 0.0} {
        set delta_min 0.0
    }
    if {$delta_max < 0.0} {
        set delta_max 0.0
    }
    if {$delay_min < 0.0} {
        set delay_min 0.0
    }
    if {$delay_max < 0.0} {
        set delay_max 0.0
    }

    if {$spread < 0.1} {
        set spread 0.1
    }
    if {$spread > 100} {
        set spread 100
    }

    set delta_min [delay_convert $delta_min $units "words"]
    set delta_max [delay_convert $delta_max $units "words"]
    set delay_min [delay_convert $delay_min $units "words"]
    set delay_max [delay_convert $delay_max $units "words"]

    set delta_min [expr floor($delta_min+0.5)]
    set delta_max [expr floor($delta_max+0.5)]
    for {set i 0} {$i<5} {incr i } {
        set dltamin($i)  [expr int(fmod($delta_min, 256.0))]
        set delta_min [expr ($delta_min / 256.0) ]
        set dltamax($i)  [expr int(fmod($delta_max, 256.0))]
        set delta_max [expr ($delta_max / 256.0) ]
    }

    set delay_min [expr floor($delay_min+0.5)]
    set delay_max [expr floor($delay_max+0.5)]
    for {set i 0} {$i<4} {incr i } {
        set dlymin($i)  [expr int(fmod($delay_min, 256.0))]
        set delay_min [expr ($delay_min / 256.0) ]
        set dlymax($i)  [expr int(fmod($delay_max, 256.0))]
        set delay_max [expr ($delay_max / 256.0) ]
    }

    set spread        [expr round($spread*10)];
    set spreadbyte(0) [expr $spread & 0xFF]
    set spread        [expr $spread >>8]
    set spreadbyte(1) [expr $spread & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x36 22 $blade $profile \
                               $dlymin(3) $dlymin(2) $dlymin(1) $dlymin(0) \
                               $dlymax(3) $dlymax(2) $dlymax(1) $dlymax(0) \
                               $dltamin(4) $dltamin(3) $dltamin(2) $dltamin(1) $dltamin(0) \
                               $dltamax(4) $dltamax(3) $dltamax(2) $dltamax(1) $dltamax(0) \
                               $spreadbyte(1) $spreadbyte(0) ]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_get_jitter_cfg
#                  : 
# Parameters       : profile {units}
#                  : 
#                  : profile is the network profile ID
#                  : units is an optional parameter; default is "ms"
#                  : 
# Purpose          : Get the current jitter configuration parameters.
######################################################################
proc gem_get_jitter_cfg {profile {units "ms"}} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x37 0x2 $blade $profile]

    set b [lrange [pong] 4 end]

    set_target $blade

    set delay_min [value_from_array [lrange $b 0 3]]
    set delay_max [value_from_array [lrange $b 4 7]]
    set delta_min [value_from_array [lrange $b 8 11]]
    set delta_max [value_from_array [lrange $b 12 15]]

    set udelay_min [delay_convert $delay_min "words" $units]
    set udelay_max [delay_convert $delay_max "words" $units]
    set udelta_min [delay_convert $delta_min "words" "ms"]
    set udelta_max [delay_convert $delta_max "words" "ms"]

    set spread     [value_from_array [lrange $b 16 17]]
    set spread     [expr ($spread/10)]

    puts "Delay Min:  $udelay_min $units"
    puts "Delay Max:  $udelay_max $units"
    puts "Delta Min:  $udelta_min ms"
    puts "Delta Max:  $udelta_max ms"
    puts "Spread:     $spread"

}


######################################################################
# Function Name    : gem_enable_basic_bwlimit
#                  : 
# Parameters       : profile      - which network profile to use
#                  : 
#                  : bitrateindex - 
#                  :  	 $BASIC_BWLIMIT_BITRATE(OC3)       1  
#                  :  	 $BASIC_BWLIMIT_BITRATE(DS3)       2 
#                  :  	 $BASIC_BWLIMIT_BITRATE(E3)        3 
#                  :  	 $BASIC_BWLIMIT_BITRATE(4Mb)       4 
#                  :  	 $BASIC_BWLIMIT_BITRATE(E1)        5 
#                  :  	 $BASIC_BWLIMIT_BITRATE(DS1)       6 
#                  :  	 $BASIC_BWLIMIT_BITRATE(768kb)     7 
#                  :  	 $BASIC_BWLIMIT_BITRATE(384kb)     8 
#                  :  	 $BASIC_BWLIMIT_BITRATE(144kb)     9 
#                  :  	 $BASIC_BWLIMIT_BITRATE(128kb)     10 
#                  :  	 $BASIC_BWLIMIT_BITRATE(64kb)      11
#                  : 
#                  : bufsizeindex - 
#                  :  	 $BASIC_BWLIMIT_BUFSIZE(1MB)       1 
#                  :  	 $BASIC_BWLIMIT_BUFSIZE(512kB)     2 
#                  :  	 $BASIC_BWLIMIT_BUFSIZE(256kB)     3 
#                  :  	 $BASIC_BWLIMIT_BUFSIZE(128kB)     4 
#                  :  	 $BASIC_BWLIMIT_BUFSIZE(64kB)      5 
#                  :  	 $BASIC_BWLIMIT_BUFSIZE(32kB)      6 
#                  :  	 $BASIC_BWLIMIT_BUFSIZE(16kB)      7 
#                  :  	 $BASIC_BWLIMIT_BUFSIZE(8kB)       8 
#                  : 
# Purpose          : Configure and enable the policer/shaper using
#                  : simplified parameters
#                  : 
######################################################################
proc gem_enable_basic_bwlimit {profile bitrateindex bufsizeindex} {
    global       GEM_MAX_PROFILES
    global 	 BASIC_BWLIMIT_BITRATE
    global 	 BASIC_BWLIMIT_BUFSIZE

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_enable_basic_bwlimit $profile $bitrateindex $bufsizeindex"

    set bitrate 4000

    if       {$bitrateindex == $BASIC_BWLIMIT_BITRATE(OC3)}   { set bitrate   155520.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(DS3)}   { set bitrate    44736.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(E3)}    { set bitrate    34368.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(4Mb)}   { set bitrate     4000.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(E1)}    { set bitrate     2048.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(DS1)}   { set bitrate     1544.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(768kb)} { set bitrate      768.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(384kb)} { set bitrate      384.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(144kb)} { set bitrate      144.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(128kb)} { set bitrate      128.0
    } elseif {$bitrateindex == $BASIC_BWLIMIT_BITRATE(64kb)}  { set bitrate       64.0
    } else {
	puts "ERROR: Invalid bitrateindex, must be between 1 and 11."
        return
    }

    if       {$bufsizeindex == $BASIC_BWLIMIT_BUFSIZE(1MB)}   { set bufsize [expr 1024.0 * 1024 - 1]
    } elseif {$bufsizeindex == $BASIC_BWLIMIT_BUFSIZE(512kB)} { set bufsize [expr  512.0 * 1024]
    } elseif {$bufsizeindex == $BASIC_BWLIMIT_BUFSIZE(256kB)} { set bufsize [expr  256.0 * 1024]
    } elseif {$bufsizeindex == $BASIC_BWLIMIT_BUFSIZE(128kB)} { set bufsize [expr  128.0 * 1024]
    } elseif {$bufsizeindex == $BASIC_BWLIMIT_BUFSIZE(64kB)}  { set bufsize [expr   64.0 * 1024]
    } elseif {$bufsizeindex == $BASIC_BWLIMIT_BUFSIZE(32kB)}  { set bufsize [expr   32.0 * 1024]
    } elseif {$bufsizeindex == $BASIC_BWLIMIT_BUFSIZE(16kB)}  { set bufsize [expr   16.0 * 1024]
    } elseif {$bufsizeindex == $BASIC_BWLIMIT_BUFSIZE(8kB)}   { set bufsize [expr    8.0 * 1024]
    } else {							 set bufsize [expr 1024.0 * 1024 - 1]
	puts "ERROR: Invalid bufsizeindex, must be between 1 and 8."
        return
    }

    gem_enable_shaper $profile $bitrate $bufsize 0 0 0 $bitrate 0

}

######################################################################
# Function Name    : gem_enable_policer
#                  : 
# Parameters       : profile - which network profile to use
#                  : CIR - committed bitrate in Kbps
#                  : CBS - committed burst size in bytes
#                  : EIR - excess bitrate in Kbps
#                  : EBS - excess burst size in bytes
#                  : coupling - 1 if you want to connect committed
#                  :            and excess buffers, 0 otherwise
#                  : 
#                  : 
# Purpose          : Configure and enable the policer.
######################################################################
proc gem_enable_policer {profile cir cbs eir ebs coupling} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_enable_policer $profile $cir $cbs $eir $ebs $coupling"

    for {set i 0} {$i<4} {incr i } {
        set dcir($i)  [expr int(fmod($cir, 256.0))]
        set dcbs($i)  [expr int(fmod($cbs, 256.0))]
        set deir($i)  [expr int(fmod($eir, 256.0))]
        set debs($i)  [expr int(fmod($ebs, 256.0))]
        set cir [expr ($cir / 256.0) ]
        set cbs [expr ($cbs / 256.0) ]
        set eir [expr ($eir / 256.0) ]
        set ebs [expr ($ebs / 256.0) ]
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x38 19 $blade $profile \
                               $dcir(3) $dcir(2) $dcir(1) $dcir(0) \
                               $dcbs(3) $dcbs(2) $dcbs(1) $dcbs(0) \
                               $deir(3) $deir(2) $deir(1) $deir(0) \
                               $debs(3) $debs(2) $debs(1) $debs(0) \
                               $coupling]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_enable_shaper
#                  : 
# Parameters       : profile - which network profile to use
#                  : rate - 
#                  : burst - 
#                  : 
# Purpose          : Configure and enable the shaper.
######################################################################
proc gem_enable_shaper {profile cir cbs eir ebs coupling rate burst} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

	if {$rate < ($cir + $eir)} { 
        puts -nonewline "Shaper Rate less the Policer Rate:  "
        puts -nonewline "Please specify a shaper rate greater than or equal "
        puts "[expr $cir + $eir]."
        return
	}

    puts "gem_enable_shaper $profile $cir $cbs $eir $ebs $coupling $rate $burst"

    for {set i 0} {$i<4} {incr i } {
        set dcir($i)  [expr int(fmod($cir, 256.0))]
        set dcbs($i)  [expr int(fmod($cbs, 256.0))]
        set deir($i)  [expr int(fmod($eir, 256.0))]
        set debs($i)  [expr int(fmod($ebs, 256.0))]
        set drate($i)   [expr int(fmod($rate, 256.0))]
        set dburst($i)  [expr int(fmod($burst, 256.0))]

        set cir [expr ($cir / 256.0) ]
        set cbs [expr ($cbs / 256.0) ]
        set eir [expr ($eir / 256.0) ]
        set ebs [expr ($ebs / 256.0) ]
        set rate  [expr ($rate / 256.0) ]
        set burst [expr ($burst / 256.0) ]
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9B 28 $blade $profile 0x03 \
					  $dcir(3) $dcir(2) $dcir(1) $dcir(0) \
					  $dcbs(3) $dcbs(2) $dcbs(1) $dcbs(0) \
					  $deir(3) $deir(2) $deir(1) $deir(0) \
					  $debs(3) $debs(2) $debs(1) $debs(0) \
					  $coupling \
					  $drate(3)  $drate(2)  $drate(1)  $drate(0) \
					  $dburst(3) $dburst(2) $dburst(1) $dburst(0)]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_disable_policer
#                  : 
# Parameters       : profile 
#                  : 
# Purpose          : Disable the policer for the specified network profile.
######################################################################
proc gem_disable_policer {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_disable_policer $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x39 2 $blade $profile]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_disable_shaper
#                  : 
# Parameters       : profile 
#                  : 
# Purpose          : Disable the shaper for the specified network profile.
######################################################################
proc gem_disable_shaper {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_disable_shaper $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9B 3 $blade $profile 0x04]
    pong_check

    set_target $blade
}

set FIXED 0
set ROUND_ROBIN 1
######################################################################
# Function Name    : gem_set_priority_schedule
#                  : 
# Parameters       : schedule
#                    1 == Round Robin, 0 == Fixed (Use string instead?)
#                  : 
# Purpose          : Set the output priority scheduler.
######################################################################
proc gem_set_priority_schedule {schedule} {
    global TX_DEST_ADDR
    global FIXED
    global ROUND_ROBIN

    if {$schedule != $FIXED && $schedule != $ROUND_ROBIN} {
        puts -nonewline "Please specify a valid priority schedule type. "
        puts "0 - Fixed ($FIXED), 1 - Round Robin ($ROUND_ROBIN)"
        return;
    }
    
    puts "gem_set_priority_schedule $schedule"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xA2 2 $blade $schedule]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_get_priority_schedule
#                  : 
# Parameters       : none
#                  :
# Return Value     : $shed (0=Fixed,1=Round Robin)
#                  :
# Purpose          : Get the output priority scheduler.
#                    
######################################################################
proc gem_get_priority_schedule {} {
#    send_command [BuildCommand 0xA3 0x0]
#    return [parse_read_value]
    global TX_DEST_ADDR
    global FIXED
    global ROUND_ROBIN

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xA3 1 $blade]
    set ret [lrange [pong] 2 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set sched [expr "0x[lindex $ret 1]" + 0]
    if {$sched == $FIXED} {
        return "FIXED"
    } elseif {$sched == $ROUND_ROBIN} {
        return "ROUND_ROBIN"
    } else {
        return $sched
    }
}


######################################################################
# Function Name    : gem_get_policer_cfg
#                  : 
# Parameters       : profile
#                  : 
# Purpose          : Get the current policer configuration.
######################################################################
proc gem_get_policer_cfg {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x3a 2 $blade $profile]
    set b [lrange [pong] 4 end]

    set enabled [value_from_array [lindex $b 0]]
    set CIR [value_from_array [lrange $b 1 4]]
    set CBS [value_from_array [lrange $b 5 8]]
    set EIR [value_from_array [lrange $b 9 12]]
    set EBS [value_from_array [lrange $b 13 16]]
    set coupled [value_from_array [lindex $b 17]]

    if {$enabled == 0} {
        puts "The policer is currently disabled."
    } else {
        puts "The policer is currently Enabled."
        puts "  CIR: $CIR Kbps"
        puts "  CBS: $CBS bytes"
        puts "  EIR: $EIR Kbps"
        puts "  EBS: $EBS bytes"
        if {$coupled == 0} {
            puts "  Coupling:  Disabled"
        } else {
            puts "  Coupling:  Enabled"
        }
    }

    set_target $blade
}


######################################################################
# Function Name    : gem_get_shaper_cfg
#                  : 
# Parameters       : profile
#                  : 
# Purpose          : Get the current shaper configuration.
######################################################################
proc gem_get_shaper_cfg {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9B 3 $blade $profile 0x01]
    set b [lrange [pong] 4 end]

    set enabled [value_from_array [lindex $b 0]]
    set rate [value_from_array [lrange $b 1 4]]
    set burst [value_from_array [lrange $b 5 8]]

    if {$enabled == 0} {
        puts "The shaper is currently disabled."
    } else {
        puts "The shaper is currently Enabled."
        puts "  Rate:  $rate Kbps"
        puts "  Burst: $burst bytes"
    }

    set_target $blade
}


######################################################################
# Function Name    : gem_set_BER <value> <options>
#                  : 
# Parameters       : <value> is the desired BER (e.g. 1.5E-9)
#                  : 
#                  : <options> can be one or more of the following:
#                  : 
#                  : Error Type options
#                  : 
#                  :   -burst=<n> - inserts a burst of N consecutive errors
#                  :                  (1 is the default)
#                  :   -burstlenvar=<n> - 0, 1, 2, 4, 8, 16, 32, 64, 128, 256,
#                  :                      512, 1024, 2048, 4096, 8192, or 16384
#                  :                  (0 is the default)
#                  :   -repeat=<n> - 0 means 1-shot, 65535 means forever
#                  :                      (65535 is the default)
#                  :   -invert - (default) invert the errored bits
#                  :   -force1 - force the errored bits to be a 1
#                  :   -force0 - force the errored bits to be a 0
#                  : 
# Purpose          : Sets the BER to be inserted 
######################################################################
proc gem_set_BER {args} {
    global TX_DEST_ADDR
    global BITRATE_GE1GFS
    global BITRATE_GE1GFD

	# get operating bitrate to be sure that BER is supported
    set oprate "0x[get_operating_bitrate]"

    if {($oprate != $BITRATE_GE1GFS) && ($oprate != $BITRATE_GE1GFD)} {
        puts "GEM BER is not supported in copper mode."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    set ber_burstlen      0x1
    set ber_burstlenvar   0
    set ber_interval      0
    set ber_repeat        65535
    set pattern           2

    set cmderrflag        0

    puts "gem_set_BER $args"

    # ----------------------------------------------------------------
    # Parse the command options
    # ----------------------------------------------------------------
    foreach a $args {
        if {[regexp -nocase {^([-+.E0-9]+)$} $a tmp ber_value]} {
            # peachy, check value below
        } \
        elseif {[regexp -nocase {^-burst=([0-9]+)$} $a tmp ber_burstlen]} {
            # peachy, too!
        } \
        elseif {[regexp -nocase {^-burstlenvar=([0-9]+)$} $a tmp ber_burstlenvar]} {
            # tastes great!
        } \
        elseif {[regexp -nocase {^-repeat=([0-9]+)$} $a tmp ber_repeat]} {
            # less filling!
        } \
        elseif {[regexp -nocase {^-invert} $a]} {
            set pattern 2
        } \
        elseif {[regexp -nocase {^-force1} $a]} {
            set pattern 1
        } \
        elseif {[regexp -nocase {^-force0} $a]} {
            set pattern 0
        } \
        else {
            puts "ERROR: gem_set_BER: bad argument '$a'."
            incr cmderrflag
        }
    }

    # ----------------------------------------------------------------
    # If there were command errors, print usage message
    # ----------------------------------------------------------------
    if {[string compare $ber_value "xxxx"] == 0} {
        puts "ERROR: set_BER: Missing BER <value>"
        incr cmderrflag
    }

    if {$ber_burstlen <= 0} {
        puts "ERROR: burst length must be >= 1."
        set_target $blade
        return
    }

    if {$ber_value < 0} {
        puts "ERROR: gem_set_BER: Bad BER value $ber_value"
        set_target $blade
        return
    }

    if {$ber_burstlenvar != 0     && \
        $ber_burstlenvar != 1     && \
        $ber_burstlenvar != 2     && \
        $ber_burstlenvar != 4     && \
        $ber_burstlenvar != 8     && \
        $ber_burstlenvar != 16    && \
        $ber_burstlenvar != 32    && \
        $ber_burstlenvar != 64    && \
        $ber_burstlenvar != 128   && \
        $ber_burstlenvar != 256   && \
        $ber_burstlenvar != 512   && \
        $ber_burstlenvar != 1024  && \
        $ber_burstlenvar != 2048  && \
        $ber_burstlenvar != 4096  && \
        $ber_burstlenvar != 8192  && \
        $ber_burstlenvar != 16384} {
            puts "ERROR: gem_set_BER: Burst length variation must be a power of 2."
            set_target $blade
            return
    }

    if {$cmderrflag} {
        puts ""
        puts "usage: gem_set_BER <value>  "
        puts ""
        puts "gem set_BER <value> <options>"
        puts ""
        puts "<value> is the desired BER (e.g. 1.5E-9)"
        puts "Specifying a <value> of 0 turns off errors"
        puts ""
        puts "<options> can be one or more of the following:"
        puts ""
        puts "Error Type options"
        puts ""
        puts "     -burst=<n> - inserts a burst of N consecutive errors"
        puts "                        (1 is the default)"
        puts "     -burstlenvar=<n> - 0, 1, 2, 4, 8, 16, 32, 64, 128, 256,"
        puts "                        512, 1024, 2048, 4096, 8192, or 16384"
        puts "                        (0 is the default)"
        puts "     -repeat=<n> - 0 means 1-shot, 65535 means forever"
        puts "                        (65535 is the default)"
        puts "     -invert - (default) invert the errored bits"
        puts "     -force1 - force the errored bits to be a 1"
        puts "     -force0 - force the errored bits to be a 0"
        puts ""
        puts ""
        set_target $blade
        return
    }

    # ----------------------------------------------------------------
    # Convert BER rate to an interval
    # ----------------------------------------------------------------
    set ber_interval [BER_rate2interval $ber_value]

    # ----------------------------------------------------------------
    # break down ber_interval into 5 bytes 
    # ----------------------------------------------------------------
    set divisor   [expr {256.0 * 256.0 * 256.0 * 256.0 * 256.0 * 256.0 * 256.0}]
    for {set i 0} {$i<8} {incr i} {
        set tmp            [expr {$ber_interval / $divisor}]
        set ltmp           [expr {int($tmp)}]
        set berbyte($i)    $ltmp
        set ber_interval   [expr {$ber_interval - ($ltmp * $divisor)}]
        set divisor        [expr {$divisor / 256.0}]
    }

    # ----------------------------------------------------------------
    # break down ber_burstlen, ber_burstlenvar & ber_repeat
    # ----------------------------------------------------------------
    set burstbyte(0) [expr ($ber_burstlen >> 8) & 0xFF]
    set burstbyte(1) [expr ($ber_burstlen >> 0) & 0xFF]

    set varlen(0)    [expr ($ber_burstlenvar >> 8) & 0xFF]
    set varlen(1)    [expr ($ber_burstlenvar >> 0) & 0xFF]

    set repeat(0)    [expr ($ber_repeat >> 8) & 0xFF]
    set repeat(1)    [expr ($ber_repeat >> 0) & 0xFF]

    # ----------------------------------------------------------------
    # Now send the command
    # ----------------------------------------------------------------
    send_command [BuildCommand 0x3B 16 $blade \
                  $berbyte(0) $berbyte(1) $berbyte(2) $berbyte(3) \
                  $berbyte(4) $berbyte(5) $berbyte(6) $berbyte(7) \
                  $burstbyte(0) $burstbyte(1) \
                  $varlen(0) $varlen(1) \
                  $repeat(0) $repeat(1) \
                  $pattern ]

    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_disable_BER
# Parameters       : none
# Return Value     : Disable any currently set line BER
######################################################################
proc gem_disable_BER {} {
    gem_set_BER 0
}


######################################################################
# Function Name    : gem_get_BER
# Parameters       : none
# Return Value     : Current bit error rate settings for target
# Purpose          : See discussion above for set_BER for a detailed
#                  :   description of possible return values.
######################################################################
proc gem_get_BER {} {
    global TX_DEST_ADDR
    global BITRATE_GE1GFS
    global BITRATE_GE1GFD

	# get operating bitrate to be sure that BER is supported
    set oprate "0x[get_operating_bitrate]"

    if {($oprate != $BITRATE_GE1GFS) && ($oprate != $BITRATE_GE1GFD)} {
        puts "GEM BER is not supported in copper mode."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x3C 1 $blade]
    set ret [lrange [pong] 2 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set enabled [expr "0x[lindex $ret 1]" + 0]
    if {$enabled == 0} {
        return "0"
    }

    # ------------------------------------------------------------
    # Get rate 
    # ------------------------------------------------------------
    set berreg(7) "0x[lindex $ret 2 ]"
    set berreg(6) "0x[lindex $ret 3 ]"
    set berreg(5) "0x[lindex $ret 4 ]"
    set berreg(4) "0x[lindex $ret 5 ]"
    set berreg(3) "0x[lindex $ret 6 ]"
    set berreg(2) "0x[lindex $ret 7 ]"
    set berreg(1) "0x[lindex $ret 8 ]"
    set berreg(0) "0x[lindex $ret 9 ]"
    
    set ber_interval 0.0
    for {set i 7} {$i>=0} {incr i -1} {
        set ber_interval  [expr {$ber_interval * 256.0 }]
        set ber_interval  [expr {$ber_interval + $berreg($i)}]
    }
    
    set ber  [BER_interval2rate $ber_interval]
    set berstr [format "%9.2e" $ber]

    # ------------------------------------------------------------
    # Get burstlen, variation and repeat cnt
    # ------------------------------------------------------------
    set ber_burstlen    [value_from_array [lrange $ret 10 11]]
    set ber_burstlenvar [value_from_array [lrange $ret 12 13]]
    set ber_repeat      [value_from_array [lrange $ret 14 15]]
    set pattern         [value_from_array [lindex $ret 16]]

    puts -nonewline "BER:  $berstr"

    if {$pattern == 2} {
        puts "  (INVERT)"
    } elseif {$pattern == 1} {
        puts "  (FORCE 1)"
    } elseif {$pattern == 0} {
        puts "  (FORCE 0)"
    }

    if {$ber_burstlen != 1} {
        puts "Burst length:  $ber_burstlen"
    }

    if {$ber_burstlenvar != 0} {
        puts "Burst length variation:  $ber_burstlenvar"
    }
	
    if {$ber_repeat == 0} {
        puts "Repeat:  0  (One-shot)"
    } elseif {$ber_repeat != 65535} {
        puts "Repeat:  $ber_repeat"
    }
}

######################################################################
# Function Name    : gem_enable_impairment
#                  :
# Purpose          : *** INTERNAL USE ONLY ***
######################################################################
proc gem_enable_impairment {cmd profile dist burstlen interval args} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {$dist == $STAT_DISTRIB(POISSON)} {
        if {$interval > 26464832} {
            puts "Interval must be less than 26464832."
            return
        }
    } else {
        if {$interval > 268000000} {
            puts "Interval must be less than 268000000."
            return
        }
    }

    if {$burstlen > $interval} {
        puts "Interval must be greater than or equal to the burst length."
        return
    }

    if {$dist != $STAT_DISTRIB(UNIFORM) && \
        $dist != $STAT_DISTRIB(PERIODIC) && \
        $dist != $STAT_DISTRIB(POISSON) && \
        $dist != $STAT_DISTRIB(GAUSSIAN)} {
        puts "Distribution must be either \$STAT_DISTRIB(PERIODIC), \$STAT_DISTRIB(UNIFORM),"
        puts "\$STAT_DISTRIB(POISSON) or \$STAT_DISTRIB(GAUSSIAN)."
        return;
    }

    if {$dist == $STAT_DISTRIB(UNIFORM) || \
        $dist == $STAT_DISTRIB(POISSON) || \
        $dist == $STAT_DISTRIB(GAUSSIAN)} {
        if {$interval == $burstlen} {
            puts "When selecting every packet for impairment,"
            puts "only \$STAT_DISTRIB(PERIODIC) is allowed."
            return
        }
    }

    set burstdur 65535
    set std_dev 1.0
    set use_rnd 1
    set use_trig 0
    set commit 1
    set cond_num 0xFF

    foreach a $args {
        if {[regexp -nocase {^-repeat=([0-9]+)$} $a tmp burstdur]} {
            if {$burstdur < 1 || $burstdur > 65535} {
                puts "The repeat count must be between 1 and 65535."
                puts "A value of 65535 means forever."
                return
            }
        } elseif {[regexp -nocase {^-std_dev=([\.0-9]+)$} $a tmp std_dev]} {
            if {$std_dev > 100.0 || $std_dev < 0.0} {
                puts "The standard deviation should be between 0-100%."
                return
            }
        } elseif {[regexp -nocase {^-trigger=([0-9]+)$} $a tmp cond_num]} {
            if {$cond_num != 0 && $cond_num != 1} {
                puts "The trigger condition number must be either 0 or 1."
                return
            }
            set use_trig 1

        } elseif {[regexp -nocase {^-no_rnd_sel$} $a tmp]} {
            set use_rnd 0
        } elseif {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }

    }

    set blade $TX_DEST_ADDR
    set_target 0

    set itvbyte(0) [expr ($interval >> 24) & 0xFF]
    set itvbyte(1) [expr ($interval >> 16) & 0xFF]
    set itvbyte(2) [expr ($interval >> 8) & 0xFF]
    set itvbyte(3) [expr ($interval >> 0) & 0xFF]

    set burstlenbyte(0) [expr ($burstlen >> 8) & 0xFF]
    set burstlenbyte(1) [expr ($burstlen >> 0) & 0xFF]

    set burstdurbyte(0) [expr ($burstdur >> 8) & 0xFF]
    set burstdurbyte(1) [expr ($burstdur >> 0) & 0xFF]

    set std_dev [expr $std_dev * 100]
    set std_devbyte(0) [expr (int($std_dev) >> 8) & 0xFF]
    set std_devbyte(1) [expr (int($std_dev) >> 0) & 0xFF]

    send_command [BuildCommand $cmd 17 $blade $profile $use_rnd \
                               $use_trig $cond_num $commit $dist \
                               $burstlenbyte(0) $burstlenbyte(1) \
                               $itvbyte(0) $itvbyte(1) $itvbyte(2) $itvbyte(3) \
                               $burstdurbyte(0) $burstdurbyte(1) \
                               $std_devbyte(0) $std_devbyte(1)]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_load_impairments
#                  :
#                  : profile - profile number on which to commit
#                  :      previously enabled impairments (set with -no_commit)
#                  :
######################################################################
proc gem_load_impairments {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x3D 2 $blade $profile]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_impairment
#                  :
# Purpose          : *** INTERNAL USE ONLY ***
######################################################################
proc gem_disable_impairment {cmd profile args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    set use_rnd  0
    set use_trig 0
    set cond_num 0
    set commit   1

    foreach a $args {
        if {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            set_target $blade
            return
        }
    }

    send_command [BuildCommand $cmd 6 $blade $profile $use_rnd \
                                      $use_trig $cond_num $commit ]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_enable_pkt_corruption
#                  :
# Parameters       : Packets affected by pkt_corruption are chosen by the
#                  : following parameters:
#                  :
#                  : profile - profile number to apply to
#                  : dist - type of distribution to apply
#                  :     $STAT_DISTRIB(UNIFORM), $STAT_DISTRIB(PERIODIC),
#                  :     $STAT_DISTRIB(POISSON), or $STAT_DISTRIB(GAUSSIAN),
#                  : burstlen - number of packets at a time to corruption
#                  : interval - interval over which to perform the corruption
#                  : rate - corruption bitrate for selected packets and bytes
#                  :
#                  : args:
#                  : -fixedbl:  e.g., -fixedbl=4 means a fixed
#                  :            corruption burstlen of 4 bytes
#                  : -randbl:   e.g., -randbl=1-3 means a random
#                  :            corruption burstlen of 1-3 bytes at a time
#                  : *** default is a fixed bl of 1 byte ***
#                  :
#                  : -offset:   e.g., -offset=3-4 means only corrupt
#                  :            bytes 3 through 4 of any packet
#                  : *** default is to corrupt any byte within the packet ***
#                  :
#                  : -no_commit:  don't commit the pkt corruption
#                  :           use gem_load_impairments to commit
#                  : -repeat:  e.g., -repeat=4 means to repeat this
#                  :           impairment 4 times, then stop
#                  : -std_dev:  e.g., -std_dev=1.0 means to use a 1.0%
#                  :           standard deviation in the case of a Gaussian
#                  :           distribution
#                  :
#                  :
# Purpose          : Turn on packet corruption for the specified profile.
######################################################################
proc gem_enable_pkt_corruption {profile dist burstlen interval rate args} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global PKTCORRUPT_BL_FIXED
    global PKTCORRUPT_BL_RAND
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {$burstlen > $interval} {
        puts "Interval must be greater than or equal to the burst length."
        return
    }

    if {$dist == $STAT_DISTRIB(POISSON)} {
        if {$interval > 26464832} {
            puts "Interval must be less than 26464832."
            return
        }
    } else {
        if {$interval > 268000000} {
            puts "Interval must be less than 268000000."
            return
        }
    }

    if {$dist != $STAT_DISTRIB(UNIFORM) && \
        $dist != $STAT_DISTRIB(PERIODIC) && \
        $dist != $STAT_DISTRIB(POISSON) && \
        $dist != $STAT_DISTRIB(GAUSSIAN)} {
        puts "Distribution must be either \$STAT_DISTRIB(PERIODIC), \$STAT_DISTRIB(UNIFORM),"
        puts "\$STAT_DISTRIB(POISSON) or \$STAT_DISTRIB(GAUSSIAN)."
        return;
    }

    if {$dist == $STAT_DISTRIB(UNIFORM) || \
        $dist == $STAT_DISTRIB(POISSON) || \
        $dist == $STAT_DISTRIB(GAUSSIAN)} {
        if {$interval == $burstlen} {
            puts "When selecting every packet for impairment,"
            puts "only \$STAT_DISTRIB(PERIODIC) is allowed."
            return
        }
    }


    if {$rate <= 0.0} {
        puts "Specified corruption rate must be > 0."
        return
    }

    puts "gem_enable_pkt_corruption $profile $dist $burstlen $interval $rate $args"

    set max_corrupt_intv [expr 65536.0 * 65536.0 - 1.0]
    set corrupt_intv [expr 1.0/$rate]

    if {$corrupt_intv > $max_corrupt_intv} {
        set corrupt_intv $max_corrupt_intv
    } elseif {$corrupt_intv <= 1.0} {
        set $corrupt_intv 1.0
    }
    set corrupt_intv [expr round($corrupt_intv)]

    set beg_offset 1
    set end_offset 2
    set min_bl 1
    set max_bl 2
    set fixed_bl 1
    set bltype  $PKTCORRUPT_BL_FIXED
    set use_offset 0

    set burstdur 65535
    set std_dev 1.0
    set use_rnd 1
    set use_trig 0
    set commit 1
    set cond_num 0xFF

    foreach a $args {
        if {[regexp -nocase {^-fixedbl=([0-9]+)$} $a tmp fixed_bl]} {
            set bltype $PKTCORRUPT_BL_FIXED
        } elseif {[regexp -nocase {^-randbl=([0-9]+)-([0-9]+)$} $a tmp min_bl max_bl]} {
            set bltype $PKTCORRUPT_BL_RAND
            if {$min_bl >= $max_bl} {
                puts "Random burst length must be a range:  -randbl=min-max where min < max."
                return
            }
        } elseif {[regexp -nocase {^-offset=([0-9]+)-([0-9]+)$} $a tmp beg_offset end_offset]} {
            if {$end_offset <= $beg_offset} {
                puts "ERROR:  The starting offset must be less than or equal to the ending offset."
                return
            }
            if {$end_offset > 16383} {
                puts "ERROR:  Offset specified is too large; may not exceed 16383."
                return
            }
            set use_offset 1
        } elseif {[regexp -nocase {^-repeat=([0-9]+)$} $a tmp burstdur]} {
            if {$burstdur < 1 || $burstdur > 65535} {
                puts "The repeat count must be between 1 and 65535."
                puts "A value of 65535 means forever."
                return
            }
        } elseif {[regexp -nocase {^-std_dev=([\.0-9]+)$} $a tmp std_dev]} {
            if {$std_dev > 100.0 || $std_dev < 0.0} {
                puts "The standard deviation should be between 0-100%."
                return
            }
        } elseif {[regexp -nocase {^-trigger=([0-9]+)$} $a tmp cond_num]} {
            if {$cond_num != 0 && $cond_num != 1} {
                puts "The trigger condition number must be either 0 or 1."
                return
            }
            set use_trig 1
        } elseif {[regexp -nocase {^-no_rnd_sel$} $a tmp]} {
            set use_rnd 0
        } elseif {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    } 

    # ------------------------------------------------------------
    # Convert bits to bytes
    # ------------------------------------------------------------
    set beg_offset [expr $beg_offset * 8]
    set end_offset [expr $end_offset * 8 + 7]
    set fixed_bl   [expr $fixed_bl * 8]
    set max_bl     [expr $max_bl * 8]
    set min_bl     [expr $min_bl * 8]

    # ------------------------------------------------------------
    # Bounds check
    # ------------------------------------------------------------
    set leftside [expr $corrupt_intv - 1]
    if {$bltype == $PKTCORRUPT_BL_FIXED} {
        set leftside [expr $leftside * $fixed_bl]
    } else {
        set leftside [expr $leftside * $min_bl]
    }

    set rightside 14
    if {$use_offset == 1} {
        set range [expr $max_bl - $min_bl + 1]
        if {$range < 16} {
            set range [expr $range - 2]
        }
    }

    if {$rightside >= $leftside} {
        puts "The corruption rate specified is too large; try reducing it."
        return
    }
    
    # ------------------------------------------------------------
    # Send
    # ------------------------------------------------------------
    set itvbyte(0) [expr ($interval >> 24) & 0xFF]
    set itvbyte(1) [expr ($interval >> 16) & 0xFF]
    set itvbyte(2) [expr ($interval >> 8) & 0xFF]
    set itvbyte(3) [expr ($interval >> 0) & 0xFF]

    set burstlenbyte(0) [expr ($burstlen >> 8) & 0xFF]
    set burstlenbyte(1) [expr ($burstlen >> 0) & 0xFF]

    set beg_offsetbyte(0) [expr ($beg_offset >> 24) & 0xFF]
    set beg_offsetbyte(1) [expr ($beg_offset >> 16) & 0xFF]
    set beg_offsetbyte(2) [expr ($beg_offset >> 8) & 0xFF]
    set beg_offsetbyte(3) [expr ($beg_offset >> 0) & 0xFF]

    set end_offsetbyte(0) [expr ($end_offset >> 24) & 0xFF]
    set end_offsetbyte(1) [expr ($end_offset >> 16) & 0xFF]
    set end_offsetbyte(2) [expr ($end_offset >> 8) & 0xFF]
    set end_offsetbyte(3) [expr ($end_offset >> 0) & 0xFF]

    set minblbyte(0) [expr ($min_bl >> 8) & 0xFF]
    set minblbyte(1) [expr ($min_bl >> 0) & 0xFF]

    set maxblbyte(0) [expr ($max_bl >> 8) & 0xFF]
    set maxblbyte(1) [expr ($max_bl >> 0) & 0xFF]

    set fixedblbyte(0) [expr ($fixed_bl >> 8) & 0xFF]
    set fixedblbyte(1) [expr ($fixed_bl >> 0) & 0xFF]

    set cintvbyte(0) [expr ($corrupt_intv >> 24) & 0xFF]
    set cintvbyte(1) [expr ($corrupt_intv >> 16) & 0xFF]
    set cintvbyte(2) [expr ($corrupt_intv >> 8) & 0xFF]
    set cintvbyte(3) [expr ($corrupt_intv >> 0) & 0xFF]

    set burstdurbyte(0) [expr ($burstdur >> 8) & 0xFF]
    set burstdurbyte(1) [expr ($burstdur >> 0) & 0xFF]

    set std_dev [expr $std_dev * 100]
    set std_devbyte(0) [expr (int($std_dev) >> 8) & 0xFF]
    set std_devbyte(1) [expr (int($std_dev) >> 0) & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x3F 37 $blade $profile $use_rnd $use_trig \
                               $cond_num $commit $dist \
                               $burstlenbyte(0) $burstlenbyte(1) \
                               $itvbyte(0) $itvbyte(1) $itvbyte(2) $itvbyte(3) \
                               $burstdurbyte(0) $burstdurbyte(1) \
                               $std_devbyte(0) $std_devbyte(1) \
                               $use_offset \
                               $beg_offsetbyte(0) $beg_offsetbyte(1) \
                               $beg_offsetbyte(2) $beg_offsetbyte(3) \
                               $end_offsetbyte(0) $end_offsetbyte(1) \
                               $end_offsetbyte(2) $end_offsetbyte(3) \
                               $bltype \
                               $minblbyte(0) $minblbyte(1) \
                               $maxblbyte(0) $maxblbyte(1) \
                               $fixedblbyte(0) $fixedblbyte(1) \
                               $cintvbyte(0) $cintvbyte(1) \
                               $cintvbyte(2) $cintvbyte(3) ]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_pkt_corruption
#                  :
#                  : args:
#                  : -no_commit:  don't commit the disable yet
#                  :           use gem_load_impairments to commit
#                  :
# Purpose          : Turn off packet corruption for the specified profile.
######################################################################
proc gem_disable_pkt_corruption {profile args} {
    puts "gem_disable_pkt_corruption $profile"
    set cmd {gem_disable_impairment 0x3F $profile}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_enable_jitter
#                  :
# Parameters       : Packets affected by jitter are chosen by the
#                  : following parameters:
#                  :
#                  : profile - profile number to apply to
#                  : dist - type of distribution to apply
#                  :     $STAT_DISTRIB(UNIFORM), $STAT_DISTRIB(PERIODIC)
#                  :     $STAT_DISTRIB(POISSON) or $STAT_DISTRIB(GAUSSIAN)
#                  : burstlen - number of packets at a time to jitter
#                  : interval - interval over which to perform the jitter
#                  :
#                  : args:
#                  : -repeat:  e.g., -repeat=4 means to repeat this
#                  :           modification 4 times, then stop
#                  : -std_dev:  e.g., -std_dev=1.0 means to use a 1.0%
#                  :           standard deviation in the case of a Gaussian
#                  :           distribution
#                  : -no_commit:  don't commit the crc corrupt
#                  :           use gem_load_impairments to commit
#                  :
# Purpose          : Turn on jitter for the specified profile.
######################################################################
proc gem_enable_jitter {profile dist burstlen interval args} {
    puts "gem_enable_jitter $profile $dist $burstlen $interval"
    set cmd {gem_enable_impairment 0x49 $profile $dist $burstlen $interval}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_disable_jitter
#                  :
#                  : args:
#                  : -no_commit:  don't commit the disable yet
#                  :           use gem_load_impairments to commit
#                  :
# Purpose          : Turn off jitter for the specified profile.
######################################################################
proc gem_disable_jitter {profile args} {
    puts "gem_disable_jitter $profile"
    set cmd {gem_disable_impairment 0x49 $profile}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_enable_pkt_drop
#                  :             
# Parameters       : Packets dropped are chosen by the following
#                  : parameters:
#                  :
#                  : profile - profile number to apply to
#                  : dist - type of distribution to apply
#                  :     $STAT_DISTRIB(UNIFORM), $STAT_DISTRIB(PERIODIC)
#                  :     $STAT_DISTRIB(POISSON) or $STAT_DISTRIB(GAUSSIAN)
#                  : burstlen - number of packets at a time to drop
#                  : interval - interval over which to perform the drop
#                  :
#                  : args:
#                  : -repeat:  e.g., -repeat=4 means to repeat this
#                  :           impairment 4 times, then stop
#                  : -std_dev:  e.g., -std_dev=1.0 means to use a 1.0%
#                  :           standard deviation in the case of a Gaussian
#                  :           distribution
#                  : -no_commit:  don't commit the pkt drop
#                  :           use gem_load_impairments to commit
#                  :           
# Purpose          : Turn on packet drop for the specified profile.
######################################################################
proc gem_enable_pkt_drop {profile dist burstlen interval args} {
    puts "gem_enable_pkt_drop $profile $dist $burstlen $interval $args"
    set cmd {gem_enable_impairment 0x45 $profile $dist $burstlen $interval}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_disable_pkt_drop
#                  :
#                  : args:
#                  : -no_commit:  don't commit the disable yet
#                  :           use gem_load_impairments to commit
#                  :
# Purpose          : Turn off packet drop for the specified profile.
######################################################################
proc gem_disable_pkt_drop {profile args} {
    puts "gem_disable_pkt_drop $profile"
    set cmd {gem_disable_impairment 0x45 $profile}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_enable_crc_corrupt
#                  :             
# Parameters       : Packets to have their CRCs corrupted are chosen
#                  : by the following parameters:
#                  :
#                  : profile - profile number to apply to
#                  : dist - type of distribution to apply
#                  :     $STAT_DISTRIB(UNIFORM), $STAT_DISTRIB(PERIODIC)
#                  :     $STAT_DISTRIB(GAUSSIAN) or $STAT_DISTRIB(POISSON)
#                  : burstlen - number of packets at a time to CRC corrupt
#                  : interval - interval over which to perform the CRC corrupt
#                  :
#                  : args:
#                  : -repeat:  e.g., -repeat=4 means to repeat this
#                  :           modification 4 times, then stop
#                  : -std_dev:  e.g., -std_dev=1.0 means to use a 1.0%
#                  :           standard deviation in the case of a Gaussian
#                  :           distribution
#                  : -no_commit:  don't commit the crc corrupt
#                  :           use gem_load_impairments to commit
#                  :  
# Purpose          : Turn on CRC corruption for the specified profile.
######################################################################
proc gem_enable_crc_corrupt {profile dist burstlen interval args} {
    puts "gem_enable_crc_corrupt $profile $dist $burstlen $interval $args"
    set cmd {gem_enable_impairment 0x47 $profile $dist $burstlen $interval}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_disable_crc_corrupt
#                  :
#                  : args:
#                  : -no_commit:  don't commit the disable yet
#                  :           use gem_load_impairments to commit
#                  :
# Purpose          : Turn off CRC corruption for the specified profile.
######################################################################
proc gem_disable_crc_corrupt {profile args} {
    puts "gem_disable_crc_corrupt $profile"
    set cmd {gem_disable_impairment 0x47 $profile}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_enable_pkt_duplication
#                  :             
# Parameters       : Packets to be duplicated are chosen
#                  : by the following parameters:
#                  :
#                  : profile - profile number to apply to
#                  : dist - type of distribution to apply
#                  :     $STAT_DISTRIB(UNIFORM), $STAT_DISTRIB(PERIODIC)
#                  :     $STAT_DISTRIB(POISSON) or $STAT_DISTRIB(GAUSSIAN)
#                  : burstlen - number of packets at a time to duplicate
#                  : interval - interval over which to perform the duplicate
#                  : min - 0-15 minimum number of times to dupe the selected pkt
#                  : max - 0-15 maximum number of times to dupe the selected pkt
#                  :
#                  : args:
#                  : -no_commit:  don't commit the pkt duplication
#                  :           use gem_load_impairments to commit
#                  : -repeat:  e.g., -repeat=4 means to repeat this
#                  :           impairment 4 times, then stop
#                  : -std_dev:  e.g., -std_dev=1.0 means to use a 1.0%
#                  :           standard deviation in the case of a Gaussian
#                  :           distribution
#                  :           
# Purpose          : Turn on packet duplication for the specified profile.
######################################################################
proc gem_enable_pkt_duplication {profile dist burstlen interval min max args} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {$burstlen > $interval} {
        puts "Interval must be greater than or equal to the burst length."
        return
    }

    if {$dist == $STAT_DISTRIB(POISSON)} {
        if {$interval > 26464832} {
            puts "Interval must be less than 26464832."
            return
        }
    } else {
        if {$interval > 268000000} {
            puts "Interval must be less than 268000000."
            return
        }
    }

    if {$dist != $STAT_DISTRIB(UNIFORM) && \
        $dist != $STAT_DISTRIB(PERIODIC) && \
        $dist != $STAT_DISTRIB(POISSON) && \
        $dist != $STAT_DISTRIB(GAUSSIAN)} {
        puts "Distribution must be either \$STAT_DISTRIB(PERIODIC), \$STAT_DISTRIB(UNIFORM),"
        puts "\$STAT_DISTRIB(POISSON) or \$STAT_DISTRIB(GAUSSIAN)."
        return;
    }

    if {$dist == $STAT_DISTRIB(UNIFORM) || \
        $dist == $STAT_DISTRIB(POISSON) || \
        $dist == $STAT_DISTRIB(GAUSSIAN)} {
        if {$interval == $burstlen} {
            puts "When selecting every packet for impairment,"
            puts "only \$STAT_DISTRIB(PERIODIC) is allowed."
            return
        }
    }

    if {$min < 0 || $min > 15} {
        puts "Duplication count minimum must be between 0 and 15."
        return
    }

    if {$max < 0 || $max > 15} {
        puts "Duplication count maximum must be between 0 and 15."
        return
    }

    if {$min > $max} {
        puts "Duplication count minimum must be less than or equal to the maximum."
        return
    }

    set burstdur 65535
    set std_dev 1.0
    set use_rnd 1
    set use_trig 0
    set commit 1
    set cond_num 0xFF

    foreach a $args {
        if {[regexp -nocase {^-repeat=([0-9]+)$} $a tmp burstdur]} {
            if {$burstdur < 1 || $burstdur > 65535} {
                puts "The repeat count must be between 1 and 65535."
                puts "A value of 65535 means forever."
                return
            }
        } elseif {[regexp -nocase {^-std_dev=([\.0-9]+)$} $a tmp std_dev]} {
            if {$std_dev > 100.0 || $std_dev < 0.0} {
                puts "The standard deviation should be between 0-100%."
                return
            }
        } elseif {[regexp -nocase {^-trigger=([0-9]+)$} $a tmp cond_num]} {
            if {$cond_num != 0 && $cond_num != 1} {
                puts "The trigger condition number must be either 0 or 1."
                return
            }
            set use_trig 1
        } elseif {[regexp -nocase {^-no_rnd_sel$} $a tmp]} {
            set use_rnd 0
        } elseif {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }

    puts "gem_enable_pkt_duplication $profile $dist $burstlen $interval $min $max"

    set blade $TX_DEST_ADDR
    set_target 0

    set itvbyte(0) [expr ($interval >> 24) & 0xFF]
    set itvbyte(1) [expr ($interval >> 16) & 0xFF]
    set itvbyte(2) [expr ($interval >> 8) & 0xFF]
    set itvbyte(3) [expr ($interval >> 0) & 0xFF]

    set burstlenbyte(0) [expr ($burstlen >> 8) & 0xFF]
    set burstlenbyte(1) [expr ($burstlen >> 0) & 0xFF]

    set burstdurbyte(0) [expr ($burstdur >> 8) & 0xFF]
    set burstdurbyte(1) [expr ($burstdur >> 0) & 0xFF]

    set std_dev [expr $std_dev * 100]
    set std_devbyte(0) [expr (int($std_dev) >> 8) & 0xFF]
    set std_devbyte(1) [expr (int($std_dev) >> 0) & 0xFF]

    send_command [BuildCommand 0x43 19 $blade $profile $use_rnd $use_trig \
                               $cond_num $commit $dist \
                               $burstlenbyte(0) $burstlenbyte(1) \
                               $itvbyte(0) $itvbyte(1) $itvbyte(2) $itvbyte(3) \
                               $burstdurbyte(0) $burstdurbyte(1) \
                               $std_devbyte(0) $std_devbyte(1) $min $max]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_pkt_duplication
#                  :
#                  : args:
#                  : -no_commit:  don't commit the disable yet
#                  :           use gem_load_impairments to commit
#                  :
# Purpose          : Turn off pkt duplication for the specified profile.
######################################################################
proc gem_disable_pkt_duplication {profile args} {
    puts "gem_disable_pkt_duplication $profile"
    set cmd {gem_disable_impairment 0x43 $profile}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_enable_pkt_reorder
#                  :             
# Parameters       : Packets to be reordered are chosen
#                  : by the following parameters:
#                  :
#                  : profile - profile number to apply to
#                  : dist - type of distribution to apply
#                  :     $STAT_DISTRIB(UNIFORM), $STAT_DISTRIB(PERIODIC)
#                  :     $STAT_DISTRIB(POISSON) or $STAT_DISTRIB(GAUSSIAN)
#                  : burstlen - number of packets at a time to reorder
#                  : interval - interval over which to perform the reorder
#                  : min - packet offset range minimum (1-256)
#                  : max - packet offset range maximum (1-256)
#                  :
#                  : args:
#                  : -no_commit:  don't commit the pkt reorder
#                  :           use gem_load_impairments to commit
#                  : -repeat:  e.g., -repeat=4 means to repeat this
#                  :           impairment 4 times, then stop
#                  : -std_dev:  e.g., -std_dev=1.0 means to use a 1.0%
#                  :           standard deviation in the case of a Gaussian
#                  :           distribution
#                  :           
# Purpose          : Turn on packet reorder for the specified profile.
######################################################################
proc gem_enable_pkt_reorder {profile dist burstlen interval min max args} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {$min < 1 || $min > 256} {
        puts "Packet offset range minimum must be between 1 and 256."
        return
    }

    if {$max < 1 || $max > 256} {
        puts "Packet offset range maximum must be between 1 and 256."
        return
    }

    if {$dist == $STAT_DISTRIB(POISSON)} {
        if {$interval > 26464832} {
            puts "Interval must be less than 26464832."
            return
        }
    } else {
        if {$interval > 268000000} {
            puts "Interval must be less than 268000000."
            return
        }
    }

    if {$dist != $STAT_DISTRIB(UNIFORM) && \
        $dist != $STAT_DISTRIB(PERIODIC) && \
        $dist != $STAT_DISTRIB(POISSON) && \
        $dist != $STAT_DISTRIB(GAUSSIAN)} {
        puts "Distribution must be either \$STAT_DISTRIB(PERIODIC), \$STAT_DISTRIB(UNIFORM),"
        puts "\$STAT_DISTRIB(POISSON) or \$STAT_DISTRIB(GAUSSIAN)."
        return;
    }

    if {$dist == $STAT_DISTRIB(UNIFORM) || \
        $dist == $STAT_DISTRIB(POISSON) || \
        $dist == $STAT_DISTRIB(GAUSSIAN)} {
        if {$interval == $burstlen} {
            puts "When selecting every packet for impairment,"
            puts "only \$STAT_DISTRIB(PERIODIC) is allowed."
            return
        }
    }

    if {$burstlen > 8} {
        puts "WARNING:  Burst length should not exceed 8 for packet reorder."
        puts "WARNING:  This setting exceeds the capability of the hardware."
        puts "WARNING:  Results may not be as expected."
    }

    if {$burstlen > [expr $interval / 2]} {
        puts "WARNING:  Selected packets for reorder must not exceed 50%."
        puts "WARNING:  These settings exceed the capability of the hardware."
        puts "WARNING:  Results may not be as expected."
    }

    if {($burstlen <= 4) && ($interval <= 8)} {
      if {[expr $max-1] > 9} {
        puts "WARNING:  For these settings, max offset range must be <= 9."
        puts "WARNING:  These settings exceed the capability of the hardware."
        puts "WARNING:  Results may not be as expected."
      }
    } else {
      if {[expr $max-1] >= [expr $interval - $burstlen]} {
        puts "WARNING:  For these settings, max offset range must be"
        puts "WARNING:  less than (interval - burstlen + 1)."
        puts "WARNING:  These settings exceed the capability of the hardware."
        puts "WARNING:  Results may not be as expected."
      }
    }

    if {$min > $max} {
        puts "Packet offset range minimum must be less than or equal to the maximum."
        return
    }

    set burstdur 65535
    set std_dev 1.0
    set use_rnd 1
    set use_trig 0
    set commit 1
    set cond_num 0xFF

    foreach a $args {
        if {[regexp -nocase {^-repeat=([0-9]+)$} $a tmp burstdur]} {
            if {$burstdur < 1 || $burstdur > 65535} {
                puts "The repeat count must be between 1 and 65535."
                puts "A value of 65535 means forever."
                return
            }
        } elseif {[regexp -nocase {^-std_dev=([\.0-9]+)$} $a tmp std_dev]} {
            if {$std_dev > 100.0 || $std_dev < 0.0} {
                puts "The standard deviation should be between 0-100%."
                return
            }
        } elseif {[regexp -nocase {^-trigger=([0-9]+)$} $a tmp cond_num]} {
            if {$cond_num != 0 && $cond_num != 1} {
                puts "The trigger condition number must be either 0 or 1."
                return
            }
            set use_trig 1
        } elseif {[regexp -nocase {^-no_rnd_sel$} $a tmp]} {
            set use_rnd 0
        } elseif {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }

    puts "gem_enable_pkt_reorder $profile $dist $burstlen $interval $min $max"

    set blade $TX_DEST_ADDR
    set_target 0

    set itvbyte(0) [expr ($interval >> 24) & 0xFF]
    set itvbyte(1) [expr ($interval >> 16) & 0xFF]
    set itvbyte(2) [expr ($interval >> 8) & 0xFF]
    set itvbyte(3) [expr ($interval >> 0) & 0xFF]

    set burstlenbyte(0) [expr ($burstlen >> 8) & 0xFF]
    set burstlenbyte(1) [expr ($burstlen >> 0) & 0xFF]

    set burstdurbyte(0) [expr ($burstdur >> 8) & 0xFF]
    set burstdurbyte(1) [expr ($burstdur >> 0) & 0xFF]

    set std_dev [expr $std_dev * 100]
    set std_devbyte(0) [expr (int($std_dev) >> 8) & 0xFF]
    set std_devbyte(1) [expr (int($std_dev) >> 0) & 0xFF]

    send_command [BuildCommand 0x41 19 $blade $profile $use_rnd $use_trig \
                               $cond_num $commit $dist \
                               $burstlenbyte(0) $burstlenbyte(1) \
                               $itvbyte(0) $itvbyte(1) $itvbyte(2) $itvbyte(3) \
                               $burstdurbyte(0) $burstdurbyte(1) \
                               $std_devbyte(0) $std_devbyte(1) \
                               $min $max]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_pkt_reorder
#                  :
#                  : args:
#                  : -no_commit:  don't commit the disable yet
#                  :           use gem_load_impairments to commit
#                  :
# Purpose          : Turn off pkt reorder for the specified profile.
######################################################################
proc gem_disable_pkt_reorder {profile args} {
    puts "gem_disable_pkt_reorder $profile"
    set cmd {gem_disable_impairment 0x41 $profile}
    eval $cmd $args
}

######################################################################
# Function Name    : gem_get_crc_corrupt_status
# Parameters       : profile
# Return Value     : CRC corruption settings on the specified profile
######################################################################
proc gem_get_crc_corrupt_status {profile} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4F 2 $blade $profile]
    set ret [lrange [pong] 2 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set rnd_enabled [expr "0x[lindex $ret 2]" + 0]
    set trig_enabled [expr "0x[lindex $ret 14]" + 0]
    if {$rnd_enabled == 0 && $trig_enabled == 0} {
        puts "CRC Corruption on profile $profile is currently DISABLED."
        return
    }


    # ------------------------------------------------------------
    # Get distribution, burstlen, interval and burstdur
    # ------------------------------------------------------------
    set dist     [expr "0x[lindex $ret 3]" + 0]
    set burstlen [value_from_array [lrange $ret 4 5]]
    set interval [value_from_array [lrange $ret 6 9]]
    set burstdur [value_from_array [lrange $ret 10 11]]
    set std_dev  [value_from_array [lrange $ret 12 13]]
    set cond_num [expr "0x[lindex $ret 15]" + 0]

    puts "CRC Corruption is ENABLED on profile $profile:"

    if {$trig_enabled == 1} {
        puts "  Using trigger condition #$cond_num."
    }

    if {$rnd_enabled == 1} {
        if {$dist == $STAT_DISTRIB(PERIODIC)} {
            puts "  Periodic Distribution"
        } elseif {$dist == $STAT_DISTRIB(UNIFORM)} {
            puts "  Uniform Distribution"
        } elseif {$dist == $STAT_DISTRIB(POISSON)} {
            puts "  Poisson Distribution"
        } elseif {$dist == $STAT_DISTRIB(GAUSSIAN)} {
            puts "  Gaussian Distribution [expr $std_dev / 100.0]"
        } else {
            puts "  ??? Distribution"
        }

        puts "  Interval:  $interval"
        puts "  Burst length:  $burstlen"
        if {$burstdur == 65535} {
            puts "  Repeat Count:  Forever"
        } else {
            puts "  Repeat Count:  $burstdur"
        }
    }
}


######################################################################
# Function Name    : gem_get_pkt_drop_status
# Parameters       : profile
# Return Value     : Packet drop settings on the specified profile
######################################################################
proc gem_get_pkt_drop_status {profile} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x46 2 $blade $profile]
    set ret [lrange [pong] 2 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set rnd_enabled [expr "0x[lindex $ret 2]" + 0]
    set trig_enabled [expr "0x[lindex $ret 14]" + 0]
    if {$rnd_enabled == 0 && $trig_enabled == 0} {
        puts "Packet drop on profile $profile is currently DISABLED."
        return
    }

    # ------------------------------------------------------------
    # Get distribution, burstlen, interval and burstdur
    # ------------------------------------------------------------
    set dist     [expr "0x[lindex $ret 3]" + 0]
    set burstlen [value_from_array [lrange $ret 4 5]]
    set interval [value_from_array [lrange $ret 6 9]]
    set burstdur [value_from_array [lrange $ret 10 11]]
    set std_dev  [value_from_array [lrange $ret 12 13]]
    set cond_num [expr "0x[lindex $ret 15]" + 0]

    puts "Packet drop is ENABLED on profile $profile:"

    if {$trig_enabled == 1} {
        puts "  Using trigger condition #$cond_num."
    }

    if {$rnd_enabled == 1} {
        if {$dist == $STAT_DISTRIB(PERIODIC)} {
            puts "  Periodic Distribution"
        } elseif {$dist == $STAT_DISTRIB(UNIFORM)} {
            puts "  Uniform Distribution"
        } elseif {$dist == $STAT_DISTRIB(POISSON)} {
            puts "  Poisson Distribution"
        } elseif {$dist == $STAT_DISTRIB(GAUSSIAN)} {
            puts "  Gaussian Distribution [expr $std_dev / 100.0]"
        } else {
            puts "  ??? Distribution"
        }
    }

    puts "  Interval:  $interval"
    puts "  Burst length:  $burstlen"
    if {$burstdur == 65535} {
        puts "  Repeat Count:  Forever"
    } else {
        puts "  Repeat Count:  $burstdur"
    }
}


######################################################################
# Function Name    : gem_get_jitter_status
# Parameters       : profile
# Return Value     : Jitter settings on the specified profile
######################################################################
proc gem_get_jitter_status {profile} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4A 2 $blade $profile]
    set ret [lrange [pong] 4 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set rnd_enabled [expr "0x[lindex $ret 0]" + 0]
    set trig_enabled [expr "0x[lindex $ret 12]" + 0]
    if {$rnd_enabled == 0 && $trig_enabled == 0} {
        puts "Jitter on profile $profile is currently DISABLED."
        return
    }

    # ------------------------------------------------------------
    # Get distribution, burstlen, interval and burstdur
    # ------------------------------------------------------------
    set dist     [expr "0x[lindex $ret 1]" + 0]
    set burstlen [value_from_array [lrange $ret 2 3]]
    set interval [value_from_array [lrange $ret 4 7]]
    set burstdur [value_from_array [lrange $ret 8 9]]
    set std_dev  [value_from_array [lrange $ret 10 11]]
    set cond_num [expr "0x[lindex $ret 13]" + 0]

    puts "Jitter is ENABLED on profile $profile:"

    if {$trig_enabled == 1} {
        puts "  Using trigger condition #$cond_num."
    }

    if {$rnd_enabled == 1} {
        if {$dist == $STAT_DISTRIB(PERIODIC)} {
            puts "  Periodic Distribution"
        } elseif {$dist == $STAT_DISTRIB(UNIFORM)} {
            puts "  Uniform Distribution"
        } elseif {$dist == $STAT_DISTRIB(POISSON)} {
            puts "  Poisson Distribution"
        } elseif {$dist == $STAT_DISTRIB(GAUSSIAN)} {
            puts "  Gaussian Distribution [expr $std_dev / 100.0]"
        } else {
            puts "  ??? Distribution"
        }
    }

    puts "  Interval:  $interval"
    puts "  Burst length:  $burstlen"
    if {$burstdur == 65535} {
        puts "  Repeat Count:  Forever"
    } else {
        puts "  Repeat Count:  $burstdur"
    }
}


######################################################################
# Function Name    : gem_get_pkt_duplication_status
# Parameters       : profile
# Return Value     : Pkt duplication settings on the specified profile
######################################################################
proc gem_get_pkt_duplication_status {profile} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x44 2 $blade $profile]
    set ret [lrange [pong] 4 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set rnd_enabled [expr "0x[lindex $ret 0]" + 0]
    set trig_enabled [expr "0x[lindex $ret 12]" + 0]
    if {$rnd_enabled == 0 && $trig_enabled == 0} {
        puts "Packet duplication on profile $profile is currently DISABLED."
        return
    }

    # ------------------------------------------------------------
    # Get distribution, burstlen, interval and burstdur
    # ------------------------------------------------------------
    set dist     [expr "0x[lindex $ret 1]" + 0]
    set burstlen [value_from_array [lrange $ret 2 3]]
    set interval [value_from_array [lrange $ret 4 7]]
    set burstdur [value_from_array [lrange $ret 8 9]]
    set std_dev  [value_from_array [lrange $ret 10 11]]
    set cond_num [expr "0x[lindex $ret 13]" + 0]
    set min      [expr "0x[lindex $ret 14]" + 0]
    set max      [expr "0x[lindex $ret 15]" + 0]

    puts "Packet duplication is ENABLED on profile $profile:"

    if {$trig_enabled == 1} {
        puts "  Using trigger condition #$cond_num."
    }

    if {$rnd_enabled == 1} {
        if {$dist == $STAT_DISTRIB(PERIODIC)} {
            puts "  Periodic Distribution"
        } elseif {$dist == $STAT_DISTRIB(UNIFORM)} {
            puts "  Uniform Distribution"
        } elseif {$dist == $STAT_DISTRIB(POISSON)} {
            puts "  Poisson Distribution"
        } elseif {$dist == $STAT_DISTRIB(GAUSSIAN)} {
            puts "  Gaussian Distribution [expr $std_dev / 100.0]"
        } else {
            puts "  ??? Distribution"
        }
    }

    puts "  Interval:  $interval"
    puts "  Burst length:  $burstlen"
    if {$burstdur == 65535} {
        puts "  Repeat Count:  Forever"
    } else {
        puts "  Repeat Count:  $burstdur"
    }
    puts "  Range:  $min to $max"
}


######################################################################
# Function Name    : gem_get_pkt_reorder_status
# Parameters       : profile
# Return Value     : Pkt reorder settings on the specified profile
######################################################################
proc gem_get_pkt_reorder_status {profile} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x42 2 $blade $profile]
    set ret [lrange [pong] 4 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set rnd_enabled [expr "0x[lindex $ret 0]" + 0]
    set trig_enabled [expr "0x[lindex $ret 12]" + 0]
    if {$rnd_enabled == 0 && $trig_enabled == 0} {
        puts "Packet reorder on profile $profile is currently DISABLED."
        return
    }

    # ------------------------------------------------------------
    # Get distribution, burstlen, interval and burstdur
    # ------------------------------------------------------------
    set dist     [expr "0x[lindex $ret 1]" + 0]
    set burstlen [value_from_array [lrange $ret 2 3]]
    set interval [value_from_array [lrange $ret 4 7]]
    set burstdur [value_from_array [lrange $ret 8 9]]
    set std_dev  [value_from_array [lrange $ret 10 11]]
    set cond_num [expr "0x[lindex $ret 13]" + 0]
    set min      [expr "0x[lindex $ret 14]" + 0]
    set max      [expr "0x[lindex $ret 15]" + 0]

    puts "Packet reorder is ENABLED on profile $profile:"

    if {$trig_enabled == 1} {
        puts "  Using trigger condition #$cond_num."
    }

    if {$rnd_enabled == 1} {
        if {$dist == $STAT_DISTRIB(PERIODIC)} {
            puts "  Periodic Distribution"
        } elseif {$dist == $STAT_DISTRIB(UNIFORM)} {
            puts "  Uniform Distribution"
        } elseif {$dist == $STAT_DISTRIB(POISSON)} {
            puts "  Poisson Distribution"
        } elseif {$dist == $STAT_DISTRIB(GAUSSIAN)} {
            puts "  Gaussian Distribution [expr $std_dev / 100.0]"
        } else {
            puts "  ??? Distribution"
        }
    }

    puts "  Interval:  $interval"
    puts "  Burst length:  $burstlen"
    if {$burstdur == 65535} {
        puts "  Repeat Count:  Forever"
    } else {
        puts "  Repeat Count:  $burstdur"
    }
    puts "  Packet offset range:  $min to $max packets"
}


######################################################################
# Function Name    : gem_get_pkt_corruption_status
# Parameters       : profile
# Return Value     : Pkt corruption settings on the specified profile
######################################################################
proc gem_get_pkt_corruption_status {profile} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global PKTCORRUPT_BL_RAND
    global PKTCORRUPT_BL_FIXED
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x40 2 $blade $profile]
    set ret [lrange [pong] 4 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set rnd_enabled [expr "0x[lindex $ret 0]" + 0]
    set trig_enabled [expr "0x[lindex $ret 12]" + 0]
    if {$rnd_enabled == 0 && $trig_enabled == 0} {
        puts "Packet corruption on profile $profile is currently DISABLED."
        return
    }

    # ------------------------------------------------------------
    # Get distribution, burstlen, interval and burstdur
    # ------------------------------------------------------------
    set dist         [expr "0x[lindex $ret 1]" + 0]
    set burstlen     [value_from_array [lrange $ret 2 3]]
    set interval     [value_from_array [lrange $ret 4 7]]
    set burstdur     [value_from_array [lrange $ret 8 9]]
    set std_dev      [value_from_array [lrange $ret 10 11]]
    set cond_num     [expr "0x[lindex $ret 13]" + 0]
    set use_offsets  [value_from_array [lindex $ret 14]]
    set beg_offset   [value_from_array [lrange $ret 15 18]]
    set end_offset   [value_from_array [lrange $ret 19 22]]
    set bl_type      [value_from_array [lindex $ret 23]]
    set min_bl       [value_from_array [lrange $ret 24 25]]
    set max_bl       [value_from_array [lrange $ret 26 27]]
    set fixed_bl     [value_from_array [lrange $ret 28 29]]
    set corrupt_intv [value_from_array [lrange $ret 30 33]]

    # ------------------------------------------------------------
    # Convert bits to bytes
    # ------------------------------------------------------------
    set beg_offset [expr $beg_offset / 8]
    set end_offset [expr ($end_offset - 7) / 8]
    set fixed_bl   [expr $fixed_bl / 8]
    set max_bl     [expr $max_bl / 8]
    set min_bl     [expr $min_bl / 8]


    # ------------------------------------------------------------
    # Display
    # ------------------------------------------------------------
    puts "Packet corruption is ENABLED on profile $profile:"

    if {$trig_enabled == 1} {
        puts "  Using trigger condition #$cond_num."
    }

    if {$rnd_enabled == 1} {
        if {$dist == $STAT_DISTRIB(PERIODIC)} {
            puts "  Periodic Distribution"
        } elseif {$dist == $STAT_DISTRIB(UNIFORM)} {
            puts "  Uniform Distribution"
        } elseif {$dist == $STAT_DISTRIB(POISSON)} {
            puts "  Poisson Distribution"
        } elseif {$dist == $STAT_DISTRIB(GAUSSIAN)} {
            puts "  Gaussian Distribution [expr $std_dev / 100.0]"
        } else {
            puts "  ??? Distribution"
        }
    }

    puts "  Interval:  $interval"
    puts "  Burst length:  $burstlen"
    if {$burstdur == 65535} {
        puts "  Repeat Count:  Forever"
    } else {
        puts "  Repeat Count:  $burstdur"
    }

    set rate [expr 1.0 / $corrupt_intv]
    set ratestr [format "%9.3e" $rate]
    puts "  Corruption Rate:  $ratestr"

    if {$use_offsets == 1} {
        puts "  Corrupting offset:  Bytes $beg_offset through $end_offset"
    } else {
        puts "  Corrupting offset:  Entire packet"
    }

    if {$bl_type == $PKTCORRUPT_BL_FIXED} {
        if {$fixed_bl == 1} {
            puts "  Corruption burst:  $fixed_bl byte"
        } else {
            puts "  Corruption burst:  $fixed_bl bytes"
        }
    } elseif {$bl_type == $PKTCORRUPT_BL_RAND} {
        puts "  Corruption burst:  $min_bl to $max_bl bytes"
    }
}


######################################################################
# Function Name    : gem_enable_incoming_crc_correction
#
# Purpose          : Enable CRC correction on incoming packets
######################################################################
proc gem_enable_incoming_crc_correction {} {
    global TX_DEST_ADDR

    puts "gem_enable_incoming_crc_correction"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4B 2 $blade 1]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_disable_incoming_crc_correction
#
# Purpose          : Disable CRC correction on incoming packets
######################################################################
proc gem_disable_incoming_crc_correction {} {
    global TX_DEST_ADDR

    puts "gem_disable_incoming_crc_correction"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4B 2 $blade 0]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_query_incoming_crc_correction
#
# Purpose          : Display whether incoming CRC correction is on
######################################################################
proc gem_query_incoming_crc_correction {} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4C 1 $blade]
    set ret [lrange [pong] 2 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set enabled [expr "0x[lindex $ret 1]" + 0]
    if {$enabled == 0} {
        puts "CRC Correction on incoming packets is currently DISABLED."
    } else {
        puts "CRC Correction on incoming packets is currently ENABLED."
    }
}

######################################################################
# Function Name    : gem_enable_autonegotiation
#
# Purpose          : Enable autonegotiation
######################################################################
proc gem_enable_autonegotiation {} {
    global TX_DEST_ADDR

    puts "gem_enable_autonegotiation"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4D 2 $blade 1]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_disable_autonegotiation
#
# Purpose          : Disable autonegotiation
######################################################################
proc gem_disable_autonegotiation {} {
    global TX_DEST_ADDR

    puts "gem_disable_autonegotiation"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4D 2 $blade 0]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_query_autonegotiation
#
# Purpose          : Display whether autonegotiation is on
######################################################################
proc gem_query_autonegotiation {} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4E 1 $blade]
    set ret [lrange [pong] 2 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set enabled [expr "0x[lindex $ret 1]" + 0]
    if {$enabled == 0} {
        puts "Autonegotiation is currently DISABLED."
    } else {
        puts "Autonegotiation is currently ENABLED."
    }
}

######################################################################
# Function Name    : gem_define_profile
#
# Parameters       : -ip_src=192.168.40.50 or * for any byte to wildcard,
#                  :    e.g. -ip_src=192.168.*.*
#                  : OR
#                  : -ip_src=192.168.30.78/24 (CIDR notation) for network match
#                  :
#                  : -ip_dst=192.168.40.50 or * for any byte to wildcard,
#                  :    e.g. -ip_dst=192.168.*.*
#                  : OR
#                  : -ip_dst=192.168.30.78/24 (CIDR notation) for network match
#                  :
#                  : -ip6_src=A050:8000:*:*:*:*:*:*
#                  :            (* for any 16-bit word to wildcard)
#                  :
#                  : -ip6_dst=A050:8000:*:*:*:*:*:*
#                  :            (* for any 16-bit word to wildcard)
#                  :
#                  : -mac_src=00:20:10:ef:ba:01 or * for any byte to wildcard,
#                  :    e.g. -mac_src=*:*:*:ef:*:02 (hex)
#                  :
#                  : -mac_dst=00:20:10:ef:ba:01 or * for any byte to wildcard,
#                  :    e.g. -mac_dst=*:*:*:ef:*:02 (hex)
#                  :
#                  : -mac_lentype=0800 (hex)
#                  :
#                  : -mpls1=100 (dec) value of the first MPLS label
#                  :
#                  : -mpls2=100 (dec) value of the second MPLS label
#                  :
#                  : -ip_diffservtos=8 (hex)
#                  :
#                  : -ip_protocol=17 (dec)
#                  :
#                  : -port_src=7822 (dec)
#                  :
#                  : -port_dst=80 (dec)
#                  :
#                  : -first_tpid=8100 (hex)
#                  :
#                  : -first_vid=0 (dec)
#                  :
#                  : -first_priority=0 (dec)
#                  :
#                  : -second_tpid=88A8 (hex)
#                  :
#                  : -second_vid=0 (dec)
#                  :
#                  : -second_priority=0 (dec)
#                  :
#                  : -custom_byte=34/0x40/0xf0 {offset/value/mask}
#                  :                 (dec offset/hex value and mask)
#                  :
#                  : -custom_value1=0/0x404040/0xFFFFFFFF {offset/value/mask}
#                  :                 (dec offset/hex value and mask)
#                  :
#                  : -custom_value2=0/0x404040/0xFFFFFFFF {offset/value/mask}
#                  :                 (dec offset/hex value and mask)
#                  :
#                  : -checkip should be used when you want to check the IP
#                  :     version (4 or 6) before matching an IPv4 or IPv6
#                  :     specific field
#                  :
#                  : -dontcheckip should be used when you dont want to check
#                  :     the IP version (4 or 6) before matching an IPv4 or 
#                  :     IPv6 specific field
#                  :
#                  : -name=My_profile
#                  : *** No spaces are allowed in the name when scripting.
#                  : 
#                  : All parameters are ANDed together to create the profile.
#                  :
# Purpose          : After setting up all of the network profile
#                  : definitions, use this routine to program them.
######################################################################
proc gem_define_profile {profile args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES
    global GEM_MAX_OFFSET

    global FP_MAC_SRC0
    global FP_MAC_SRC1
    global FP_MAC_SRC2
    global FP_MAC_SRC3
    global FP_MAC_SRC4
    global FP_MAC_SRC5

    global FP_MAC_DST0
    global FP_MAC_DST1
    global FP_MAC_DST2
    global FP_MAC_DST3
    global FP_MAC_DST4
    global FP_MAC_DST5

    global FP_MAC_LENTYPE

    global FP_IP_SRC0
    global FP_IP_SRC1
    global FP_IP_SRC2
    global FP_IP_SRC3

    global FP_IP_DST0
    global FP_IP_DST1
    global FP_IP_DST2
    global FP_IP_DST3

    global FP_IP_DSCP
    global FP_IP_PROTOCOL

    global FP_PORT_SRC
    global FP_PORT_DST

    global FP_VLANID
    global FP_PRIO

    global FP_QINQ_VLANID
    global FP_QINQ_PRIO

    global FP_CUSTOM_BYTE

    global FP_NAME

    global FP_IP_SRC_MASK
    global FP_IP_DST_MASK

    global FP_CUSTOM_VALUE

    global FP_IP6_SRC0
    global FP_IP6_SRC1
    global FP_IP6_SRC2
    global FP_IP6_SRC3
    global FP_IP6_SRC4
    global FP_IP6_SRC5
    global FP_IP6_SRC6
    global FP_IP6_SRC7
    global FP_IP6_SRC8
    global FP_IP6_SRC9
    global FP_IP6_SRC10
    global FP_IP6_SRC11
    global FP_IP6_SRC12
    global FP_IP6_SRC13
    global FP_IP6_SRC14
    global FP_IP6_SRC15

    global FP_IP6_DST0
    global FP_IP6_DST1
    global FP_IP6_DST2
    global FP_IP6_DST3
    global FP_IP6_DST4
    global FP_IP6_DST5
    global FP_IP6_DST6
    global FP_IP6_DST7
    global FP_IP6_DST8
    global FP_IP6_DST9
    global FP_IP6_DST10
    global FP_IP6_DST11
    global FP_IP6_DST12
    global FP_IP6_DST13
    global FP_IP6_DST14
    global FP_IP6_DST15

    global FP_CHECK_IP_VERSION

    global FP_MPLS_LABEL1
    global FP_MPLS_LABEL2

    global FP_INGRESS_PORT
    global FP_EGRESS_PORT

    global FP_NXTHOP_IP0
    global FP_NXTHOP_IP1
    global FP_NXTHOP_IP2
    global FP_NXTHOP_IP3

    global FP_TPID
    global FP_QINQ_TPID

    global FP_IP6_2_SRC0
    global FP_IP6_2_SRC1
    global FP_IP6_2_SRC2
    global FP_IP6_2_SRC3
    global FP_IP6_2_SRC4
    global FP_IP6_2_SRC5
    global FP_IP6_2_SRC6
    global FP_IP6_2_SRC7

    global FP_IP6_2_DST0
    global FP_IP6_2_DST1
    global FP_IP6_2_DST2
    global FP_IP6_2_DST3
    global FP_IP6_2_DST4
    global FP_IP6_2_DST5
    global FP_IP6_2_DST6
    global FP_IP6_2_DST7

    if {$profile >= $GEM_MAX_PROFILES || $profile <= 0} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 1 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR

    set cmd {}

    # CMD
    lappend cmd 0xF2

    # LEN PLACEHOLDER (to be filled in later)
    lappend cmd 0

    # BLADE AND PROFILE
    lappend cmd $blade
    lappend cmd $profile

    # ENABLE THIS FILTER
    lappend cmd 1


    foreach a $args {


        if {[regexp -nocase \
             {^-ip_src=([\*0-9]+).([\*0-9]+).([\*0-9]+).([\*0-9]+)$} \
              $a tmp byte1 byte2 byte3 byte4]} \
        {
            puts "  IP Src:  $byte1.$byte2.$byte3.$byte4"

            if {[string compare $byte1 "*"] != 0} {
                lappend cmd $FP_IP_SRC0
                lappend cmd $byte1
            }
            if {[string compare $byte2 "*"] != 0} {
                lappend cmd $FP_IP_SRC1
                lappend cmd $byte2
            }
            if {[string compare $byte3 "*"] != 0} {
                lappend cmd $FP_IP_SRC2
                lappend cmd $byte3
            }
            if {[string compare $byte4 "*"] != 0} {
                lappend cmd $FP_IP_SRC3
                lappend cmd $byte4
            }
        }\
        elseif {[regexp -nocase \
             {^-ip_src=([\*0-9]+).([\*0-9]+).([\*0-9]+).([\*0-9]+)/([0-9]+)$} \
              $a tmp byte1 byte2 byte3 byte4 cidr]} \
        {
            puts "  IP Src:  $byte1.$byte2.$byte3.$byte4/$cidr"

            if {[string compare $byte1 "*"] != 0} {
                lappend cmd $FP_IP_SRC0
                lappend cmd $byte1
            }
            if {[string compare $byte2 "*"] != 0} {
                lappend cmd $FP_IP_SRC1
                lappend cmd $byte2
            }
            if {[string compare $byte3 "*"] != 0} {
                lappend cmd $FP_IP_SRC2
                lappend cmd $byte3
            }
            if {[string compare $byte4 "*"] != 0} {
                lappend cmd $FP_IP_SRC3
                lappend cmd $byte4
            }

            lappend cmd $FP_IP_SRC_MASK
            lappend cmd $cidr
        }\
        elseif {[regexp -nocase \
             {^-ip_dst=([\*0-9]+).([\*0-9]+).([\*0-9]+).([\*0-9]+)$} \
              $a tmp byte1 byte2 byte3 byte4]} \
        {
            puts "  IP Dst:  $byte1.$byte2.$byte3.$byte4"

            if {[string compare $byte1 "*"] != 0} {
                lappend cmd $FP_IP_DST0
                lappend cmd $byte1
            }
            if {[string compare $byte2 "*"] != 0} {
                lappend cmd $FP_IP_DST1
                lappend cmd $byte2
            }
            if {[string compare $byte3 "*"] != 0} {
                lappend cmd $FP_IP_DST2
                lappend cmd $byte3
            }
            if {[string compare $byte4 "*"] != 0} {
                lappend cmd $FP_IP_DST3
                lappend cmd $byte4
            }
        }\
        elseif {[regexp -nocase \
             {^-ip_dst=([\*0-9]+).([\*0-9]+).([\*0-9]+).([\*0-9]+)/([0-9]+)$} \
              $a tmp byte1 byte2 byte3 byte4 cidr]} \
        {
            puts "  IP Dst:  $byte1.$byte2.$byte3.$byte4/$cidr"

            if {[string compare $byte1 "*"] != 0} {
                lappend cmd $FP_IP_DST0
                lappend cmd $byte1
            }
            if {[string compare $byte2 "*"] != 0} {
                lappend cmd $FP_IP_DST1
                lappend cmd $byte2
            }
            if {[string compare $byte3 "*"] != 0} {
                lappend cmd $FP_IP_DST2
                lappend cmd $byte3
            }
            if {[string compare $byte4 "*"] != 0} {
                lappend cmd $FP_IP_DST3
                lappend cmd $byte4
            }

            lappend cmd $FP_IP_DST_MASK
            lappend cmd $cidr
        }\
        elseif {[regexp -nocase \
{^-mac_src=([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+)$} \
              $a tmp byte1 byte2 byte3 byte4 byte5 byte6]} \
        {
            puts "  MAC Src:  $byte1:$byte2:$byte3:$byte4:$byte5:$byte6"

            if {[string compare $byte1 "*"] != 0} {
                set byte1 [expr "0x$byte1" + 0]
                lappend cmd $FP_MAC_SRC0
                lappend cmd $byte1
            }
            if {[string compare $byte2 "*"] != 0} {
                set byte2 [expr "0x$byte2" + 0]
                lappend cmd $FP_MAC_SRC1
                lappend cmd $byte2
            }
            if {[string compare $byte3 "*"] != 0} {
                set byte3 [expr "0x$byte3" + 0]
                lappend cmd $FP_MAC_SRC2
                lappend cmd $byte3
            }
            if {[string compare $byte4 "*"] != 0} {
                set byte4 [expr "0x$byte4" + 0]
                lappend cmd $FP_MAC_SRC3
                lappend cmd $byte4
            }
            if {[string compare $byte5 "*"] != 0} {
                set byte5 [expr "0x$byte5" + 0]
                lappend cmd $FP_MAC_SRC4
                lappend cmd $byte5
            }
            if {[string compare $byte6 "*"] != 0} {
                set byte6 [expr "0x$byte6" + 0]
                lappend cmd $FP_MAC_SRC5
                lappend cmd $byte6
            }
        }\
        elseif {[regexp -nocase \
{^-mac_dst=([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+).([\*A-Fa-f0-9]+)$} \
              $a tmp byte1 byte2 byte3 byte4 byte5 byte6]} \
        {
            puts "  MAC Dst:  $byte1:$byte2:$byte3:$byte4:$byte5:$byte6"

            if {[string compare $byte1 "*"] != 0} {
                set byte1 [expr "0x$byte1" + 0]
                lappend cmd $FP_MAC_DST0
                lappend cmd $byte1
            }
            if {[string compare $byte2 "*"] != 0} {
                set byte2 [expr "0x$byte2" + 0]
                lappend cmd $FP_MAC_DST1
                lappend cmd $byte2
            }
            if {[string compare $byte3 "*"] != 0} {
                set byte3 [expr "0x$byte3" + 0]
                lappend cmd $FP_MAC_DST2
                lappend cmd $byte3
            }
            if {[string compare $byte4 "*"] != 0} {
                set byte4 [expr "0x$byte4" + 0]
                lappend cmd $FP_MAC_DST3
                lappend cmd $byte4
            }
            if {[string compare $byte5 "*"] != 0} {
                set byte5 [expr "0x$byte5" + 0]
                lappend cmd $FP_MAC_DST4
                lappend cmd $byte5
            }
            if {[string compare $byte6 "*"] != 0} {
                set byte6 [expr "0x$byte6" + 0]
                lappend cmd $FP_MAC_DST5
                lappend cmd $byte6
            }
        }\
        elseif {[regexp -nocase \
{^-ip6_src=([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+)$} \
              $a tmp byte0 byte1 byte2 byte3 byte4 byte5 byte6 byte7 byte8 byte9 byte10 byte11 byte12 byte13 byte14 byte15]} \
        {
            puts "WARNING:  This IPv6 address format is no longer supported."
            puts "WARNING:  Please use the following format:"
            puts "WARNING:     -ip6_src=A050:8000:*:*:*:*:*:*"
            puts "WARNING:              (* for any 16-bit word to wildcard)"
        }\
        elseif {[regexp -nocase \
{^-ip6_src=([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+)$} \
              $a tmp word0 word1 word2 word3 word4 word5 word6 word7]} \
        {
            puts "  IPv6 Src:  $word0:$word1:$word2:$word3:$word4:$word5:$word6:$word7"

            if {[string compare $word0 "*"] != 0} {
                set word0 [expr "0x$word0" + 0]
                lappend cmd $FP_IP6_2_SRC0
                lappend cmd [expr ($word0 >> 8) & 0xFF]
                lappend cmd [expr ($word0 >> 0) & 0xFF]
            }
            if {[string compare $word1 "*"] != 0} {
                set word1 [expr "0x$word1" + 0]
                lappend cmd $FP_IP6_2_SRC1
                lappend cmd [expr ($word1 >> 8) & 0xFF]
                lappend cmd [expr ($word1 >> 0) & 0xFF]
            }
            if {[string compare $word2 "*"] != 0} {
                set word2 [expr "0x$word2" + 0]
                lappend cmd $FP_IP6_2_SRC2
                lappend cmd [expr ($word2 >> 8) & 0xFF]
                lappend cmd [expr ($word2 >> 0) & 0xFF]
            }
            if {[string compare $word3 "*"] != 0} {
                set word3 [expr "0x$word3" + 0]
                lappend cmd $FP_IP6_2_SRC3
                lappend cmd [expr ($word3 >> 8) & 0xFF]
                lappend cmd [expr ($word3 >> 0) & 0xFF]
            }
            if {[string compare $word4 "*"] != 0} {
                set word4 [expr "0x$word4" + 0]
                lappend cmd $FP_IP6_2_SRC4
                lappend cmd [expr ($word4 >> 8) & 0xFF]
                lappend cmd [expr ($word4 >> 0) & 0xFF]
            }
            if {[string compare $word5 "*"] != 0} {
                set word5 [expr "0x$word5" + 0]
                lappend cmd $FP_IP6_2_SRC5
                lappend cmd [expr ($word5 >> 8) & 0xFF]
                lappend cmd [expr ($word5 >> 0) & 0xFF]
            }
            if {[string compare $word6 "*"] != 0} {
                set word6 [expr "0x$word6" + 0]
                lappend cmd $FP_IP6_2_SRC6
                lappend cmd [expr ($word6 >> 8) & 0xFF]
                lappend cmd [expr ($word6 >> 0) & 0xFF]
            }
            if {[string compare $word7 "*"] != 0} {
                set word7 [expr "0x$word7" + 0]
                lappend cmd $FP_IP6_2_SRC7
                lappend cmd [expr ($word7 >> 8) & 0xFF]
                lappend cmd [expr ($word7 >> 0) & 0xFF]
            }
        }\
        elseif {[regexp -nocase \
{^-ip6_dst=([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+)$} \
              $a tmp byte0 byte1 byte2 byte3 byte4 byte5 byte6 byte7 byte8 byte9 byte10 byte11 byte12 byte13 byte14 byte15]} \
        {
            puts "WARNING:  This IPv6 address format is no longer supported."
            puts "WARNING:  Please use the following format:"
            puts "WARNING:     -ip6_dst=A050:8000:*:*:*:*:*:*"
            puts "WARNING:              (* for any 16-bit word to wildcard)"
        }\
        elseif {[regexp -nocase \
{^-ip6_dst=([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+):([\*A-Fa-f0-9]+)$} \
              $a tmp word0 word1 word2 word3 word4 word5 word6 word7]} \
        {
            puts "  IPv6 Dst:  $word0:$word1:$word2:$word3:$word4:$word5:$word6:$word7"

            if {[string compare $word0 "*"] != 0} {
                set word0 [expr "0x$word0" + 0]
                lappend cmd $FP_IP6_2_DST0
                lappend cmd [expr ($word0 >> 8) & 0xFF]
                lappend cmd [expr ($word0 >> 0) & 0xFF]
            }
            if {[string compare $word1 "*"] != 0} {
                set word1 [expr "0x$word1" + 0]
                lappend cmd $FP_IP6_2_DST1
                lappend cmd [expr ($word1 >> 8) & 0xFF]
                lappend cmd [expr ($word1 >> 0) & 0xFF]
            }
            if {[string compare $word2 "*"] != 0} {
                set word2 [expr "0x$word2" + 0]
                lappend cmd $FP_IP6_2_DST2
                lappend cmd [expr ($word2 >> 8) & 0xFF]
                lappend cmd [expr ($word2 >> 0) & 0xFF]
            }
            if {[string compare $word3 "*"] != 0} {
                set word3 [expr "0x$word3" + 0]
                lappend cmd $FP_IP6_2_DST3
                lappend cmd [expr ($word3 >> 8) & 0xFF]
                lappend cmd [expr ($word3 >> 0) & 0xFF]
            }
            if {[string compare $word4 "*"] != 0} {
                set word4 [expr "0x$word4" + 0]
                lappend cmd $FP_IP6_2_DST4
                lappend cmd [expr ($word4 >> 8) & 0xFF]
                lappend cmd [expr ($word4 >> 0) & 0xFF]
            }
            if {[string compare $word5 "*"] != 0} {
                set word5 [expr "0x$word5" + 0]
                lappend cmd $FP_IP6_2_DST5
                lappend cmd [expr ($word5 >> 8) & 0xFF]
                lappend cmd [expr ($word5 >> 0) & 0xFF]
            }
            if {[string compare $word6 "*"] != 0} {
                set word6 [expr "0x$word6" + 0]
                lappend cmd $FP_IP6_2_DST6
                lappend cmd [expr ($word6 >> 8) & 0xFF]
                lappend cmd [expr ($word6 >> 0) & 0xFF]
            }
            if {[string compare $word7 "*"] != 0} {
                set word7 [expr "0x$word7" + 0]
                lappend cmd $FP_IP6_2_DST7
                lappend cmd [expr ($word7 >> 8) & 0xFF]
                lappend cmd [expr ($word7 >> 0) & 0xFF]
            }
        }\
        elseif {[regexp -nocase {^-mpls1=([\*0-9]+)$} $a tmp val]} \
        {
            puts "  MPLS Label #1:  $val"
            set val [expr "$val" + 0]
            lappend cmd $FP_MPLS_LABEL1
            lappend cmd [expr ($val >> 24) & 0xFF]
            lappend cmd [expr ($val >> 16) & 0xFF]
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-mpls2=([\*0-9]+)$} $a tmp val]} \
        {
            puts "  MPLS Label #2:  $val"
            set val [expr "$val" + 0]
            lappend cmd $FP_MPLS_LABEL2
            lappend cmd [expr ($val >> 24) & 0xFF]
            lappend cmd [expr ($val >> 16) & 0xFF]
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-mac_lentype=([\*A-Za-z0-9]+)$} $a tmp val]} \
        {
            set val [expr "0x$val" + 0]
            puts "  MAC Len/Type:  $val"
            lappend cmd $FP_MAC_LENTYPE
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-ip_dscp=([\*A-Za-z0-9]+)$} $a tmp val]} \
        {
            set val [expr "0x$val" + 0]
            puts "  IP DiffServ/TOS:  $val"
            lappend cmd $FP_IP_DSCP
            lappend cmd $val
        }\
        elseif {[regexp -nocase {^-ip_diffservtos=([\*A-Za-z0-9]+)$} $a tmp val]} \
        {
            set val [expr "0x$val" + 0]
            puts "  IP DiffServ/TOS:  $val"
            lappend cmd $FP_IP_DSCP
            lappend cmd $val
        }\
        elseif {[regexp -nocase {^-ip_protocol=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  IP Protocol:  $val"
            lappend cmd $FP_IP_PROTOCOL
            lappend cmd $val
        }\
        elseif {[regexp -nocase {^-port_src=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  Source Port:  $val"
            lappend cmd $FP_PORT_SRC
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-port_dst=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  Destination Port:  $val"
            lappend cmd $FP_PORT_DST
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-tpid=([\*A-Za-z0-9]+)$} $a tmp val]} \
        {
            puts "  TPID:  $val"
            set val [expr "0x$val" + 0]
            lappend cmd $FP_TPID
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-first_tpid=([\*A-Za-z0-9]+)$} $a tmp val]} \
        {
            puts "  First TPID:  $val"
            set val [expr "0x$val" + 0]
            lappend cmd $FP_TPID
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-vid=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr "$val" + 0]
            puts "  VLAN ID:  $val"
            lappend cmd $FP_VLANID
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-first_vid=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr "$val" + 0]
            puts "  First VLAN ID:  $val"
            lappend cmd $FP_VLANID
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-priority=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  Priority:  $val"
            lappend cmd $FP_PRIO
            lappend cmd $val
        }\
        elseif {[regexp -nocase {^-first_priority=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  First Priority:  $val"
            lappend cmd $FP_PRIO
            lappend cmd $val
        }\
        elseif {[regexp -nocase {^-qinq_tpid=([\*A-Za-z0-9]+)$} $a tmp val]} \
        {
            puts "  Q-in-Q TPID:  $val"
            set val [expr "0x$val" + 0]
            lappend cmd $FP_QINQ_TPID
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-second_tpid=([\*A-Za-z0-9]+)$} $a tmp val]} \
        {
            puts "  Second TPID:  $val"
            set val [expr "0x$val" + 0]
            lappend cmd $FP_QINQ_TPID
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-qinq_vid=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr "$val" + 0]
            puts "  Q-in-Q VLAN ID:  $val"
            lappend cmd $FP_QINQ_VLANID
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-second_vid=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr "$val" + 0]
            puts "  Second VLAN ID:  $val"
            lappend cmd $FP_QINQ_VLANID
            lappend cmd [expr ($val >> 8) & 0xFF]
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-qinq_priority=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  Q-in-Q Priority:  $val"
            lappend cmd $FP_QINQ_PRIO
            lappend cmd $val
        }\
        elseif {[regexp -nocase {^-second_priority=([\*0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  Second Priority:  $val"
            lappend cmd $FP_QINQ_PRIO
            lappend cmd $val
        }\
        elseif {[regexp -nocase {^-checkip$} $a tmp]} \
        {
            puts "  Check IP Version:  Enabled"
            lappend cmd $FP_CHECK_IP_VERSION
            lappend cmd 1
        }\
        elseif {[regexp -nocase {^-dontcheckip$} $a tmp]} \
        {
            puts "  Check IP Version:  Disabled"
            lappend cmd $FP_CHECK_IP_VERSION
            lappend cmd 0
        }\
        elseif {[regexp -nocase {^-name=(.*)$} $a tmp val]} \
        {
            puts "  Name:  $val"
            lappend cmd $FP_NAME

            set namelist [split $val {}]
            foreach char $namelist {
                scan $char %c asciival
                lappend cmd $asciival
            }
            lappend cmd 0
        }\
        elseif {[regexp -nocase {^-custom=([0-9]+)\/([0-9]+)\/(0x[A-Za-z0-9]+)$} $a tmp offset value mask]} \
        {
            puts "  Custom:  Byte $offset ($mask) == $value"
            set offset [expr $offset + 0]
            set mask [expr $mask + 0]
            set value [expr $value + 0]
            if {$offset > $GEM_MAX_OFFSET} {
                puts "ERROR:  Offset for custom byte value cannot be greater than $GEM_MAX_OFFSET."
                return
            }
            lappend cmd $FP_CUSTOM_BYTE
            lappend cmd 1
            lappend cmd [expr ($offset >> 8) & 0xFF]
            lappend cmd [expr ($offset >> 0) & 0xFF]
            lappend cmd $mask
            lappend cmd $value
        }\
        elseif {[regexp -nocase {^-custom_byte=([0-9]+)\/([0-9]+)\/(0x[A-Za-z0-9]+)$} $a tmp offset value mask]} \
        {
            puts "  Custom:  Byte $offset ($mask) == $value"
            set offset [expr $offset + 0]
            set mask [expr $mask + 0]
            set value [expr $value + 0]
            if {$offset > $GEM_MAX_OFFSET} {
                puts "ERROR:  Offset for custom byte value cannot be greater than $GEM_MAX_OFFSET."
                return
            }
            lappend cmd $FP_CUSTOM_BYTE
            lappend cmd 1
            lappend cmd [expr ($offset >> 8) & 0xFF]
            lappend cmd [expr ($offset >> 0) & 0xFF]
            lappend cmd $mask
            lappend cmd $value
        }\
        elseif {[regexp -nocase {^-custom_byte([1-4])=([0-9]+)\/(0x[A-Za-z0-9]+)\/(0x[A-Za-z0-9]+)$} $a tmp id offset value mask]} \
        {
            puts "  Custom:  Byte #$id $offset ($mask) == $value"
            set offset [expr $offset + 0]
            set mask [expr $mask + 0]
            set value [expr $value + 0]
            if {$offset > $GEM_MAX_OFFSET} {
                puts "ERROR:  Offset for custom byte value cannot be greater than $GEM_MAX_OFFSET."
                return
            }
            lappend cmd $FP_CUSTOM_BYTE
            lappend cmd $id
            lappend cmd [expr ($offset >> 8) & 0xFF]
            lappend cmd [expr ($offset >> 0) & 0xFF]
            lappend cmd $mask
            lappend cmd $value
        }\
        elseif {[regexp -nocase {^-custom_value=([0-9]+)\/(0x[A-Za-z0-9]+)\/(0x[A-Za-z0-9]+)$} $a tmp offset value mask]} \
        {
            puts "  Custom:  Value @ $offset ($mask) == $value"
            set offset [expr $offset + 0]
            set mask [expr $mask + 0]
            set value [expr $value + 0]
            if {$offset > [expr $GEM_MAX_OFFSET - 3]} {
                puts "ERROR:  Offset for custom value cannot be greater than [expr $GEM_MAX_OFFSET - 3]."
                return
            }
            lappend cmd $FP_CUSTOM_VALUE
            lappend cmd 1
            lappend cmd [expr ($offset >> 8) & 0xFF]
            lappend cmd [expr ($offset >> 0) & 0xFF]
            lappend cmd [expr ($mask >> 24) & 0xFF]
            lappend cmd [expr ($mask >> 16) & 0xFF]
            lappend cmd [expr ($mask >> 8) & 0xFF]
            lappend cmd [expr ($mask >> 0) & 0xFF]
            lappend cmd [expr ($value >> 24) & 0xFF]
            lappend cmd [expr ($value >> 16) & 0xFF]
            lappend cmd [expr ($value >> 8) & 0xFF]
            lappend cmd [expr ($value >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-custom_value([1-8])=([0-9]+)\/(0x[A-Za-z0-9]+)\/(0x[A-Za-z0-9]+)$} $a tmp id offset value mask]} \
        {
            puts "  Custom:  Value #$id @ $offset ($mask) == $value"
            set offset [expr $offset + 0]
            set mask [expr $mask + 0]
            set value [expr $value + 0]
            if {$offset > [expr $GEM_MAX_OFFSET - 3]} {
                puts "ERROR:  Offset for custom value cannot be greater than [expr $GEM_MAX_OFFSET - 3]."
                return
            }
            lappend cmd $FP_CUSTOM_VALUE
            lappend cmd $id
            lappend cmd [expr ($offset >> 8) & 0xFF]
            lappend cmd [expr ($offset >> 0) & 0xFF]
            lappend cmd [expr ($mask >> 24) & 0xFF]
            lappend cmd [expr ($mask >> 16) & 0xFF]
            lappend cmd [expr ($mask >> 8) & 0xFF]
            lappend cmd [expr ($mask >> 0) & 0xFF]
            lappend cmd [expr ($value >> 24) & 0xFF]
            lappend cmd [expr ($value >> 16) & 0xFF]
            lappend cmd [expr ($value >> 8) & 0xFF]
            lappend cmd [expr ($value >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-ingress_port=([0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  Ingress Port:  $val"
            lappend cmd $FP_INGRESS_PORT
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase {^-egress_port=([0-9]+)$} $a tmp val]} \
        {
            set val [expr $val + 0]
            puts "  Egress Port:  $val"
            lappend cmd $FP_EGRESS_PORT
            lappend cmd [expr ($val >> 0) & 0xFF]
        }\
        elseif {[regexp -nocase \
              {^-next_hop=([\*0-9]{1,3})[.]([\*0-9]{1,3})[.]([\*0-9]{1,3})[.]([\*0-9]{1,3})$} \
              $a tmp byte1 byte2 byte3 byte4]} \
        {
            puts "  Next Hop:  $byte1.$byte2.$byte3.$byte4"

            if {[string compare $byte1 "*"] != 0} {
                lappend cmd $FP_NXTHOP_IP0
                lappend cmd $byte1
            }
            if {[string compare $byte2 "*"] != 0} {
                lappend cmd $FP_NXTHOP_IP1
                lappend cmd $byte2
            }
            if {[string compare $byte3 "*"] != 0} {
                lappend cmd $FP_NXTHOP_IP2
                lappend cmd $byte3
            }
            if {[string compare $byte4 "*"] != 0} {
                lappend cmd $FP_NXTHOP_IP3
                lappend cmd $byte4
            }
        }\
        else {
            puts "Invalid argument:  $a"
            return
        }
    } 

    if {[llength $cmd] == 5} {
        puts "Please specify one or more filters."
        return
    }

    puts "gem_define_profile $profile $args"

    set_target 0

    # INSERT REAL LENGTH
    set cmd [lreplace $cmd 1 1 [expr [llength $cmd] - 2]]

    send_command [BuildCommand $cmd]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_show_profile
#                  :
# Parameters       : profile - the profile whose profile is to be displayed
######################################################################
proc gem_show_profile {profile} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global PKTCORRUPT_BL_RAND
    global PKTCORRUPT_BL_FIXED
    global GEM_MAX_PROFILES

    if {$profile >= $GEM_MAX_PROFILES || $profile <= 0} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 1 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xF3 2 $blade $profile]
    set ret [lrange [pong] 4 end]
    set info [lrange $ret 1 end]

    set_target $blade
    
    set enabled [value_from_array [lrange $ret 0 0]]

    set namepos [lsearch $info 00]
    incr namepos

    set namelist [lrange $info $namepos [expr [llength $info] - 2]]
    set namechars {}
    foreach a $namelist {
        lappend namechars [format %c "0x$a"]
    }

    set filterlist [lrange $info 0 [expr $namepos -2]]
    set filterchars {}
    foreach a $filterlist {
        lappend filterchars [format %c "0x$a"]
    }

    set name [join $namechars ""]

    puts -nonewline "Profile #$profile"
    if {[string compare $name ""] == 0} {
        puts -nonewline ": "
    } else {
        puts -nonewline " ($name): "
    }

    set filter [join $filterchars ""]
    puts $filter

    if {$enabled == 1} {
        puts "This profile is currently ENABLED."
    } else {
        puts "This profile is currently DISABLED."
    }
}

######################################################################
# Function Name    : gem_disable_profile
#                  :
# Parameters       : profile - the profile to be disabled
#                  :
# Purpose          : Disable a previously configured profile.
######################################################################
proc gem_disable_profile {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {$profile >= $GEM_MAX_PROFILES || $profile <= 0} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 1 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_disable_profile $profile"

    set blade $TX_DEST_ADDR

    set_target 0

    send_command [BuildCommand 0xF2 3 $blade $profile 0]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_program_profiles
#
# Purpose          : After setting up all of the profile definitions,
#                  : use this routine to program them.
######################################################################
proc gem_program_profiles {} {
    global TX_DEST_ADDR
    global COMM_WARN
    global COMM_TIMEOUT

    set old_warn $COMM_WARN
    set COMM_WARN $COMM_TIMEOUT

    puts "gem_program_profiles"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xF4 1 $blade]
    set ret [pong]
    nack_msg $ret

    set msg {}
    foreach a [lrange $ret 3 end] {
        lappend msg [format %c "0x$a"]
    }

    set_target $blade
    set COMM_WARN $old_warn

    puts [join $msg ""]
}

######################################################################
# Function Name    : gem_reset_profile_stats
#                  :
# Parameters       : profile
#                  :
# Purpose          : Reset the cumulative profile statistics counters.
######################################################################
proc gem_reset_profile_stats {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xF7 2 $blade $profile]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_reset_line_stats
#                  :
# Purpose          : Reset the cumulative profile statistics counters.
######################################################################
proc gem_reset_line_stats {} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xF8 1 $blade]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_clear_alarms
#                  :
# Purpose          : Clear the alarms.
######################################################################
proc gem_clear_alarms {} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xFA 1 $blade]
    pong_check

    set_target $blade
}


######################################################################
# INTERNAL ROUTINES
######################################################################
set COLUMN1  20
set COLUMN2  17
set COLUMN3  30

set COLUMN12 [expr $COLUMN1 + $COLUMN2]

proc disp_hdr {} {
    global COLUMN12
    global COLUMN3

    puts [format "%${COLUMN12}s%${COLUMN3}s" "Current" "Cumulative"]
}

proc disp_hdr2 {} {
    global COLUMN12
    global COLUMN3

    puts [format "%${COLUMN12}s%${COLUMN3}s" "Last Second" "Entire Test"]
}

proc disp_rate {name cur cum} {
    global COLUMN1
    global COLUMN2
    global COLUMN3

    set cur [expr $cur / 100.0]
    set cum [expr $cum / 100.0]
    puts [format "%-${COLUMN1}s%${COLUMN2}.0f%${COLUMN3}.0f" $name $cur $cum]
}

proc disp_stat {name cur cum} {
    global COLUMN1
    global COLUMN2
    global COLUMN3

    puts [format "%-${COLUMN1}s%${COLUMN2}d%${COLUMN3}.0f" $name $cur $cum]
}

proc disp_stat2 {name cur cum units} {
    global COLUMN1
    global COLUMN2
    global COLUMN3

    set c1 $COLUMN1
    set c2 $COLUMN2
    set c3 [expr $COLUMN3 - [string length $units] - 1]

    puts [format "%-${c1}s%${c2}f ${units}%${c3}f ${units}" $name $cur $cum]
}

proc alarm_to_string {state} {

    if {$state == 0} {
        return "RED"
    } elseif {$state == 1} {
        return "YELLOW"
    } elseif {$state == 2} {
        return "GREEN"
    } else {
        return "(unknown)"
    }
}

proc disp_alarm {name state} {

    puts [format "%-20s : %6s" $name [alarm_to_string $state]]
}

######################################################################
# Function Name    : gem_show_profile_stats
#                  :
# Parameters       : profile
#                  :
# Returns          : An associative array indexed by the following keys:
#                  :
#                  :    RX_BYTES_CURRENT
#                  :    RX_BYTES_CUMULATIVE
#                  :    RX_PACKETS_CURRENT
#                  :    RX_PACKETS_CUMULATIVE
#                  :    RX_BYTES_PER_SEC_CURRENT
#                  :    RX_BYTES_PER_SEC_CUMULATIVE
#                  :    RX_PACKETS_PER_SEC_CURRENT
#                  :    RX_PACKETS_PER_SEC_CUMULATIVE
#                  :    RX_CRC_ERRORS_CURRENT
#                  :    RX_CRC_ERRORS_CUMULATIVE
#                  :    TX_BYTES_CURRENT
#                  :    TX_BYTES_CUMULATIVE
#                  :    TX_PACKETS_CURRENT
#                  :    TX_PACKETS_CUMULATIVE
#                  :    TX_BYTES_PER_SEC_CURRENT
#                  :    TX_BYTES_PER_SEC_CUMULATIVE
#                  :    TX_PACKETS_PER_SEC_CURRENT
#                  :    TX_PACKETS_PER_SEC_CUMULATIVE
#                  :    TX_CRC_ERRORS_CURRENT
#                  :    TX_CRC_ERRORS_CUMULATIVE
#                  :    GREEN_BYTES_CURRENT
#                  :    GREEN_BYTES_CUMULATIVE
#                  :    GREEN_PACKETS_CURRENT
#                  :    GREEN_PACKETS_CUMULATIVE
#                  :    YELLOW_BYTES_CURRENT
#                  :    YELLOW_BYTES_CUMULATIVE
#                  :    YELLOW_PACKETS_CURRENT
#                  :    YELLOW_PACKETS_CUMULATIVE
#                  :    RED_BYTES_CURRENT
#                  :    RED_BYTES_CUMULATIVE
#                  :    RED_PACKETS_CURRENT
#                  :    RED_PACKETS_CUMULATIVE
#                  :    IMP_BYTES_DROPPED_CURRENT
#                  :    IMP_BYTES_DROPPED_CUMULATIVE
#                  :    IMP_PACKETS_DROPPED_CURRENT
#                  :    IMP_PACKETS_DROPPED_CUMULATIVE
#                  :    IMP_BYTES_CORRUPTED_CURRENT
#                  :    IMP_BYTES_CORRUPTED_CUMULATIVE
#                  :    IMP_PACKETS_CORRUPTED_CURRENT
#                  :    IMP_PACKETS_CORRUPTED_CUMULATIVE
#                  :    IMP_PACKETS_REORDERED_CURRENT
#                  :    IMP_PACKETS_REORDERED_CUMULATIVE
#                  :    IMP_PACKETS_DUPLICATED_CURRENT
#                  :    IMP_PACKETS_DUPLICATED_CUMULATIVE
#                  :    IMP_CRC_CORRUPTED_CURRENT
#                  :    IMP_CRC_CORRUPTED_CUMULATIVE
#                  :    IMP_PACKETS_MODIFIED_CURRENT
#                  :    IMP_PACKETS_MODIFIED_CUMULATIVE
#                  :    IMP_BITS_MODIFIED_CURRENT
#                  :    IMP_BITS_MODIFIED_CUMULATIVE
#                  :    OF_PACKETS_DROPPED_CURRENT
#                  :    OF_PACKETS_DROPPED_CUMULATIVE
#                  :    OF_BYTES_DROPPED_CURRENT
#                  :    OF_BYTES_DROPPED_CUMULATIVE
#                  :    MIN_DELAY_CURRENT
#                  :    MIN_DELAY_CUMULATIVE
#                  :    MAX_DELAY_CURRENT
#                  :    MAX_DELAY_CUMULATIVE
#                  :    AVG_DELAY_CURRENT
#                  :    AVG_DELAY_CUMULATIVE
#                  :    IPFRAG_PKTS_SELECTED_CURRENT
#                  :    IPFRAG_PKTS_SELECTED_CUMULATIVE
#                  :    IPFRAG_PKTS_FRAGMENTED_CURRENT
#                  :    IPFRAG_PKTS_FRAGMENTED_CUMULATIVE
#                  :    IPFRAG_FRAGMENTS_SENT_CURRENT
#                  :    IPFRAG_FRAGMENTS_SENT_CUMULATIVE
#                  :    IPFRAG_DNF_PKTS_DROPPED_CURRENT
#                  :    IPFRAG_DNF_PKTS_DROPPED_CUMULATIVE
#                  :    SECS_SINCE_RESET
#                  :
# Purpose          : Display the statistics for a specific network profile.
######################################################################
proc gem_show_profile_stats {profile {units "ms"}} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xF5 2 $blade $profile]
    set ret [lrange [pong] 4 end]

    set rxbytes        [value_from_array [lrange $ret 0  3 ]]
    set rxbytes_tot    [value_from_array [lrange $ret 4  11]]
    set rxpkts         [value_from_array [lrange $ret 12 15]]
    set rxpkts_tot     [value_from_array [lrange $ret 16 23]]
    set rxbyterate     [value_from_array [lrange $ret 24 27]]
    set rxbyterate_tot [value_from_array [lrange $ret 28 31]]
    set rxpktrate      [value_from_array [lrange $ret 32 35]]
    set rxpktrate_tot  [value_from_array [lrange $ret 36 39]]
    set rxcrc          [value_from_array [lrange $ret 40 43]]
    set rxcrc_tot      [value_from_array [lrange $ret 44 51]]

    set txbytes        [value_from_array [lrange $ret 52 55]]
    set txbytes_tot    [value_from_array [lrange $ret 56 63]]
    set txpkts         [value_from_array [lrange $ret 64 67]]
    set txpkts_tot     [value_from_array [lrange $ret 68 75]]
    set txbyterate     [value_from_array [lrange $ret 76 79]]
    set txbyterate_tot [value_from_array [lrange $ret 80 83]]
    set txpktrate      [value_from_array [lrange $ret 84 87]]
    set txpktrate_tot  [value_from_array [lrange $ret 88 91]]
    set txcrc          [value_from_array [lrange $ret 92 95]]
    set txcrc_tot      [value_from_array [lrange $ret 96 103]]

    set polbgreen      [value_from_array [lrange $ret 104 107]]
    set polbgreen_tot  [value_from_array [lrange $ret 108 115]]
    set polpgreen      [value_from_array [lrange $ret 116 119]]
    set polpgreen_tot  [value_from_array [lrange $ret 120 127]]
    set polbyellow     [value_from_array [lrange $ret 128 131]]
    set polbyellow_tot [value_from_array [lrange $ret 132 139]]
    set polpyellow     [value_from_array [lrange $ret 140 143]]
    set polpyellow_tot [value_from_array [lrange $ret 144 151]]
    set polbred        [value_from_array [lrange $ret 152 155]]
    set polbred_tot    [value_from_array [lrange $ret 156 163]]
    set polpred        [value_from_array [lrange $ret 164 167]]
    set polpred_tot    [value_from_array [lrange $ret 168 175]]

    set impbdrop       [value_from_array [lrange $ret 176 179]]
    set impbdrop_tot   [value_from_array [lrange $ret 180 185]]
    set imppdrop       [value_from_array [lrange $ret 186 189]]
    set imppdrop_tot   [value_from_array [lrange $ret 190 195]]
    set impbcrpt       [value_from_array [lrange $ret 196 199]]
    set impbcrpt_tot   [value_from_array [lrange $ret 200 205]]
    set imppcrpt       [value_from_array [lrange $ret 206 209]]
    set imppcrpt_tot   [value_from_array [lrange $ret 210 215]]
    set impreord       [value_from_array [lrange $ret 216 219]]
    set impreord_tot   [value_from_array [lrange $ret 220 225]]
    set impdupe        [value_from_array [lrange $ret 226 229]]
    set impdupe_tot    [value_from_array [lrange $ret 230 235]]
    set impcrc         [value_from_array [lrange $ret 236 239]]
    set impcrc_tot     [value_from_array [lrange $ret 240 245]]

    set tot_time       [value_from_array [lrange $ret 246 249]]

    send_command [BuildCommand 0x6E 2 $blade $profile]
    set ret [lrange [pong] 4 end]

    set ofpkts         [value_from_array [lrange $ret 0  3 ]]
    set ofpkts_tot     [value_from_array [lrange $ret 4  11]]
    set ofbytes        [value_from_array [lrange $ret 12  15]]
    set ofbytes_tot    [value_from_array [lrange $ret 16  23]]

    set impmodpkts     [value_from_array [lrange $ret 24  27 ]]
    set impmodpkts_tot [value_from_array [lrange $ret 28  35]]
    set impmodbits     [value_from_array [lrange $ret 36  39]]
    set impmodbits_tot [value_from_array [lrange $ret 40  47]]

    set mindelay       [value_from_array [lrange $ret 48  51]]
    set maxdelay       [value_from_array [lrange $ret 52  55]]
    set avgdelay       [value_from_array [lrange $ret 56  59]]

    set mindelay_tot   [value_from_array [lrange $ret 60  63]]
    set maxdelay_tot   [value_from_array [lrange $ret 64  67]]
    set avgdelay_tot   [value_from_array [lrange $ret 68  71]]

    set ipfpkts        [value_from_array [lrange $ret 72  75]]
    set ipfpkts_tot    [value_from_array [lrange $ret 76  83]]

    set ipfpktsfd      [value_from_array [lrange $ret 84  87]]
    set ipfpktsfd_tot  [value_from_array [lrange $ret 88  95]]

    set ipffrags       [value_from_array [lrange $ret 96  99]]
    set ipffrags_tot   [value_from_array [lrange $ret 100 107]]

    set ipfdrops       [value_from_array [lrange $ret 108 111]]
    set ipfdrops_tot   [value_from_array [lrange $ret 112 119]]

# Comment out Mantis 1590
#    set avgscheddelay  [value_from_array [lrange $ret 72  75]]
#    set avgscheddelay_tot [value_from_array [lrange $ret 76  83]]
#    set avgshapdelay  [value_from_array [lrange $ret 84  87]]
#    set avgshapdelay_tot [value_from_array [lrange $ret 88  95]]
    

    set_target $blade

    set array vals


    puts "Profile #$profile:"
    puts ""
    puts "    Received Statistics"
    puts "    -------------------"
    disp_hdr
    disp_stat "Rx Bytes" $rxbytes $rxbytes_tot
    set vals(RX_BYTES_CURRENT)    $rxbytes
    set vals(RX_BYTES_CUMULATIVE) $rxbytes_tot

    disp_stat "Rx Packets" $rxpkts $rxpkts_tot
    set vals(RX_PACKETS_CURRENT)    $rxpkts
    set vals(RX_PACKETS_CUMULATIVE) $rxpkts_tot

    disp_rate "Rx Bytes/sec" $rxbyterate $rxbyterate_tot
    set vals(RX_BYTES_PER_SEC_CURRENT)    $rxbyterate
    set vals(RX_BYTES_PER_SEC_CUMULATIVE) $rxbyterate_tot

    disp_rate "Rx Packets/sec" $rxpktrate $rxpktrate_tot
    set vals(RX_PACKETS_PER_SEC_CURRENT)    $rxpktrate
    set vals(RX_PACKETS_PER_SEC_CUMULATIVE) $rxpktrate_tot

    disp_stat "CRC Errors" $rxcrc $rxcrc_tot
    set vals(RX_CRC_ERRORS_CURRENT)    $rxcrc
    set vals(RX_CRC_ERRORS_CUMULATIVE) $rxcrc_tot


    puts ""
    puts ""
    puts "    Transmit Statistics"
    puts "    -------------------"
    disp_hdr
    disp_stat "Tx Bytes" $txbytes $txbytes_tot
    set vals(TX_BYTES_CURRENT)    $txbytes
    set vals(TX_BYTES_CUMULATIVE) $txbytes_tot

    disp_stat "Tx Packets" $txpkts $txpkts_tot
    set vals(TX_PACKETS_CURRENT)    $txpkts
    set vals(TX_PACKETS_CUMULATIVE) $txpkts_tot

    disp_rate "Tx Bytes/sec" $txbyterate $txbyterate_tot
    set vals(TX_BYTES_PER_SEC_CURRENT)    $txbyterate
    set vals(TX_BYTES_PER_SEC_CUMULATIVE) $txbyterate_tot

    disp_rate "Tx Packets/sec" $txpktrate $txpktrate_tot
    set vals(TX_PACKETS_PER_SEC_CURRENT)    $txpktrate
    set vals(TX_PACKETS_PER_SEC_CUMULATIVE) $txpktrate_tot

    disp_stat "CRC Errors" $txcrc $txcrc_tot
    set vals(TX_CRC_ERRORS_CURRENT)    $txcrc
    set vals(TX_CRC_ERRORS_CUMULATIVE) $txcrc_tot


    puts ""
    puts ""
    puts "    Policer Statistics"
    puts "    ------------------"
    disp_hdr
    disp_stat "Green (Bytes)" $polbgreen $polbgreen_tot
    set vals(GREEN_BYTES_CURRENT)    $polbgreen
    set vals(GREEN_BYTES_CUMULATIVE) $polbgreen_tot

    disp_stat "Green (Packets)" $polpgreen $polpgreen_tot
    set vals(GREEN_PACKETS_CURRENT)    $polpgreen
    set vals(GREEN_PACKETS_CUMULATIVE) $polpgreen_tot

    disp_stat "Yellow (Bytes)" $polbyellow $polbyellow_tot
    set vals(YELLOW_BYTES_CURRENT)    $polbyellow
    set vals(YELLOW_BYTES_CUMULATIVE) $polbyellow_tot

    disp_stat "Yellow (Packets)" $polpyellow $polpyellow_tot
    set vals(YELLOW_PACKETS_CURRENT)    $polpyellow
    set vals(YELLOW_PACKETS_CUMULATIVE) $polpyellow_tot

    disp_stat "Red (Bytes)" $polbred $polbred_tot
    set vals(RED_BYTES_CURRENT)    $polbred
    set vals(RED_BYTES_CUMULATIVE) $polbred_tot

    disp_stat "Red (Packets)" $polpred $polpred_tot
    set vals(RED_PACKETS_CURRENT)    $polpred
    set vals(RED_PACKETS_CUMULATIVE) $polpred_tot

                
    puts ""
    puts ""
    puts "    Impairment Statistics"
    puts "    ---------------------"
    disp_hdr
    disp_stat "Bytes Dropped" $impbdrop $impbdrop_tot
    set vals(IMP_BYTES_DROPPED_CURRENT)    $impbdrop
    set vals(IMP_BYTES_DROPPED_CUMULATIVE) $impbdrop_tot

    disp_stat "Packets Dropped" $imppdrop $imppdrop_tot
    set vals(IMP_PACKETS_DROPPED_CURRENT)    $imppdrop
    set vals(IMP_PACKETS_DROPPED_CUMULATIVE) $imppdrop_tot

    disp_stat "Bytes Corrupted" $impbcrpt $impbcrpt_tot
    set vals(IMP_BYTES_CORRUPTED_CURRENT)    $impbcrpt
    set vals(IMP_BYTES_CORRUPTED_CUMULATIVE) $impbcrpt_tot

    disp_stat "Packets Corrupted" $imppcrpt $imppcrpt_tot
    set vals(IMP_PACKETS_CORRUPTED_CURRENT)    $imppcrpt
    set vals(IMP_PACKETS_CORRUPTED_CUMULATIVE) $imppcrpt_tot

    disp_stat "Packets Reordered" $impreord $impreord_tot
    set vals(IMP_PACKETS_REORDERED_CURRENT)    $impreord
    set vals(IMP_PACKETS_REORDERED_CUMULATIVE) $impreord_tot

    disp_stat "Packets Duplicated" $impdupe $impdupe_tot
    set vals(IMP_PACKETS_DUPLICATED_CURRENT)    $impdupe
    set vals(IMP_PACKETS_DUPLICATED_CUMULATIVE) $impdupe_tot

    disp_stat "CRCs Corrupted" $impcrc $impcrc_tot
    set vals(IMP_CRC_CORRUPTED_CURRENT)    $impcrc
    set vals(IMP_CRC_CORRUPTED_CUMULATIVE) $impcrc_tot

    disp_stat "Packets Modified" $impmodpkts $impmodpkts_tot
    set vals(IMP_PACKETS_MODIFIED_CURRENT)    $impmodpkts
    set vals(IMP_PACKETS_MODIFIED_CUMULATIVE) $impmodpkts_tot

    disp_stat "Bits Modified" $impmodbits $impmodbits_tot
    set vals(IMP_BITS_MODIFIED_CURRENT)    $impmodbits
    set vals(IMP_BITS_MODIFIED_CUMULATIVE) $impmodbits_tot


    puts ""
    puts ""
    puts "    Overflow Statistics"
    puts "    -------------------"
    disp_hdr
    disp_stat "Packets Dropped" $ofpkts $ofpkts_tot
    set vals(OF_PACKETS_DROPPED_CURRENT)    $ofpkts
    set vals(OF_PACKETS_DROPPED_CUMULATIVE) $ofpkts_tot

    disp_stat "Bytes Dropped" $ofbytes $ofbytes_tot
    set vals(OF_BYTES_DROPPED_CURRENT)    $ofbytes
    set vals(OF_BYTES_DROPPED_CUMULATIVE) $ofbytes_tot


    puts ""
    puts ""
    puts "    Delay Statistics"
    puts "    ----------------"
    disp_hdr2
    set mindelay_in_units     [delay_convert $mindelay "words" $units]
    set mindelay_tot_in_units [delay_convert $mindelay_tot "words" $units]
    disp_stat2 "Minimum Delay" $mindelay_in_units $mindelay_tot_in_units $units
    set vals(MIN_DELAY_CURRENT)    [lindex $mindelay_in_units 0]
    set vals(MIN_DELAY_CUMULATIVE) [lindex $mindelay_tot_in_units 0]

    set maxdelay_in_units     [delay_convert $maxdelay "words" $units]
    set maxdelay_tot_in_units [delay_convert $maxdelay_tot "words" $units]
    disp_stat2 "Maximum Delay" $maxdelay_in_units $maxdelay_tot_in_units $units
    set vals(MAX_DELAY_CURRENT)    [lindex $maxdelay_in_units 0]
    set vals(MAX_DELAY_CUMULATIVE) [lindex $maxdelay_tot_in_units 0]

    set avgdelay_in_units     [delay_convert $avgdelay "words" $units]
    set avgdelay_tot_in_units [delay_convert $avgdelay_tot "words" $units]
    disp_stat2 "Average Delay" $avgdelay_in_units $avgdelay_tot_in_units $units
    set vals(AVG_DELAY_CURRENT)    [lindex $avgdelay_in_units 0]
    set vals(AVG_DELAY_CUMULATIVE) [lindex $avgdelay_tot_in_units 0]


    puts ""
    puts ""
    puts "    IPv4 Fragment Statistics"
    puts "    ------------------------"
    disp_hdr
    disp_stat "Packets Selected" $ipfpkts $ipfpkts_tot
    set vals(IPFRAG_PKTS_SELECTED_CURRENT)    $ipfpkts
    set vals(IPFRAG_PKTS_SELECTED_CUMULATIVE) $ipfpkts_tot

    disp_stat "Packets Fragmented" $ipfpktsfd $ipfpktsfd_tot
    set vals(IPFRAG_PKTS_FRAGMENTED_CURRENT)    $ipfpktsfd
    set vals(IPFRAG_PKTS_FRAGMENTED_CUMULATIVE) $ipfpktsfd_tot

    disp_stat "Fragments Sent" $ipffrags $ipffrags_tot
    set vals(IPFRAG_FRAGMENTS_SENT_CURRENT)    $ipffrags
    set vals(IPFRAG_FRAGMENTS_SENT_CUMULATIVE) $ipffrags_tot

    disp_stat "DNF Packets Dropped" $ipfdrops $ipfdrops_tot
    set vals(IPFRAG_DNF_PKTS_DROPPED_CURRENT)    $ipfdrops
    set vals(IPFRAG_DNF_PKTS_DROPPED_CUMULATIVE) $ipfdrops_tot



# Comment out Mantis 1590
#    puts ""
#    puts ""
#    puts "    Scheduler & Shaper Statistics"
#    puts "    -----------------------------"
#    disp_hdr2
#    disp_stat2 "Avg Scheduling Delay" [sched_shape_convert $avgscheddelay $txpkts] \
#                               [sched_shape_convert $avgscheddelay_tot $txpkts_tot] \
#                              "ms"                              
#    disp_stat2 "Avg Shaping Delay" [sched_shape_convert $avgshapdelay $txpkts] \
#                               [sched_shape_convert $avgshapdelay_tot $txpkts_tot] \
#                               "ms"

    puts ""
    puts "Elapsed time since last reset: $tot_time seconds"
    set vals(SECS_SINCE_RESET) $tot_time

    return [array get vals]
}

######################################################################
# Function Name    : sched_shape_convert
# Parameters       : del txpkts
# Return Value     : converted average value
# Purpose          : Converts the scheduler and shaping statistics to
#                  : an average in milliseconds. See the description
#                  : in the gem.reg.vpp file for Average_Shaping_Delay_Count
#                  : and Average_Scheduling_Delay_Count
######################################################################
proc sched_shape_convert {del txpkts} {
    # Convert to milliseconds
    set del [expr $del / 140000.0]
    # do average, divide by packet count if non-zero
    if {($txpkts != 0)} {
        set del [expr $del / $txpkts]
    }
    return $del
}
######################################################################
# Function Name    : gem_show_individual_profile_stat
#                  :
# Parameters       : profile - the profile number
#                  : name - the name of the stat to return:
#                  :
#                  :   (All stats are in the last second, except those
#                  :    with a _tot suffix, which means since last stats
#                  :    reset.)
#                  :
#                  :   rxbytes - Bytes received.
#                  :   rxbytes_tot
#                  :   rxpkts - Pkts received.
#                  :   rxpkts_tot
#                  :   rxbyterate - Bytes received rate.
#                  :   rxbyterate_tot
#                  :   rxpktrate - Pkt receive rate.
#                  :   rxpktrate_tot
#                  :   rxcrc - Incoming CRC errors.
#                  :   rxcrc_tot
#                  :
#                  :   txbytes - Bytes transmitted.
#                  :   txbytes_tot 
#                  :   txpkts - Packets transmitted.
#                  :   txpkts_tot
#                  :   txbyterate - Bytes transmitted rate.
#                  :   txbyterate_tot
#                  :   txpktrate - Packets transmitted rate.
#                  :   txpktrate_tot
#                  :   txcrc - Outgoing CRC errors.
#                  :   txcrc_tot 
#                 
#                  :   greenbytes - # of 'green' bytes.
#                  :   greenbytes_tot 
#                  :   greenpkts - # of 'green' packets.
#                  :   greenpkts_tot 
#                  :   yellowbytes - # of 'yellow' bytes.
#                  :   yellowbytes_tot 
#                  :   yellowpkts - # of 'yellow' packets.
#                  :   yellowpkts_tot 
#                  :   redbytes - # of 'red' bytes.
#                  :   redbytes_tot 
#                  :   redpkts - # of 'red' packets.
#                  :   redpkts_tot 
#                 
#                  :   dropbytes - # of dropped bytes due to impairment.
#                  :   dropbytes_tot
#                  :   droppkts - # of dropped packets due to impairment.
#                  :   droppkts_tot
#                  :   bcrpt - # of corrupted bytes due to impairment.
#                  :   bcrpt_tot
#                  :   pcrptpkts - # of corrupted packets due to impairment.
#                  :   pcrptpkts_tot
#                  :   reordpkts - # of reordered packets due to impairment.
#                  :   reordpkts_tot
#                  :   dupepkts - # of duplicated packets due to impairment.
#                  :   dupepkts_tot
#                  :   crccorrpkts - # of crc corrupted pkts due to impairment.
#                  :   crccorrpkts_tot 
#                  :   modpkts - # of modified packets due to impairment.
#                  :   modpkts_tot
#                  :   modbits - # of modified bits due to impairment.
#                  :   modbits_tot
#                 
#                  :   tot_time - total time gathering stats since last
#                  :              stats reset (in seconds)
#                 
#                  :   ofpkts - # of packets dropped due to overflow
#                  :   ofpkts_tot
#                  :   ofbytes - # of bytes dropped due to overflow
#                  :   ofbytes_tot
#                 
#                 
#                  :   mindelay - minimum delay in units specified
#                  :   mindelay_tot
#                  :   maxdelay - maximum delay in units specified
#                  :   maxdelay_tot
#                  :   avgdelay - average delay in units specified
#                  :   avgdelay_tot
#                  :
#                  :   ipfpkts - number of packets selected for ipv4 fragment
#                  :   ipfpkts_tot
#                  :   ipfpktsfd - actual number of packets fragmented
#                  :   ipfpktsfd_tot
#                  :   ipffrags - number of fragments generated
#                  :   ipffrags_tot
#                  :   ipfdrops - number of packets dropped due to honoring
#                  :              the don't fragment flag
#                  :   ipfdrops_tot
#                  :
#                  : force_load - either "-no_load" or "-load"
#                  :              if "-no_load is specified, a cached
#                  :              value is returned from the last time
#                  :              the stats were retrieved from the box.
#                  :              (This is the default.)  Otherwise,
#                  :              the stats are loaded from the box, and
#                  :              the cache is refilled.
#                  :
# Purpose          : Display a statistic for a specific network profile.
######################################################################
proc gem_show_individual_profile_stat {profile name {force_load "-no_load"} {units "ms"}} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES
    global PSTAT_CACHE

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR

    set b $blade
    set p $profile

    if {[string compare $force_load "-no_load"] == 0 &&
        [info exists PSTAT_CACHE($b,$p,$name)] != 0} \
    {
        set val $PSTAT_CACHE($b,$p,$name)
        if {[string compare $name "mindelay"] == 0 || 
            [string compare $name "maxdelay"] == 0 ||
            [string compare $name "avgdelay"] == 0 ||
            [string compare $name "mindelay_tot"] == 0 || 
            [string compare $name "maxdelay_tot"] == 0 ||
            [string compare $name "avgdelay_tot"] == 0} \
        {
            set val [delay_convert $val "words" $units]
        }
        return $val
    }

    set_target 0

    send_command [BuildCommand 0xF5 2 $blade $profile]
    set ret [lrange [pong] 4 end]

  set PSTAT_CACHE($b,$p,rxbytes)        [value_from_array [lrange $ret 0  3 ]]
  set PSTAT_CACHE($b,$p,rxbytes_tot)    [value_from_array [lrange $ret 4  11]]
  set PSTAT_CACHE($b,$p,rxpkts)         [value_from_array [lrange $ret 12 15]]
  set PSTAT_CACHE($b,$p,rxpkts_tot)     [value_from_array [lrange $ret 16 23]]
  set PSTAT_CACHE($b,$p,rxbyterate)     [value_from_array [lrange $ret 24 27]]
  set PSTAT_CACHE($b,$p,rxbyterate_tot) [value_from_array [lrange $ret 28 31]]
  set PSTAT_CACHE($b,$p,rxpktrate)      [value_from_array [lrange $ret 32 35]]
  set PSTAT_CACHE($b,$p,rxpktrate_tot)  [value_from_array [lrange $ret 36 39]]
  set PSTAT_CACHE($b,$p,rxcrc)          [value_from_array [lrange $ret 40 43]]
  set PSTAT_CACHE($b,$p,rxcrc_tot)      [value_from_array [lrange $ret 44 51]]

  set PSTAT_CACHE($b,$p,txbytes)        [value_from_array [lrange $ret 52 55]]
  set PSTAT_CACHE($b,$p,txbytes_tot)    [value_from_array [lrange $ret 56 63]]
  set PSTAT_CACHE($b,$p,txpkts)         [value_from_array [lrange $ret 64 67]]
  set PSTAT_CACHE($b,$p,txpkts_tot)     [value_from_array [lrange $ret 68 75]]
  set PSTAT_CACHE($b,$p,txbyterate)     [value_from_array [lrange $ret 76 79]]
  set PSTAT_CACHE($b,$p,txbyterate_tot) [value_from_array [lrange $ret 80 83]]
  set PSTAT_CACHE($b,$p,txpktrate)      [value_from_array [lrange $ret 84 87]]
  set PSTAT_CACHE($b,$p,txpktrate_tot)  [value_from_array [lrange $ret 88 91]]
  set PSTAT_CACHE($b,$p,txcrc)          [value_from_array [lrange $ret 92 95]]
  set PSTAT_CACHE($b,$p,txcrc_tot)      [value_from_array [lrange $ret 96 103]]

  set PSTAT_CACHE($b,$p,greenbytes)     [value_from_array [lrange $ret 104 107]]
  set PSTAT_CACHE($b,$p,greenbytes_tot) [value_from_array [lrange $ret 108 115]]
  set PSTAT_CACHE($b,$p,greenpkts)      [value_from_array [lrange $ret 116 119]]
  set PSTAT_CACHE($b,$p,greenpkts_tot)  [value_from_array [lrange $ret 120 127]]
  set PSTAT_CACHE($b,$p,yellowbytes)    [value_from_array [lrange $ret 128 131]]
 set PSTAT_CACHE($b,$p,yellowbytes_tot) [value_from_array [lrange $ret 132 139]]
  set PSTAT_CACHE($b,$p,yellowpkts)     [value_from_array [lrange $ret 140 143]]
  set PSTAT_CACHE($b,$p,yellowpkts_tot) [value_from_array [lrange $ret 144 151]]
  set PSTAT_CACHE($b,$p,redbytes)       [value_from_array [lrange $ret 152 155]]
  set PSTAT_CACHE($b,$p,redbytes_tot)   [value_from_array [lrange $ret 156 163]]
  set PSTAT_CACHE($b,$p,redpkts)        [value_from_array [lrange $ret 164 167]]
  set PSTAT_CACHE($b,$p,redpkts_tot)    [value_from_array [lrange $ret 168 175]]

  set PSTAT_CACHE($b,$p,dropbytes)      [value_from_array [lrange $ret 176 179]]
  set PSTAT_CACHE($b,$p,dropbytes_tot)  [value_from_array [lrange $ret 180 185]]
  set PSTAT_CACHE($b,$p,droppkts)       [value_from_array [lrange $ret 186 189]]
  set PSTAT_CACHE($b,$p,droppkts_tot)   [value_from_array [lrange $ret 190 195]]
  set PSTAT_CACHE($b,$p,bcrpt)          [value_from_array [lrange $ret 196 199]]
  set PSTAT_CACHE($b,$p,bcrpt_tot)      [value_from_array [lrange $ret 200 205]]
  set PSTAT_CACHE($b,$p,pcrptpkts)      [value_from_array [lrange $ret 206 209]]
  set PSTAT_CACHE($b,$p,pcrptpkts_tot)  [value_from_array [lrange $ret 210 215]]
  set PSTAT_CACHE($b,$p,reordpkts)      [value_from_array [lrange $ret 216 219]]
  set PSTAT_CACHE($b,$p,reordpkts_tot)  [value_from_array [lrange $ret 220 225]]
  set PSTAT_CACHE($b,$p,dupepkts)       [value_from_array [lrange $ret 226 229]]
  set PSTAT_CACHE($b,$p,dupepkts_tot)   [value_from_array [lrange $ret 230 235]]
  set PSTAT_CACHE($b,$p,crccorrpkts)    [value_from_array [lrange $ret 236 239]]
 set PSTAT_CACHE($b,$p,crccorrpkts_tot) [value_from_array [lrange $ret 240 245]]

  set PSTAT_CACHE($b,$p,tot_time)       [value_from_array [lrange $ret 246 249]]

  send_command [BuildCommand 0x6E 2 $blade $profile]
  set ret [lrange [pong] 4 end]

  set PSTAT_CACHE($b,$p,ofpkts)         [value_from_array [lrange $ret 0  3 ]]
  set PSTAT_CACHE($b,$p,ofpkts_tot)     [value_from_array [lrange $ret 4  11]]
  set PSTAT_CACHE($b,$p,ofbytes)        [value_from_array [lrange $ret 12  15]]
  set PSTAT_CACHE($b,$p,ofbytes_tot)    [value_from_array [lrange $ret 16  23]]

  set PSTAT_CACHE($b,$p,modpkts)     [value_from_array [lrange $ret 24  27 ]]
  set PSTAT_CACHE($b,$p,modpkts_tot) [value_from_array [lrange $ret 28  35]]
  set PSTAT_CACHE($b,$p,modbits)     [value_from_array [lrange $ret 36  39]]
  set PSTAT_CACHE($b,$p,modbits_tot) [value_from_array [lrange $ret 40  47]]

  set PSTAT_CACHE($b,$p,mindelay)       [value_from_array [lrange $ret 48  51]]
  set PSTAT_CACHE($b,$p,maxdelay)       [value_from_array [lrange $ret 52  55]]
  set PSTAT_CACHE($b,$p,avgdelay)       [value_from_array [lrange $ret 56  59]]

  set PSTAT_CACHE($b,$p,mindelay_tot)   [value_from_array [lrange $ret 60  63]]
  set PSTAT_CACHE($b,$p,maxdelay_tot)   [value_from_array [lrange $ret 64  67]]
  set PSTAT_CACHE($b,$p,avgdelay_tot)   [value_from_array [lrange $ret 68  71]]

  set PSTAT_CACHE($b,$p,ipfpkts)        [value_from_array [lrange $ret 72  75]]
  set PSTAT_CACHE($b,$p,ipfpkts_tot)    [value_from_array [lrange $ret 76  83]]

  set PSTAT_CACHE($b,$p,ipfpktsfd)      [value_from_array [lrange $ret 84  87]]
  set PSTAT_CACHE($b,$p,ipfpktsfd_tot)  [value_from_array [lrange $ret 88  95]]

  set PSTAT_CACHE($b,$p,ipffrags)       [value_from_array [lrange $ret 96  99]]
  set PSTAT_CACHE($b,$p,ipffrags_tot)   [value_from_array [lrange $ret 100 107]]

  set PSTAT_CACHE($b,$p,ipfdrops)       [value_from_array [lrange $ret 108 111]]
  set PSTAT_CACHE($b,$p,ipfdrops_tot)   [value_from_array [lrange $ret 112 119]]

  set PSTAT_CACHE($b,$p,rxbyterate) [expr $PSTAT_CACHE($b,$p,rxbyterate)/100.0]
  set PSTAT_CACHE($b,$p,rxpktrate) [expr $PSTAT_CACHE($b,$p,rxpktrate)/100.0]
  set PSTAT_CACHE($b,$p,txbyterate) [expr $PSTAT_CACHE($b,$p,txbyterate)/100.0]
  set PSTAT_CACHE($b,$p,txpktrate) [expr $PSTAT_CACHE($b,$p,txpktrate)/100.0]
  set PSTAT_CACHE($b,$p,rxbyterate_tot) [expr $PSTAT_CACHE($b,$p,rxbyterate_tot)/100.0]
  set PSTAT_CACHE($b,$p,rxpktrate_tot) [expr $PSTAT_CACHE($b,$p,rxpktrate_tot)/100.0]
  set PSTAT_CACHE($b,$p,txbyterate_tot) [expr $PSTAT_CACHE($b,$p,txbyterate_tot)/100.0]
  set PSTAT_CACHE($b,$p,txpktrate_tot) [expr $PSTAT_CACHE($b,$p,txpktrate_tot)/100.0]

  set_target $blade

  set val $PSTAT_CACHE($b,$p,$name)
  if {[string compare $name "mindelay"] == 0 || 
      [string compare $name "maxdelay"] == 0 ||
      [string compare $name "avgdelay"] == 0 ||
      [string compare $name "mindelay_tot"] == 0 || 
      [string compare $name "maxdelay_tot"] == 0 ||
      [string compare $name "avgdelay_tot"] == 0} \
  {
      set val [delay_convert $val "words" $units]
  }
  return $val
}

######################################################################
# Function Name    : gem_show_individual_line_stat
#                  :
# Parameters       : name - the name of the stat to return:
#                  :
#                  :   (All stats are in the last second, except those
#                  :    with a _tot suffix, which means since last stats
#                  :    reset.)
#                  :
#                  :  rxbytes - Bytes received.
#                  :  rxbytes_tot
#                  :  rxpkts - Packets received.
#                  :  rxpkts_tot
#                  :  rxbyterate - Bytes received rate.
#                  :  rxbyterate_tot
#                  :  rxpktrate - Packets received rate.
#                  :  rxpktrate_tot
#                  :  rxidle - Idle errors received.
#                  :  rxidle_tot
#                  :  rxfrm - Framing errors received.
#                  :  rxfrm_tot
#                  :  rxcrc - CRC errors received.
#                  :  rxcrc_tot
#                  :  rxdisp - Disparity errors received.
#                  :  rxdisp_tot
#                  :  rxcw - Codeword errors received.
#                  :  rxcw_tot
#                  :  
#                  :  txbytes - Bytes transmitted.
#                  :  txbytes_tot
#                  :  txpkts - Packets transmitted.
#                  :  txpkts_tot
#                  :  txbyterate - Bytes transmitted rate.
#                  :  txbyterate_tot
#                  :  txpktrate - Packets transmitted rate.
#                  :  txpktrate_tot
#                  :  txdisp - Disparity errors transmitted.
#                  :  txdisp_tot
#                  :  txcw - Codeword errors transmitted.
#                  :  txcw_tot
#                  :  
#                  :  rxbw_bytesdrop - Bytes dropped due to Rx Throttle
#                  :  rxbw_bytesdrop_tot
#                  :  rxbw_pktsdrop - Packets dropped due to Rx Throttle
#                  :  rxbw_pktsdrop_tot 
#                  :  txbw_pframecnt - Pause frames sent
#                  :  txbw_pframecnt_tot
#
#                  :  tot_time - total time gathering stats since last
#                  :              stats reset (in seconds)
#                  :  
#                  : force_load - either "-no_load" or "-load"
#                  :              if "-no_load is specified, a cached
#                  :              value is returned from the last time
#                  :              the stats were retrieved from the box.
#                  :              (This is the default.)  Otherwise,
#                  :              the stats are loaded from the box, and
#                  :              the cache is refilled.
#                  :  
# Purpose          : Display a PHY/MAC statistic for the line.
######################################################################
proc gem_show_individual_line_stat {name {force_load "-no_load"}} {
    global TX_DEST_ADDR
    global LSTAT_CACHE

    set b $TX_DEST_ADDR

    if {[string compare $force_load "-no_load"] == 0 &&
        [info exists LSTAT_CACHE($b,$name)] != 0} \
    {
            return $LSTAT_CACHE($b,$name)
    }

    set_target 0

    send_command [BuildCommand 0xF6 1 $b]
    set ret [lrange [pong] 3 end]

    set_target $b

    set LSTAT_CACHE($b,rxbytes)        [value_from_array [lrange $ret 0  3 ]]
    set LSTAT_CACHE($b,rxbytes_tot)    [value_from_array [lrange $ret 4  11]]
    set LSTAT_CACHE($b,rxpkts)         [value_from_array [lrange $ret 12 15]]
    set LSTAT_CACHE($b,rxpkts_tot)     [value_from_array [lrange $ret 16 23]]
    set LSTAT_CACHE($b,rxbyterate)     [value_from_array [lrange $ret 24 27]]
    set LSTAT_CACHE($b,rxbyterate_tot) [value_from_array [lrange $ret 28 31]]
    set LSTAT_CACHE($b,rxpktrate)      [value_from_array [lrange $ret 32 35]]
    set LSTAT_CACHE($b,rxpktrate_tot)  [value_from_array [lrange $ret 36 39]]
    set LSTAT_CACHE($b,rxidle)         [value_from_array [lrange $ret 40 43]]
    set LSTAT_CACHE($b,rxidle_tot)     [value_from_array [lrange $ret 44 51]]
    set LSTAT_CACHE($b,rxfrm)          [value_from_array [lrange $ret 52 55]]
    set LSTAT_CACHE($b,rxfrm_tot)      [value_from_array [lrange $ret 56 63]]
    set LSTAT_CACHE($b,rxcrc)          [value_from_array [lrange $ret 64 67]]
    set LSTAT_CACHE($b,rxcrc_tot)      [value_from_array [lrange $ret 68 75]]
    set LSTAT_CACHE($b,rxdisp)         [value_from_array [lrange $ret 76 79]]
    set LSTAT_CACHE($b,rxdisp_tot)     [value_from_array [lrange $ret 80 87]]
    set LSTAT_CACHE($b,rxcw)           [value_from_array [lrange $ret 88 91]]
    set LSTAT_CACHE($b,rxcw_tot)       [value_from_array [lrange $ret 92 99]]

    set LSTAT_CACHE($b,txbytes)        [value_from_array [lrange $ret 100 103]]
    set LSTAT_CACHE($b,txbytes_tot)    [value_from_array [lrange $ret 104 111]]
    set LSTAT_CACHE($b,txpkts)         [value_from_array [lrange $ret 112 115]]
    set LSTAT_CACHE($b,txpkts_tot)     [value_from_array [lrange $ret 116 123]]
    set LSTAT_CACHE($b,txbyterate)     [value_from_array [lrange $ret 124 127]]
    set LSTAT_CACHE($b,txbyterate_tot) [value_from_array [lrange $ret 128 131]]
    set LSTAT_CACHE($b,txpktrate)      [value_from_array [lrange $ret 132 135]]
    set LSTAT_CACHE($b,txpktrate_tot)  [value_from_array [lrange $ret 136 139]]
    set LSTAT_CACHE($b,txdisp)         [value_from_array [lrange $ret 140 143]]
    set LSTAT_CACHE($b,txdisp_tot)     [value_from_array [lrange $ret 144 151]]
    set LSTAT_CACHE($b,txcw)           [value_from_array [lrange $ret 152 155]]
    set LSTAT_CACHE($b,txcw_tot)       [value_from_array [lrange $ret 156 163]]

    set LSTAT_CACHE($b,tot_time)       [value_from_array [lrange $ret 164 167]]

 set LSTAT_CACHE($b,rxbw_bytesdrop) [value_from_array [lrange $ret 168 171]]
 set LSTAT_CACHE($b,rxbw_bytesdrop_tot) [value_from_array [lrange $ret 172 179]]
 set LSTAT_CACHE($b,rxbw_pktsdrop) [value_from_array [lrange $ret 180 183]]
 set LSTAT_CACHE($b,rxbw_pktsdrop_tot) [value_from_array [lrange $ret 184 191]]
 set LSTAT_CACHE($b,rxbw_onframes) [value_from_array [lrange $ret 192 195]]
 set LSTAT_CACHE($b,rxbw_onframes_tot) [value_from_array [lrange $ret 196 203]]
 set LSTAT_CACHE($b,rxbw_offframes) [value_from_array [lrange $ret 204 207]]
 set LSTAT_CACHE($b,rxbw_offframes_tot) [value_from_array [lrange $ret 208 215]]

  set LSTAT_CACHE($b,txbw_pframecnt)  \
          [expr $LSTAT_CACHE($b,rxbw_onframes) + \
                $LSTAT_CACHE($b,rxbw_offframes)]

  set LSTAT_CACHE($b,txbw_pframecnt_tot)  \
          [expr $LSTAT_CACHE($b,rxbw_onframes_tot) + \
                $LSTAT_CACHE($b,rxbw_offframes_tot)]

  set LSTAT_CACHE($b,rxbyterate)     [expr $LSTAT_CACHE($b,rxbyterate)/100.0]
  set LSTAT_CACHE($b,rxpktrate)      [expr $LSTAT_CACHE($b,rxpktrate)/100.0]
  set LSTAT_CACHE($b,txbyterate)     [expr $LSTAT_CACHE($b,txbyterate)/100.0]
  set LSTAT_CACHE($b,txpktrate)      [expr $LSTAT_CACHE($b,txpktrate)/100.0]
  set LSTAT_CACHE($b,rxbyterate_tot) [expr $LSTAT_CACHE($b,rxbyterate_tot)/100.0]
  set LSTAT_CACHE($b,rxpktrate_tot)  [expr $LSTAT_CACHE($b,rxpktrate_tot)/100.0]
  set LSTAT_CACHE($b,txbyterate_tot) [expr $LSTAT_CACHE($b,txbyterate_tot)/100.0]
  set LSTAT_CACHE($b,txpktrate_tot)  [expr $LSTAT_CACHE($b,txpktrate_tot)/100.0]

    return $LSTAT_CACHE($b,$name)
}

######################################################################
# Function Name    : gem_show_line_stats
#                  :
# Returns          : An associative array indexed by the following keys:
#                  :
#                  :    RX_BYTES_CURRENT
#                  :    RX_BYTES_CUMULATIVE
#                  :    RX_PACKETS_CURRENT
#                  :    RX_PACKETS_CUMULATIVE
#                  :    RX_BYTES_PER_SEC_CURRENT
#                  :    RX_BYTES_PER_SEC_CUMULATIVE
#                  :    RX_PACKETS_PER_SEC_CURRENT
#                  :    RX_PACKETS_PER_SEC_CUMULATIVE
#                  :    IDLE_ERRORS_CURRENT
#                  :    IDLE_ERRORS_CUMULATIVE
#                  :    FRAMING_ERRORS_CURRENT
#                  :    FRAMING_ERRORS_CUMULATIVE
#                  :    CRC_ERRORS_CURRENT
#                  :    CRC_ERRORS_CUMULATIVE
#                  :    RX_DISPARITY_ERRORS_CURRENT
#                  :    RX_DISPARITY_ERRORS_CUMULATIVE
#                  :    RX_CODEWORD_ERRORS_CURRENT
#                  :    RX_CODEWORD_ERRORS_CUMULATIVE
#                  :    TX_BYTES_CURRENT
#                  :    TX_BYTES_CUMULATIVE
#                  :    TX_PACKETS_CURRENT
#                  :    TX_PACKETS_CUMULATIVE
#                  :    TX_BYTES_PER_SEC_CURRENT
#                  :    TX_BYTES_PER_SEC_CUMULATIVE
#                  :    TX_PACKETS_PER_SEC_CURRENT
#                  :    TX_PACKETS_PER_SEC_CUMULATIVE
#                  :    TX_DISPARITY_ERRORS_CURRENT
#                  :    TX_DISPARITY_ERRORS_CUMULATIVE
#                  :    TX_CODEWORD_ERRORS_CURRENT
#                  :    TX_CODEWORD_ERRORS_CUMULATIVE
#                  :    BW_BYTES_DROPPED_CURRENT
#                  :    BW_BYTES_DROPPED_CUMULATIVE
#                  :    BW_PACKETS_DROPPED_CURRENT
#                  :    BW_PACKETS_DROPPED_CUMULATIVE
#                  :    TX_PAUSE_FRAMES_CURRENT
#                  :    TX_PAUSE_FRAMES_CUMULATIVE
#                  :    SECS_SINCE_RESET
#                  :
# Purpose          : Display the PHY/MAC statistics for the line.
######################################################################
proc gem_show_line_stats {} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xF6 1 $blade]
    set ret [lrange [pong] 3 end]

    set_target $blade

    set rxbytes        [value_from_array [lrange $ret 0  3 ]]
    set rxbytes_tot    [value_from_array [lrange $ret 4  11]]
    set rxpkts         [value_from_array [lrange $ret 12 15]]
    set rxpkts_tot     [value_from_array [lrange $ret 16 23]]
    set rxbyterate     [value_from_array [lrange $ret 24 27]]
    set rxbyterate_tot [value_from_array [lrange $ret 28 31]]
    set rxpktrate      [value_from_array [lrange $ret 32 35]]
    set rxpktrate_tot  [value_from_array [lrange $ret 36 39]]
    set rxidle         [value_from_array [lrange $ret 40 43]]
    set rxidle_tot     [value_from_array [lrange $ret 44 51]]
    set rxfrm          [value_from_array [lrange $ret 52 55]]
    set rxfrm_tot      [value_from_array [lrange $ret 56 63]]
    set rxcrc          [value_from_array [lrange $ret 64 67]]
    set rxcrc_tot      [value_from_array [lrange $ret 68 75]]
    set rxdisp         [value_from_array [lrange $ret 76 79]]
    set rxdisp_tot     [value_from_array [lrange $ret 80 87]]
    set rxcw           [value_from_array [lrange $ret 88 91]]
    set rxcw_tot       [value_from_array [lrange $ret 92 99]]

    set txbytes        [value_from_array [lrange $ret 100 103]]
    set txbytes_tot    [value_from_array [lrange $ret 104 111]]
    set txpkts         [value_from_array [lrange $ret 112 115]]
    set txpkts_tot     [value_from_array [lrange $ret 116 123]]
    set txbyterate     [value_from_array [lrange $ret 124 127]]
    set txbyterate_tot [value_from_array [lrange $ret 128 131]]
    set txpktrate      [value_from_array [lrange $ret 132 135]]
    set txpktrate_tot  [value_from_array [lrange $ret 136 139]]
    set txdisp         [value_from_array [lrange $ret 140 143]]
    set txdisp_tot     [value_from_array [lrange $ret 144 151]]
    set txcw           [value_from_array [lrange $ret 152 155]]
    set txcw_tot       [value_from_array [lrange $ret 156 163]]

    set tot_time       [value_from_array [lrange $ret 164 167]]

    set rxbw_bytesdrop [value_from_array [lrange $ret 168 171]]
    set rxbw_bytesdrop_tot [value_from_array [lrange $ret 172 179]]

    set rxbw_pktsdrop [value_from_array [lrange $ret 180 183]]
    set rxbw_pktsdrop_tot [value_from_array [lrange $ret 184 191]]

    set rxbw_onframes [value_from_array [lrange $ret 192 195]]
    set rxbw_onframes_tot [value_from_array [lrange $ret 196 203]]

    set rxbw_offframes [value_from_array [lrange $ret 204 207]]
    set rxbw_offframes_tot [value_from_array [lrange $ret 208 215]]

    set array vals

    puts ""
    puts "    Received Statistics"
    puts "    -------------------"
    disp_hdr
    disp_stat "Rx Bytes" $rxbytes $rxbytes_tot
    set vals(RX_BYTES_CURRENT)    $rxbytes
    set vals(RX_BYTES_CUMULATIVE) $rxbytes_tot

    disp_stat "Rx Packets" $rxpkts $rxpkts_tot
    set vals(RX_PACKETS_CURRENT)    $rxpkts
    set vals(RX_PACKETS_CUMULATIVE) $rxpkts_tot

    disp_rate "Rx Bytes/sec" $rxbyterate $rxbyterate_tot
    set vals(RX_BYTES_PER_SEC_CURRENT)    $rxbyterate
    set vals(RX_BYTES_PER_SEC_CUMULATIVE) $rxbyterate_tot

    disp_rate "Rx Packets/sec" $rxpktrate $rxpktrate_tot
    set vals(RX_PACKETS_PER_SEC_CURRENT)    $rxpktrate
    set vals(RX_PACKETS_PER_SEC_CUMULATIVE) $rxpktrate_tot

    disp_stat "Idle Errors" $rxidle $rxidle_tot
    set vals(IDLE_ERRORS_CURRENT)    $rxidle
    set vals(IDLE_ERRORS_CUMULATIVE) $rxidle_tot

    disp_stat "Framing Errors" $rxfrm $rxfrm_tot
    set vals(FRAMING_ERRORS_CURRENT)    $rxfrm
    set vals(FRAMING_ERRORS_CUMULATIVE) $rxfrm_tot

    disp_stat "CRC Errors" $rxcrc $rxcrc_tot
    set vals(CRC_ERRORS_CURRENT)    $rxcrc
    set vals(CRC_ERRORS_CUMULATIVE) $rxcrc_tot

    disp_stat "Disparity Errors" $rxdisp $rxdisp_tot
    set vals(RX_DISPARITY_ERRORS_CURRENT)    $rxdisp
    set vals(RX_DISPARITY_ERRORS_CUMULATIVE) $rxdisp_tot

    disp_stat "Codeword Errors" $rxcw $rxcw_tot
    set vals(RX_CODEWORD_ERRORS_CURRENT)    $rxcw
    set vals(RX_CODEWORD_ERRORS_CUMULATIVE) $rxcw_tot


    puts ""
    puts ""
    puts "    Transmit Statistics"
    puts "    -------------------"
    disp_hdr
    disp_stat "Tx Bytes" $txbytes $txbytes_tot
    set vals(TX_BYTES_CURRENT)    $txbytes
    set vals(TX_BYTES_CUMULATIVE) $txbytes_tot

    disp_stat "Tx Packets" $txpkts $txpkts_tot
    set vals(TX_PACKETS_CURRENT)    $txpkts
    set vals(TX_PACKETS_CUMULATIVE) $txpkts_tot

    disp_rate "Tx Bytes/sec" $txbyterate $txbyterate_tot
    set vals(TX_BYTES_PER_SEC_CURRENT)    $txbyterate
    set vals(TX_BYTES_PER_SEC_CUMULATIVE) $txbyterate_tot

    disp_rate "Tx Packets/sec" $txpktrate $txpktrate_tot
    set vals(TX_PACKETS_PER_SEC_CURRENT)    $txpktrate
    set vals(TX_PACKETS_PER_SEC_CUMULATIVE) $txpktrate_tot

    disp_stat "Disparity Errors" $txdisp $txdisp_tot
    set vals(TX_DISPARITY_ERRORS_CURRENT)    $txdisp
    set vals(TX_DISPARITY_ERRORS_CUMULATIVE) $txdisp_tot

    disp_stat "Codeword Errors" $txcw $txcw_tot
    set vals(TX_CODEWORD_ERRORS_CURRENT)    $txcw
    set vals(TX_CODEWORD_ERRORS_CUMULATIVE) $txcw_tot


    puts ""
    puts ""
    puts "    Bandwidth Control Statistics"
    puts "    ----------------------------"
    disp_hdr
    disp_stat "Bytes Dropped" $rxbw_bytesdrop $rxbw_bytesdrop_tot
    set vals(BW_BYTES_DROPPED_CURRENT)    $rxbw_bytesdrop
    set vals(BW_BYTES_DROPPED_CUMULATIVE) $rxbw_bytesdrop_tot

    disp_stat "Packets Dropped" $rxbw_pktsdrop $rxbw_pktsdrop_tot
    set vals(BW_PACKETS_DROPPED_CURRENT)    $rxbw_pktsdrop
    set vals(BW_PACKETS_DROPPED_CUMULATIVE) $rxbw_pktsdrop_tot

    set txpauseframes [expr $rxbw_onframes + $rxbw_offframes]
    set txpauseframes_tot [expr $rxbw_onframes_tot + $rxbw_offframes_tot]

    disp_stat "Tx Pause Frame Count" $txpauseframes $txpauseframes_tot
    set vals(TX_PAUSE_FRAMES_CURRENT)    $txpauseframes
    set vals(TX_PAUSE_FRAMES_CUMULATIVE) $txpauseframes_tot

    puts ""
    puts "Elapsed time since last reset: $tot_time seconds"
    set vals(SECS_SINCE_RESET) $tot_time

    return [array get vals]
}

######################################################################
# Function Name    : gem_show_alarms
#                  :
# Returns          : An associative array indexed by the following keys:
#                  :
#                  :    OPTICS_PRESENT
#                  :    RX_LOS
#                  :    RX_LOL
#                  :    TX_LOL
#                  :    RX_CRC
#                  :    RX_LOF
#                  :    RX_RUNNING_DISPARITY
#                  :    RX_CODEWORD_ERRORS
#                  :
#                  :    OVERFLOW,n
#                  :    (where n is the profile number)
#                  :
#                  : Each array value is the current alarm state:
#                  :     <red|green|yellow>
#                  :
# Purpose          : Display the current alarms.
######################################################################
proc gem_show_alarms {} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xF9 1 $blade]
    set ret [lrange [pong] 3 end]

    set_target $blade

    set optics   [value_from_array [lindex $ret 0]]
    set rxlos    [value_from_array [lindex $ret 1]]
    set rxlol    [value_from_array [lindex $ret 2]]
    set txlol    [value_from_array [lindex $ret 3]]
    set rxcrc    [value_from_array [lindex $ret 4]]
    set rxfifo   [value_from_array [lindex $ret 5]]
    set rxcomma  [value_from_array [lindex $ret 6]]
    set rxrd     [value_from_array [lindex $ret 7]]
    set rxcw     [value_from_array [lindex $ret 8]]
    set rxoof    [value_from_array [lindex $ret 9]]
 
    set array vals

    disp_alarm "Optics Present" $optics
    set vals(OPTICS_PRESENT) [alarm_to_string $optics]

    disp_alarm "Rx LOS" $rxlos
    set vals(RX_LOS) [alarm_to_string $rxlos]

    disp_alarm "Rx LOL" $rxlol
    set vals(RX_LOL) [alarm_to_string $rxlol]

    disp_alarm "Tx LOL" $txlol
    set vals(TX_LOL) [alarm_to_string $txlol]

    disp_alarm "Rx CRC" $rxcrc
    set vals(RX_CRC) [alarm_to_string $rxcrc]

    disp_alarm "Rx LOF" $rxoof
    set vals(RX_LOF) [alarm_to_string $rxoof]

    disp_alarm "Rx Running Disparity" $rxrd
    set vals(RX_RUNNING_DISPARITY) [alarm_to_string $rxrd]

    disp_alarm "Rx Codeword Errors" $rxcw
    set vals(RX_CODEWORD_ERRORS) [alarm_to_string $rxcw]

    for {set q 0} {$q < $GEM_MAX_PROFILES} {incr q} {
        set q_alarm    [value_from_array [lindex $ret [expr 10 + $q]]]
        disp_alarm "Overflow Alarm for Queue #$q" $q_alarm
        set vals(OVERFLOW,$q) [alarm_to_string $q_alarm]
    }

    return [array get vals]
}

######################################################################
# Function Name    : gem_set_copper_link_up
# Parameters       : none
# Return Value     : none
# Purpose          : sets the link 'up' on a gem copper interface
######################################################################
proc gem_set_copper_link_up {} {
    global LASERCTL_NORM
    global TX_DEST_ADDR

    set_laserctl_mode $LASERCTL_NORM

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x4E 1 $blade]
    set ret [lrange [pong] 2 end]

    set_target $blade

    puts "gem_set_copper_link_up"
    set enabled [expr "0x[lindex $ret 1]" + 0]
    if {$enabled == 0} {
        gem_disable_autonegotiation
    } else {
        gem_enable_autonegotiation
    }
}

######################################################################
# Function Name    : gem_set_copper_link_down
# Parameters       : none
# Return Value     : none
# Purpose          : sets the link 'down' on a gem copper interface
######################################################################
proc gem_set_copper_link_down {} {
    global LASERCTL_LOS
    set_laserctl_mode $LASERCTL_LOS
    puts "gem_set_copper_link_down"
}

######################################################################
# Function Name    : gem_get_copper_link
# Parameters       : none
# Purpose          : gets whether current gem copper link is up/down
######################################################################
proc gem_get_copper_link {} {
    global LASERCTL_LOS

    if {[get_laserctl_mode] == $LASERCTL_LOS} {
        puts "Link is down."
    } else {
        puts "Link is up."
    }
}


######################################################################
# Function Name    : gem_set_trigger_condition
# Parameters       : profile - the profile this trigger condition is to be
#                  :        used with
#                  : cond_num - 0 or 1; there are a maximum of 2
#                  :        trigger conditions per profile.
#                  : start_offset - byte offset of the first byte to compare
#                  : end_offset - byte offset of the last byte to compare
#                  : data - list of the individual byte values to compare
#                  :         the packet with
#                  : mask - list of the individual byte mask values to
#                  :         apply before making the comparison
#                  : *** the length of the data and mask lists must be
#                  :     equal to the number of bytes being compared
#                  :
#                  : args:
#                  : -no_commit:  don't commit this trigger yet;
#                  :           use gem_load_impairments to commit
#                  :
######################################################################
proc gem_set_trigger_condition {profile cond_num start_offset end_offset op data mask args} {
    global TX_DEST_ADDR

    puts "gem_set_trigger_condition $profile $cond_num $start_offset $end_offset $op $data $mask"

    if {[llength $data] != [llength $mask]} {
        puts "The data and mask lists must be equal in length."
        return
    }

    if {[llength $data] == 0 || [llength $data] > 8} {
        puts "The data and mask lists cannot be empty and must be less than 8 bytes."
        return
    }

    if {[expr $end_offset - $start_offset + 1] != [llength $mask]} {
        puts "ERROR: The data and mask lists must be equal in length to"
        puts "the number of bytes being modified."
        return
    }

    if {[llength $data] < 8} {
        for {set i [llength $data]} {$i < 8} {incr i} {
            lappend data 0
            lappend mask 0
        }
    }

    set commit 1

    foreach a $args {
        if {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    } 


    if {[string compare $op "=="] == 0} {
        set op_num 0
    } elseif {[string compare $op "!="] == 0} {
        set op_num 1
    } elseif {[string compare $op "<"] == 0} {
        set op_num 2
    } elseif {[string compare $op ">"] == 0} {
        set op_num 3
    } elseif {[string compare $op "<="] == 0} {
        set op_num 4
    } elseif {[string compare $op ">="] == 0} {
        set op_num 5
    } else {
        puts "Invalid operator.  Must be one of:  ==, !=, <, >, <=, or >=."
        return
    }

    if {$op_num > 1} {
        # Mask MUST be contiguous if we're using a > or < operator.

        set x2 [expr ([lindex $mask 0] << 24) + \
                     ([lindex $mask 1] << 16) + \
                     ([lindex $mask 2] << 8)  + \
                      [lindex $mask 3]]

        set x1 [expr ([lindex $mask 4] << 24) + \
                     ([lindex $mask 5] << 16) + \
                     ([lindex $mask 6] << 8)  + \
                      [lindex $mask 7]]

        set mask_started 0
        set mask_complete 0

        for {set bit_count 0} {$bit_count < 32} {incr bit_count} {
            set this_bit [expr $x1 & 0x1]
            if {$this_bit == 1 && $mask_started == 0} {
                set mask_started 1
            } elseif {$this_bit == 0 && $mask_started == 1} {
                set mask_complete 1
            } elseif {$this_bit == 1 && $mask_complete == 1} {
                puts "ERROR:  When using the $op operator, the mask must be contiguous."
                return
            }

            set x1 [expr $x1 >> 1]
        }

        for {set bit_count 0} {$bit_count < 32} {incr bit_count} {
            set this_bit [expr $x2 & 0x1]
            if {$this_bit == 1 && $mask_started == 0} {
                set mask_started 1
            } elseif {$this_bit == 0 && $mask_started == 1} {
                set mask_complete 1
            } elseif {$this_bit == 1 && $mask_complete == 1} {
                puts "ERROR:  When using the $op operator, the mask must be contiguous."
                return
            }

            set x2 [expr $x2 >> 1]
        }
    }

    set sobyte(0) [expr ($start_offset >> 8) & 0xFF]
    set sobyte(1) [expr ($start_offset >> 0) & 0xFF]

    set eobyte(0) [expr ($end_offset >> 8) & 0xFF]
    set eobyte(1) [expr ($end_offset >> 0) & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand [concat 0x6A 25 $blade $profile $cond_num \
                      $sobyte(0) $sobyte(1) $eobyte(0) $eobyte(1) \
                      $data $mask $op_num $commit]]

    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_get_trigger_condition
# Parameters       : profile - the profile of the trigger condition
#                  :        we're querying
#                  : cond_num - 0 or 1; condition number of the trigger
#                  :        we're querying
######################################################################
proc gem_get_trigger_condition {profile cond_num} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6B 3 $blade $profile $cond_num]
    set ret [lrange [pong] 2 end]

    set_target $blade

    set cond_num     [value_from_array [lindex $ret 2]]
    set start_offset [value_from_array [lrange $ret 3 4]]
    set end_offset   [value_from_array [lrange $ret 5 6]]
    set data         [lrange $ret 7 14]
    set mask         [lrange $ret 15 22]
    set op           [expr "0x[lindex $ret 23]" + 0]

    if {$start_offset == $end_offset} {
        puts "Triggering on byte $start_offset: (all values are in hex)"
    } else {
        puts "Triggering on bytes $start_offset through $end_offset: (all values are in hex)"
    }

    puts "  Data: [lrange $data 0 [expr $end_offset - $start_offset]]"
    puts "  Mask: [lrange $mask 0 [expr $end_offset - $start_offset]]"
    puts -nonewline "  Op:  "

    switch $op {
        0 {puts "=="}
        1 {puts "!="}
        2 {puts "<"}
        3 {puts ">"}
        4 {puts "<="}
        5 {puts ">="}
        default {puts "(unknown operator)"}
    }
}

######################################################################
# Function Name    : gem_enable_pkt_modify
#                  :
# Parameters       : Packets affected by packet modification are chosen
#                  : by the following parameters:
#                  :
#                  : profile - profile number to apply to
#                  : instance - which modification (0-5) on this profile
#                  :                         to enable
#                  : dist - type of distribution to apply
#                  :     $STAT_DISTRIB(UNIFORM), $STAT_DISTRIB(PERIODIC),
#                  :     $STAT_DISTRIB(POISSON), or $STAT_DISTRIB(GAUSSIAN),
#                  : burstlen - number of packets at a time to modify
#                  : interval - interval over which to perform the modification
#                  : start_offset - byte offset of the first byte to modify
#                  : end_offset - byte offset of the last byte to modify
#                  :   Note that the start and end offsets are NOT simple offsets from the 
#                  :     start of the frame.  These offsets skip over a number
#                  :     of numbers in order to provide room for any 
#                  :     VLAN tags or MPLS labels that may exist in the frame.
#                  :     Offset 34, however, is always a constant offset which
#                  :     specifies the start of the IP header.
#                  :     
#                  :       For example, if the user inputs a packet with 2 VLAN tags, the
#                  :       offsets would look like the following:
#                  :      
#                  :       Field Name               Byte Offset
#                  :       -------------------------------------
#                  :       Mac_Dest_Addr            0
#                  :       Mac_Src_Addr             6
#                  :       VLAN Tag 1 (0x8100)      12
#                  :       VLAN ID 1                14
#                  :       VLAN Tag 2 (0x8100)      16
#                  :       VLAN ID 2                18
#                  :       Ethertype (0x800)        32
#                  :       IP Ver/Len Field         34
#                  :       IP Type of service       35
#                  :       IP Total Length          36
#                  :       
#                  :       
#                  :       If, on the other hand, the user inputs a packet with 2 MPLS
#                  :       labels, the offsets would look like the following:
#                  :
#                  :       Field Name               Byte Offset
#                  :       -------------------------------------
#                  :       Mac_Dest_Addr            0
#                  :       Mac_Src_Addr             6
#                  :       Ethertype (0x8847)       12
#                  :       MPLS Tag 1               14
#                  :       MPLS Tag 2               18
#                  :       IP Ver/Len Field         34
#                  :       IP Type of service       35
#                  :       IP Total Length          36
#                  :       
#                  :
#                  :       If the user inputs a packet with neither an MPLS label nor a
#                  :       VLAN tag, the offsets would look like the following:
#                  :
#                  :       Field Name               Byte Offset
#                  :       -------------------------------------
#                  :       Mac_Dest_Addr            0
#                  :       Mac_Src_Addr             6
#                  :       Ethertype (0x800)        32
#                  :       IP Ver/Len Field         34
#                  :       IP Type of service       35
#                  :       IP Total Length          36
#                  :       
#                  :       ..OR..
#                  :
#                  :       Field Name               Byte Offset
#                  :       -------------------------------------
#                  :       Mac_Dest_Addr            0
#                  :       Mac_Src_Addr             6
#                  :       Ethertype (ANY TYPE)     32
#                  :       1st Byte in Mac Payload  34
#                  :       2nd Byte in Mac Payload  35
#                  :       3rd Byte in Mac Payload  36
#                  :     
#                  :     
#                  : data - list of the individual byte values to modify
#                  :         the packet with
#                  : mask - list of the individual byte mask values to
#                  :         apply with modification
#                  : *** the length of the data and mask lists must be
#                  :     equal to the number of bytes being modified
#                  :
#                  : args:
#                  : -repeat:  e.g., -repeat=4 means to repeat this
#                  :           modification 4 times, then stop
#                  : -std_dev:  e.g., -std_dev=1.0 means to use a 1.0%
#                  :           standard deviation in the case of a Gaussian
#                  :           distribution
#                  : -no_commit:  don't commit the modification
#                  :           use gem_load_impairments to commit
#                  :
#                  : For example:
#                  : In order to modify the IP Src Address on every incoming
#                  :   packet to 192.168.40.1 on profile 0 with modification #0, 
#                  :   one would perform the following command to configure 
#                  :   the modification block:
#                  :   
#                  :   gem_enable_pkt_modify 0 0 $STAT_DISTRIB(PERIODIC) 1 1 46 
#                  :      49 [list 0xC0 0xA8 0x28 0x01] [list 0xFF 0xFF 0xFF 0xFF]
#                  :   
# Purpose          : Turn on packet modification for the specified profile.
######################################################################
proc gem_enable_pkt_modify {profile instance dist burstlen interval start_offset end_offset data mask args} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {$burstlen > $interval} {
        puts "ERROR: Interval must be greater than or equal to the burst length."
        return
    }

    if {$dist == $STAT_DISTRIB(POISSON)} {
        if {$interval > 26464832} {
            puts "Interval must be less than 26464832."
            return
        }
    } else {
        if {$interval > 268000000} {
            puts "Interval must be less than 268000000."
            return
        }
    }

    if {$dist != $STAT_DISTRIB(UNIFORM) && \
        $dist != $STAT_DISTRIB(PERIODIC) && \
        $dist != $STAT_DISTRIB(POISSON) && \
        $dist != $STAT_DISTRIB(GAUSSIAN)} {
        puts "ERROR: Distribution must be either \$STAT_DISTRIB(PERIODIC),"
        puts "\$STAT_DISTRIB(UNIFORM), \$STAT_DISTRIB(POISSON) or \$STAT_DISTRIB(GAUSSIAN)."
        return;
    }

    if {$dist == $STAT_DISTRIB(UNIFORM) || \
        $dist == $STAT_DISTRIB(POISSON) || \
        $dist == $STAT_DISTRIB(GAUSSIAN)} {
        if {$interval == $burstlen} {
            puts "When selecting every packet for impairment,"
            puts "only \$STAT_DISTRIB(PERIODIC) is allowed."
            return
        }
    }

    if {$instance > 5 || $instance < 0} {
        puts "ERROR: Please specify pkt modify number 0-5."
        return
    }

    if {[llength $data] != [llength $mask]} {
        puts "ERROR: The data and mask lists must be equal in length."
        return
    }

    if {$end_offset < $start_offset} {
        puts "ERROR: The starting offset must be less than or equal to the ending offset."
        return
    }
    if {$end_offset > 16383} {
        puts "ERROR: Offset specified is too large; may not exceed 16383."
        return
    }

    if {[expr $end_offset - $start_offset + 1] != [llength $mask]} {
        puts "ERROR: The data and mask lists must be equal in length to"
        puts "the number of bytes being modified."
        return
    }

    if {[llength $data] == 0 || [llength $data] > 8} {
        puts "ERROR: The data and mask lists cannot be empty and must be less than 8 bytes."
        return
    }

    if {[llength $data] < 8} {
        for {set i [llength $data]} {$i < 8} {incr i} {
            lappend data 0
            lappend mask 0
        }
    }

    puts "gem_enable_pkt_modify $profile $instance $dist $burstlen $interval $start_offset $end_offset $data $mask $args"

    set burstdur 65535
    set std_dev 1.0
    set use_rnd 1
    set use_trig 0
    set commit 1
    set cond_num 0xFF

    foreach a $args {
        if {[regexp -nocase {^-repeat=([0-9]+)$} $a tmp burstdur]} {
            if {$burstdur < 1 || $burstdur > 65535} {
                puts "The repeat count must be between 1 and 65535."
                puts "A value of 65535 means forever."
                return
            }
        } elseif {[regexp -nocase {^-std_dev=([\.0-9]+)$} $a tmp std_dev]} {
            if {$std_dev > 100.0 || $std_dev < 0.0} {
                puts "The standard deviation should be between 0-100%."
                return
            }
        } elseif {[regexp -nocase {^-trigger=([0-9]+)$} $a tmp cond_num]} {
            if {$cond_num != 0 && $cond_num != 1} {
                puts "The trigger condition number must be either 0 or 1."
                return
            }
            set use_trig 1
        } elseif {[regexp -nocase {^-no_rnd_sel$} $a tmp]} {
            set use_rnd 0
        } elseif {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    } 

    # ------------------------------------------------------------
    # Send
    # ------------------------------------------------------------

    set sobyte(0) [expr ($start_offset >> 8) & 0xFF]
    set sobyte(1) [expr ($start_offset >> 0) & 0xFF]

    set eobyte(0) [expr ($end_offset >> 8) & 0xFF]
    set eobyte(1) [expr ($end_offset >> 0) & 0xFF]

    set itvbyte(0) [expr ($interval >> 24) & 0xFF]
    set itvbyte(1) [expr ($interval >> 16) & 0xFF]
    set itvbyte(2) [expr ($interval >> 8) & 0xFF]
    set itvbyte(3) [expr ($interval >> 0) & 0xFF]

    set burstlenbyte(0) [expr ($burstlen >> 8) & 0xFF]
    set burstlenbyte(1) [expr ($burstlen >> 0) & 0xFF]

    set burstdurbyte(0) [expr ($burstdur >> 8) & 0xFF]
    set burstdurbyte(1) [expr ($burstdur >> 0) & 0xFF]

    set std_dev [expr $std_dev * 100]
    set std_devbyte(0) [expr (int($std_dev) >> 8) & 0xFF]
    set std_devbyte(1) [expr (int($std_dev) >> 0) & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand [concat 0x50 24 $blade $profile $instance \
                               $use_rnd $use_trig $cond_num $commit $dist \
                               $burstlenbyte(0) $burstlenbyte(1) \
                               $itvbyte(0) $itvbyte(1) $itvbyte(2) $itvbyte(3) \
                               $burstdurbyte(0) $burstdurbyte(1) \
                               $std_devbyte(0) $std_devbyte(1) \
                               $sobyte(0) $sobyte(1) $eobyte(0) $eobyte(1) \
                               $data $mask]]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_disable_pkt_modify
#                  :
# Parameters       : profile  - the specified profile
#                  : instance - which modification on this profile (0-5)
#                  :               to disable
#                  : args:
#                  : -no_commit:  don't commit the disable yet
#                  :           use gem_load_impairments to commit
#                  :
# Purpose          : Turn off packet modify for the specified profile.
######################################################################
proc gem_disable_pkt_modify {profile instance args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    puts "gem_disable_pkt_modify $profile $instance"

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {$instance > 5 || $instance < 0} {
        puts "Please specify pkt modify number 0-5."
        return
    }

    set use_rnd  0
    set use_trig 0
    set cond_num 0
    set commit   1

    foreach a $args {
        if {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x50 7 $blade $profile $instance $use_rnd \
                                      $use_trig $cond_num $commit ]
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_get_pkt_modify_status
# Parameters       : profile - the specified profile
#                  : instance - the pkt modify instance on that profile (0-5)
#                  :     (each profile has up to 6 possible modifications)
# Return Value     : Pkt modify settings on the specified profile
######################################################################
proc gem_get_pkt_modify_status {profile instance} {
    global TX_DEST_ADDR
    global STAT_DISTRIB
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {$instance > 5 || $instance < 0} {
        puts "Please specify pkt modify number 0-5."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x5E 3 $blade $profile $instance]
    set ret [lrange [pong] 5 end]

    set_target $blade

    # ------------------------------------------------------------
    # If disabled, quickly return
    # ------------------------------------------------------------
    set rnd_enabled [expr "0x[lindex $ret 0]" + 0]
    set trig_enabled [expr "0x[lindex $ret 12]" + 0]
    if {$rnd_enabled == 0 && $trig_enabled == 0} {
        puts "Packet modify #$instance on profile $profile is currently DISABLED."
        return
    }

    # ------------------------------------------------------------
    # Get distribution, burstlen, interval and burstdur
    # ------------------------------------------------------------
    set dist         [expr "0x[lindex $ret 1]" + 0]
    set burstlen     [value_from_array [lrange $ret 2 3]]
    set interval     [value_from_array [lrange $ret 4 7]]
    set burstdur     [value_from_array [lrange $ret 8 9]]
    set std_dev      [value_from_array [lrange $ret 10 11]]
    set cond_num     [expr "0x[lindex $ret 13]" + 0]

    set start_offset [value_from_array [lrange $ret 14 15]]
    set end_offset   [value_from_array [lrange $ret 16 17]]
    set data         [lrange $ret 18 25]
    set mask         [lrange $ret 26 33]

    # ------------------------------------------------------------
    # Display
    # ------------------------------------------------------------
    puts "Packet modify #$instance is ENABLED on profile $profile:"

    if {$trig_enabled == 1} {
        puts "  Using trigger condition #$cond_num."
    }

    if {$rnd_enabled == 1} {
        if {$dist == $STAT_DISTRIB(PERIODIC)} {
            puts "  Periodic Distribution"
        } elseif {$dist == $STAT_DISTRIB(UNIFORM)} {
            puts "  Uniform Distribution"
        } elseif {$dist == $STAT_DISTRIB(POISSON)} {
            puts "  Poisson Distribution"
        } elseif {$dist == $STAT_DISTRIB(GAUSSIAN)} {
            puts "  Gaussian Distribution [expr $std_dev / 100.0]"
        } else {
            puts "  ??? Distribution"
        }
    }

    puts "  Interval:  $interval"
    puts "  Burst length:  $burstlen"
    if {$burstdur == 65535} {
        puts "  Repeat Count:  Forever"
    } else {
        puts "  Repeat Count:  $burstdur"
    }

    if {$start_offset == $end_offset} {
        puts "Modifying byte $start_offset: (all values are in hex)"
    } else {
        puts "Modifying bytes $start_offset through $end_offset: (all values are in hex)"
    }

    puts "  Data: [lrange $data 0 [expr $end_offset - $start_offset]]"
    puts "  Mask: [lrange $mask 0 [expr $end_offset - $start_offset]]"
}


######################################################################
# Function Name    : gem_enable_ip_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : enable IP checksum correction on this profile
######################################################################
proc gem_enable_ip_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_enable_ip_checksum_correction $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6C 4 $blade $profile 1 1]
    print_error_on_nack [pong] "Checksum correction is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_ip_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : disable IP checksum correction on this profile
######################################################################
proc gem_disable_ip_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_disable_ip_checksum_correction $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    # We cannot disable IP checksum correction if
    # IPv4 Fragment is in use on this profile.
    send_command [BuildCommand 0xE9 2 $blade $profile]
    set ret [lrange [pong] 4 end]
    set ip_fragment_enabled [expr "0x[lindex $ret 0]" + 0]

    if {$ip_fragment_enabled} {
        puts "Cannot disable IP Checksum Correction when IP Fragment is in use."
        set_target $blade
        return
    }

    send_command [BuildCommand 0x6C 4 $blade $profile 1 0]
    print_error_on_nack [pong] "Checksum correction is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_enable_tcp_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : enable TCP checksum correction on this profile
######################################################################
proc gem_enable_tcp_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_enable_tcp_checksum_correction $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6C 4 $blade $profile 2 1]
    print_error_on_nack [pong] "Checksum correction is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_tcp_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : disable TCP checksum correction on this profile
######################################################################
proc gem_disable_tcp_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_disable_tcp_checksum_correction $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6C 4 $blade $profile 2 0]
    print_error_on_nack [pong] "Checksum correction is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_enable_udp_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : enable UDP checksum correction on this profile
######################################################################
proc gem_enable_udp_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_enable_udp_checksum_correction $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6C 4 $blade $profile 3 1]
    print_error_on_nack [pong] "Checksum correction is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_udp_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : disable UDP checksum correction on this profile
######################################################################
proc gem_disable_udp_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_disable_udp_checksum_correction $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6C 4 $blade $profile 3 0]
    print_error_on_nack [pong] "Checksum correction is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_enable_rsvp_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : enable RSVP checksum correction on this profile
######################################################################
proc gem_enable_rsvp_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_enable_rsvp_checksum_correction $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6C 4 $blade $profile 4 1]
    print_error_on_nack [pong] "Checksum correction is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_rsvp_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : disable RSVP checksum correction on this profile
######################################################################
proc gem_disable_rsvp_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    puts "gem_disable_rsvp_checksum_correction $profile"

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6C 4 $blade $profile 4 0]
    print_error_on_nack [pong] "Checksum correction is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_query_checksum_correction
# Parameters       : profile - the profile number
# Purpose          : display whether checksum correction is enabled
######################################################################
proc gem_query_checksum_correction {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x6D 2 $blade $profile]
    set reply [pong]
 
    set ret [lrange $reply 2 end]

    set_target $blade

    if {"0x[lindex $reply 0]" == 0xC7} {
        puts "Checksum correction is not available."
        return 
    }

    if {[expr "0x[lindex $ret 2]" + 0] == 0} {
        puts "IP Checksum Correction is currently DISABLED."
    } else {
        puts "IP Checksum Correction is currently ENABLED."
    }
    if {[expr "0x[lindex $ret 3]" + 0] == 0} {
        puts "TCP Checksum Correction is currently DISABLED."
    } else {
        puts "TCP Checksum Correction is currently ENABLED."
    }
    if {[expr "0x[lindex $ret 4]" + 0] == 0} {
        puts "UDP Checksum Correction is currently DISABLED."
    } else {
        puts "UDP Checksum Correction is currently ENABLED."
    }
    if {[expr "0x[lindex $ret 5]" + 0] == 0} {
        puts "RSVP Checksum Correction is currently DISABLED."
    } else {
        puts "RSVP Checksum Correction is currently ENABLED."
    }
}

######################################################################
# Function Name    : gem_enable_line_throttle
# Parameters       : limit - Bandwidth Limit.
#                  : units - For Bandwidth Limit. %, B/s (bytes/s), b/s (bits/s).
#                  : type  - gross(inc. preamble+minIPG)/net
#                  : drop_threshold - drop threshold in bytes.
#                  : burst tolerance - burst tolerance in bytes.
#                  : Syntax for specifying Pause ON/OFF :
#                  :   -pause=[XOFF Threshold]/[XON Threshold].
#                  : Note : Pause is not supported in 1Gb/s Fiber Uncouple mode.
# Return Value     : none.
# Purpose          : Enable Line Throttle.
#                  :
######################################################################
proc gem_enable_line_throttle {limit units type drop_threshold burst_tolerance args} {
    global TX_DEST_ADDR
    global BITRATE_GE1GFS
    global BITRATE_GE100M
    global BITRATE_GE10M

    set limittype 0
    set limitunits 0
    set pause 0

    set oprate "0x[get_operating_bitrate]"

    # ----------------------------------------------------------------
    # parse the command options
    # ----------------------------------------------------------------
    foreach a $args {
        if {[regexp -nocase {^-pause=([0-9]+)/([0-9]+)$} $a tmp pause_on pause_off]} {
            if {$oprate == $BITRATE_GE1GFS} {
                puts "MAC Pause cannot be enabled in 1Gb/s Fiber Uncouple Mode."
                return
            }
            if {$pause_off < 0 || $pause_off > 268435455} {
                puts "XON Threshold must be between 0 and 268435455."
                return
            }
            if {$pause_on < 0 || $pause_on > 268435455} {
                puts "XOFF Threshold must be between 0 and 268435455."
                return
            }
            if {$drop_threshold < $pause_on} {
                puts "Drop Threshold must be greater than XOFF Threshold."
                return
            }
            if {$pause_on <= $pause_off} {
                puts "XOFF Threshold must be greater than XON Threshold."
                return
            }
            set pause 1
        } \
        else {
            puts "error: gem_enable_line_throttle: bad argument '$a'."
            return
        }
    }

    if {$limit <= 0} {
        puts "Bandwidth limit cannot be less than or equal to 0."
        return
    }

    set linerate 1e9

    if {$oprate == $BITRATE_GE100M} {
        set linerate 1e8
    }
    if {$oprate == $BITRATE_GE10M} {
        set linerate 1e7
    }

    if {[string compare $units "%"] == 0} {
        if {$limit > 100} {
            puts "Bandwidth limit cannot exceed 100% of line rate."
            return
        }
        set limitunits 0
    } elseif {[string compare $units "B/s"] == 0} {
        set linerate [expr $linerate / 8]
        if {$limit > $linerate} {
            puts "Bandwidth limit cannot exceed line rate."
            return
        }
        set limitunits 1
    } elseif {[string compare $units "b/s"] == 0} {
        if {$limit > $linerate} {
            puts "Bandwidth limit cannot exceed line rate."
            return
        }
        set limitunits 2
    } else {
        puts "Unknown limit units."
        return
    }

    if {[string compare $type "gross"] == 0} {
        set limittype 0
    } elseif {[string compare $type "net"] == 0} {
        set limittype 1
    } else {
        puts "Unknown limit type."
        return
    }

    if {$drop_threshold < 0 || $drop_threshold > 268435455} {
        puts "Drop Threshold must be between 0 and 268435455."
        return
    }

    if {$burst_tolerance < 0 || $burst_tolerance > 65535} {
        puts "Burst tolerance must be between 0 and 65535."
        return
    }

    puts "gem_enable_line_throttle $limit $units $type $drop_threshold $burst_tolerance $args"

    if {$limitunits == 0} {
        set limit [expr round($limit * 1000.0)]
    } else {
        set limit [expr round($limit)]
	}

    # ----------------------------------------------------------------
    # break down limit, pause_on & pause_off
    # ----------------------------------------------------------------
    set limitbyte(0) [expr ($limit >> 24) & 0xFF]
    set limitbyte(1) [expr ($limit >> 16) & 0xFF]
    set limitbyte(2) [expr ($limit >> 8) & 0xFF]
    set limitbyte(3) [expr ($limit >> 0) & 0xFF]

    if {$pause == 1} {
        set pause_onb(0) [expr ($pause_on >> 24) & 0xFF]
        set pause_onb(1) [expr ($pause_on >> 16) & 0xFF]
        set pause_onb(2) [expr ($pause_on >> 8) & 0xFF]
        set pause_onb(3) [expr ($pause_on >> 0) & 0xFF]

        set pause_offb(0) [expr ($pause_off >> 24) & 0xFF]
        set pause_offb(1) [expr ($pause_off >> 16) & 0xFF]
        set pause_offb(2) [expr ($pause_off >> 8) & 0xFF]
        set pause_offb(3) [expr ($pause_off >> 0) & 0xFF]
    } else {
        set pause_onb(0) 0
        set pause_onb(1) 0
        set pause_onb(2) 0
        set pause_onb(3) 0

        set pause_offb(0) 0
        set pause_offb(1) 0
        set pause_offb(2) 0
        set pause_offb(3) 0
    }

    set dropbyte(0) [expr ($drop_threshold >> 24) & 0xFF]
    set dropbyte(1) [expr ($drop_threshold >> 16) & 0xFF]
    set dropbyte(2) [expr ($drop_threshold >> 8) & 0xFF]
    set dropbyte(3) [expr ($drop_threshold >> 0) & 0xFF]

    set burstbyte(0) [expr ($burst_tolerance >> 24) & 0xFF]
    set burstbyte(1) [expr ($burst_tolerance >> 16) & 0xFF]
    set burstbyte(2) [expr ($burst_tolerance >> 8) & 0xFF]
    set burstbyte(3) [expr ($burst_tolerance >> 0) & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    # ----------------------------------------------------------------
    # Now send the command
    # ----------------------------------------------------------------
    send_command [BuildCommand 0xAA 25 $blade 1 \
                  $limitbyte(0) $limitbyte(1) $limitbyte(2) $limitbyte(3) \
                  $limitunits $limittype \
                  $dropbyte(0) $dropbyte(1) $dropbyte(2) $dropbyte(3) \
                  $pause \
                  $pause_onb(0) $pause_onb(1) $pause_onb(2) $pause_onb(3) \
                  $pause_offb(0) $pause_offb(1) $pause_offb(2) $pause_offb(3) \
                  $burstbyte(0) $burstbyte(1) $burstbyte(2) $burstbyte(3)]

    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_line_throttle
# Parameters       : none.
# Return Value     : none.
# Purpose          : Disable Line Throttle.
#                  :
######################################################################
proc gem_disable_line_throttle {} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    # ----------------------------------------------------------------
    # Send the command
    # ----------------------------------------------------------------
    send_command [BuildCommand 0xAA 2 $blade 0]

    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_get_line_throttle
# Parameters       :
# Return Value     : 
# Purpose          : Get Current Line Throttle Setting. 
#                  :
######################################################################
proc gem_get_line_throttle {} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xAC 1 $blade]
    set ret [lrange [pong] 3 end]

    set_target $blade

    # ------------------------------------------------------------
    # Get bandwidth control parameters
    # ------------------------------------------------------------
    set enabled      [expr "0x[lindex $ret 0]" + 0]
    set limit        [value_from_array [lrange $ret 1 4]]
    set limitunits   [expr "0x[lindex $ret 5]" + 0]
    set limittype    [expr "0x[lindex $ret 6]" + 0]
    set drop_thresh  [value_from_array [lrange $ret 7 10]]
    set pause        [expr "0x[lindex $ret 11]" + 0]
    set on_thresh    [value_from_array [lrange $ret 12 15]]
    set off_thresh   [value_from_array [lrange $ret 16 19]]
    set burst_tol    [value_from_array [lrange $ret 20 23]]

    if {$limitunits == 0} {
        set limit [expr $limit / 1000.0]
    }

    if {$enabled == 0} {
        puts "Line Throttle Control is disabled."
        return
    }

    puts "Line Throttle Control"
    puts "-------------------"
    puts ""
    puts -nonewline "Bandwidth Limit:  $limit"
    switch $limitunits {
        0 {puts -nonewline "%"}
        1 {puts -nonewline " B/s"}
        2 {puts -nonewline " b/s"}
        default {puts -nonewline "(unknown units)"}
    }
    switch $limittype {
        0 {puts " (gross bandwidth)"}
        1 {puts " (net bandwidth)"}
        default {puts " (unknown)"}
    }

    if {$pause == 1} {
        puts "MAC Control Pause Enabled"
        puts "    Pause ON Threshold: $on_thresh bytes"
        puts "    Pause OFF Threshold: $off_thresh bytes"
    } else {
        puts "MAC Control Pause Disabled"
    }

    puts "Drop Threshold: $drop_thresh bytes"
    puts "Burst Tolerance: $burst_tol bytes"
}

######################################################################
# Function Name    : gem_set_mem_alloc
# Parameters       : profile - which network profile to set
#                  : delay - maximum delay for this profile in ms
#                  : bw - configured bandwidth for this profile in Mbps
#                  :
#                  : Note that DSX must be enabled in order to
#                  : configure bandwidth.
#                  : 
# Return Value     : 
# Purpose          : Set Current Memory Allocation Settings by profile. 
#                  :
######################################################################
proc gem_set_mem_alloc {profile delay {bw 0} } {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES
    global BITRATE_GE100M
	global BITRATE_GE10M
    global MODE_GEM

	# get operating mode to be sure that memory allocation is supported
    set opmode [get_operating_mode]
    set opmode  [expr "0x[lindex $opmode 0]" + 0]
    set oprate "0x[get_operating_bitrate]"
    set dsxoption [get_config_option 0xEC ]
    set x2option [get_config_option 0xF0 ]
    set linerate 1e9
    set linebw 1000

    # values hardcoded here must be kept consistent with those in RamQueue.h
    set minbw 266

    if {$oprate == $BITRATE_GE100M} {
        set linerate 1e8
        set linebw 100
        set minbw 26
    }
    if {$oprate == $BITRATE_GE10M} {
        set linerate 1e7
        set linebw 10
        set minbw 10
    }

	set delay_limit 2000
	if {$x2option != 0} {
		set delay_limit 4000
	}
	if {$dsxoption != 0} { 
		set delay_limit 15000
		if {$bw == 0} {
			puts "Missing bandwidth parameter."
			return
		}
	} elseif {$bw != 0} {
		puts "Bandwidth parameter will be ignored because DSX is not enabled."
	}
	if {$oprate == $BITRATE_GE100M || $oprate == $BITRATE_GE10M} {
		set delay_limit [expr $delay_limit * 10]
	}
	if {$bw == 0} {
		set bw $linebw
	}

	# do error checking
    if {$opmode != $MODE_GEM} {
		puts "Invalid Operating Mode"
		return
	}
    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }
	if {$delay < 0 || $delay > $delay_limit} {
		puts "Delay must be between 0 and $delay_limit ms"
		return
	}
	if {$bw < $minbw || $bw > $linebw} {
		puts "Bandwidth must be between $minbw and $linebw Mbps"
		return 
	}

	# convert to Mbps 
	set lbw    [expr $bw / 8.0 * 1e9]

	# format everything for transmission
	set delay [expr round($delay * 1000)]
    set delaybyte(0) [expr ($delay >> 24) & 0xFF]
    set delaybyte(1) [expr ($delay >> 16) & 0xFF]
    set delaybyte(2) [expr ($delay >> 8) & 0xFF]
    set delaybyte(3) [expr ($delay >> 0) & 0xFF]

    # ----------------------------------------------------------------
    # break down bw into bytes; tcl won't do shift on 64 bit values
    # ----------------------------------------------------------------
    set divisor   [expr {256.0 * 256.0 * 256.0 * 256.0 * 256.0 * 256.0 * 256.0}]
    for {set i 0} {$i<8} {incr i} {
		set tmp            [expr {$lbw / $divisor}]
		set ltmp           [expr {int($tmp)}]
		set bwbyte($i)     $ltmp
		set lbw             [expr {$lbw - ($ltmp * $divisor)}]
		set divisor        [expr {$divisor / 256.0}]
    }

	# this command goes to the NB
    set blade $TX_DEST_ADDR
    set_target 0

	# everythings fine, send the command
    send_command [BuildCommand 0x98 15 $blade $profile 0x02 \
					 $delaybyte(0) $delaybyte(1) $delaybyte(2) $delaybyte(3) \
					 $bwbyte(0) $bwbyte(1) $bwbyte(2) $bwbyte(3) \
					 $bwbyte(4) $bwbyte(5) $bwbyte(6) $bwbyte(7) ]

	# decode message
	pong_check

	# go back to the correct blade
    set_target $blade
}

######################################################################
# Function Name    : gem_get_mem_alloc
# Parameters       : profile - which network profile to get
# Return Value     : 
# Purpose          : Get Current Memory Allocation Settings by profile. 
#                  :
######################################################################
proc gem_get_mem_alloc {profile} {
    global TX_DEST_ADDR

	# this command goes to the NB
    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x98 3 $blade $profile 0x01]

	# read response from remote side
    set ret [lrange [pong] 2 end]

	# go back to the correct blade
    set_target $blade

	# decode message
    set blade     [expr "[lindex $ret 0]" + 0]
    set flow      [value_from_array [lrange $ret 1 2]]
    set o_enabled [expr "[lindex $ret 3]" + 0]
    set delay     [value_from_array [lrange $ret 4 7]]
    set bw        [value_from_array [lrange $ret 8 15]]
    set used_mem  [value_from_array [lrange $ret 16 23]]
    set max_mem   [value_from_array [lrange $ret 24 31]]
    set free_mem  [value_from_array [lrange $ret 32 39]]

	# account for floating point by removing scaling factor
	set delay    [expr $delay    / 1000.0]
	set bw       [expr $bw       / 1000.0]
	set used_mem [expr $used_mem / 1000.0]
	set max_mem  [expr $max_mem  / 1000.0]
	set free_mem [expr $free_mem / 1000.0]

	# convert to Mbps 
	set bw    [expr $bw * 8.0 / 1000000.0]

	# display information
	puts "Profile \#$flow"
	puts ""
	puts "    Memory Allocation"
	puts "    -----------------"
	puts ""
	puts "Delay: $delay ms"
	puts "BW:    $bw Mbps"
	puts ""
	puts "Used Memory:      $used_mem MB"
	puts "Max Memory:       $max_mem MB"
	puts "Available memory: $free_mem MB"
	puts ""
    switch $o_enabled {
        0 {puts "DSX:   Disabled"}
        1 {puts "DSX:   Enabled"}
		default {puts "DSX:   (unknown)"}
    }
}

######################################################################
# Function Name    : gem_is_dsf_in_use
#                  :
# Purpose          : *** INTERNAL USE ONLY ***
######################################################################
proc gem_is_dsf_in_use {profile} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0
    send_command [BuildCommand 0xEB 3 $blade $profile 0x11]
	set ret [lrange [pong] 5 end]
    set_target $blade

    return [lindex $ret 0]
}

######################################################################
# Function Name    : gem_set_video_format
# Parameters       : profile - profile to modify
#                  : svideo_format - "mpeg-2" or "mpeg-4"
# Return Value     : 
# Purpose          : Set current IP TV video format for a profile.
#                  :
######################################################################
proc gem_set_video_format {profile svideo_format} {

    global TX_DEST_ADDR
    global GEM_MAX_PROFILES
    global MODE_GEM

	# get operating mode to be sure that memory allocation is supported
    set opmode  [get_operating_mode]
    set opmode  [expr "0x[lindex $opmode 0]" + 0]
	set cfgoption [get_config_option 0xEB ]

	# error check the entered values
	if {$cfgoption == 0} { 
		puts "IPTV Option is not enabled on this blade"
		return
	}

    if {$opmode != $MODE_GEM} {
		puts "Invalid Operating Mode ($opmode) ($gemmode)"
		return
	}

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

	# input validated
	if {[string compare $svideo_format "mpeg-2"] == 0} {
		set video_format 0
	} elseif {[string compare $svideo_format "mpeg-4"] == 0} {
		set video_format 1
    } else {
		puts "Invalid video format. Please specify mpeg-2 or mpeg-4."
        return
	}

	# this command goes to the NB
    set blade $TX_DEST_ADDR
    set_target 0

	# output so we can check what is happening
	#puts "BuildCommand 0x9C 4 $blade $profile 0x06 $video_format"

	# everythings fine, send the command
    send_command [BuildCommand 0x9C 4 $blade $profile 0x06 $video_format]

	# decode message
	pong_check

	# go back to the correct blade
    set_target $blade
}

######################################################################
# Function Name    : gem_get_video_format
# Parameters       : profile - profile to retrieve video format for.
# Return Value     : 
# Purpose          : Get Current IP TV video format by profile. 
#                  :
######################################################################
proc gem_get_video_format {profile} {
    global TX_DEST_ADDR

	set cfgoption [get_config_option 0xEB ]

	# error check the entered values
	if {$cfgoption == 0} { 
		puts "IPTV Option is not enabled on this blade"
		return
	}

	# this command goes to the NB
    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9c 3 $blade $profile 0x5]

	# read response from remote side
    set rcvd [pong]
    set ret [lrange $rcvd 2 end]

	# go back to the correct blade
    set_target $blade

	#puts "received: $rcvd"
	#puts "parsing: $ret"

	# decode message
    set blade           [expr "[lindex $ret 0]" + 0]
    set flow            [value_from_array [lrange $ret 1 2]]
    set video_format    [expr "[lindex $ret 3]" + 0]

	# display information
	puts "Profile \#$flow"

    switch $video_format {
        0 {puts "    MPEG-2"}
        1 {puts "    MPEG-4"}
		default {puts "    IP TV Unknown Video Format"}
    }
}

######################################################################
# Function Name    : gem_enable_iptv_config
# Parameters       : profile - profile to modify
#                  : sframe_id - "i-frame", "p-frame" or "b-frame"
#                  : rptCnt - Repeat count (1 - 15 or "infinite")
#                  : dist - type of distribution to apply
#                  :        "uniform", "periodic", "poisson" or "guassian"
#                  : select_len - number of packets at a time to modify
#                  : select_interval - interval over which to perform the modification
#                  : min_drop_delay - min frame drop delay
#                  : max_drop_delay - max frame drop delay
#                  :
#                  : Optional parameter:
#                  : std_dev - e.g., 1.0 means to use a 1.0%
#                  :           standard deviation in the case of a Gaussian
#                  :           distribution
# Return Value     : 
# Purpose          : Enable the iptv configuration by profile and frame type. 
#                  :
######################################################################
proc gem_enable_iptv_config {profile sframe_id rptCnt dist select_len select_interval min_drop_delay max_drop_delay args} {

    global TX_DEST_ADDR
    global GEM_MAX_PROFILES
    global STAT_DISTRIB
    global MODE_GEM

	# get operating mode to be sure that memory allocation is supported
    set opmode  [get_operating_mode]
    set opmode  [expr "0x[lindex $opmode 0]" + 0]
	set cfgoption [get_config_option 0xEB ]

	# error check the entered values
	if {$cfgoption == 0} { 
		puts "IPTV Option is not enabled on this blade"
		return
	}

    if {$opmode != $MODE_GEM} {
		puts "Invalid Operating Mode ($opmode) ($gemmode)"
		return
	}

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {[gem_is_dsf_in_use $profile]} {
        puts "IPTV cannot be enabled because DSF is currently in use."
        puts "If you wish to use IPTV, please disable all DSF search strings."
        return
    }

	# input validated
	if {[string compare $sframe_id "i-frame"] == 0} {
		set frame_id 0
	} elseif {[string compare $sframe_id "p-frame"] == 0} {
		set frame_id 1
	} elseif {[string compare $sframe_id "b-frame"] == 0} {
		set frame_id 2
    } else {
		puts "Invalid frame type. Please specify i-frame, p-frame, or b-frame."
        return
	}

	#if {[regexp -nocase {^-periodic$} $dist ]} 
	if {[string compare $dist "periodic"] == 0} {
	    set iptv_distrib $STAT_DISTRIB(PERIODIC)
	} \
	elseif {[string compare $dist "poisson"] == 0} {
	    set iptv_distrib $STAT_DISTRIB(POISSON)
	} \
	elseif {[string compare $dist "gaussian"] == 0} {
	    set iptv_distrib $STAT_DISTRIB(GAUSSIAN)
	} \
	elseif {[string compare $dist "uniform"] == 0} {
	    set iptv_distrib $STAT_DISTRIB(UNIFORM)
	} \
	else {
	    puts "Invalid distribution type ($dist). Please enter periodic, poisson, gaussian, or uniform."
		return
	}

	if {$rptCnt < 1 || $rptCnt > 15} {

		if {([string compare $rptCnt "forever"] != 0) &&
		    ([string compare $rptCnt "infinite"] != 0)} {
			puts "Repeat Count must be between 1 and 15 or forever"
			return 
		} else {
			set rptCnt 16
		}
		
	}
	
	if {$select_len > $select_interval} {
		puts "Frame Drop Selection first parameter can not be greater than the second parameter."
		return
	}

	if {$min_drop_delay < 0 || $min_drop_delay > 15 || $max_drop_delay < 0 || $max_drop_delay > 15} {
		puts " Frame Drop Delay must be between 0 and 15 for both values"
		return 
	}

	# validate std_dev
    if {[llength $args] > 0} {
        set std_dev [lindex $args 0]
        if {$std_dev > 100.0 || $std_dev < 0.0} {
            puts "The standard deviation should be between 0-100%."
            return
        }
    } else {
        if {$iptv_distrib == $STAT_DISTRIB(GAUSSIAN)} {
          puts " Standard deviation must be provided for Gaussian distribution."
          return 
        }
        set std_dev 30
    }

	# format everything for transmission
	set rptCntbyte(0) [expr ($rptCnt >> 8) & 0xFF]
	set rptCntbyte(1) [expr ($rptCnt >> 0) & 0xFF]
	
	set sel_lenbyte(0) [expr ($select_len >> 8) & 0xFF]
	set sel_lenbyte(1) [expr ($select_len >> 0) & 0xFF]
	
	set sel_intbyte(0) [expr ($select_interval >> 24) & 0xFF]
	set sel_intbyte(1) [expr ($select_interval >> 16) & 0xFF]
	set sel_intbyte(2) [expr ($select_interval >>  8) & 0xFF]
	set sel_intbyte(3) [expr ($select_interval >>  0) & 0xFF]
	
	set istd_dev [expr round($std_dev * 100)]
    set istd_devbyte(0) [expr ($istd_dev >> 8) & 0xFF]
    set istd_devbyte(1) [expr ($istd_dev >> 0) & 0xFF]

	# this command goes to the NB
    set blade $TX_DEST_ADDR
    set_target 0

	# output so we can check what is happening
	#puts -nonewline "BuildCommand 0x9C 18 $blade $profile 0x02 $frame_id 0x1 "
    #puts            "$rptCntbyte(0) $rptCntbyte(1) $iptv_distrib"
	#puts -nonewline "    $sel_lenbyte(0) $sel_lenbyte(1) $sel_intbyte(0) $sel_intbyte(1) $sel_intbyte(2) "
	#puts            "$sel_intbyte(3) $min_drop_delay $max_drop_delay $istd_devbyte(0) $istd_devbyte(1)"

	# everythings fine, send the command
    send_command [BuildCommand 0x9C 18 $blade $profile 0x02 $frame_id 0x1 \
					  $rptCntbyte(0) $rptCntbyte(1) \
					  $iptv_distrib \
					  $sel_lenbyte(0) $sel_lenbyte(1) \
					  $sel_intbyte(0) $sel_intbyte(1) $sel_intbyte(2) $sel_intbyte(3) \
					  $min_drop_delay $max_drop_delay \
					  $istd_devbyte(0) $istd_devbyte(1) ]

	# decode message
	pong_check

	# go back to the correct blade
    set_target $blade
}

######################################################################
# Function Name    : gem_get_iptv_config
# Parameters       : profile - profile to retrieve IPTV config for.
#                  : sframe_id - "i-frame", "p-frame" or "b-frame"
# Return Value     : 
# Purpose          : Get Current IP TV configuration by profile and frame id. 
#                  :
######################################################################
proc gem_get_iptv_config {profile sframe_id} {
    global TX_DEST_ADDR
    global STAT_DISTRIB

	set cfgoption [get_config_option 0xEB ]

	# error check the entered values
	if {$cfgoption == 0} { 
		puts "IPTV Option is not enabled on this blade"
		return
	}

	# input validated
	if {[string compare $sframe_id "i-frame"] == 0} {
		set frame_id 0
	} elseif {[string compare $sframe_id "p-frame"] == 0} {
		set frame_id 1
	} elseif {[string compare $sframe_id "b-frame"] == 0} {
		set frame_id 2
    } else {
		puts "Invalid frame type. Please specify i-frame, p-frame, or b-frame."
        return
	}

	# this command goes to the NB
    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9c 4 $blade $profile 0x1 $frame_id]

	# read response from remote side
    set rcvd [pong]
    set ret [lrange $rcvd 2 end]

	# go back to the correct blade
    set_target $blade

	#puts "received: $rcvd"
	#puts "parsing: $ret"

	# decode message
    set blade           [expr "[lindex $ret 0]" + 0]
    set flow            [value_from_array [lrange $ret 1 2]]
    set rframe_id       [expr "[lindex $ret 3]" + 0]
    set o_enabled       [expr "[lindex $ret 4]" + 0]
    set rptCnt          [value_from_array [lrange $ret 5 6]]
    set dist            [expr "[lindex $ret 7]" + 0]
    set select_len      [value_from_array [lrange $ret 8 9]]
    set select_interval [value_from_array [lrange $ret 10 13]]
    set drop_delay      [expr "[lindex $ret 14]" + 0]
    set drop_interval   [expr "[lindex $ret 15]" + 0]
    set istd_dev        [value_from_array [lrange $ret 16 17]]
    set video_format    [expr "[lindex $ret 18]" + 0]

	# account for floating point by removing scaling factor
	set std_dev [expr $istd_dev  / 100.0]

	# display information
	puts "Profile \#$flow"

    switch $video_format {
        0 {puts -nonewline "    MPEG-2"}
        1 {puts -nonewline "    MPEG-4"}
		default {puts "    IP TV Unknown Video Format"}
    }

    switch $rframe_id {
        0 {puts "; IP TV I-Frame Configuration"}
        1 {puts "; IP TV P-Frame Configuration"}
        2 {puts "; IP TV B-Frame Configuration"}
		default {puts "; IP TV Unknown Frame Configuration"}
    }

	puts "    ---------------------------"
	puts ""

	if {$rptCnt > 15} {
		puts "Repeat Count:       Infinite"
	} else {
		puts "Repeat Count:       $rptCnt"
	}

	puts ""
	puts "Selection Criteria: $select_len in $select_interval"
	puts "Drop Criteria:      $drop_delay to $drop_interval"

    if {$dist == $STAT_DISTRIB(PERIODIC)} {
		puts "Distribution:       Periodic"
    } elseif {$dist == $STAT_DISTRIB(UNIFORM)} {
		puts "Distribution:       Uniform"
    } elseif {$dist == $STAT_DISTRIB(POISSON)} {
		puts "Distribution:       Poisson"
    } elseif {$dist == $STAT_DISTRIB(GAUSSIAN)} {
		puts "Distribution:       Gaussian; Standard Deviation: $std_dev"
    } else {
		puts "Distribution:       Unknown"
    }

	puts ""
    switch $o_enabled {
        0 {puts "IPTV:   Disabled"}
        1 {puts "IPTV:   Enabled"}
		default {puts "IPTV:   (unknown)"}
    }
}

######################################################################
# Function Name    : gem_disable_iptv_config
# Parameters       : profile - profile to modify
#                    sframe_id - "i-frame", "p-frame", "b-frame" or "all"
# Return Value     : 
# Purpose          : Disable a specific or all Video Frame/Primary Picture Type Selection 
#                  :
######################################################################
proc gem_disable_iptv_config {profile sframe_id} {

    global TX_DEST_ADDR
    global GEM_MAX_PROFILES
    global MODE_GEM

	# get operating mode to be sure that memory allocation is supported
    set opmode  [get_operating_mode]
    set opmode  [expr "0x[lindex $opmode 0]" + 0]
	set cfgoption [get_config_option 0xEB ]

	# error check the entered values
	if {$cfgoption == 0} { 
		puts "IPTV Option is not enabled on this blade"
		return
	}

    if {$opmode != $MODE_GEM} {
		puts "Invalid Operating Mode ($opmode) ($gemmode)"
		return
	}

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {[gem_is_dsf_in_use $profile]} {
        puts "IPTV cannot be enabled because DSF is currently in use."
        puts "If you wish to use IPTV, please disable all DSF search strings."
        return
    }

	# input validated
	if {[string compare $sframe_id "i-frame"] == 0} {
		set frame_id 0
	} elseif {[string compare $sframe_id "p-frame"] == 0} {
		set frame_id 1
	} elseif {[string compare $sframe_id "b-frame"] == 0} {
		set frame_id 2
	} elseif {[string compare $sframe_id "all"] == 0} {
		set frame_id 255
    } else {
		puts "Invalid frame type. Please specify i-frame, p-frame, b-frame, or all."
        return
	}

	# this command goes to the NB
    set blade $TX_DEST_ADDR
    set_target 0

	# output so we can check what is happening
	#puts "BuildCommand 0x9C 4 $blade $profile 0x04 $frame_id"

	# everythings fine, send the command
    send_command [BuildCommand 0x9C 4 $blade $profile 0x04 $frame_id ]

	# decode message
	pong_check

	# go back to the correct blade
    set_target $blade
}

######################################################################
# Function Name    : gem_enable_accumulate_burst
# Parameters       : profile
#                  : mode: $ACCUM_MODE(COUNT_ONLY), $ACCUM_MODE(TIMEOUT_ONLY),
#                  :       $ACCUM_MODE(COUNT_OR_TIMEOUT), or
#                  :       $ACCUM_MODE(COUNT_AND_TIMEOUT)
#                  : args:
#                  :   -no_commit:  don't commit the pkt drop
#                  :               use gem_load_impairments to commit
#                  :   -packets=:  number of packets to accumulate
#                  :   -timeout=:  number of ms to accumulate
#                  :   -gap=:  minimum interpacket gap during burst
#                  :           
# Return Value     : 
# Purpose          : Display current Accumulate & Burst settings for
#                  : the specified profile.
######################################################################
proc gem_enable_accumulate_burst {profile mode args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES
    global ACCUM_MODE

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {$mode != $ACCUM_MODE(COUNT_ONLY) && \
        $mode != $ACCUM_MODE(TIMEOUT_ONLY) && \
        $mode != $ACCUM_MODE(COUNT_OR_TIMEOUT) && \
        $mode != $ACCUM_MODE(COUNT_AND_TIMEOUT)} {
        puts "Please select a valid mode:"
        puts "  \$ACCUM_MODE(COUNT_ONLY),"
        puts "  \$ACCUM_MODE(TIMEOUT_ONLY),"
        puts "  \$ACCUM_MODE(COUNT_OR_TIMEOUT), or"
        puts "  \$ACCUM_MODE(COUNT_AND_TIMEOUT)."
        return
    }

    set commit 1
    set burst_size 1
    set timeout 1.0
    set gap 1.0

    set packets_specified 0
    set timeout_specified 0
    set gap_specified 0

    foreach a $args {
        if {[regexp -nocase {^-packets=([0-9]+)$} $a tmp burst_size]} {
            puts "packets = $burst_size"
            set packets_specified 1
        } elseif {[regexp -nocase {^-timeout=([0-9\.]+)$} $a tmp timeout]} {
            puts "timeout = $timeout"
            set timeout_specified 1
        } elseif {[regexp -nocase {^-gap=([0-9\.]+)$} $a tmp gap]} {
            puts "gap = $gap"
            set gap_specified 1
        } elseif {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    } 

    if {$mode == $ACCUM_MODE(COUNT_ONLY)} {
        if {$packets_specified == 0} {
            puts "For \$ACCUM_MODE(COUNT_ONLY), please use the -packets option"
            puts "to specify how many packets to accumulate before burst."
            return
        }
    } elseif {$mode == $ACCUM_MODE(TIMEOUT_ONLY)} {
        if {$timeout_specified == 0} {
           puts "For \$ACCUM_MODE(TIMEOUT_ONLY), please use the -timeout option"
           puts "to specify how long (in ms) to accumulate before burst."
           return
        }
    } elseif {$mode == $ACCUM_MODE(COUNT_OR_TIMEOUT) || \
              $mode == $ACCUM_MODE(COUNT_AND_TIMEOUT)} {
        if {$timeout_specified == 0 || $packets_specified == 0} {
            puts "Please use -packets and -timeout to specify the packet"
            puts "count and timeout."
            return
        }
    }

    if {$gap_specified == 0} {
        puts "Please use the -gap option to specify the minimum interburst gap."
        return
    }

    if {(($burst_size > 65536) || ($burst_size < 1)) && \
        ($mode != $ACCUM_MODE(TIMEOUT_ONLY))} {
       puts "Accumulate and Burst's Burst Size must be between 1 and 65536."
       return
    }

    if {($timeout > 490853.0) && ($mode != $ACCUM_MODE(COUNT_ONLY))} {
       puts "Accumulate and Burst's Timeout must be less than 490853ms."
       return
    }

    if {($gap > 30678.0)} {
       puts "Accumulate and Burst's Gap must be less than 30678ms."
       return
    }

    set timeout [expr round($timeout * 1000.0)]
    set gap [expr round($gap * 1000.0)]

    set bsbyte(0) [expr ($burst_size >> 8) & 0xFF]
    set bsbyte(1) [expr ($burst_size >> 0) & 0xFF]

    set tobyte(0) [expr ($timeout >> 24) & 0xFF]
    set tobyte(1) [expr ($timeout >> 16) & 0xFF]
    set tobyte(2) [expr ($timeout >> 8) & 0xFF]
    set tobyte(3) [expr ($timeout >> 0) & 0xFF]

    set gapbyte(0) [expr ($gap >> 24) & 0xFF]
    set gapbyte(1) [expr ($gap >> 16) & 0xFF]
    set gapbyte(2) [expr ($gap >> 8) & 0xFF]
    set gapbyte(3) [expr ($gap >> 0) & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xA0 15 $blade $profile 1 $commit $mode \
                  $bsbyte(0) $bsbyte(1) \
                  $tobyte(0) $tobyte(1) $tobyte(2) $tobyte(3) \
                  $gapbyte(0) $gapbyte(1) $gapbyte(2) $gapbyte(3)]


#    send_command [BuildCommand 0xA0 1 $blade]
#    set ret [lrange [pong] 3 end]
    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_disable_accumulate_burst
# Parameters       : profile
#                  : args:
#                  :   -no_commit:  don't commit the settings
#                  :             use gem_load_impairments to commit
#                  :           
# Purpose          : Disable Accumulate & Burst on the specified
#                  : profile.
#                  :
######################################################################
proc gem_disable_accumulate_burst {profile args} {
    puts "gem_disable_accumulate_burst $profile"
    set cmd {gem_disable_impairment 0xA0 $profile}
    eval $cmd $args
}


######################################################################
# Function Name    : gem_get_accumulate_burst_status
# Parameters       : profile
# Purpose          : Display the current configuration for GEM's
#                  : accumulate and burst feature on the specified
#                  : profile.
#                  :
######################################################################
proc gem_get_accumulate_burst_status {profile} {
    global TX_DEST_ADDR
    global ACCUM_MODE
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xA1 2 $blade $profile]
    set ret [lrange [pong] 4 end]

    set_target $blade

    # ------------------------------------------------------------
    # Get bandwidth control parameters
    # ------------------------------------------------------------
    set enabled      [expr "0x[lindex $ret 0]" + 0]
    set mode         [expr "0x[lindex $ret 1]" + 0]
    set burst_size   [value_from_array [lrange $ret 2 3]]
    set timeout      [expr [value_from_array [lrange $ret 4 7]] / 1000.0]
    set min_gap      [expr [value_from_array [lrange $ret 8 11]] / 1000.0]

    if {$enabled == 0} {
        puts "Accumulate & Burst is disabled on profile $profile."
        return
    }

    puts "Accumulate & Burst is enabled on profile $profile."

    if {$mode == $ACCUM_MODE(COUNT_ONLY)} {
        puts "Accumulates $burst_size packets before burst."
    } elseif {$mode == $ACCUM_MODE(TIMEOUT_ONLY)} {
        puts "Accumulates for $timeout ms before burst."
    } elseif {$mode == $ACCUM_MODE(COUNT_OR_TIMEOUT)} {
        puts "Accumulates for $timeout ms or $burst_size packets before burst."
    } elseif {$mode == $ACCUM_MODE(COUNT_AND_TIMEOUT)} {
        puts "Accumulates for $timeout ms and $burst_size packets before burst."
    }
    puts "Minimum gap during burst is $min_gap ms."
}

######################################################################
# Function Name    : gem_enable_ipv4_fragment
# Parameters       : profile interval mtu
#                  : interval - interval over which to perform the fragment
#                  : mtu:  64 to 10000 (in bytes)
#                  : args:
#                  :   -no_commit:  don't commit the pkt drop
#                  :               use gem_load_impairments to commit
#                  :   -repeat:  e.g., -repeat=4 means to repeat this
#                  :           impairment 4 times, then stop
#                  :           the default is to repeat the impairment
#                  :           forever; the maximum is 65534.
#                  :   -ignore_dff:  ignore the don't fragment flag
#                  :           
# Return Value     : 
# Purpose          : Enable IP Fragment on the specified profile
#                  : using the mtu size to determine what size
#                  : packets to fragment.  The -ignore_dff option
#                  : can be used to ignore the Don't Fragment flag;
#                  : by default the flag is honored.
######################################################################
proc gem_enable_ipv4_fragment {profile interval mtu args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {($mtu < 64) || ($mtu > 10000)} {
        puts "Please select a MTU size between 64 and 10000 bytes."
        return
    }

    if {($interval < 1) || ($interval > 4294967295)} {
        puts "Please select an interval between 1 and 4294967295 (2^32-1)."
        return
    }

    set commit 1
    set honor_dff 1
    set repeat 65535
    set burstlen 1

    foreach a $args {
        if {[regexp -nocase {^-ignore_dff$} $a tmp]} {
            set honor_dff 0
        } elseif {[regexp -nocase {^-no_commit$} $a tmp]} {
            set commit 0
        } elseif {[regexp -nocase {^-repeat=([0-9\.]+)$} $a tmp repeat]} {
            if {($repeat < 0) || ($repeat > 65535)} {
                puts "-repeat must be between 0 and 65535."
                return
            }
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    } 

    set mtubyte(0) [expr ($mtu >> 8) & 0xFF]
    set mtubyte(1) [expr ($mtu >> 0) & 0xFF]

    set repbyte(0) [expr ($repeat >> 8) & 0xFF]
    set repbyte(1) [expr ($repeat >> 0) & 0xFF]

    set blbyte(0) [expr ($burstlen >> 8) & 0xFF]
    set blbyte(1) [expr ($burstlen >> 0) & 0xFF]

    set intbyte(0) [expr ($interval >> 24) & 0xFF]
    set intbyte(1) [expr ($interval >> 16) & 0xFF]
    set intbyte(2) [expr ($interval >> 8) & 0xFF]
    set intbyte(3) [expr ($interval >> 0) & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xE2 17 $blade $profile 1 $commit $honor_dff \
                  $blbyte(0) $blbyte(1) \
                  $intbyte(0) $intbyte(1) $intbyte(2) $intbyte(3) \
                  $repbyte(0) $repbyte(1) \
                  $mtubyte(0) $mtubyte(1)]


    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    pong_check

    set_target $blade
}


######################################################################
# Function Name    : gem_disable_ipv4_fragment
# Parameters       : profile
#                  : args:
#                  :   -no_commit:  don't commit the settings
#                  :             use gem_load_impairments to commit
#                  :           
# Purpose          : Disable IP fragment on the specified profile.
#                  :
######################################################################
proc gem_disable_ipv4_fragment {profile args} {
    puts "gem_disable_ipv4_fragment $profile"
    set cmd {gem_disable_impairment 0xE2 $profile}
    eval $cmd $args
}


######################################################################
# Function Name    : gem_get_ipv4_fragment_status
# Parameters       : profile
# Purpose          : Display the current configuration for GEM's
#                  : ip fragment feature on the specified
#                  : profile.
#                  :
######################################################################
proc gem_get_ipv4_fragment_status {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xE9 2 $blade $profile]
    set ret [lrange [pong] 4 end]

    set_target $blade

    # ------------------------------------------------------------
    # Get bandwidth control parameters
    # ------------------------------------------------------------
    set enabled      [expr "0x[lindex $ret 0]" + 0]
    set burstlen     [expr [value_from_array [lrange $ret 1 2]]]
    set interval     [expr [value_from_array [lrange $ret 3 6]]]
    set burstdur     [expr [value_from_array [lrange $ret 7 8]]]
    set mtu          [expr [value_from_array [lrange $ret 9 10]]]
    set honor_dff    [expr [value_from_array [lrange $ret 11 12]]]

    if {$enabled == 0} {
        puts "IP Fragment is disabled on profile $profile."
        return
    }

    puts "IP Fragment is enabled on profile $profile."

    puts "  Interval:  $interval"
    puts "  Burst length:  $burstlen"
    if {$burstdur == 65535} {
        puts "  Repeat Count:  Forever"
    } else {
        puts "  Repeat Count:  $burstdur"
    }
    puts "  MTU: $mtu bytes"

    if {$honor_dff == 0} {
        puts "Ignore don't-fragment flag."
    } else {
        puts "Honor don't-fragment flag."
    }
}

######################################################################
# Function Name    : gem_set_external_timing_ref <ref>
#                  :
# Parameters       : <ref> must be one of the following values:
#                  :
#                  :   $GEM_REF_BITS_T1
#                  :   $GEM_REF_PRS_E1
#                  :   $GEM_REF_EXT_10MHZ
#                  :   $GEM_REF_INT_10MHZ
#                  :   $GEM_REF_LINE
#                  :
# Purpose          : Selects the reference clock to use.
######################################################################
proc gem_set_external_timing_ref {ref} {
    global TX_DEST_ADDR

    global GEM_REF_BITS_T1
    global GEM_REF_PRS_E1
    global GEM_REF_EXT_10MHZ
    global GEM_REF_INT_10MHZ
    global GEM_REF_LINE

    if {($ref != $GEM_REF_BITS_T1) &&
        ($ref != $GEM_REF_PRS_E1) &&
        ($ref != $GEM_REF_EXT_10MHZ) &&
        ($ref != $GEM_REF_INT_10MHZ) &&
        ($ref != $GEM_REF_LINE)} \
    {
        puts "ERROR:  The reference must be one of the following:"
        puts "         \$GEM_REF_BITS_T1"
        puts "         \$GEM_REF_PRS_E1"
        puts "         \$GEM_REF_EXT_10MHZ"
        puts "         \$GEM_REF_INT_10MHZ"
        puts "         \$GEM_REF_LINE"
        return
    }

    puts -nonewline "gem_set_external_timing_ref "
    switch $ref {
        0 {puts "\$GEM_REF_BITS_T1"}
        1 {puts "\$GEM_REF_PRS_E1"}
        2 {puts "\$GEM_REF_EXT_10MHZ"}
        3 {puts "\$GEM_REF_INT_10MHZ"}
        4 {puts "\$GEM_REF_LINE"}
    }

    set blade $TX_DEST_ADDR
    set_target 0

    # ----------------------------------------------------------------
    # Now send the command
    # ----------------------------------------------------------------
    send_command [BuildCommand 0x09 4 1 0 0x02 $ref]

    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    print_error_on_nack [pong] "External Timing is not available."

    set_target $blade
}

######################################################################
# Function Name    : gem_get_external_timing_ref
#                  :
# Parameters       : none
#                  :
# Purpose          : Displays which reference clock is currently in use,
#                  : and whether it has LOS or LOL.
######################################################################
proc gem_get_external_timing_ref {} {
    global TX_DEST_ADDR

    global GEM_REF_BITS_T1
    global GEM_REF_PRS_E1
    global GEM_REF_EXT_10MHZ
    global GEM_REF_INT_10MHZ
    global GEM_REF_LINE

    set blade $TX_DEST_ADDR
    set_target 0

    # ----------------------------------------------------------------
    # Now send the command
    # ----------------------------------------------------------------
    send_command [BuildCommand 0x09 3 1 0 0x01]
    set ret [pong]
    set_target $blade

    set ref [expr [lindex $ret 2]]
    set lol [expr [lindex $ret 3]]
    set los [expr [lindex $ret 4]]

    puts -nonewline "Selected Reference:  "

    switch $ref {
        0 {puts "1.544 MHz (T1 BITS)"}
        1 {puts "2.048 MHz (E1 MTS)"}
        2 {puts "10 MHz (external)"}
        3 {puts "10 MHz (internal)"}
        4 {puts "Rx Line"}
    }

    if {$ref != 4} {
        set color(0) "RED"
        set color(1) "YELLOW"
        set color(2) "GREEN"

        puts [format "Selected Reference LOS = %s" $color($los)]
        puts [format "Selected Reference LOL = %s" $color($lol)]
    }

    return $ref
}

######################################################################
# Function Name    : gem_clear_external_timing_ref_alarms
#                  :
# Parameters       : none
#                  :
# Purpose          : Clear any alarm states on the external timing
#                  : ref source currently being used.
######################################################################
proc gem_clear_external_timing_ref_alarms {} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0

    # ----------------------------------------------------------------
    # Send the command
    # ----------------------------------------------------------------
    send_command [BuildCommand 0x09 3 1 0 0x15]

    # ----------------------------------------------------------------
    # check for success
    # ----------------------------------------------------------------
    print_error_on_nack [pong] "External Timing is not available."

}

######################################################################
# Function Name    : gem_is_iptv_using_dsf
#                  :
# Purpose          : *** INTERNAL USE ONLY ***
######################################################################
proc gem_is_iptv_using_dsf {profile} {
    global TX_DEST_ADDR

    set blade $TX_DEST_ADDR
    set_target 0
    send_command [BuildCommand 0xEB 3 $blade $profile 0x10]
	set ret [lrange [pong] 5 end]
    set_target $blade

    return [lindex $ret 0]
}

######################################################################
# Function Name    : gem_enable_dsf
# Parameters       : profile string_id string_content
#                  : string_id: which string to enable (1-8)
#                  : ascii_string: search string
#                  : args:
#                  :   -repeat:  e.g., -repeat=4 means to drop 4 times,
#                  :           then stop.  The default is to drop
#                  :           matches forever; the maximum is 15.
# Purpose          : Turn on DSF string searching for the specified string.
#                  :
######################################################################
proc gem_enable_dsf {profile string_id ascii_string args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {[gem_is_iptv_using_dsf $profile]} {
        if {($string_id < 1) || ($string_id > 8)} {
            puts "No such string #$string_id in DSF:  "
            puts "Please specify string ID 7 or 8."
            return
        } elseif {($string_id != 7) && ($string_id != 8)} {
            puts "String #$string_id is currently in use by IPTV."
            puts "Please specify string ID 7 or 8."
            return
        }
    } elseif {($string_id < 1) || ($string_id > 8)} {
        puts "No such string #$string_id in DSF:  "
        puts "Please specify a string ID between 1 and 8."
        return
    }

    set len [string length $ascii_string]

    if {($len < 1) || ($len > 8)} {
        puts "Search string must be 1-8 characters in length."
        return
    }

    set repeat 16

    foreach a $args {
        if {[regexp -nocase {^-repeat=([0-9\.]+)$} $a tmp repeat]} {
            if {($repeat < 1) || ($repeat > 15)} {
                puts "-repeat must be between 1 and 15."
                return
            }
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    } 

    set blade $TX_DEST_ADDR
    set_target 0

    binary scan $ascii_string c* string_vals

    send_command [BuildCommand [concat 0xEB [expr 6 + $len] $blade $profile \
                                    0x03 $string_id $repeat $string_vals 0] ]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_disable_dsf
# Parameters       : profile string_id
#                  : string_id: which string to enable (1-8)
# Purpose          : Disable the specified DSF search string.
#                  :
######################################################################
proc gem_disable_dsf {profile string_id} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {[gem_is_iptv_using_dsf $profile]} {
        if {($string_id < 1) || ($string_id > 8)} {
            puts "No such string #$string_id in DSF:  "
            puts "Please specify string ID 7 or 8."
            return
        } elseif {($string_id != 7) && ($string_id != 8)} {
            puts "String #$string_id is currently in use by IPTV."
            puts "Please specify string ID 7 or 8."
            return
        }
    } elseif {($string_id < 1) || ($string_id > 8)} {
        puts "No such string #$string_id in DSF:  "
        puts "Please specify a string ID between 1 and 8."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xEB 4 $blade $profile 0x04 $string_id]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_get_dsf_status
# Parameters       : profile
# Purpose          : Display the current configuration for GEM's
#                  : DSF feature on the specified profile.
######################################################################
proc gem_get_dsf_status {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {[gem_is_iptv_using_dsf $profile]} {
        for {set j 1} {$j <= 6} {incr j} {
            puts "String #$j is in use by IPTV."
        }
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xEB 3 $blade $profile 0x01]
    set ret [lrange [pong] 5 end]

    set_target $blade

    set i 0
    while {1} {
        set id [expr "0x[lindex $ret $i]" + 0]
        incr i

        # If the string ID is zero, this signifies that
        # there are no more DSF specifications.
        if {$id == 0} {
            break
        }

        set enabled [expr "0x[lindex $ret $i]" + 0]
        incr i
        set repeat [expr "0x[lindex $ret $i]" + 0]
        incr i
        set len [expr "0x[lindex $ret $i]" + 0]
        incr i

        set namelist [lrange $ret $i [expr $len + $i - 1] ]
        incr i $len
        incr i

        set namechars {}
        foreach a $namelist {
            lappend namechars [format %c "0x$a"]
        }
        set name [join $namechars ""]

        puts -nonewline "String #$id is "

        if {$enabled} {
            puts -nonewline "enabled:  \"$name\" "
            if {$repeat == 16} {
                puts "(repeat infinite)"
            } else {
                puts "(repeat $repeat times)"
            }
        } else {
            puts "disabled."
        }
    }

}

######################################################################
# Function Name    : gem_reset_profile
#                  :
# Parameters       : profile (1-15)
#                  :
# Purpose          : Erase the specified profile including the filters,
#                  : policer settings, delay, and impairments.
######################################################################
proc gem_reset_profile {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 1) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "Invalid network profile $profile:  "
        puts -nonewline "Please specify a profile number between 1 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0xC9 2 $blade $profile]
    pong_check

    set_target $blade
}

######################################################################
# Function Name    : gem_tia921_mode_enable
#                  :
# Parameters       : profile (0-15)
#                  :
# Purpose          : Enable TIA-921 mode on the specified profile.
#                  : Only one profile per blade can be in TIA-921 mode.
######################################################################
proc gem_tia921_mode_enable {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "Invalid network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9A 3 $blade $profile 0x03]
    nack_msg [pong]

    set_target $blade
}


######################################################################
# Function Name    : gem_tia921_mode_disable
#                  :
# Parameters       : profile (0-15)
#                  :
# Purpose          : Disable TIA-921 mode on the specified profile.
#                  : Only one profile per blade can be in TIA-921 mode.
######################################################################
proc gem_tia921_mode_disable {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "Invalid network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9A 3 $blade $profile 0x04]
    nack_msg [pong]

    set_target $blade
}


######################################################################
# Function Name    : gem_tia921_set_params
#                  :
# Parameters       : profile (0-15)
#                  :
#                  : Optional parameters:
#                  :
#                  :   Packet size; controls serialization delay
#                  :   (Must be between 64 and 10000 bytes, inclusive)
#                  :    -pktsize=<pktsize>         (default: 255)
#                  :
#                  :   Interval between packets in ms
#                  :   (Must be between .001 and 1000ms, inclusive)
#                  :    -pktinterval=<pktinterval> (default: 4)
#                  :
#                  :   Enable/Disable bandwidth limitation
#                  :    -bwlimit=<yes/no>          (default: disable)
#                  :
#                  :   Enable/Disable intercontinental delay values
#                  :   in the Core part of the model. (G.1050)
#                  :    -intercontinental=<yes/no> (default: disable)
#                  :
#                  :   Enable/Disable the LANA model
#                  :    -LANA=<enable/disable>     (default: enable)
#                  :
#                  :   Enable/Disable the AccessA model
#                  :    -AccessA=<enable/disable>  (default: enable)
#                  :
#                  :   Enable/Disable the Core model
#                  :    -Core=<enable/disable>     (default: enable)
#                  :
#                  :   Enable/Disable the AccessB model
#                  :    -AccessB=<enable/disable>  (default: enable)
#                  :
#                  :   Enable/Disable the LANB model
#                  :    -LANB=<enable/disable>     (default: enable)
#                  :
#                  :   Default duration of a test.
#                  :    -duration=<time> (default: 2 minutes)
#                  :
#                  :     <time> can be any of the following formats:
#                  :        seconds (e.g. 55)
#                  :        minutes (e.g. 2min[utes])
#                  :        minutes:seconds (e.g. 2:30min[utes])
#                  :        hours (e.g. 1hr|hour)
#                  :        hr:min (e.g. 1:30hr|hour)
#                  :        hr:min:sec (e.g. 1:30:00)
#                  :
#                  :   Default random number seed to use.
#                  :    -seed=<#> (default: 1)
#                  :
#                  :     <#> can be any of the following formats:
#                  :        -seed=0 thru -seed=4294967295 are valid values
#                  :        -seed=none (means keep same random # state
#                  :                    when running without resetting)
#                  :
# Purpose          : This TCL command sets the TIA parameters
#                  : for a given profile.
#                  :
# Example          :   % gem_tia921_set_params 2
#                  :   -pktsize=255 -pktinterval=4ms \
#                  :   -bwlimit=enable -intercontinental=disable \
#                  :   -LANA=enable -AccessA=enable -Core=enable \
#                  :   -LANB=enable -AccessB=enable
######################################################################
proc gem_tia921_set_params {profile args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "Invalid network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set pkt_size 255
    set pkt_interval 4
    set bw_limit 0
    set intercontinental 0
    set LANA 1
    set AccessA 1
    set Core 1
    set AccessB 1
    set LANB 1
    set reset_seed 1
    set seed 1
    set hr 0
    set min 2
    set sec 0

    foreach a $args {
        if {[regexp -nocase {^-pktsize=([0-9]+)$} $a tmp pkt_size]} {
            if {$pkt_size < 64 || $pkt_size > 10000} {
                puts "The pktsize must be between 64 and 10000."
                return
            }
        } elseif {[regexp -nocase {^-pktinterval=([\.0-9]+)(ms)?$} $a tmp pkt_interval]} {
            if {$pkt_interval < .001 || $pkt_interval > 1000} {
                puts "The pktinterval must be between .001ms and 1000ms."
                return
            }
        } elseif {[regexp -nocase {^-bwlimit=(yes|no|disable|enable)} $a tmp enarg]} {
            if {[string compare -nocase $enarg "yes"] == 0} {
                set bw_limit 1
            } elseif {[string compare -nocase $enarg "enable"] == 0} {
                set bw_limit 1
            } elseif {[string compare -nocase $enarg "no"] == 0} {
                set bw_limit 0
            } elseif {[string compare -nocase $enarg "disable"] == 0} {
                set bw_limit 0
            }
        } elseif {[regexp -nocase {^-intercontinental=(yes|no|disable|enable)} $a tmp enarg]} {
            if {[string compare -nocase $enarg "yes"] == 0} {
                set intercontinental 1
            } elseif {[string compare -nocase $enarg "enable"] == 0} {
                set intercontinental 1
            } elseif {[string compare -nocase $enarg "no"] == 0} {
                set intercontinental 0
            } elseif {[string compare -nocase $enarg "disable"] == 0} {
                set intercontinental 0
            }
        } elseif {[regexp -nocase {^-LANA=(yes|no|disable|enable)} $a tmp enarg]} {
            if {[string compare -nocase $enarg "yes"] == 0} {
                set LANA 1
            } elseif {[string compare -nocase $enarg "enable"] == 0} {
                set LANA 1
            } elseif {[string compare -nocase $enarg "no"] == 0} {
                set LANA 0
            } elseif {[string compare -nocase $enarg "disable"] == 0} {
                set LANA 0
            }
        } elseif {[regexp -nocase {^-AccessA=(yes|no|disable|enable)} $a tmp enarg]} {
            if {[string compare -nocase $enarg "yes"] == 0} {
                set AccessA 1
            } elseif {[string compare -nocase $enarg "enable"] == 0} {
                set AccessA 1
            } elseif {[string compare -nocase $enarg "no"] == 0} {
                set AccessA 0
            } elseif {[string compare -nocase $enarg "disable"] == 0} {
                set AccessA 0
            }
        } elseif {[regexp -nocase {^-LANB=(yes|no|disable|enable)} $a tmp enarg]} {
            if {[string compare -nocase $enarg "yes"] == 0} {
                set LANB 1
            } elseif {[string compare -nocase $enarg "enable"] == 0} {
                set LANB 1
            } elseif {[string compare -nocase $enarg "no"] == 0} {
                set LANB 0
            } elseif {[string compare -nocase $enarg "disable"] == 0} {
                set LANB 0
            }
        } elseif {[regexp -nocase {^-AccessB=(yes|no|disable|enable)} $a tmp enarg]} {
            if {[string compare -nocase $enarg "yes"] == 0} {
                set AccessB 1
            } elseif {[string compare -nocase $enarg "enable"] == 0} {
                set AccessB 1
            } elseif {[string compare -nocase $enarg "no"] == 0} {
                set AccessB 0
            } elseif {[string compare -nocase $enarg "disable"] == 0} {
                set AccessB 0
            }
        } elseif {[regexp -nocase {^-Core=(yes|no|disable|enable)} $a tmp enarg]} {
            if {[string compare -nocase $enarg "yes"] == 0} {
                set Core 1
            } elseif {[string compare -nocase $enarg "enable"] == 0} {
                set Core 1
            } elseif {[string compare -nocase $enarg "no"] == 0} {
                set Core 0
            } elseif {[string compare -nocase $enarg "disable"] == 0} {
                set Core 0
            }
        } elseif {[regexp -nocase {^-seed=([0-9]+)$} $a tmp seed]} {
            if {$seed < 0 || $seed > 4294967295} {
                puts "The seed must be between 0 and 4294967295."
                return
            }
            set reset_seed 1
        } elseif {[regexp -nocase {^-seed=none$} $a tmp]} {
            set reset_seed 0
        } elseif {[regexp {^-duration=(.+)$} $a tmp dstr]} {
            if {[regexp -nocase {^\d+$} $dstr sec]} {
                set hr 0
                set min 0
            } elseif {[regexp -nocase {^(\d+)min(ute)?s?$} $dstr tmp min]} {
                set hr 0
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+)min(ute)?s?$} $dstr tmp min sec]} {
                set hr 0
            } elseif {[regexp -nocase {^(\d+)(h|hr|hour)s?$} $dstr tmp hr]} {
                set min 0
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+)(h|hr|hour)s?$} $dstr tmp hr min]} {
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+):(\d+)$} $dstr tmp hr min sec]} {
            } else {
                puts "ERROR:  Unknown duration option $dstr"
                return
            }

        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }

    scan $hr %d hr
    scan $min %d min
    scan $sec %d sec
    set duration [expr ($hr * 3600) + ($min * 60) + $sec]

    if {$duration < 0 || $duration > 1000000} {
        puts -nonewline "ERROR: The duration must be "
        puts "between 0 and 1000000 secs."
        return
    }

    # Convert pkt_interval to us, our maximum resolution,
    # so it can be transmitted as an int
    set pkt_interval [expr round($pkt_interval * 1000)]

    set seedbyte(0) [expr ($seed >> 24) & 0xFF]
    set seedbyte(1) [expr ($seed >> 16) & 0xFF]
    set seedbyte(2) [expr ($seed >> 8) & 0xFF]
    set seedbyte(3) [expr ($seed >> 0) & 0xFF]

    set durbyte(0) [expr ($duration >> 24) & 0xFF]
    set durbyte(1) [expr ($duration >> 16) & 0xFF]
    set durbyte(2) [expr ($duration >> 8) & 0xFF]
    set durbyte(3) [expr ($duration >> 0) & 0xFF]

    set pktibyte(0) [expr ($pkt_interval >> 24) & 0xFF]
    set pktibyte(1) [expr ($pkt_interval >> 16) & 0xFF]
    set pktibyte(2) [expr ($pkt_interval >> 8) & 0xFF]
    set pktibyte(3) [expr ($pkt_interval >> 0) & 0xFF]

    set pktsizebyte(0) [expr ($pkt_size >> 8) & 0xFF]
    set pktsizebyte(1) [expr ($pkt_size >> 0) & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9A 25 $blade $profile 0x02 \
                    $pktibyte(0) $pktibyte(1) $pktibyte(2) $pktibyte(3) \
                    $pktsizebyte(0) $pktsizebyte(1) \
                    $intercontinental $bw_limit  \
                    $LANA $AccessA $Core $AccessB $LANB \
                    $durbyte(0) $durbyte(1) $durbyte(2) $durbyte(3) \
                    $reset_seed \
                    $seedbyte(0) $seedbyte(1) $seedbyte(2) $seedbyte(3)]
    nack_msg [pong] "TIA is not enabled on that blade and profile."

    set_target $blade
}


######################################################################
# Function Name    : gem_tia921_get_params
#                  :
# Parameters       : profile (0-15)
#                  :
#                  : Optional parameters:
#                  :
#                  :   If the user specifies the -verbose option,
#                  :   the parameters are pretty-printed to the
#                  :   screen instead of being returned as a list.
#                  :    -verbose
#                  :
# Purpose          : This TCL command gets the TIA parameters for
#                  : a given profile.
#                  :
#                  : By default, the result is returned as a list,
#                  : where each list element contains one of the
#                  : above options and its values.
######################################################################
proc gem_tia921_get_params {profile args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set verbose 0

    foreach a $args {
        if {[regexp -nocase {^-verbose$} $a tmp]} {
            set verbose 1
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9A 3 $blade $profile 0x01]
    set ret [pong]

    set_target $blade

    if {"0x[lindex $ret 0]" == 0xC7} {
        puts "ERROR: TIA is not enabled on that blade and profile."
        return
    }

    set b [lrange $ret 5 end]

    set pkt_interval     [value_from_array [lrange $b 0 3]]
    set pkt_interval     [expr ($pkt_interval / 1000.0)]
    set pkt_size         [value_from_array [lrange $b 4 5]]
    set intercontinental [value_from_array [lindex $b 6]]
    set bwlimit          [value_from_array [lindex $b 7]]
    set LANA             [value_from_array [lindex $b 8]]
    set AccessA          [value_from_array [lindex $b 9]]
    set Core             [value_from_array [lindex $b 10]]
    set AccessB          [value_from_array [lindex $b 11]]
    set LANB             [value_from_array [lindex $b 12]]
    set duration         [value_from_array [lrange $b 13 16]]
    set reset_seed       [value_from_array [lindex $b 17]]
    set seed             [value_from_array [lrange $b 18 21]]

    set hrs_left   [expr $duration / (60 * 60)]
    set duration   [expr $duration - ($hrs_left * 60 * 60)]
    set mins_left  [expr $duration / 60]
    set duration   [expr $duration - ($mins_left * 60)]
    set secs_left  $duration
    set duration_str ""
    if {$hrs_left > 0} {
        append duration_str [format "%d:" $hrs_left]
    }
    if {($mins_left > 0) || ($hrs_left > 0)} {
        append duration_str [format "%02d:" $mins_left]
    }
    append duration_str [format "%02d" $secs_left]

    if {$verbose == 0} {
        set list params
        lappend params [list -pktinterval $pkt_interval]
        lappend params [list -pktsize $pkt_size]
        lappend params [list -bwlimit [display_enabled $bwlimit]]
        lappend params [list -intercontinental [display_enabled $intercontinental]]
        lappend params [list -LANA [display_enabled $LANA]]
        lappend params [list -AccessA [display_enabled $AccessA]]
        lappend params [list -Core [display_enabled $Core]]
        lappend params [list -LANB [display_enabled $LANB]]
        lappend params [list -AccessB [display_enabled $AccessB]]
        lappend params [list -duration $duration_str]

        if {$reset_seed} {
            lappend params [list -seed $seed]
        } else {
            lappend params [list -seed "none"]
        }
        return $params
    }

    puts "TIA-921/G.1050 on Blade $blade Profile $profile:"
    puts "Packet Interval:  ${pkt_interval}ms"
    puts "Packet Size:      $pkt_size bytes"
    puts -nonewline "Bandwidth Limit:  "
    puts [display_enabled $bwlimit]
    puts -nonewline "Intercontinental: "
    puts [display_enabled $intercontinental]
    puts -nonewline "LANA:             "
    puts [display_enabled $LANA]
    puts -nonewline "AccessA:          "
    puts [display_enabled $AccessA]
    puts -nonewline "Core:             "
    puts [display_enabled $Core]
    puts -nonewline "AccessB:          "
    puts [display_enabled $AccessB]
    puts -nonewline "LANB:             "
    puts [display_enabled $LANB]
    puts "Duration:         $duration_str"
    puts -nonewline "Seed:             "
    if {$reset_seed} {
        puts $seed
    } else {
        puts "none"
    }
}


######################################################################
# Function Name    : gem_tia921_start_test
#                  :
# Parameters       : profile (0-15)
#                  : testname is the name of the test to run (e.g. 133A or 133H)
#                  :
#                  : Optional parameters:
#                  :
#                  :   Duration of the test to run.
#                  :    -duration=<time>
#                  :
#                  :     <time> can be any of the following formats:
#                  :        seconds (e.g. 55)
#                  :        minutes (e.g. 2min[utes])
#                  :        minutes:seconds (e.g. 2:30min[utes])
#                  :        hours (e.g. 1hr|hour)
#                  :        hr:min (e.g. 1:30hr|hour)
#                  :        hr:min:sec (e.g. 1:30:00)
#                  :
#                  :   Random number seed to use.
#                  :    -seed=<#>
#                  :
#                  :     <#> can be any of the following formats:
#                  :        -seed=0 thru -seed=4294967295 are valid values
#                  :        -seed=none (means keep same random # state
#                  :                    when running without resetting)
#                  :
#                  : If not specified, the duration and seed retain
#                  : their previous values.
#                  :
# Purpose          : This TCL command starts a specified test to run
#                  : for a specified amount of time. This command is
#                  : ignored and an error message is printed if a
#                  : test is already in progress.
#                  :
# Example          :   % gem_tia921_start_test 0 -duration=1hr 133A
######################################################################
proc gem_tia921_start_test {profile args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "Invalid network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set reset_seed 0
    set seed 1
    set hr 0
    set min 2
    set sec 0
    set test_specified 0
    set duration_specified 0
    set seed_specified 0

    foreach a $args {
        if {[regexp -nocase {^-seed=([0-9]+)$} $a tmp seed]} {
            if {$seed < 0 || $seed > 4294967295} {
                puts "The seed must be between 0 and 4294967295."
                return
            }
            set seed_specified 1
            set reset_seed 1
        } elseif {[regexp -nocase {^-seed=none$} $a tmp]} {
            set seed_specified 1
            set reset_seed 0
        } elseif {[regexp {^-duration=(.+)$} $a tmp dstr]} {
            if {[regexp -nocase {^\d+$} $dstr sec]} {
                set hr 0
                set min 0
            } elseif {[regexp -nocase {^(\d+)min(ute)?s?$} $dstr tmp min]} {
                set hr 0
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+)min(ute)?s?$} $dstr tmp min sec]} {
                set hr 0
            } elseif {[regexp -nocase {^(\d+)(h|hr|hour)s?$} $dstr tmp hr]} {
                set min 0
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+)(h|hr|hour)s?$} $dstr tmp hr min]} {
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+):(\d+)$} $dstr tmp hr min sec]} {
            } else {
                puts "ERROR:  Unknown duration option $dstr"
                return
            }
            set duration_specified 1
        } elseif {[regexp -nocase {^([0-9]+)([a-h])$} $a tmp testnum testsev]} {
            if {$testnum < 1 || $testnum > 133} {
                puts "ERROR:  Invalid test case '$a'."
                puts "ERROR:  The test case must be between 1 and 133."
                return
            }
            set testsev [string tolower $testsev]
            scan $testsev %c severity
            set test_specified 1
        } elseif {[regexp -nocase {^Custom([0-9]+)$} $a tmp testnum]} {
            if {$testnum == 0} {
                puts "ERROR:  No such custom test."
                return
            }
            set severity 0
            set test_specified 1
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }

    if {$test_specified == 0} {
        puts "ERROR: No test specified."
        return
    }

    scan $hr %d hr
    scan $min %d min
    scan $sec %d sec
    set duration [expr ($hr * 3600) + ($min * 60) + $sec]

    if {$duration < 0 || $duration > 1000000} {
        puts -nonewline "ERROR: The duration must be "
        puts "between 0 and 1000000 secs."
        return
    }

    set seedbyte(0) [expr ($seed >> 24) & 0xFF]
    set seedbyte(1) [expr ($seed >> 16) & 0xFF]
    set seedbyte(2) [expr ($seed >> 8) & 0xFF]
    set seedbyte(3) [expr ($seed >> 0) & 0xFF]

    set durbyte(0) [expr ($duration >> 24) & 0xFF]
    set durbyte(1) [expr ($duration >> 16) & 0xFF]
    set durbyte(2) [expr ($duration >> 8) & 0xFF]
    set durbyte(3) [expr ($duration >> 0) & 0xFF]

    set testnumbyte(0) [expr ($testnum >> 8) & 0xFF]
    set testnumbyte(1) [expr ($testnum >> 0) & 0xFF]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9A 17 $blade $profile 0x10 \
                    $testnumbyte(0) $testnumbyte(1) $severity \
                    $seed_specified $reset_seed\
                    $seedbyte(0) $seedbyte(1) $seedbyte(2) $seedbyte(3) \
                    $duration_specified \
                    $durbyte(0) $durbyte(1) $durbyte(2) $durbyte(3)]
    nack_msg [pong] "TIA is not enabled on that blade and profile."

    set_target $blade
}


######################################################################
# Function Name    : gem_tia921_stop_test
#                  :
# Parameters       : profile (0-15)
#                  :
# Purpose          : This TCL command stops any ongoing test case abruptly.
######################################################################
proc gem_tia921_stop_test {profile} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "Invalid network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9A 3 $blade $profile 0x11]
    nack_msg [pong] "TIA is not enabled on that blade and profile."

    set_target $blade
}


######################################################################
# Function Name    : gem_tia921_status
#                  :
# Parameters       : profile (0-15)
#                  :
# Purpose          : This TCL command returns a the status of the TIA
#                  : mode for the given profile. It immediately returns
#                  : a status code as follows:
#                  :
#                  : If TIA mode is not enabled, it returns the string
#                  : "disabled".
#                  :
#                  : If TIA mode is enabled, but no tests are active it
#                  : returns the string "enabled".
#                  :
#                  : If TIA mode is enabled, and a test is active, it
#                  : returns a list {e.g. {enabled 133A 12:34:00})
#                  : indicating the following:
#                  :
#                  :   * Whether TIA mode is enabled
#                  :   * The name of any ongoing test
#                  :   * The amount of time remaining in the
#                  :     test in [[HH:]MM:]SS format.
#                  :
#                  : If TIA mode is enabled, and a sequence of tests,
#                  : it returns a similar list to the above, but with
#                  : one additional element indicating that more tests
#                  : are pending.
#                  :     {e.g. {enabled 133A 12:34:00 +more})
#                  :
#                  : If the user specifies the -verbose option,
#                  : the parameters are pretty-printed to the
#                  : screen instead of being returned as a list.
#                  :  -verbose
#                  :
#                  :
######################################################################
proc gem_tia921_status {profile args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set verbose 0

    foreach a $args {
        if {[regexp -nocase {^-verbose$} $a tmp]} {
            set verbose 1
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }


    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9A 3 $blade $profile 0x12]
    set b [lrange [pong] 5 end]

    set_target $blade

    set tia_mode [value_from_array [lindex $b 0]]
    if {$tia_mode == 0} {
        if {$verbose == 1} {
            puts "TIA is not enabled on that blade and profile."
            return
        } else {
            return "disabled";
        }
    }

    set in_progress [value_from_array [lindex $b 1]]
    if {$in_progress == 0} {
        if {$verbose == 1} {
            puts "TIA is enabled, but no test is in progress."
            return
        } else {
            return "enabled";
        }
    }

    set retval [list "enabled"]

    set namelist [lrange $b 7 [expr [llength $b] - 2]]
    set namechars {}
    foreach a $namelist {
        lappend namechars [format %c "0x$a"]
    }
    lappend retval [join $namechars ""]

    set duration_left [value_from_array [lrange $b 3 6]]
    set duration_secs [expr $duration_left / 1000]
    set msecs_left    [expr $duration_left % 1000]

    set hrs_left        [expr $duration_secs / (60 * 60)]
    set duration_secs   [expr $duration_secs - ($hrs_left * 60 * 60)]
    set mins_left       [expr $duration_secs / 60]
    set duration_secs   [expr $duration_secs - ($mins_left * 60)]
    set secs_left       $duration_secs

    set left_str ""
    if {$hrs_left > 0} {
        append left_str [format "%d:" $hrs_left]
    }
    if {($mins_left > 0) || ($hrs_left > 0)} {
        append left_str [format "%02d:" $mins_left]
    }
    append left_str [format "%02d" $secs_left]
    # append left_str [format ".%03d" $msecs_left]
    lappend retval $left_str

    set more [value_from_array [lindex $b 2]]
    if {$more == 1} {
        lappend retval "+more"
    }

    if {$verbose == 1} {

        puts "TIA is enabled, and test is in progress."
        puts -nonewline "Time remaining on test [lindex $retval 1]:  "
        puts -nonewline "[lindex $retval 2]"
        if {[llength $retval] == 4} {
            puts " (more tests remaining)"
        } else {
           puts ""
        }
        return
    }

    return $retval
}


######################################################################
# Function Name    : gem_tia921_wait_done
#                  :
# Parameters       : profile (0-15)
#                  : testname is the name of the test to run (e.g. 133A or 133H)
#                  :
#                  : Optional parameters:
#                  :
#                  :   Maximum time to wait for the test to complete.
#                  :    -timeout=<time> (default: infinite)
#                  :
#                  :     <time> can be any of the following formats:
#                  :        seconds (e.g. 55)
#                  :        minutes (e.g. 2min[utes])
#                  :        minutes:seconds (e.g. 2:30min[utes])
#                  :        hours (e.g. 1hr|hour)
#                  :        hr:min (e.g. 1:30hr|hour)
#                  :        hr:min:sec (e.g. 1:30:00)
#                  :
#                  :   Suppress output status to the screen.
#                  :    -quiet
#                  :
#                  :   How often to poll the box in seconds
#                  :    -poll=<polltime> (default: 1 second)
#                  :
#                  :     <polltime> can be any of the following formats:
#                  :        seconds (e.g. 55)
#                  :        minutes (e.g. 2min[utes])
#                  :        minutes:seconds (e.g. 2:30min[utes])
#                  :        hours (e.g. 1hr|hour)
#                  :        hr:min (e.g. 1:30hr|hour)
#                  :        hr:min:sec (e.g. 1:30:00)
#                  :
#                  :     The polltime must be between 1 and 14400 seconds.
#                  :
#                  :     If not using -quiet, this is also how
#                  :     often status msgs are printed.
#                  :
#                  :
# Purpose          : This TCL command waits for any pending or
#                  : ongoing test to finish before returning.
#                  :
#                  : If no tests are ongoing or pending, this
#                  : routine returns immediately.
#                  :
#                  : The user may optionally specify a maximum
#                  : amount of time to wait (in the same format
#                  : as the -duration option for startin a test).
#                  :
#                  : By default, this routine periodically checks
#                  : on the status of the test and prints a nice
#                  : message regarding the test status to the screen.
#                  : This behavior can be suppressed specifying the
#                  : -quiet option.
#                  :
#                  : If a GUI-initiated sequence of multiple TIA
#                  : tests is active, the gem_tia921_wait_done
#                  : command waits till all pending and active
#                  : tests are finished before returning.
######################################################################
proc gem_tia921_wait_done {profile args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set quiet 0
    set hr 0
    set min 0
    set sec 0
    set pollhr 0
    set pollmin 0
    set pollsec 1


    foreach a $args {
        if {[regexp -nocase {^-quiet$} $a tmp]} {
            set quiet 1
        } elseif {[regexp {^-timeout=(.+)$} $a tmp dstr]} {
            if {[regexp -nocase {^\d+$} $dstr sec]} {
                set hr 0
                set min 0
            } elseif {[regexp -nocase {^(\d+)min(ute)?s?$} $dstr tmp min]} {
                set hr 0
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+)min(ute)?s?$} $dstr tmp min sec]} {
                set hr 0
            } elseif {[regexp -nocase {^(\d+)(h|hr|hour)s?$} $dstr tmp hr]} {
                set min 0
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+)(h|hr|hour)s?$} $dstr tmp hr min]} {
                set sec 0
            } elseif {[regexp -nocase {^(\d+):(\d+):(\d+)$} $dstr tmp hr min sec]} {
            } else {
                puts "ERROR:  Unknown timeout option $dstr"
                return
            }
        } elseif {[regexp {^-poll=(.+)$} $a tmp pstr]} {
            if {[regexp -nocase {^\d+$} $pstr pollsec]} {
                set pollhr 0
                set pollmin 0
            } elseif {[regexp -nocase {^(\d+)min(ute)?s?$} $pstr tmp pollmin]} {
                set pollhr 0
                set pollsec 0
            } elseif {[regexp -nocase {^(\d+):(\d+)min(ute)?s?$} $pstr tmp pollmin pollsec]} {
                set pollhr 0
            } elseif {[regexp -nocase {^(\d+)(h|hr|hour)s?$} $pstr tmp pollhr]} {
                set pollmin 0
                set pollsec 0
            } elseif {[regexp -nocase {^(\d+):(\d+)(h|hr|hour)s?$} $pstr tmp pollhr pollmin]} {
                set pollsec 0
            } elseif {[regexp -nocase {^(\d+):(\d+):(\d+)$} $pstr tmp pollhr pollmin pollsec]} {
            } else {
                puts "ERROR:  Unknown timeout option $pstr"
                return
            }
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }

    scan $pollhr %d pollhr
    scan $pollmin %d pollmin
    scan $pollsec %d pollsec
    set poll [expr ($pollhr * 3600) + ($pollmin * 60) + $pollsec]
    if {$poll <= 0 || $poll > 3600} {
        puts -nonewline "ERROR: The poll time must be "
        puts "between 0 and 3600 secs."
    }

    scan $hr %d hr
    scan $min %d min
    scan $sec %d sec
    set timeout [expr ($hr * 3600) + ($min * 60) + $sec]

    set basetime [clock clicks -milliseconds]

    while {1} {
        set status [gem_tia921_status $profile]

        if {[llength $status] == 1} {
            if {![string compare [lindex $status 0] "disabled"]} {
                puts "ERROR:  TIA is not enabled on that blade and profile."
                return
            }
            return "done";
        }

        set elapsedtime [expr ([clock clicks -milliseconds] - $basetime) / 1000]
        if {($timeout > 0) && ($elapsedtime >= $timeout)} {
            return "timeout"
        }

        if {$quiet == 0} {
           puts -nonewline "Time remaining on test [lindex $status 1]:  "
           puts -nonewline "[lindex $status 2]"
           if {[llength $status] == 4} {
               puts " (more tests remaining)"
           } else {
               puts ""
           }
        }

        set wait_secs $poll
        if {$timeout > 0} {
            set remaintime_secs [expr $timeout - $elapsedtime]
            if {$remaintime_secs < $wait_secs} {
                set wait_secs $remaintime_secs
            }
        }
        after [expr $wait_secs * 1000]
    }
}


######################################################################
# Function Name    : gem_tia921_add_custom_test
#                  :
# Parameters       : profile (0-15)
#                  : LanARate in Mbps (1 to 10000)
#                  : LanBRate in Mbps (1 to 10000)
#                  : LanAOcc in % (0 to 100)
#                  : LanBOcc in % (0 to 100)
#                  : AccessARateToCore in kbps (1 to 1e7)
#                  : AccessBRateFromCore in kbps (1 to 1e7)
#                  : AccessAOcc in % (0 to 100)
#                  : AccessBOcc in % (0 to 100)
#                  : AccessAMtu in bytes (63 to 10000)
#                  : AccessBMtu in bytes (63 to 10000)
#                  : CoreDelay in ms (1 to 1000)
#                  : CoreJitter in ms (1 to 1000)
#                  : CoreReorder in % (0 to 100)
#                  : CorePacketLoss in % (0 to 100)
#                  : CoreRouteFlapHit in ms (0 to 1000)
#                  : CoreRouteFlapInt in secs (0 to 15000)
#                  : CoreLinkFailHit in ms (0 to 10000)
#                  : CoreLinkFailInt in secs (0 to 15000)
#                  :
# Purpose          : Create a custom test for TIA.
#                  :
# Returns          : The name of the custom test created.
#                  : This name can then be passed to gem_tia921_start_test.
######################################################################
proc gem_tia921_add_custom_test {profile \
                                 LanARate LanBRate \
                                 LanAOcc LanBOcc \
                                 AccessARateToCore AccessBRateFromCore \
                                 AccessAOcc AccessBOcc \
                                 AccessAMtu AccessBMtu \
                                 CoreDelay \
                                 CoreJitter \
                                 CoreReorder \
                                 CorePacketLoss \
                                 CoreRouteFlapHit \
                                 CoreRouteFlapInt \
                                 CoreLinkFailHit \
                                 CoreLinkFailInt} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    if {($LanARate < 1) || ($LanARate > 10000)} {
        puts "ERROR:  Invalid LanARate value:  $LanARate"
        puts "ERROR:  LanARate must be between 1 and 10000 Mbps."
        return
    }

    if {($LanBRate < 1) || ($LanBRate > 10000)} {
        puts "ERROR:  Invalid LanBRate:  $LanBRate"
        puts "ERROR:  LanBRate must be between 1 and 10000 Mbps."
        return
    }

    if {($LanAOcc < 0) || ($LanAOcc > 100)} {
        puts "ERROR:  Invalid LanAOcc:  $LanAOcc"
        puts "ERROR:  LanAOcc must be between 0% and 100%."
        return
    }

    if {($LanBOcc < 0) || ($LanBOcc > 100)} {
        puts "ERROR:  Invalid LanBOcc:  $LanBOcc"
        puts "ERROR:  LanBOcc must be between 0% and 100%."
        return
    }

    if {($AccessARateToCore < 1) || ($AccessARateToCore > 10000000)} {
        puts "ERROR:  Invalid AccessARateToCore:  $AccessARateToCore"
        puts "ERROR:  AccessARateToCore must be between 1 and 10000000 kbps."
        return
    }

    if {($AccessBRateFromCore < 1) || ($AccessBRateFromCore > 10000000)} {
        puts "ERROR:  Invalid AccessBRateFromCore:  $AccessBRateFromCore"
        puts "ERROR:  AccessBRateFromCore must be between 1 and 10000000 kbps."
        return
    }

    if {($AccessAOcc < 0) || ($AccessAOcc > 100)} {
        puts "ERROR:  Invalid AccessAOcc:  $AccessAOcc"
        puts "ERROR:  AccessAOcc must be between 0% and 100%."
        return
    }

    if {($AccessBOcc < 0) || ($AccessBOcc > 100)} {
        puts "ERROR:  Invalid AccessBOcc:  $AccessBOcc"
        puts "ERROR:  AccessBOcc must be between 0% and 100%."
        return
    }

    if {($AccessAMtu < 63) || ($AccessAMtu > 10000)} {
        puts "ERROR:  Invalid AccessBOcc:  $AccessAMtu"
        puts "ERROR:  AccessAMtu must be between 63 and 10000 bytes."
        return
    }

    if {($AccessBMtu < 63) || ($AccessBMtu > 10000)} {
        puts "ERROR:  Invalid AccessBOcc:  $AccessBMtu"
        puts "ERROR:  AccessBMtu must be between 63 and 10000 bytes."
        return
    }

    if {($CoreDelay < 1) || ($CoreDelay > 1000)} {
        puts "ERROR:  Invalid CoreDelay:  $CoreDelay"
        puts "ERROR:  CoreDelay must be between 1 and 1000 ms."
        return
    }

    if {($CoreJitter < 1) || ($CoreJitter > 1000)} {
        puts "ERROR:  Invalid CoreJitter:  $CoreJitter"
        puts "ERROR:  CoreJitter must be between 1 and 1000 ms."
        return
    }

    if {($CoreReorder < 0) || ($CoreReorder > 100)} {
        puts "ERROR:  Invalid CoreReorder:  $CoreReorder"
        puts "ERROR:  CoreReorder must be between 0% and 100%."
        return
    }

    if {($CorePacketLoss < 0) || ($CorePacketLoss > 100)} {
        puts "ERROR:  Invalid CorePacketLoss:  $CorePacketLoss"
        puts "ERROR:  CorePacketLoss must be between 0% and 100%."
        return
    }

    if {($CoreRouteFlapHit < 0) || ($CoreRouteFlapHit > 1000)} {
        puts "ERROR:  Invalid CoreRouteFlapHit:  $CoreRouteFlapHit"
        puts "ERROR:  CoreRouteFlapHit must be between 0 and 1000 ms."
        return
    }

    if {($CoreRouteFlapInt < 0) || ($CoreRouteFlapInt > 15000)} {
        puts "ERROR:  Invalid CoreRouteFlapInt:  $CoreRouteFlapInt"
        puts "ERROR:  CoreRouteFlapInt must be between 0 and 15000 secs."
        return
    }

    if {($CoreLinkFailHit < 0) || ($CoreLinkFailHit > 10000)} {
        puts "ERROR:  Invalid CoreLinkFailHit:  $CoreLinkFailHit"
        puts "ERROR:  CoreLinkFailHit must be between 0 and 10000 ms."
        return
    }

    if {($CoreLinkFailInt < 0) || ($CoreLinkFailInt > 15000)} {
        puts "ERROR:  Invalid CoreLinkFailInt:  $CoreLinkFailInt"
        puts "ERROR:  CoreLinkFailInt must be between 0 and 15000 secs."
        return
    }

    set CoreReorder    [expr int($CoreReorder * 1e6)];
    set CorePacketLoss [expr int($CorePacketLoss * 1e6)];

    set data [list]
    set data [concat $data [list_from_value $LanARate 4]]
    set data [concat $data [list_from_value $LanBRate 4]]
    set data [concat $data [list_from_value $LanAOcc 2]]
    set data [concat $data [list_from_value $LanBOcc 2]]
    set data [concat $data [list_from_value $AccessARateToCore 4]]
    set data [concat $data [list_from_value $AccessBRateFromCore 4]]
    set data [concat $data [list_from_value $AccessAOcc 2]]
    set data [concat $data [list_from_value $AccessBOcc 2]]
    set data [concat $data [list_from_value $AccessAMtu 2]]
    set data [concat $data [list_from_value $AccessBMtu 2]]
    set data [concat $data [list_from_value $CoreDelay 4]]
    set data [concat $data [list_from_value $CoreJitter 4]]
    set data [concat $data [list_from_value $CoreReorder 4]]
    set data [concat $data [list_from_value $CorePacketLoss 4]]
    set data [concat $data [list_from_value $CoreRouteFlapHit 2]]
    set data [concat $data [list_from_value $CoreRouteFlapInt 2]]
    set data [concat $data [list_from_value $CoreLinkFailHit 2]]
    set data [concat $data [list_from_value $CoreLinkFailInt 2]]

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [eval {BuildCommand 0x9A 55 $blade $profile 0x13} $data]
    set response [pong]

    set_target $blade

    nack_msg $response "TIA is not enabled on that blade and profile."
    if {[is_nack $response]} {
        return
    }

    return [format "Custom%u" [lindex $response 3]]
}


######################################################################
# Function Name    : gem_tia921_show_custom_test
#                  :
# Parameters       : profile (0-15)
#                  : test (custom test name)
#                  :
# Purpose          : Return a list of all of the parameters of the
#                  : specified custom test.
#                  :
#                  : If the user specifies the -verbose option,
#                  : the parameters are pretty-printed to the
#                  : screen instead of being returned as a list.
#                  :  -verbose
#                  :
######################################################################
proc gem_tia921_show_custom_test {profile test args} {
    global TX_DEST_ADDR
    global GEM_MAX_PROFILES

    if {($profile < 0) || ($profile >= $GEM_MAX_PROFILES)} {
        puts -nonewline "No such network profile $profile:  "
        puts -nonewline "Please specify a profile number between 0 and "
        puts "[expr $GEM_MAX_PROFILES - 1]."
        return
    }

    set verbose 0

    foreach a $args {
        if {[regexp -nocase {^-verbose$} $a tmp]} {
            set verbose 1
        } else {
            puts "ERROR:  Invalid argument '$a'."
            return
        }
    }

    scan $test "Custom%u" testnum
    if {($testnum < 1) || ($testnum >= 250)} {
        puts "ERROR:  Invalid custom test:  Custom$testnum"
        return
    }

    set blade $TX_DEST_ADDR
    set_target 0

    send_command [BuildCommand 0x9A 3 $blade $profile 0x14 $testnum]
    set response [pong]

    set_target $blade

    nack_msg $response "TIA is not enabled on that blade and profile."
    if {[is_nack $response]} {
        return
    }

    set b [lrange $response 6 end]

    set LanARate            [value_from_array [lrange $b 0 3]]
    set LanBRate            [value_from_array [lrange $b 4 7]]
    set LanAOcc             [value_from_array [lrange $b 8 9]]
    set LanBOcc             [value_from_array [lrange $b 10 11]]
    set AccessARateToCore   [value_from_array [lrange $b 12 15]]
    set AccessBRateFromCore [value_from_array [lrange $b 16 19]]
    set AccessAOcc          [value_from_array [lrange $b 20 21]]
    set AccessBOcc          [value_from_array [lrange $b 22 23]]
    set AccessAMtu          [value_from_array [lrange $b 24 25]]
    set AccessBMtu          [value_from_array [lrange $b 26 27]]
    set CoreDelay           [value_from_array [lrange $b 28 31]]
    set CoreJitter          [value_from_array [lrange $b 32 35]]
    set CoreReorder         [value_from_array [lrange $b 36 39]]
    set CorePacketLoss      [value_from_array [lrange $b 40 43]]
    set CoreRouteFlapHit    [value_from_array [lrange $b 44 45]]
    set CoreRouteFlapInt    [value_from_array [lrange $b 46 47]]
    set CoreLinkFailHit     [value_from_array [lrange $b 48 49]]
    set CoreLinkFailInt     [value_from_array [lrange $b 50 51]]

    set CoreReorder [expr $CoreReorder / 1e6]
    set CorePacketLoss [expr $CorePacketLoss / 1e6]

    if {$verbose == 0} {
        set list params
        lappend params [list LanARate $LanARate]
        lappend params [list LanBRate $LanBRate]
        lappend params [list LanAOcc $LanAOcc]
        lappend params [list LanBOcc $LanBOcc]
        lappend params [list AccessARateToCore $AccessARateToCore]
        lappend params [list AccessBRateFromCore $AccessBRateFromCore]
        lappend params [list AccessAOcc $AccessAOcc]
        lappend params [list AccessBOcc $AccessBOcc]
        lappend params [list AccessAMtu $AccessAMtu]
        lappend params [list AccessBMtu $AccessBMtu]
        lappend params [list CoreDelay $CoreDelay]
        lappend params [list CoreJitter $CoreJitter]
        lappend params [list CoreReorder $CoreReorder]
        lappend params [list CorePacketLoss $CorePacketLoss]
        lappend params [list CoreRouteFlapHit $CoreRouteFlapHit]
        lappend params [list CoreRouteFlapInt $CoreRouteFlapInt]
        lappend params [list CoreLinkFailHit $CoreLinkFailHit]
        lappend params [list CoreLinkFailInt $CoreLinkFailInt]
        return $params
    }

    puts "TIA-921/G.1050 Custom Test #$testnum"
    puts "LanARate:            $LanARate Mbps"
    puts "LanBRate:            $LanBRate Mbps"
    puts "LanAOcc:             ${LanAOcc}%"
    puts "LanBOcc:             ${LanBOcc}%"
    puts "AccessARateToCore:   $AccessARateToCore kbps"
    puts "AccessBRateFromCore: $AccessBRateFromCore kbps"
    puts "AccessAOcc:          ${AccessAOcc}%"
    puts "AccessBOcc:          ${AccessBOcc}%"
    puts "AccessAMtu:          $AccessAMtu bytes"
    puts "AccessBMtu:          $AccessBMtu bytes"
    puts "CoreDelay:           $CoreDelay ms"
    puts "CoreJitter:          $CoreJitter ms"
    puts "CoreReorder:         ${CoreReorder}%"
    puts "CorePacketLoss:      ${CorePacketLoss}%"
    puts "CoreRouteFlapHit:    $CoreRouteFlapHit ms"
    puts "CoreRouteFlapInt:    $CoreRouteFlapInt secs"
    puts "CoreLinkFailHit:     $CoreLinkFailHit ms"
    puts "CoreLinkFailInt:     $CoreLinkFailInt secs"
}
