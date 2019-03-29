General Notes
=============

Fonts
-----

* OpenSceneryX font (for header, 'X', 'Enhanced By…' etc.) is Book Antiqua Bold


Website Homepage editing
------------------------

1. Editing the home page, or switching between visual and text editing, will usually strip out the spans around the `<h2>` text alongside the glass numbers. It should be:

    ```html
    <h2><img class="icon" src="https://www.opensceneryx.com/doc/glass_numbers_x.png" alt="1" /><span>Title Goes Here</span></h2>
    ```
2. Editing the home page, or switching between visual and text editing, can sometimes strip out the extra carriage returns in the first PayPal donation block  It should be:

    ```html
    If you like the library,
    please consider supporting it

    <input alt="PayPal – The safer, easier way to pay online!" name="submit" …
    ```
