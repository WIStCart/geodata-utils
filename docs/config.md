# Configure Geodata Utilities

## Open Config File
Run the command below to open your config for editing:
```bash
gu_config -e
```

## Settings

### Solr Connections

You can configure your Solr connections under `solr instances`. Add any number of connections using the following format:
```yaml
solr instances:
  my-server-name:
    url: "https://geodata-dev.shc.wisc.edu/solr/geodata-core/"
    username: "solrusername"
    password: "mypasswordforsolr"
```

You can replace `my-server-name` with whatever you want to call your server. The `url` points to the Solr core.

### Error Checks

Geodata Utils uses the config file to decide what error checks are on or off by default. This is set in the `error-checks` section of the config, an example of which is shown below.

```yaml
error-checks:
  properties-not-null: ["dc_title_s", "dc_identifier_s", "layer_slug_s", "solr_geom", "dct_provenance_s", "dc_rights_s", "geoblacklight_version", "dc_creator_sm", "dc_description_s", "dct_references_s", "dct_temporal_sm", "solr_year_i", "layer_modified_dt"]
  identifier-layer-slug-match: true
  temporal-contains-solr-year: true
  title-contains-solr-year: true
  references-contains-solr-year: false
  existing-uid: true
```

For `properties-not-null`, list all the properties you want to ensure are not empty or missing. Missing means not included in the JSON file; empty means an empty string, i.e. `""`. It will fail on other types like an empty array `[]`.

The other error checks are turned on or off using `true` or `false` respectively. For instance, in the example above, all the error checks are turned on except for `references-contains-solr-year`.

### Logging

The entire logging config is contained in the `log` section. See the [python `logging` library documentation](https://docs.python.org/3/library/logging.config.html) for detailed information on configuration of the `logging` library. But for use here, you most likely will only be interested in changing the logging level.

To change the logging level look under `handlers` and find `console` or `file`. `console` is the config used for logging to your console and `file` is the config used for logging to `gedatautils.log`. Below is an example of the `handlers`.

```yaml
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    filters: [indent]
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: default
    filters: [indent]
    filename: geodatautils.log
    mode: w
    encoding: utf8
```

By changing the `level` in either handler, you will change how verbose the logging is. By default Geodata Utils logs more detailed information in the log file than to console because its `level` is set to `DEBUG`. But you could change `console`'s  `level` to `DEBUG` as well if you would like to see that level of detail in the console.

To read about all the available logging levels see the python `logging` documentation about [Logging Levels](https://docs.python.org/3/library/logging.html#logging-levels).

In geodatautils we use the levels as follows:
| Level | Use |
| :-- | --- |
| `DEBUG` | Detailed information to help with debugging. |
| `INFO` | Most messages to tell you what the code is doing. |
| `WARNING` | Letting the user know about something important, but continue running. |
| `ERROR` | Used for logging errors that are found. |
| `CRITICAL` |  |

### Metadata Schema

In the `metadata-schema` section you can configure the metadata schema options under `options`. Give the option a name for the property then for the value enter the filename. The metadata schema files are located in `geodatautils/config/schemas`.

The default schema is set in `default`. When a schema is needed and not specified, for instance when using `update_solr` instead of the library directly, the default schema is used.

An example of the `metadata-schema` section is below.

```yaml
metadata-schema:
  options:
    geoblacklight-aardvark: geoblacklight-schema-aardvark.json
    geoblacklight-1: geoblacklight-schema-1.0.json
    geoblacklight-1-wisc: geoblacklight-schema-1.0-wisc.json
  default: geoblacklight-1-wisc
```

In this example `geoblacklight-1-wisc` is being used by `update_solr` as it is set as the default.