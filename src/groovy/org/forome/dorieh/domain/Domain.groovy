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


class Domain {
  String name
  String schema
  String auditSchema
  String description
  String quoting
  String indexingPolicy
  List<Table> _tables = [] as List<Table>

  def table(String name, String type, Closure tableDef) {
    Table table = new Table(name: name, type: type)
    table.with(tableDef)
    _tables << table
  }

  def tables(Object args) {
    
  }

  public void setProperty(String name, Object value)
  {
    if ("ps".equals (name)) {
      print (name)
    }
  }

    String toString() {
    return "Domain(name: ${name}, schema: ${schema}, tables: ${_tables})"
  }
}

