Census Variable File Structure
==============================

The variables used to create the census data using the ``get_census``
package must be formally described in a yaml file. Each variable is defined by a top
level entry in this file. The format for a variable is as follows: ::

    <var_name>:
        <year>:
            <source>:
                num:
                     - <numerator_variable_1>
                     - <numerator_variable_2>
                [den]:
                     - <denominator_variable_1>
                     - <denominator_variable_2>


These descriptions provide instructions to the code on which variables
to ask for from which api and how to calculate the desired variable from
the information available in the API.

Field Definitions
-----------------

  - `var_name`: The user chosen name for a variable
  - `year`: Which year the specification should be used for. The code
    uses the specification for the closest year to the input year that
    is current with or after the input year.
  - `source`: This should be either “census” or “acs”. If it is census,
    the code knows to make the call for this variable from the decennial
    census, and if acs the code uses the 5 year ACS data. As a reminder,
    decennial census data is available in 2000 and 2010, and ACS data is
    available 2009-2018. Some variables present in the 2000 census are
    not available in the 2010 decennial census.
  - `num`: This field should always be named “num”. All variables listed
    in this field are summed and divided by the sum of the `den`
    variables. If no `den` field is present, the sum of these fields
    will be the value reported for the variable
  - `den`: An optional field. This must always be named `den`. The
    variables listed here are summed, and then the sum of the numerator
    variables is divided by this to produce the final reported value.

Examples
--------

- % of the population that is Black, ::

     blk_pct:
        2000:
            census:
                num: P007003
                den: P007001
        2009:
            acs:
                num: B02001_003
                den: B02001_001
        2010:
            census:
                num: P006003
                den: P006001
        2018:
            acs:
                num: B02001_003
                den: B02001_001

Here a variable named ``blk_pct`` will be created. In 2000, the census
data will be used, and the variable will be calculated as
``P007003/P007001``. In 2009, ACS data will be used, and the variable will
be calculated as ``B02001_003/B02001_001``. In 2010, back the the census
data and the variable will be calculated as ``P007003/P007001``. Then
finally, from 2011-2018, ACS data will be used and the variable will be
calculated as ``B02001_003/B02001_001``.

- Median Household Income: ::

    median_household_income:
        2000:
            census:
                num: P053001
        2018:
            acs:
                num: B19013_001


Here a variable named ``median_household_income`` will be created. Note
the lack of a denominator. In 2000, the census variable ``P053001`` is
reported. This value was missing from the 2010 census, so from 2009-2018
the acs variable ``B19013_001`` will be used instead.

Skipping years for a Variable
-----------------------------
Sometimes, you may want to skip getting data for a variable for a given year.
The most common reason to do this is when working with ZCTAs. ZCTA level data
is not available from the 5 year ACS (acs5) for 2009 and 2010, despite the acs5 being
available in those years. To further complicate things, ZCTAs are available for the
decennial census in 2010. If you do not provide instructions on how to handles those
years and you try to query the ACS for ZCTAs, you query will hit an error and fail.

To handle this, instead of specifying a data set in your variable for a given year,
you can instead write "``skip``" for that year.

For example, a file trying to get ZCTA level poverty rates
and population might look something like this: ::

    population:
        2000:
            census:
                num: P001001
        2009: skip
        2010:
            census:
                num: P001001
        2018:
            acs:
                num: B01001_001
    poverty:
        2000:
            census:
                num:
                    - P087002
                den:
                    - P087001
        2010: skip
        2018:
            acs:
                num:
                    - B17001_002
                den:
                    - B17001_001

For ``population``, only 2009 will be skipped, but for ``poverty``,
2009 and 2010 will be skipped.

Census Variable Documentation
-----------------------------

Assembling these files will require reading through the census variable documentation,
which can be quite tedious, especially when trying to figure out how to assemble more
complex estimates. Links to this documentation can be found here:


  - 2000 Census:
      - SF1 (Whole US sample, not all questions asked):
        https://api.census.gov/data/2000/sf1/variables.html
      - SF3 (more detailed, smaller sample):
        https://www.census.gov/data/developers/data-sets/decennial-census.2000.html
  - 2010 Census (because of course they’re not consistent):
      - SF1: https://api.census.gov/data/2010/dec/sf1/variables.html
  - ACS List: https://www.census.gov/data/developers/data-sets/acs-5year.html