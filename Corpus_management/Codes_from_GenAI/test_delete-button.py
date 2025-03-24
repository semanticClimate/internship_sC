<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deletable List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border: 1px solid #ccc;
            margin: 5px 0;
            border-radius: 5px;
            transition: all 0.3s;
        }
        li:hover {
            background-color: #f0f0f0;
        }
        button {
            background-color: #ff4d4d;
            color: white;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 3px;
        }
        button:hover {
            background-color: #ff1a1a;
        }
    </style>
</head>
<body>

<h2>Deletable List</h2>
<ul id="itemList">
    <li>Item 1 <button onclick="deleteItem(this)">Delete</button></li>
    <li>Item 2 <button onclick="deleteItem(this)">Delete</button></li>
    <li>Item 3 <button onclick="deleteItem(this)">Delete</button></li>
</ul>

<script>
    function deleteItem(button) {
        const listItem = button.parentElement;
        listItem.remove();
    }
</script>

</body>
</html>
