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

package org.forome.dorieh.dsl

import org.forome.dorieh.domain.Base
import org.forome.dorieh.domain.Domain
import org.forome.dorieh.domain.Table
import org.forome.dorieh.domain.Workflow


class Dataflow extends Base
{
  Map<String, Table> tableDefinitions = [:]
  Map<String, Domain> domains = [:]
  Map<String, Workflow> workflows = [:]


  // Stack <Base> stack;

  def methodMissing(String name, Object args)
  {
    println "methodMissing called with name: $name and args: $args"
    switch (name) {
      case "table":
        String tableName = currentContext.get ("name")
        Closure closure = (Closure) currentContext.get ("closure")
        table (tableName, closure)
        return
    }
    currentContext = [
            name: name,
            closure: args[0]
    ]

  }

//  public void table()
//  {
//    if (currentContext != null && currentContext instanceof Map) {
//      String name = currentContext.get ("name")
//      Closure closure = (Closure) currentContext.get ("closure")
//      table (name, closure)
//    }
//  }
  public void table(String name, Closure closure)
  {
    assert name != null : "Unnamed table block is not allowed"
    println "Defining table: ${name}"
    Table table = new Table(name: name)
    tableDefinitions[name] = table              // Store the defined table
    call (closure, table)
  }

  public void domain (Closure closure)
  {
    domain ("Unnamed domain", closure)
  }

  public void domain (String name, Closure closure)
  {
    println "Defining domain: ${name}"
    domains[name] = new Domain ()
    call (closure, domains[name])
  }

  public void workflow(Closure closure)
  {
     workflow ("Default workflow", closure)
  }

  public void workflow(String name, Closure closure)
  {
    if (workflows.containsKey (name)) {
      throw new IllegalStateException("Duplicate workflow ${name}")
    }
    Workflow workflow = new Workflow ()
    workflows[name] = workflow
    call (closure, workflow)
    String domain = workflow.domain
    println "Workflow: ${name} building ${workflow.goal} for domain ${domain}"
  }

  void toYAML()
  {
    print "tables:\n"
    for (String table: tableDefinitions.keySet ()) {
      print (tableDefinitions[table].toYAML (2))
    }
  }
}

