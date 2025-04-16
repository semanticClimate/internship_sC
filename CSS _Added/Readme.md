### CSS Added MY Dictionary WG2 Chapter07

I recently learning **CSS** through tutorials and understood the basic well.

I applied CSS in my own project **IPCC WG02 Chapter07 Dictionary**.

This is my own Dictionary IPCC chapter07 **https://github.com/semanticClimate/internship_sC/blob/suman/wg02chapt07_dict.html**

The dictionary appears like this.

![IPCC Dictionary Screenshot] ("C:\Users\priya\OneDrive\Desktop\internship_sC\CSS _Added\Screenshot 2025-04-16 141537.png", "C:\Users\priya\OneDrive\Desktop\internship_sC\CSS _Added\Screenshot 2025-04-16 141557.png")

## CSS styling - First Update

**Applied CSS:** I added CSS to change the border color to green, increased the margin and padding, set a light grey background, added rounded corners and a box shadow, included smooth hover effects with lift and shadow transition, and improved text readability by setting the font to Arial, font size to 16px, color to #333, and line height to 1.5.

<style>
        /* General style for div with role attribute */
        div[role] {
            border: 2px solid #4CAF50; /* Green border for a clean look */
            margin: 10px;
            padding: 15px;
            background-color: #f9f9f9; /* Light grey background */
            border-radius: 8px; /* Rounded corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
            transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth hover effect */
        }

        /* Hover effect */
        div[role]:hover {
            transform: translateY(-5px); /* Slight lift on hover */
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Stronger shadow on hover */
        }

        /* Adding style for better readability */
        div[role] p {
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            color: #333;
            line-height: 1.5;
        }
    </style>

**Effect on Dictionary:** After applying the above CSS, The dictionary entries now appear as clean, modern cards with better spacing and visual appeal. The green borders and shadows make each entry stand out, while the hover effect adds interactivity. The improved font and layout enhance readability, making the content easier and more pleasant to read.

**Updated View:** This is how the dictionary looks after the first CSS update:["C:\Users\priya\OneDrive\Desktop\internship_sC\CSS _Added\Screenshot 2025-04-16 150101.png","C:\Users\priya\OneDrive\Desktop\internship_sC\CSS _Added\Screenshot 2025-04-16 150123.png","C:\Users\priya\OneDrive\Desktop\internship_sC\CSS _Added\Screenshot 2025-04-16 150151.png"]

This is the link **https://github.com/semanticClimate/internship_sC/blob/suman/wg02chapt07_dict_N.html** to my dictionary with the applied CSS Style.

## CSS Styling  - second Update

I applied the following CSS,
 <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdada, sans-serif;
            background-color: #f0f4f8;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            color: #333;
        }

        div[role="ami_dictionary"] {
            display: flex;
            flex-direction: column;
            gap: 20px;
            max-width: 900px;
            width: 100%;
        }

        div[role="ami_entry"] {
            background: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: flex-start;
            gap: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 5px solid #4CAF50;
        }

        div[role="ami_entry"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.2);
        }

        div[role="ami_entry"] img {
            width: 120px;
            height: 120px;
            border-radius: 12px;
            object-fit: cover;
            border: 3px solid #4CAF50;
            transition: transform 0.3s ease;
        }

        div[role="ami_entry"]:hover img {
            transform: scale(1.05);
        }

        .entry-text {
            flex:1;
        }

        .entry-text b {
            color: #4CAF50;
            font-size: 20px;
            font-weight: 600;
            display: block;
            margin-bottom: 8px;
        }
    </style> 
    and it resulted in the following changes. The ddictionary now looks like this.
    ![IPCC Dictionary] ("C:\Users\priya\OneDrive\Desktop\internship_sC\CSS _Added\Screenshot 2025-04-16 142803.png","C:\Users\priya\OneDrive\Desktop\internship_sC\CSS _Added\Screenshot 2025-04-16 142823.png")

    The updated CSS significantly improves the UI and UX of the dictionary entries. It transforms the plain, bordered layout into a modern card-based design with better visuals, interactivity, and readability. Enhancements include image support, font improvements, color theming (green for consistency), and smooth hover animations that make the interface more engaging and accessible.
    
    This is the link **https://github.com/semanticClimate/internship_sC/blob/suman/wg02chapt07_dict%20%20new.html** to my dictionary with the applied CSS styles.






