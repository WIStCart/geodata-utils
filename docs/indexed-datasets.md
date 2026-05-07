# Indexed Datasets

## Check URLs
Check URLs in geojson of indexed datasets to confirm they resolve.

### Usage

```text
indexed check-urls [-h] [-v] searchPath

positional arguments:
  searchPath     Path to geojson or geojsons.

options:
  -h, --help     show this help message and exit
  -v, --verbose  Write successful responses to log.
```

### Example

```bash
# Write only bad requests to log
indexed check-urls "test datasets/"

# Write all responses to log
indexed check-urls "test datasets/adams-2010-BareEarthPointsLAS.geojson" -v
```

## Coordinate Precision
Read indexed dataset GeoJSON, reduce coordinate precision, and output to specified directory.

### Usage

```text
indexed coordinate-precision [-h] [-p PRECISION] [-i INDENTATION] [-s] [-v] inPath outPath

positional arguments:
  inPath                Path to geojson or geojsons.
  outPath               Output path to place updated geojsons.

options:
  -h, --help            show this help message and exit
  -p, --precision PRECISION
                        How many digits after the decimial. (default=4)
  -i, --indentation INDENTATION
                        Indent level. (default=None)
  -s, --skip-feature    Gracefully skip feature instead of entire dataset if there is an unsupported geometry type.
  -v, --verbose         Write successful responses to log.
```

### Example

```bash
# Use the default of four digits after the decimal
indexed coordinate-precision test/ test/output/

# Reduce precision to three digits, indentation of 2, and log all datasets processed
indexed coordinate-precision test/ test/output/ -p 3 -i 2 -v
```

## Minify GeoJSON
Minify geojson to have no return/new lines and no indentation. Optionally choose an indentation level.

### Usage

```text
indexed minify-geojson [-h] [-i INDENTATION] [-v] path

positional arguments:
  path                  Path to geojson or geojsons.

options:
  -h, --help            show this help message and exit
  -i, --indentation INDENTATION
                        Indent level. (default=None)
  -v, --verbose         Write successful responses to log.
```

### Example

```bash
# Use the default to minify
indexed minify-geojson "test/"

# Use and indentation level of four
indexed minify-geojson "test/" -i 4
```

## Update Website URLs
Update websiteUrl of geojson to specified new url.

### Usage

```text
indexed update-url [-h] path newUrl

positional arguments:
  path        Path to geojson or geojsons.
  newUrl      The new websiteUrl.

options:
  -h, --help  show this help message and exit
```

### Example

```bash
indexed update-url "test/" "https://www.sco.wisc.edu/"
```

## Remove Missing Tiles
Remove tiles from index geojson where downloadUrl returns 404.

### Usage

```text
indexed remove-missing-tiles [-h] [-i INDENTATION] inPath outPath

positional arguments:
  inPath                Path to geojson or geojsons.
  outPath               Output path to place updated geojsons.

options:
  -h, --help            show this help message and exit
  -i, --indentation INDENTATION
                        Indent level. (default=None)
```

### Example

```bash
# Remove missing tiles from datasets in "test datasets" and place the outputs in "test datasets\output" 
indexed remove-missing-tiles "test datasets" "test datasets\output"   
```

