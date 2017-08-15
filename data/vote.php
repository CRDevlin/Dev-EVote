<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST["token"])) {
        $tokenErr = "Token is required";
    } else if (count($_POST["token"]) != 32) {
        $tokenErr = "Invalid token";
    } else {
        // check if name only contains letters, numbers and whitespace
        if (!preg_match("/^[a-zA-Z0-9]*$/",$_POST["token"])) {
          $tokenErr = "Invalid format";
        }
    }
}?>
