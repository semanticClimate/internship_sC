<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deletable List</title>

    <!-- CSS Styles -->
    <style>
        /* Styling for the entire page */
        body {
            font-family: Arial, sans-serif;   /* Set font style */
            max-width: 600px;                 /* Limit the width of the content */
            margin: 0 auto;                   /* Center the content horizontally */
        }

        /* Styling for the unordered list */
        ul {
            list-style: none;                 /* Remove bullet points */
            padding: 0;                       /* Remove default padding */
        }

        /* Styling for each list item */
        li {
            display: flex;                    /* Use flexbox for alignment */
            justify-content: space-between;   /* Space text and button apart */
            align-items: center;              /* Center content vertically */
            padding: 10px;                    /* Add space around the content */
            border: 1px solid #ccc;           /* Add a light border */
            margin: 5px 0;                    /* Add spacing between items */
            border-radius: 5px;               /* Round the corners */
            transition: all 0.3s;             /* Smooth transition effect */
        }

        /* Hover effect on list items */
        li:hover {
            background-color: #f0f0f0;        /* Light gray background on hover */
        }

        /* Styling for the delete button */
        button {
            background-color: #ff4d4d;        /* Red background color */
            color: white;                     /* White text color */
            border: none;                     /* Remove border */
            padding: 5px 10px;                /* Add padding */
            cursor: pointer;                  /* Show pointer cursor on hover */
            border-radius: 3px;               /* Round button corners */
        }

        /* Hover effect on the button */
        button:hover {
            background-color: #ff1a1a;        /* Darker red on hover */
        }
    </style>
</head>
<body>

<!-- Page Title -->
<h2>Deletable List</h2>

<!-- Unordered List with List Items -->
<ul id="itemList">
    <!-- Each list item has text and a delete button -->
    <li>Item 1 <button onclick="deleteItem(this)">Delete</button></li>
    <li>Item 2 <button onclick="deleteItem(this)">Delete</button></li>
    <li>Item 3 <button onclick="deleteItem(this)">Delete</button></li>
</ul>

<!-- JavaScript Function -->
<script>
    // Function to delete the clicked list item
    function deleteItem(button) {
        const listItem = button.parentElement;  // Get the parent <li> element of the button
        listItem.remove();                      // Remove the list item from the DOM
    }
</script>

</body>
</html>
