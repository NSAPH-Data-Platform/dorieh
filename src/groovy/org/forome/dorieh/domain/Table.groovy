/*
 * Copyright (c) 2024. Harvard University
 *
 * Developed by Research Software Engineering,
 * Harvard University Research Computing and Data (RCD) Services.
 *
 * Author: Michael A Bouzinier
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 *
 *
 *
 *
 */

package org.forome.dorieh.domain



class Table extends Base
{
    enum TableTransformationType {
        union,
        aggregation,
        copy
    }
    static final public DEFAULT_TYPE = "VARCHAR"
    String name
    String description
    String type = "table" // Could be view, table, etc.
    List<String> from
    List<String> groupBy
    List<Column> columns = []

    private String currentColumn = null

    private TableTransformationType transformType

    def methodMissing(String name, Object args)
    {
        Object arg0 = args == null ? null : args [0]
        if (currentContext != null) {
            switch (currentContext) {
                case "columns_reconcile":
                    if (arg0 instanceof Closure) {
                        Closure closure = arg0
                        closure.owner = this
                        this.@currentColumn = name.toLowerCase ()
                        try {
                            closure.call ()
                        } finally {
                            this.@currentColumn = null
                        }
                    } else {
                        throw new IllegalArgumentException(
                           "Reconciliation strategy is invalid for $name"
                        )
                    }
                    return
                case "columns":
                    if (arg0 instanceof String) {
                        column (name, arg0)
                    } else if (arg0 instanceof Closure) {
                        Closure closure = arg0
                        Column column = new Column(name)
                        closure.delegate = column
                        closure.resolveStrategy = Closure.DELEGATE_FIRST
                        closure.call ()
                        columns << column
                    }
                    return 
                default:
                    break
            }
        }  else  if (arg0 == null) {
            currentContext = name.toLowerCase ()
            return
        }

        println "Table methodMissing called with name: $name and args: $args"
    }

    public def pick(String... args)
    {
        String arg  = args[0]
        Column column = new Column(currentColumn)
        String aggr = arg.toUpperCase()
        column.addSourceColumn ("$aggr($currentColumn)")
        columns << column
        return new Object() {
            def over(String... overArgs) {
                String alt = overArgs[0].toUpperCase()
                String sql = """
                CASE
                    WHEN ${alt}($currentColumn) <> ${aggr}($currentColumn) THEN ${alt}($currentColumn) 
                END
                """
                String cname = "${currentColumn}_$arg"
                Column overColumn = new Column(cname)
                overColumn.addSourceColumn(sql)
                columns << overColumn
            }
        }
    }

    public def aggregate (Closure closure)
    {
        closure.delegate = new Object () {
            private String lastValue

            void setProperty(String name, def value) {
                value = value ?: lastValue
                columns << new Column(name).tap {
                    addSourceColumn(value?.toString() ?: '')
                }
            }

            def methodMissing(String name, def args) {
                lastValue = "${name}(${formatArgs(args)})"
            }

            private String formatArgs(def args) {
                args instanceof Object[] ? args.grep().join(', ') : args.toString()
            }
        }
        closure.resolveStrategy = Closure.DELEGATE_FIRST
        closure.call ()
    }

    public void record (String... args)
    {
        for (String arg: args) {
            String postfix = arg.split (" ")[0]
            String cname = "${currentColumn}_$postfix"
            Column column = new Column (cname)
            String aggr = arg.toUpperCase ()
            column.addSourceColumn ("$aggr($currentColumn)")
            columns << column
        }
    }

    public void of (args)
    {
        if (currentContext == null) {
            currentContext = args
            return
        }

        throw new IllegalStateException("Unexpected identifier 'of'")
    }

    public void columns(Closure closure)
    {
        currentContext = "columns"
        closure.call ()
    }

    public void from (String... tables)
    {
        from = tables.toList ()
    }

    public void from (Closure listClosure)
    {
        ListCollector collector = new ListCollector()
        call (listClosure, collector)
        from = collector.getItems ()
    }

    private arg0(args)
    {
        if (args == null)
            args = currentContext
        Object arg0 = null
        if (args instanceof List && args.size () > 0) {
            arg0 = args [0]
        } else if (args instanceof Closure || args instanceof String) {
            arg0 = args
        }
        return arg0
    }

    public void union (args)
    {
        transformType = TableTransformationType.union
        def arg0 = arg0 (args)
        if (arg0 instanceof Closure) {
            from((Closure)arg0)
        } else if (arg0 instanceof String) {
            from = [args]
        } else {
            throw new IllegalStateException("Invalid union statement")
        }
    }

    public void aggregation (args)
    {
        transformType = TableTransformationType.aggregation
        def arg0 = arg0 (args)
        if (arg0 instanceof Closure) {
            from((Closure)arg0)
        } else if (arg0 instanceof String) {
            from = [arg0]
        } else {
            throw new IllegalStateException("Invalid aggregation statement")
        }
    }

    public void on(String... args)
    {
        if (transformType != TableTransformationType.aggregation) {
            throw new IllegalStateException("Keyword 'on' is only supported for aggregation")
        }
        for (String arg: args) {
            column (arg)
        }
        groupBy = args.grep ()
    }

    def column(String name, String type, Map<String, Object> attributes = [:]) {
        Column column = new Column(name, type, attributes)
        // column.with(columnDef)
        columns << column
    }

    def column(String name, Map<String, Object> attributes = [:]) {
        column (name, DEFAULT_TYPE, attributes)
    }

    String toString() {
        return "Table(name: ${name}, type: ${type}, columns: ${columns})"
    }

    public void setProperty(String name, Object value)
    {
        switch (name) {
            case "currentContext":
                super.setProperty(name, value)
                return
            case "columns":
                currentContext = "columns"
                return
            default:
                break
        }

        switch (currentContext) {
            case "columns":
                column(name, (String)value)
                break
            default:
                super.setProperty(name, value)
        }

    }

    public void reconcile (Closure closure)
    {
        this.@currentContext = "columns_reconcile"
        closure.delegate = this
        closure.resolveStrategy = Closure.DELEGATE_FIRST
        try {
            closure.call ()
        }  finally {
            this.@currentContext = null
        }
    }

    public Object getProperty (String name)
    {
        try {
            super.getProperty (name)
        } catch (MissingPropertyException x) {
            return name
        }
    }

    String toYAML(int indent)
    {
        String prefix = "  " * indent
        String body = "${prefix}# ${type}: ${name}\n"
        body = addElement (body, name, "", indent)
        indent += 1
        if (description != null)   {
            body = addText (body, "description", description, indent)
        }
        if (type != null) {
            body = addElement (body, "type", type, indent)
        }
        if  (from != null) {
            if (from.size () > 1)  {
                body = addList (body, "from", from, indent)
            }
            else if (!from.isEmpty ()) {
                body = addElement (body, "from", from [0], indent)
            }
        }
        if (groupBy != null) {
            body = addList (body, "group by", groupBy, indent)
        }
        List<String> columnNames = new ArrayList<>()
        for (Column column: columns) {
            columnNames.add (column.name)
        }
        body = addElement (body, "columns", "", indent)
        for (Column column: columns) {
            String cc = column.toYAML(indent)
            body += cc + '\n'
        }
        return body
    }
}


