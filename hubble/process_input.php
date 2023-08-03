<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the root folder path
    $rootFolder = $_SERVER['DOCUMENT_ROOT'] . '/hubble/';

    // Sanitize and retrieve user input
    $search_url = $_POST["search_url"];
    $search_query = $_POST["search_query"];

    // Construct the command to execute input.py
    $inputCommand = "python $rootFolder/backend/crawl.py $search_url";
    $inputCommand .= " 2>&1";  // Redirect stderr to stdout to capture the output

    // Execute input.py and capture the output
    $inputOutput = shell_exec($inputCommand);

    // Display the output of input.py (for debugging purposes)
    // echo "Execution Result:\n";
    // echo nl2br($inputOutput);

    // Construct the command to execute search.py
    $searchCommand = "python $rootFolder/backend/search.py \"$search_query\"";
    $searchCommand .= " 2>&1";  // Redirect stderr to stdout to capture the output

    // Execute search.py and capture the output
    $searchOutput = shell_exec($searchCommand);

    // Display the output of search.py (for debugging purposes)
    // echo "\nSearch Results:\n";
    // echo nl2br($searchOutput);

    // Display confirmation for successful execution
    // echo "\nInput.py and Search.py have been executed successfully.";



    // Redirect to the search result page after processing the input
    header("Location: search_result.php");
    exit;
}
?>
