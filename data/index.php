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
    <form method="post" name="submit" action="vote.php">
        <p><strong><span style="font-family:arial,helvetica,sans-serif;">Enter your token</span></strong></p>
        <p><input maxlength="32" size="32" name="token" type="password" value="">
        <button type="submit" id="btnSubmit" value="Submit">Submit</button>
    </form>
</body>
</html>
