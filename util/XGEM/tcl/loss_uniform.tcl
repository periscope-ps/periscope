catch {cd tcl/}
source anue_tcl_library.tcl

set loss [lindex $argv 0]
if {$loss > 0} {
    set rloss [expr int(100/$loss)]
} else {
    set rloss 0
}

est_com 149.165.150.100:2003:1
puts "Setting packet loss on Blade #1 to $loss% (1 in $rloss)"
if {$rloss > 0} {
    gem_enable_pkt_drop 0 $STAT_DISTRIB(UNIFORM) 1 $rloss
} else {
    gem_disable_pkt_drop 0
}
close_com

est_com 149.165.150.100:2003:3
puts "Setting packet loss on Blade #3 to $loss% (1 in $rloss)"
if {$rloss > 0} {
    gem_enable_pkt_drop 0 $STAT_DISTRIB(UNIFORM) 1 $rloss
} else {
    gem_disable_pkt_drop 0
}
close_com
