# Querying Medicaid Data

```{contents}
---
local:
---
```

## Querying diagnoses

> Querying by diagnoses might be expensive. 
> Use EXPLAIN to understand and optimize your queries
> See 
> [SampleQuery](../../core-platform/doc/SampleQuery.md#using-explain-to-optimize-queries).

### Listing patients

The following sample lists all patient hospitalized with specified diagnosis 
codes. The code can be either primary or secondary diagnosis.

    SELECT 
        state, 
        zip,
        YEAR, 
        age(admission_date::timestamp, dob::timestamp) as bene_age, 
        admission_date, 
        discharge_date, 
        diagnosis, 
        file, 
        bene_id 
    FROM 
        medicaid.admissions 
            natural join medicaid.enrollments
            natural join medicaid.beneficiaries
    WHERE 
        diagnosis && ARRAY['29620'::varchar, '29633'::varchar]
        AND EXTRACT (YEAR FROM age(admission_date::timestamp, dob::timestamp)) 
            BETWEEN 10 and 18

This query uses array operator `&&`. 
See [documentation](https://www.postgresql.org/docs/13/functions-array.html) 
to understand how it works.
It also uses two conditions in WHERE clause: 

* Diagnosis has to be one of those listed (ICD9 29620 or 29633)
* Age at a date of admission has to be between 10 and 18 years.

### Problem: no wildcarding
Here we encounter to one of the problems. 
The  syntax above (based on array operators) does not support wildcards. 
You must write all the ICD codes explicitly, 
something like this '2962*' or '2962%' will not fly. 
You technically can get around this with UNNEST function, 
but then the index built on  
diagnosis column will not be used and query performance might become horrible. 

One solution can be to write a Python program that will generate the query
explicitly listing all required ICD codes, i.e. '2962', '29620','29621', etc.
You would need to download ICD9 data for it, e.g. from 
[UMLS](https://www.nlm.nih.gov/research/umls/index.html) website.

### Calculating numbers

Instead of listing patients we can just calculate the number of those patients
that are of interest to us, without seeing individual records. This is done
through aggregate queries.

If we want to calculate hospitalizations in every zip code for every year
separately, we can use the following query:

    SELECT
        zip,
        year,
        count(*) as enrollees,
        COUNT(*) FILTER (
            WHERE bene_id IN (
                SELECT bene_id 
                FROM medicaid.admissions natural join medicaid.beneficiaries
                WHERE 
                    diagnosis && ARRAY['2962'::varchar, '2963'::varchar]
                    AND EXTRACT (
                        YEAR FROM age(admission_date::timestamp, dob::timestamp)
                    ) BETWEEN 10 and 18
            )
        )  AS hospitalized  
    FROM 
        medicaid.enrollments
        
    GROUP BY
        year, 
        zip    
    ORDER BY 
        year, 
        zip    
    
This query uses an 
[array operator](https://www.postgresql.org/docs/13/functions-array.html) 
and 
[FILTER clause](https://www.postgresql.org/docs/13/sql-expressions.html#SYNTAX-AGGREGATES). 

This query calculates the number of all people enrolled in Medicaid in a certain
zip code. Instead you might want to calculate just those whos age is between 10
and 18 years. To do this you should use FILTER clause to calculate enrollees
similar to how it is used to calculate hospitalized patients.

Now, to calculate hospitalizations in every Zip code over all years:

    SELECT
        zip,
        count(*) as enrollees,
        COUNT(*) FILTER (
            WHERE bene_id IN (
                SELECT bene_id 
                FROM medicaid.admissions natural join medicaid.beneficiaries
                WHERE 
                    diagnosis && ARRAY['2962'::varchar, '2963'::varchar]
                    AND EXTRACT (
                        YEAR FROM age(admission_date::timestamp, dob::timestamp)
                    ) BETWEEN 10 and 18
            )
        )  AS hospitalized  
    FROM 
        medicaid.enrollments
        
    GROUP BY
        zip    
    ORDER BY 
        3 desc, 
        zip    
