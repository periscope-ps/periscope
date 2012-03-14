// Personal JavaScript utility functions
// RCSID: $Id$


// Format #secs in a more readable form
fmt_interval = function(sec) {
    dy = Math.floor(sec/86400)
    hr = Math.floor((sec%86400)/3600)
    mn = Math.floor((sec%3600)/60)
    sc = sec % 60
    if (dy == 0 && hr == 0 && mn == 0) {
        return sc + "s"
    }
    if (dy == 0 && hr == 0) {
        return mn + "m "+ sc + "s"
    }
    if (dy == 0) {
        return hr +"h " + mn + "m " + sc + "s"
    }
    return dy + "d "+ hr +"h " + mn + "m " + sc + "s"
}
