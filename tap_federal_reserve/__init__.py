#!/usr/bin/env python3
import json
import singer
import requests
import pathlib

from singer import utils
from singer.catalog import Catalog
from singer.catalog import CatalogEntry
from singer.schema import Schema

REQUIRED_CONFIG_KEYS = ["start_date", "api_key"]
LOGGER = singer.get_logger()


class TapFred():

    def __init__(self, api_key: str) -> None:
        """Initializes the `TapFred` client object.

        ### Parameters:
        ----
        api_key : str
            The API Key provided by the FRED API.
        """

        # Define the schemas folder.
        self.schemas_folder = pathlib.Path(
            __file__
        ).parents[0].joinpath('schemas')

        self.schemas = {}
        self.resource = 'https://api.stlouisfed.org/fred/series'
        self.api_key = api_key

    def load_schemas(self) -> dict:
        """Loads the tap's schema files found in the
        schemas folder.

        ### Returns:
        ----
        dict :
            A collection of schemas.
        """

        # Read the schema files.
        for file in self.schemas_folder.iterdir():
            with file.open() as file_read:

                # Store the schemas.
                self.schemas[file.stem] = Schema.from_dict(
                    data=json.load(file_read)
                )

    def get_series(self, series_id: str, realtime_start: str = None, realtime_end: str = None) -> dict:
        """Get an economic data series.

        ### Parameters:
        ----
        series_id : str
            The series ID you want to query.

        realtime_start : str (optional, Default=today's date)
            The start of the real-time period. For more information, see 
            Real-Time Periods. YYYY-MM-DD formatted string.

        realtime_end : str (optional, Default=today's date)
            The end of the real-time period. For more information, see 
            Real-Time Periods. YYYY-MM-DD formatted string.

        ### Returns:
        ----
        Dict
            A collection of `Series` resources.
        """

        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'realtime_start': realtime_start,
            'realtime_end': realtime_end
        }

        response = requests.get(url=self.resource, params=params)

        return response.json()

    def do_discover(self) -> Catalog:
        """Runs the tap in Discovery mode.

        ### Returns:
        ----
        Catalog:
            A catalog of stream objects.
        """

        self.load_schemas()

        streams = []
        for stream_id, schema in self.schemas.items():
            # TODO: populate any metadata and stream's key properties here..
            stream_metadata = []
            key_properties = []
            streams.append(
                CatalogEntry(
                    tap_stream_id=stream_id,
                    stream=stream_id,
                    schema=schema,
                    key_properties=key_properties,
                    metadata=stream_metadata,
                    replication_key=None,
                    is_view=None,
                    database=None,
                    table=None,
                    row_count=None,
                    stream_alias=None,
                    replication_method=None,
                )
            )
        return Catalog(streams)

    def do_sync(self, config: dict, state: dict = None, catalog: dict = None) -> None:
        """Sync data from tap source.

        ### Parameters:
        ----
        config : dict
            The `config.json` file that contains information like the API key
            and dates.

        state: dict (optional, Default=None)
            State is a JSON map used to persist information between invocations
            of a tap.
        """

        # Grab the configuration values.
        series_id = config['series_id']
        start_date = config['series_start_date']
        end_date = config['series_end_date']

        # Grab the Series Data.
        data = self.get_series(
            series_id=series_id,
            realtime_start=start_date,
            realtime_end=end_date
        )

        # Load the schema.
        self.load_schemas()

        # Write the Schema.
        singer.write_schema(
            stream_name='fred_series',
            schema=self.schemas['federal_reserve_series'].to_dict(),
            key_properties='timestamp'
        )

        # Write the records.
        singer.write_records(
            stream_name='fred_series',
            records=data['seriess']
        )


@utils.handle_top_exception(LOGGER)
def main():

    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    args_config = args.config

    # Initialize the Tap Fred Client.
    fred_tap = TapFred(api_key=args_config["api_key"])

    # If discover flag was passed, run discovery mode and dump output to stdout.
    if args.discover:
        catalog = fred_tap.do_discover()
        catalog.dump()

    # Otherwise run in sync mode.
    else:
        catalog = args.properties if args.properties else fred_tap.do_discover()
        fred_tap.do_sync(args_config, args.state, catalog)


if __name__ == "__main__":
    main()
