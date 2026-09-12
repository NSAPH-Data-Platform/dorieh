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

class Column extends Base
{
    String name
    String type
    Map<String, Object> source = [:]
    // Contains details about source, type, code, etc.
    List<String> sourceColumns
    List<String> requires
    def index  // Can be boolean or Map<String, Object>
    String description
    String reference
    List<String> columns // For computed sources
    List<String> parameters
    boolean optional = false
    String transformation
    Map<String, String> casts

    Column (String name)
    {
        this.name = name
    }

    Column (String name, String type, Map<String, Object> attributes = [:])
    {
        this.name = name
        this.type = type
        def sourceAttr = attributes.source ?: [:]
        if (sourceAttr instanceof String) {
            this.source = ["source": sourceAttr]
        } else if (sourceAttr instanceof Map) {
            this.source = sourceAttr
        } else if (sourceAttr instanceof List) {
            this.sourceColumns = sourceAttr
        } else {
            throw new IllegalArgumentException (
                    "Column source cannot be " + sourceAttr.getClass ().getName ()
            )
        }

        this.requires = attributes.requires ?: []
        this.index = attributes.index ?: false
        this.description = attributes.description ?: ""
        this.reference = attributes.reference ?: ""
        this.optional = attributes.optional ?: false

        if (source)
            {
                this.columns = source.columns ?: []
                this.parameters = source.parameters ?: []
            }
    }

    public void addSourceColumn(String sql)
    {
        if (sourceColumns == null) {
            sourceColumns = new ArrayList<>()
        }
        sourceColumns.add (sql)
    }

    public void setProperty (String name, Object value)
    {
        switch (name)
            {
                case "sql":
                    source ['sql'] = (String) value
                    return
                default:
                    break
            }
        super.setProperty (name, value)
    }

    def methodMissing(String name, Object args)
    {
        switch (name) {
            case "of":
                of(args)
                return
        }
        println "Column methodMissing called with name: $name and args: $args"
    }

    public void of (args)
    {
        if (currentContext != null) {
            switch (currentContext) {
                case "transformation":
                    return
            }
        } else {
            currentContext = args
            return
        }

        throw new IllegalStateException("Unexpected identifier 'of'")
    }

    public void cast(Map<String, String> args)
    {
        casts = args
    }

    public void isomorphic_transformation(args)
    {
        if (args == null)
            args = currentContext
        Object arg0 = null
        if (args instanceof Object[] && args.length > 0) {
            arg0 = args [0]
        } else if (args instanceof List && args.size () > 0) {
            arg0 = args [0]
        } else if (args instanceof Closure || args instanceof String) {
            arg0 = args
            args = [arg0]
        }
        if (arg0 instanceof Closure) {
            
        } else if (arg0 instanceof String) {
            sourceColumns = (List) args
            transformation = "isomorphic_transformation of $sourceColumns"
        } else {
            throw new IllegalStateException("Invalid transformation statement")
        }
    }

    // Method to display column properties in a readable format (For debugging)
    String toString ()
    {
        return "Column(name: $name, type: $type, source: $source, requires: $requires)"
    }

    String toYAML (int indent)
    {
        String prefix = "  " * indent
        String header = "${prefix}- ${name}"
        if (transformation) {
            if (description) {
                if (
                        (description.length () + transformation.length () < 120)
                        && (description.indexOf('\n') < 0)
                ) {
                    description = description.trim ()
                    description += "; "
                }
                description +=  transformation
            } else {
                description = transformation
            }
        }
        if (
            source || sourceColumns || optional || description || reference
            || parameters || requires
            || type
        ) {
            String body = header + ":\n"
            indent++
            if (description) {
                body = addElement (body, "description", description, indent)
            }
            if (type) {
                body = addElement (body, "type", type, indent)
            }
            if (reference) {
                body = addElement (body, "reference", reference, indent)
            }
            if (requires) {
                body = addList (body, "requires", requires, indent)
            }
            if (sourceColumns) {
                if (sourceColumns.size () > 1) {
                    body = addList (body, "source", sourceColumns, indent)
                } else if (sourceColumns[0] != name) {
                    body = addElement (body, "source", sourceColumns[0], indent)
                }
                if (source && source.containsKey ("sql")) {
                    body = addElement (body, "source", source["sql"].toString (), indent)
                }
            } else if (source) {
                body = addElement (body, "source", "", indent)
                indent++
                for (String key: source.keySet ()) {
                    body = addElement (body, key, source[key].toString (), indent)
                }
                indent--
            }
            if (casts) {
                body = addElement (body, "cast", "", indent)
                indent++
                for (String key: casts.keySet ()) {
                    body = addElement (body, key, casts[key], indent)
                }
                indent--
            }
            // Remove empty lines:
            def lines = body.lines ().grep { it.trim() }
            return String.join ("\n", lines)
        }  else {
            return header
        }
    }

}