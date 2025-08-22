# Complete Markdown Guide - Testing All Features

This document tests all Markdown features supported by your PDF generator.

## Headers

# Header level 1
## Header level 2  
### Header level 3
#### Header level 4
##### Header level 5
###### Header level 6

## Text emphasis and formatting

**Bold text** or __bold text__

*Italic text* or _italic text_

***Bold and italic text*** or ___bold and italic text___

~~Strikethrough text~~

## Lists

### Unordered list

* First item
* Second item
  * Sub-item 1
  * Sub-item 2
    * Sub-sub-item
* Third item

### Ordered list

1. First item
2. Second item
   1. Numbered sub-item
   2. Another sub-item
3. Third item

### Task list

- [x] Completed task
- [ ] Task in progress
- [ ] Task to do

## Links and references

[Link to Google](https://www.google.com)

[Link with title](https://www.github.com "GitHub Homepage")

Automatic link: https://www.example.com

Automatic email: contact@example.com

## Blockquotes

> This is a simple quote.
> 
> It can span multiple lines.

> This is a quote
>> with a nested quote
>>> and an even more nested quote

## Code

### Inline code

Use `console.log()` to display messages in JavaScript.

Here's a variable `let x = 42;` in the text.

### Code blocks

```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Usage example
console.log(fibonacci(10)); // Output: 55
```

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Test with a list
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers.copy())
print(f"Sorted list: {sorted_numbers}")
```

```sql
SELECT 
    users.name,
    users.email,
    COUNT(orders.id) as total_orders,
    SUM(orders.amount) as total_spent
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE users.created_at >= '2024-01-01'
GROUP BY users.id, users.name, users.email
HAVING COUNT(orders.id) > 0
ORDER BY total_spent DESC
LIMIT 10;
```

### Code without syntax highlighting

```
This is a code block
without syntax highlighting.
It can contain any text.
```

## Tables

### Simple table

| Name | Age | City |
|------|-----|------|
| Alice | 25 | Paris |
| Bob | 30 | Lyon |
| Charlie | 35 | Marseille |

### Table with alignment

| Left | Center | Right |
|:-----|:------:|------:|
| Left-aligned text | Centered text | Right-aligned text |
| Short | Medium | Very long text here |
| A | B | C |

### Complex table

| Feature | Support | Notes |
|---------|---------|-------|
| **Headers** | ✅ | All levels (H1-H6) |
| *Italic* | ✅ | Single and double underscore |
| `Inline code` | ✅ | With backticks |
| ~~Strikethrough~~ | ✅ | With tildes |

## Horizontal separators

Here are different types of separators:

---

***

___

## Line breaks

This is a line.  
This is a new line (with two spaces at the end of the previous one).

This is a new paragraph (with a blank line).

## Character escaping

Here's how to escape special characters:

\*This is not italic\*

\`This is not code\`

\# This is not a header

\[This is not a link\]

## Complex mixed content

### Technical documentation example

The `calculateTotal()` function takes the following parameters:

1. **price** (*number*) - The unit price
2. **quantity** (*number*) - The quantity
3. **taxRate** (*number*, optional) - The tax rate (default: 0.2)

```typescript
interface Product {
    id: string;
    name: string;
    price: number;
    inStock: boolean;
}

function calculateTotal(price: number, quantity: number, taxRate: number = 0.2): number {
    const subtotal = price * quantity;
    const tax = subtotal * taxRate;
    return subtotal + tax;
}

// Usage example
const product: Product = {
    id: "prod-001",
    name: "Laptop",
    price: 999.99,
    inStock: true
};

const total = calculateTotal(product.price, 2, 0.196);
console.log(`Total with tax: ${total.toFixed(2)}€`);
```

> **Important note:** This function doesn't handle error cases like negative values.

### Performance comparison table

| Algorithm | Time Complexity | Space Complexity | Use Cases |
|-----------|----------------|------------------|----------|
| Bubble Sort | O(n²) | O(1) | Small lists, educational |
| Quick Sort | O(n log n) | O(log n) | General purpose |
| Merge Sort | O(n log n) | O(n) | Large datasets |
| Heap Sort | O(n log n) | O(1) | Memory constraints |

### Code with very long lines (wrapping test)

```python
def very_long_function_name_that_exceeds_normal_line_length(parameter_one, parameter_two, parameter_three, parameter_four, parameter_five):
    # This line is intentionally very long to test the automatic wrapping system for code lines in the PDF generator
    result = parameter_one + parameter_two + parameter_three + parameter_four + parameter_five
    
    # Another very long line with lots of text to see how the system handles automatic line breaks
    long_string = "This is an extremely long character string that should be automatically cut by the wrapping system to avoid page overflows"
    
    return result, long_string

# Function call with many parameters on a single very long line
result, message = very_long_function_name_that_exceeds_normal_line_length("parameter 1", "parameter 2", "parameter 3", "parameter 4", "parameter 5")
```

## End of document

This document tests most common Markdown features. It should help verify that your PDF generator correctly handles:

- ✅ Headers of all levels
- ✅ Text formatting (bold, italic, strikethrough)
- ✅ Ordered and unordered lists
- ✅ Links and references
- ✅ Blockquotes
- ✅ Inline code and code blocks
- ✅ Tables with alignment
- ✅ Horizontal separators
- ✅ Automatic wrapping of long code lines

---

*Document generated to test the Markdown PDF generator - © 2024*
