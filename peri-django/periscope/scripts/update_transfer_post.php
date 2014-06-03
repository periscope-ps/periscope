<?php

// Work out the data
$wannasay = array (
        "t_id" => "grid-0003",
	"status" => "done",
        );
 
$dataels = array();
foreach (array_keys($wannasay) as $thiskey) {
	array_push($dataels,urlencode($thiskey) ."=". urlencode($wannasay[$thiskey]));
}
$data = implode("&",$dataels);

// work out the request

$header =
         "POST /topology/update_transfer HTTP/1.1\n" .
         "Host: localhost\n" .
         "Content-Type: application/x-www-form-urlencoded\n" .
         "Content-Length: " . strlen($data) . "\n\n" .
         $data . "\n";

// establish the connection and send the request

$s = socket_create(AF_INET, SOCK_STREAM, 0);
$z = socket_connect($s, gethostbyname("localhost"), 8000);
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
