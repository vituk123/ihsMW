# Convert Agricultural Units to Kilograms

Converts reported harvest units (e.g., Pails, Oxcarts, Heaps) into
standard kilograms using official NSO crop-specific conversion factors.

## Usage

``` r
ihs_convert_units(data, qty_col, unit_col, crop_col, unmapped = "warn")
```

## Arguments

- data:

  A data.frame

- qty_col:

  The name of the column containing the quantity

- unit_col:

  The name of the column containing the unit code or name

- crop_col:

  The name of the column containing the crop code

- unmapped:

  Action to take when a unit cannot be mapped: \`"warn"\` (default),
  \`"error"\`, or \`"ignore"\`.

## Value

A data.frame with a new `qty_col_kg` column.
