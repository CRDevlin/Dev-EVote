<!doctype html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.5">
    <style>
    .error {color: #FF0000;}
    </style>
    <title>CSUCI E-Vote</title>
</head>
<body>
    <form method="post" name="submit" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']);?>">
        <p><strong><span style="font-family:arial,helvetica,sans-serif;">Enter your token</span></strong></p>
        <p><input maxlength="32" size="32" name="token" type="password" value=""></p>
        <span class="error"><?php echo $tokenErr;?></span>
        <button type="submit" name="btnSubmit" value="Submit">Submit</button>
    </form>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    if (empty($_POST["choice"])) {
        $tokenErr = "Choice is required";
    } else {
        $scannedToken = scan_input($_POST["token"])

        if (count($scannedToken) != 32) {
            $tokenErr = "Invalid choice";
        } else {
            //TODO: SAVE TO SQL SERVER
            unset($_SESSION["token"]);
            header('Location: index.php');
        }
    }

    function scan_input($data) {
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }
}?>
