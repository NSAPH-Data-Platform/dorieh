# Basic Dorieh Examples (not using backend)

The main example here is [climate-example.cwl](climate-example.cwl), a
three-step CWL workflow that needs no database backend: it downloads a
NetCDF file with gridded (gridMET) climate data, downloads shapefiles for
the selected geography from the US Census website, and aggregates the
gridded values over ZCTA (or county) polygons into a compressed CSV file
with three columns: the variable value (by default `tmmx`, maximum daily
temperature), `date` and `zcta`.

To run it you need a CWL runner such as Toil (see the
[general README](../README.md) for installation) and the required
`--date` argument:

```shell
toil-cwl-runner --retryCount 1 --cleanWorkDir never --outdir tmmx --workDir . climate-example.cwl --date 2020-10-03
```

The narrated version of this example, including Docker-based options, is
[Example of a workflow: aggregating a climate variable](https://foromeplatform.github.io/dorieh/Example-climate-workflow.html)
(source: `doc/Example-climate-workflow.md`).

For the full database-backed Bronze/Silver/Gold (medallion) pipeline that
continues from this CSV, see [../with-postgres/climate](../with-postgres/climate)
and the tutorial
[Building a Bronze–Silver–Gold Climate Pipeline](https://foromeplatform.github.io/dorieh/tutorial/climate/building-climate-pipeline.html).

This directory also contains [example_request.yaml](example_request.yaml),
a sample data-request file described in the
[User Requests documentation](https://foromeplatform.github.io/dorieh/UserRequests.html).
