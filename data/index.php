<?php
session_start();
?>
<!doctype html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.5">
    <style>
    .error {color: #FF0000;}
    .message {color: #00FF00;}
    </style>
    <title>CSUCI E-Vote</title>
</head>
<body>
    <form method="post" name="submit" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']);?>">
        <p><strong><span style="font-family:arial,helvetica,sans-serif;">Enter your token</span></strong></p>
        <p><input maxlength="32" size="32" name="token" type="password" value=""></p>
        <p><span class="message"><?php echo $success;?></span></p>
        <p><span class="error"><?php echo $tokenErr;?></span></p>
        <p><button type="submit" name="btnSubmit" value="Submit">Submit</button></p>
    </form>

<?php
function scan_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

function isValid($token) {
    return 0
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST["token"])) {
        $tokenErr = "Token is required";
    } else {
        if (count($_POST["token"]) != 32) {
            $tokenErr = "Invalid token";
        } else {
            //Validate token
            $scannedToken = scan_input($_POST["token"])
            // check if name only contains letters, numbers and whitespace
            if (!preg_match("/^[a-zA-Z0-9]*$/", $scannedToken)) {
                $tokenErr = "Invalid token";
            } else {
                //Check is token is valid
                if(isValid($token) {
                    $_SESSION["token"] = $scannedToken;
                    header('Location: vote.php');
                } else {
                    $tokenErr = "Invalid token";
                }
            }
        }
    }
} else if ($_SERVER["REQUEST_METHOD"] == "GET") {
    if(isset($_GET['result'])) {
        $success = filter_var($_GET['result'], FILTER_VALIDATE_BOOLEAN)
        if($result) {
            $success = "Vote saved successfully."
        } else {
            $error = "Error saving vote. Please consult your administrator."
        }
    }
}?>


</body>
</html>
