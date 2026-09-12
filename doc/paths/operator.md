# Learning Path: Platform Operators

**This path is for you if** you deploy and run Dorieh for others —
standing up the database, executing and monitoring workflows, and
keeping the platform healthy — without necessarily writing data models
yourself.

**At the end you will be able to** provision the PostgreSQL backend,
run a full pipeline with Toil, monitor long-running database
operations, and manage access to the resulting tables.

## The path

1. **Understand the moving parts** with the deployment overview in the
   [Introduction](../home.md) and
   [What is Data Platform](../rationale.md): a PostgreSQL DBMS, a CWL
   runner, and the Dorieh Python package.
2. **Provision the backend.** The
   [with-postgres examples directory](https://github.com/ForomePlatform/dorieh/tree/main/examples/with-postgres)
   provides a Docker Compose stack (plain PostgreSQL, or PostgreSQL
   with Superset) and the `database.ini` convention;
   [Database Connections](../DBConnections.md) documents how workflows
   reference named connections.
3. **Run a real pipeline**: follow the
   [Medicare example](../medicare-example.md) with the synthetic
   dataset — it exercises ingestion, in-database processing, and the
   dashboard, exactly as a production run would.
   [Data Processing Pipelines](../pipelines.md) covers the runner
   options (Toil job stores, restarts, work directories) and
   troubleshooting.
4. **Monitor and maintain**:
   [Monitoring database activity](../MonitoringDB.md) for watching
   long-running operations such as indexing;
   the [grant tool](../pipeline/grant.md) for giving analysts read
   access to newly created tables.
5. **Know the internals** when something misbehaves:
   [Data Platform Internals](../guts.md) and
   [Deployment](../deployment.md).

## Going deeper

* [Docker containers for Dorieh](../docker_readme.md) — building and
  customizing the images.
* [Platform capabilities](../capabilities.md) — the how-to guides your
  users will follow; knowing them helps you support them.
