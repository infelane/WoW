<?php
ini_set('display_errors',1);  // For Error Reporting
error_reporting(E_ALL);       // For Error Reporting

//This is the URL where the Auction Data Status can be downloaded from
//It is locale and realm specific, but contains data for both factions and neutral AH
$status_URL = "http://us.battle.net/api/wow/auction/data/boulderfist";
//This is where we'll store the resultant plain text JSON of the HTTP request
$JSON = null; //Initially set to null, since we have No JSON yet

for($attempt = 0; $attempt < 3; $attempt++) { //Try 3 times to fetch status URL
	$JSON = file_get_contents($status_URL); //Attempt to fetch, then check Response Header
	if( !$JSON && isset($http_response_header) && strstr($http_request_header[0], '503') )
		continue; //503 response: server was busy, so try again
	else
		break; //$JSON is populated, must be a 200 response
}

if(!$JSON) die("Could not get JSON file"); //Terminate script if we failed to get JSON

$AH_status = json_decode($JSON,true);  //decode the JSON into an associative

print_r($AH_status);  //Print human readable information, could also use var_dump

?>