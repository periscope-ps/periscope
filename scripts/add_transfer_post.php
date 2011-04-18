<?php

// Work out the data
$wannasay = array (
        "t_id" => "grid-0044",
	"status" => "active",
        "dst" => "dtn01.nersc.gov",
	"src" => "endpoint1.tutorial.globus.org",
	"sport" => "45333",
	"dport" => "2811",
	"user" => "kissel",
	"misc" => "woo"
        );
 
$dataels = array();
foreach (array_keys($wannasay) as $thiskey) {
	array_push($dataels,urlencode($thiskey) ."=". urlencode($wannasay[$thiskey]));
}
$data = implode("&",$dataels);

// work out the request

$header =
         "POST /topology/add_transfer HTTP/1.1\n" .
         "Host: lyra.damsl.cis.udel.edu\n" .
         "Content-Type: application/x-www-form-urlencoded\n" .
         "Content-Length: " . strlen($data) . "\n\n" .
         $data . "\n";

// establish the connection and send the request

$s = socket_create(AF_INET, SOCK_STREAM, 0);
$z = socket_connect($s, gethostbyname("192.168.1.20"), 8000);
socket_write ($s, $header, strlen($header));

$header = "";

while (true) {
	if (strlen($c = socket_read($s, 1))) {
		$header .= $c;
        }
	else
		break;
}

socket_close($s);
print nl2br(htmlspecialchars($header));

?> 
